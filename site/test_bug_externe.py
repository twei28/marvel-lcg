"""Les rapports des AUTRES jeux du site (Arkham, Seigneur des Anneaux) : `POST /api/bug-externe`, rangés dans la MEME
table `rapports` avec leur jeu, vus et gérés depuis /admin.

Passe par les VRAIES routes (serveur HTTP réel, base temporaire).

Usage : python3 site/test_bug_externe.py
"""
import base64
import gzip
import http.client
import json
import os
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer

_base = os.path.join(tempfile.gettempdir(), "nc-bug-externe.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
os.environ["DOSSIER_RAPPORTS"] = tempfile.mkdtemp(prefix="nc-rapports-externes-")
os.environ["CLE_RAPPORTS_EXTERNES"] = "cle-de-test-externe"
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


def appel(methode, chemin, corps=None, entetes=None):
    donnees = json.dumps(corps).encode() if corps is not None else b""
    tetes = dict(entetes or {})
    if methode == "POST":
        tetes["Content-Type"] = "application/json"
        tetes["Content-Length"] = str(len(donnees))
    lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=8)
    try:
        lien.request(methode, chemin, body=donnees or None, headers=tetes)
        reponse = lien.getresponse()
        return reponse.status, reponse.read()
    finally:
        lien.close()


def rapports():
    with o._cx() as cx:
        return [dict(r) for r in cx.execute("SELECT * FROM rapports ORDER BY id")]


CLE = {"X-Cle-Rapports": "cle-de-test-externe"}
PNG = "data:image/png;base64," + base64.b64encode(
    bytes.fromhex("89504e470d0a1a0a0000000d4948445200000001000000010806000000"
                  "1f15c4890000000d49444154789c6360000002000001e221bc330000000049454e44ae426082")).decode()
ETAT = base64.b64encode(gzip.compress(json.dumps({"game": {"name": "Ma partie", "log": ["a", "b"]}}).encode())).decode()
rapport = {"jeu": "arkham", "titre": "La carte ne bouge plus", "texte": "Je clique et rien ne se passe.", "contact": "moi@exemple.be",
           "route": "?partie=abc#", "client": {"navigateur": "Firefox", "fenetre": "390x844", "telephone": True},
           "partie": {"nom": "Ma partie", "scenario": "c01104", "etape": 7}, "journal": "ligne un\nligne deux",
           "captures": [PNG, PNG, "n'importe quoi"], "etat": ETAT, "source_id": "20261116-070339-abc123"}

# --- La route est FERMEE sans le secret ------------------------------------------------------------
verifier("sans secret : 403", appel("POST", "/api/bug-externe", rapport)[0] == 403)
verifier("mauvais secret : 403", appel("POST", "/api/bug-externe", rapport, {"X-Cle-Rapports": "faux"})[0] == 403)
verifier("le bon secret MAIS un X-Forwarded-For (appel venu d'Internet par Caddy) : 403",
         appel("POST", "/api/bug-externe", rapport, {**CLE, "X-Forwarded-For": "203.0.113.9"})[0] == 403)
verifier("rien n'est range", rapports() == [])

# --- Un rapport valide -----------------------------------------------------------------------------
code, corps = appel("POST", "/api/bug-externe", rapport, CLE)
rep = json.loads(corps or b"{}")
verifier("rapport valide : 200 et un numero", code == 200 and rep.get("ok") and rep.get("nouveau") is True, str(corps))
r = rapports()
verifier("un rapport rangé, du bon jeu", len(r) == 1 and r[0]["jeu"] == "arkham", str(r))
verifier("la description porte le titre puis le texte", r[0]["description"].startswith("La carte ne bouge plus\n\nJe clique"))
verifier("le contact devient le nom", r[0]["nom"] == "moi@exemple.be")
verifier("etat « nouveau », pas un ticket (aucun compte)", r[0]["etat"] == "nouveau" and not r[0]["compte_verifie"] and r[0]["hote"] is None)
verifier("le journal garde le contexte puis les logs", "Partie : Ma partie" in r[0]["journal"] and "Firefox" in r[0]["journal"] and "ligne deux" in r[0]["journal"])
caps = json.loads(r[0]["captures"] or "[]")
verifier("deux captures valides gardees (la troisieme est illisible)", len(caps) == 2 and r[0]["capture"] == caps[0], str(caps))
verifier("l'etat complet de la partie est un fichier", bool(r[0]["etat_fichier"]) and os.path.isfile(os.path.join(o.DOSSIER_RAPPORTS, r[0]["etat_fichier"])))

