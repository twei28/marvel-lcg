"""Le compteur anonyme des parties lancees sur play.

Passe par la VRAIE route `/compteur_play` (serveur HTTP reel, base temporaire).

Usage : python3 site/test_compteur_play.py
"""
import http.client
import json
import os
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer

_base = os.path.join(tempfile.gettempdir(), "nc-compteur-play.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
os.environ["COMPTEUR_PLAY_MAX_PAR_JOUR"] = "5"
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


def envoyer(corps: bytes, annonce=None):
    lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=5)
    try:
        lien.putrequest("POST", "/compteur_play", skip_accept_encoding=True)
        lien.putheader("Content-Type", "text/plain;charset=UTF-8")
        lien.putheader("Content-Length", str(len(corps) if annonce is None else annonce))
        lien.endheaders()
        if corps:
            try:
                lien.send(corps)
            except OSError:
                pass
        return lien.getresponse().status
    finally:
        lien.close()


def lignes():
    with o._cx() as cx:
        return [dict(r) for r in cx.execute("SELECT * FROM parties_play ORDER BY id")]


nominal = {"mechant": "Vermin", "heros": ["Spider-Man", "Captain Marvel"], "joueurs": 2,
           "mode": "campagne", "difficulte": "expert"}
verifier("une partie nominale rend 204", envoyer(json.dumps(nominal).encode()) == 204)
l = lignes()
verifier("elle est enregistree", len(l) == 1, str(l))
verifier("avec ses champs", l and l[0]["mechant"] == "Vermin" and json.loads(l[0]["heros"]) == ["Spider-Man", "Captain Marvel"]
         and l[0]["joueurs"] == 2 and l[0]["mode"] == "campagne" and l[0]["difficulte"] == "expert", str(l))
verifier("sans adresse ni identifiant", l and set(l[0]) == {"id", "jour", "mechant", "heros", "joueurs", "mode", "difficulte"})

verifier("un corps annonce trop gros est refuse (413)", envoyer(b"", annonce=o.COMPTEUR_PLAY_MAX_OCTETS + 1) == 413)
verifier("et rien n'est ecrit", len(lignes()) == 1)

verifier("du JSON illisible rend 204", envoyer(b"pas du json") == 204)
verifier("mais n'ecrit rien", len(lignes()) == 1)
verifier("un signal sans mechant ni heros n'ecrit rien", envoyer(b'{"mode":"solo"}') == 204 and len(lignes()) == 1)

bizarre = {"mechant": "X" * 500, "heros": ["A", 3, None, "B", "C", "D", "E"], "joueurs": 99,
           "mode": "pirate", "difficulte": "<script>"}
envoyer(json.dumps(bizarre).encode())
b = lignes()[-1]
verifier("le nom trop long est coupe", len(b["mechant"]) == 60, str(len(b["mechant"] or "")))
verifier("les heros non textuels sont ecartes, 4 au plus lus", json.loads(b["heros"]) == ["A", "B"], b["heros"])
verifier("un nombre de joueurs hors bornes est recalcule", b["joueurs"] == 2, str(b["joueurs"]))
verifier("un mode inconnu devient solo", b["mode"] == "solo")
verifier("une difficulte inconnue est ignoree", b["difficulte"] is None)

for _ in range(10):
    envoyer(json.dumps({"mechant": "Rhino", "heros": ["Hulk"]}).encode())
verifier("le plafond du jour est tenu", len(lignes()) == 5, str(len(lignes())))

page = o.bloc_stats_play()
verifier("l'admin affiche le total", "5 partie(s)" in page, page[:200])
verifier("l'admin liste les mechants", "Vermin" in page and "Rhino" in page)
verifier("l'admin liste les heros", "Spider-Man" in page and "Hulk" in page)
with o._cx() as cx:
    cx.execute("INSERT INTO parties_play (jour, mechant, heros) VALUES ('2099-01-01', '<b>x</b>', '[]')")
o.COMPTEUR_PLAY_MAX_PAR_JOUR = 10
envoyer(json.dumps({"mechant": "<img src=x>", "heros": ["<i>h</i>"]}).encode())
page = o.bloc_stats_play()
verifier("ce qui vient du joueur est echappe", "<img src=x>" not in page and "&lt;img src=x&gt;" in page)

try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")
_lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=10)
_lien.request("GET", "/admin", headers={"Cookie": "nc_session=" + o.ouvrir_session(o.ADMIN)})
_rep = _lien.getresponse()
_admin = _rep.read().decode("utf-8", "replace")
verifier("la page admin se rend (200)", _rep.status == 200, str(_rep.status))
verifier("avec le sous-onglet Play et ses chiffres",
         'data-sous="parties-play"' in _admin and "Mechants les plus joues" in _admin)

_serveur.shutdown()
print("\n%d echec(s)" % len(echecs))
sys.exit(1 if echecs else 0)
