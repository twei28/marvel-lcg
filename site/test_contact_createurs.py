"""Le formulaire public des createurs (/contact-createurs) et sa liste dans /admin.

Passe par les VRAIES routes (serveur HTTP reel, base temporaire).

Usage : python3 site/test_contact_createurs.py
"""
import http.client
import os
import sys
import tempfile
import threading
import urllib.parse
from http.server import ThreadingHTTPServer

_base = os.path.join(tempfile.gettempdir(), "nc-contact-createurs.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
os.environ["DEMANDES_CREATEURS_PAR_HEURE"] = "3"
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
    """Une requete reelle. Rend (code, corps texte)."""
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


def demandes():
    with o._cx() as cx:
        return [dict(r) for r in cx.execute("SELECT * FROM demandes_createurs ORDER BY id")]


def ip(adresse):
    return {"X-Forwarded-For": adresse}


valide = {"nom": "Artiste", "contact": "artiste@exemple.fr", "genre": "crediter",
          "message": "J'ai fait l'image de Kestrel, elle est sur la page des heros."}

# --- La page publique, sans compte ------------------------------------------
code, page = appel("GET", "/contact-createurs")
verifier("GET sans compte rend 200", code == 200, str(code))
verifier("la page montre le formulaire", 'action="/contact-createurs"' in page and 'name="message"' in page)
verifier("sans champ mot de passe", 'type="password"' not in page)
verifier("avec le pot de miel cache", 'name="site_web"' in page and 'class="pot"' in page)

# --- Un envoi valide est enregistre ------------------------------------------
code, page = appel("POST", "/contact-createurs", valide, ip("10.0.0.1"))
verifier("POST valide rend 200", code == 200, str(code))
verifier("avec la confirmation", "ta demande est bien arrivee" in page)
d = demandes()
verifier("la demande est enregistree", len(d) == 1 and d[0]["nom"] == "Artiste"
         and d[0]["genre"] == "crediter" and d[0]["etat"] == "nouvelle", str(d))

# --- Champ manquant ou genre inconnu : 400, rien d'ecrit ----------------------
code, page = appel("POST", "/contact-createurs", dict(valide, message=""), ip("10.0.0.2"))
verifier("message vide : 400", code == 400, str(code))
verifier("et le formulaire garde ce qui etait tape", "artiste@exemple.fr" in page)
code, _ = appel("POST", "/contact-createurs", dict(valide, genre="pirater"), ip("10.0.0.2"))
verifier("genre inconnu : 400", code == 400, str(code))
verifier("rien d'ecrit pour ces envois", len(demandes()) == 1)

# --- Le pot de miel : meme confirmation, rien d'enregistre --------------------
code, page = appel("POST", "/contact-createurs", dict(valide, site_web="http://spam"), ip("10.0.0.3"))
verifier("pot de miel rempli : la meme confirmation", code == 200 and "ta demande est bien arrivee" in page)
verifier("et rien d'enregistre", len(demandes()) == 1)

# --- La limite par adresse et par heure ---------------------------------------
codes = [appel("POST", "/contact-createurs", valide, ip("10.0.0.9"))[0] for _ in range(4)]
verifier("3 envois passent, le 4e est freine (429)", codes == [200, 200, 200, 429], str(codes))
verifier("une autre adresse n'est pas freinee",
         appel("POST", "/contact-createurs", valide, ip("10.0.0.10"))[0] == 200)

# --- L'echappement dans /admin, et /admin reserve -----------------------------
o.enregistrer_demande_createur("<script>alert(1)</script>", "x@y.z", "retirer",
                               "<img src=x onerror=alert(2)>")
try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")
cookie_admin = {"Cookie": "nc_session=" + o.ouvrir_session(o.ADMIN)}
code, admin = appel("GET", "/admin", entetes=cookie_admin)
verifier("l'admin voit la section", code == 200 and "Demandes des createurs" in admin, str(code))
verifier("le nom est echappe", "<script>alert(1)</script>" not in admin
         and "&lt;script&gt;alert(1)&lt;/script&gt;" in admin)
verifier("le message est echappe", "<img src=x onerror" not in admin and "&lt;img src=x" in admin)

try:
    o.inscrire("joueur", "joueur@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut("joueur", "valide")
code, autre = appel("GET", "/admin", entetes={"Cookie": "nc_session=" + o.ouvrir_session("joueur")})
verifier("un autre compte ne voit pas les demandes", "Demandes des createurs" not in autre, str(code))
code, _ = appel("GET", "/admin")
verifier("sans compte non plus", code != 200 or "Demandes des createurs" not in _, str(code))

# --- « Traitee » : reserve a l'admin -----------------------------------------
premier = demandes()[0]["id"]
code, _ = appel("POST", "/admin", {"action": "createur_traitee", "id": str(premier)},
                {"Cookie": "nc_session=" + o.ouvrir_session("joueur")})
verifier("un autre compte ne peut pas classer (403)", code == 403 and demandes()[0]["etat"] == "nouvelle", str(code))
appel("POST", "/admin", {"action": "createur_traitee", "id": str(premier)}, cookie_admin)
verifier("l'admin classe la demande en traitee", demandes()[0]["etat"] == "traitee")

# --- L'anglais ----------------------------------------------------------------
code, page = appel("GET", "/contact-createurs", entetes={"Cookie": "nc_langue=en"})
verifier("la page existe en anglais", code == 200 and "Credits and removal" in page and "Your request" in page)

_serveur.shutdown()
print()
print("BILAN : %d echec(s)" % len(echecs) if echecs else "BILAN : tout est vert")
sys.exit(1 if echecs else 0)