# --- Idempotent : le meme rapport envoye deux fois n'est range qu'une -------------------------------
code, corps = appel("POST", "/api/bug-externe", rapport, CLE)
rep2 = json.loads(corps)
verifier("meme source_id : meme numero, pas de doublon", rep2.get("nouveau") is False and rep2.get("numero") == rep.get("numero") and len(rapports()) == 1, str(rep2))
r2 = dict(rapport, source_id="autre-id", jeu="lotr")
code, corps = appel("POST", "/api/bug-externe", r2, CLE)
verifier("un autre jeu, un autre source_id : nouveau rapport", code == 200 and len(rapports()) == 2 and rapports()[1]["jeu"] == "lotr")

# --- Refus ------------------------------------------------------------------------------------------
verifier("jeu inconnu : 400", appel("POST", "/api/bug-externe", dict(rapport, jeu="autre", source_id="x1"), CLE)[0] == 400)
verifier("« marvel » n'a pas cette route : 400", appel("POST", "/api/bug-externe", dict(rapport, jeu="marvel", source_id="x2"), CLE)[0] == 400)
verifier("rapport vide : 400", appel("POST", "/api/bug-externe", {"jeu": "arkham", "titre": " ", "texte": ""}, CLE)[0] == 400)
verifier("un etat qui n'est pas un gzip n'est pas garde", (lambda: (appel("POST", "/api/bug-externe", dict(rapport, source_id="x3", etat=base64.b64encode(b"pas gzip").decode()), CLE), rapports()[-1]["etat_fichier"] is None)[1])())

# --- L'admin le voit, avec l'étiquette du jeu, et peut le gérer ---------------------------------------
try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")
cookie = {"Cookie": "nc_session=" + o.ouvrir_session(o.ADMIN)}
o.enregistrer_rapport("hote-marvel", {"nom": "Joueur", "description": "Bug Marvel ordinaire", "siege": 0})
code, admin = appel("GET", "/admin", entetes=cookie)
admin = admin.decode("utf-8", "replace")
verifier("l'admin voit les rapports des trois jeux", code == 200 and "La carte ne bouge plus" in admin and "Bug Marvel ordinaire" in admin, str(code))
verifier("chaque rapport porte l'étiquette de son jeu (Marvel aussi)", 'class="jeu jeu-arkham">Arkham' in admin and 'class="jeu jeu-lotr">Seigneur des Anneaux' in admin and 'class="jeu jeu-marvel">Marvel' in admin)
verifier("le filtre par jeu existe", 'id="filtres-jeu"' in admin and 'data-jeu="arkham"' in admin)
verifier("les deux captures et le lien vers l'etat complet", "/admin/capture?id=%d&amp;n=2" % r[0]["id"] in admin and "/admin/etat?id=%d" % r[0]["id"] in admin)
code, img = appel("GET", "/admin/capture?id=%d&n=2" % r[0]["id"], entetes=cookie)
verifier("la 2e capture se sert (png)", code == 200 and img[1:4] == b"PNG")
code, gz = appel("GET", "/admin/etat?id=%d" % r[0]["id"], entetes=cookie)
verifier("l'etat de la partie se telecharge (gzip lisible)", code == 200 and json.loads(gzip.decompress(gz))["game"]["name"] == "Ma partie")
verifier("l'etat est reserve a l'administrateur", appel("GET", "/admin/etat?id=%d" % r[0]["id"])[0] in (302, 303, 401, 403))
verifier("un numero sans etat : 404", appel("GET", "/admin/etat?id=99999", entetes=cookie)[0] == 404)

