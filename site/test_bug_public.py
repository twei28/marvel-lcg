"""Le formulaire PUBLIC de rapport de bug (/signaler-un-bug) : sans compte, sans table.

Passe par les VRAIES routes (serveur HTTP reel, base temporaire).

Usage : python3 site/test_bug_public.py
"""
import base64
import http.client
import os
import sys
import tempfile
import threading
import urllib.parse
from http.server import ThreadingHTTPServer

_base = os.path.join(tempfile.gettempdir(), "nc-bug-public.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
os.environ["BUGS_PUBLICS_PAR_HEURE"] = "3"
os.environ["DOSSIER_RAPPORTS"] = tempfile.mkdtemp(prefix="nc-rapports-")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

o.initialiser_base()
echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


_serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
_port = _serveur.server_address[1]
threading.Thread(target=_serveur.serve_forever, daemon=True).start()


def appel(methode, chemin, champs=None, entetes=None):
    corps = urllib.parse.urlencode(champs or {}).encode() if methode == "POST" else b""
    tetes = dict(entetes or {})
    if methode == "POST":
        tetes["Content-Type"] = "application/x-www-form-urlencoded"
        tetes["Content-Length"] = str(len(corps))
    lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=5)
    try:
        lien.request(methode, chemin, body=corps or None, headers=tetes)
        reponse = lien.getresponse()
        return reponse.status, reponse.read().decode("utf-8", "replace")
    finally:
        lien.close()


def rapports():
    with o._cx() as cx:
        return [dict(r) for r in cx.execute("SELECT * FROM rapports ORDER BY id")]


def ip(adresse):
    return {"X-Forwarded-For": adresse}


# Un PNG de 1 pixel : la capture est verifiee sur ses octets, pas sur son etiquette.
PNG = "data:image/png;base64," + base64.b64encode(
    bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                  "1f15c4890000000d49444154789c6360000002000001e221bc330000000049454e44ae426082")).decode()
valide = {"nom": "Visiteur", "contact": "visiteur@exemple.fr",
          "description": "Le bouton Jouer ne répond pas sur mon téléphone."}

# --- La page publique, sans compte ------------------------------------------
code, page = appel("GET", "/signaler-un-bug")
verifier("GET sans compte rend 200", code == 200, str(code))
verifier("formulaire vers /signaler-un-bug", 'action="/signaler-un-bug"' in page and 'name="description"' in page)
verifier("sans champ mot de passe", 'type="password"' not in page)
verifier("pot de miel cache", 'name="site_web"' in page and 'class="pot"' in page)
verifier("champ de capture", 'name="capture"' in page and 'type="file"' in page)
code, connexion = appel("GET", "/connexion")
verifier("la page de connexion renvoie vers le formulaire", 'href="/signaler-un-bug"' in connexion)

# --- Un envoi valide est range, sans table ni compte --------------------------
code, page = appel("POST", "/signaler-un-bug", dict(valide, capture=PNG), ip("10.1.0.1"))
verifier("POST valide rend 200 avec la confirmation", code == 200 and "bien arrivé" in page, str(code))
r = rapports()
verifier("un rapport est enregistre", len(r) == 1 and r[0]["nom"] == "Visiteur" and r[0]["etat"] == "nouveau", str(r))
verifier("sans hote ni auteur verifie (ce n'est PAS un ticket)", r[0]["hote"] is None and not r[0]["compte_verifie"])
verifier("le contact est dans la description", r[0]["description"].startswith("[Contact : visiteur@exemple.fr]"))
verifier("l'ecran dit d'ou il vient", r[0]["ecran"] == "site (sans compte)")
verifier("la capture est sur disque", bool(r[0]["capture"]) and r[0]["capture"].endswith(".png"), str(r[0]["capture"]))
verifier("personne n'est ticket", o._est_un_ticket(r[0]) is False)
verifier("aucune table ne le voit", o.rapports_de_ses_tables("nimporte") == [])

# --- Description vide : 400, rien d'ecrit --------------------------------------
code, page = appel("POST", "/signaler-un-bug", dict(valide, description="  "), ip("10.1.0.2"))
verifier("description vide : 400", code == 400, str(code))
verifier("le formulaire garde ce qui etait tape", "visiteur@exemple.fr" in page)
verifier("rien d'ecrit", len(rapports()) == 1)

# --- Nom absent : « anonyme » ; capture illisible : rapport garde, sans image ---
code, _ = appel("POST", "/signaler-un-bug", {"description": "sans nom", "capture": "data:image/png;base64,AAAA"}, ip("10.1.0.3"))
verifier("sans nom, sans capture valide : accepte", code == 200)
r = rapports()
verifier("nom « anonyme »", r[-1]["nom"] == "anonyme", r[-1]["nom"])
verifier("capture illisible ignoree", not r[-1]["capture"])

# --- Pot de miel -----------------------------------------------------------------
n = len(rapports())
code, page = appel("POST", "/signaler-un-bug", dict(valide, site_web="http://spam"), ip("10.1.0.4"))
verifier("pot de miel : meme confirmation", code == 200 and "bien arrivé" in page)
verifier("et rien d'enregistre", len(rapports()) == n)

# --- Frein PAR ADRESSE -----------------------------------------------------------
codes = [appel("POST", "/signaler-un-bug", valide, ip("10.1.0.9"))[0] for _ in range(4)]
verifier("3 envois passent, le 4e est freine (429)", codes == [200, 200, 200, 429], str(codes))
verifier("une autre adresse n'est pas freinee", appel("POST", "/signaler-un-bug", valide, ip("10.1.0.10"))[0] == 200)

# --- L'admin le voit, echappe, sans fil de reponse ---------------------------------
o.enregistrer_bug_public({"nom": "<script>alert(1)</script>", "description": "<img src=x onerror=alert(2)>"})
try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")
code, admin = appel("GET", "/admin", entetes={"Cookie": "nc_session=" + o.ouvrir_session(o.ADMIN)})
verifier("l'admin voit le rapport", code == 200 and "Le bouton Jouer ne répond pas" in admin, str(code))
verifier("nom et description echappes", "<script>alert(1)</script>" not in admin and "<img src=x onerror" not in admin)

# --- L'anglais -------------------------------------------------------------------
code, page = appel("GET", "/signaler-un-bug", entetes={"Cookie": "nc_langue=en"})
verifier("la page existe en anglais", code == 200 and "Report a bug" in page and "What happened?" in page
         and "bien arrivé" not in page and "No account needed" in page, str(code))
code, page = appel("POST", "/signaler-un-bug", valide, {**ip("10.1.0.11"), "Cookie": "nc_langue=en"})
verifier("la confirmation est en anglais", "has arrived" in page, page[-300:])

_serveur.shutdown()
print("\n" + ("TOUT EST VERT" if not echecs else "ECHECS : %s" % echecs))
sys.exit(1 if echecs else 0)