# gerer : classer, puis supprimer (les fichiers partent aussi)
o.changer_etat_rapport(r[0]["id"], "traite")
verifier("classé", [x for x in rapports() if x["id"] == r[0]["id"]][0]["etat"] == "traite")
fichiers = o._fichiers_d_un_rapport(r[0])
verifier("trois fichiers a effacer (2 captures + l'etat)", len(fichiers) == 3, str(fichiers))
o.supprimer_rapport(r[0]["id"])
verifier("supprimé : la ligne et TOUS ses fichiers", all(x["id"] != r[0]["id"] for x in rapports()) and not any(os.path.exists(os.path.join(o.DOSSIER_RAPPORTS, f)) for f in fichiers))

# --- La purge allege aussi les rapports des autres jeux ------------------------------------------------
code, _ = appel("POST", "/api/bug-externe", dict(rapport, source_id="ancien", titre="Vieux rapport"), CLE)
vieux = [x for x in rapports() if x["source_id"] == "ancien"][0]
with o._cx() as cx:
    cx.execute("UPDATE rapports SET etat = 'traite', traite_le = '2020-01-01 00:00' WHERE id = ?", (vieux["id"],))
fichiers = o._fichiers_d_un_rapport(vieux)
verifier("la purge allege 1 rapport", o.purger_rapports_traites(30) == 1)
apres = [x for x in rapports() if x["id"] == vieux["id"]][0]
verifier("captures et etat effaces, le texte reste", apres["capture"] is None and apres["captures"] is None and apres["etat_fichier"] is None and "Vieux rapport" in apres["description"])
verifier("les fichiers ont disparu du disque", not any(os.path.exists(os.path.join(o.DOSSIER_RAPPORTS, f)) for f in fichiers))

# --- Un joueur Marvel ne voit JAMAIS ces rapports -----------------------------------------------------
verifier("aucune table Marvel ne les voit", o.rapports_de_ses_tables("hote-marvel") != [] and all(x["jeu"] == "marvel" for x in o.rapports_de_ses_tables("hote-marvel")))

# --- Le compte des parties de chaque jeu --------------------------------------------------------------
lot = {"jeu": "arkham", "parties": [{"source_id": "g1", "jour": o.time.strftime("%Y-%m-%d", o.time.gmtime()), "joueurs": 2, "scenario": "c01104"},
                                    {"source_id": "g2", "jour": "2020-01-01"}, {"source_id": "", "jour": "2020-01-01"}, {"source_id": "g3", "jour": "pas une date"}]}
verifier("parties : sans secret, 403", appel("POST", "/api/parties-externes", lot)[0] == 403)
code, corps = appel("POST", "/api/parties-externes", lot, CLE)
verifier("parties : 2 valides comptees, les 2 invalides ignorees", code == 200 and json.loads(corps)["nouvelles"] == 2, str(corps))
verifier("parties : renvoyer le meme lot ne compte rien de plus", json.loads(appel("POST", "/api/parties-externes", lot, CLE)[1])["nouvelles"] == 0)
verifier("parties : jeu inconnu / marvel refuses", appel("POST", "/api/parties-externes", dict(lot, jeu="marvel"), CLE)[0] == 400
         and appel("POST", "/api/parties-externes", dict(lot, jeu="x"), CLE)[0] == 400)
st = {l["jeu"]: l for l in o.stats_parties_par_jeu()}
verifier("stats : Arkham 2 au total, 1 aujourd'hui", st["arkham"]["total"] == 2 and st["arkham"]["auj"] == 1 and st["arkham"]["j7"] == 1, str(st["arkham"]))
verifier("stats : LOTR 0, Marvel compte site + play", st["lotr"]["total"] == 0 and "sur le site" in st["marvel"]["detail"])
code, admin = appel("GET", "/admin", entetes=cookie)
admin = admin.decode("utf-8", "replace")
verifier("l'admin affiche le tableau « Par jeu »", 'data-sous="parties-jeux"' in admin and "Seigneur des Anneaux</span></td><td data-label=\"Total\">0" in admin)

_serveur.shutdown()
print("\n" + ("TOUT EST VERT" if not echecs else "ECHECS : %s" % echecs))
sys.exit(1 if echecs else 0)
