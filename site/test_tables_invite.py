"""Les tables invite de Play : jouer en ligne SANS compte (03/11/2026).

Passe par les VRAIES routes `/places_invite` et `/jouer-invite` (serveur HTTP reel, base
temporaire, aucun moteur lance : `demarrer_en_fond` est neutralise).

Usage : python3 site/test_tables_invite.py
"""
import http.client
import json
import os
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer

_base = os.path.join(tempfile.gettempdir(), "nc-tables-invite.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

o.initialiser_base()
o.demarrer_en_fond = lambda pseudo, joueurs=1: None      # aucun moteur
o._nettoyer_emplacement = lambda emplacement: None       # aucun dossier touche
echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + str(detail) if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
port = serveur.server_address[1]
threading.Thread(target=serveur.serve_forever, daemon=True).start()


def get(chemin, entetes=None):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=10)
    c.request("GET", chemin, headers=entetes or {})
    r = c.getresponse()
    corps = r.read()
    sortie = (r.status, dict((k.lower(), v) for k, v in r.getheaders()), corps)
    c.close()
    return sortie


def nb_prises():
    return json.loads(get("/places_invite")[2])["prises"]


o.INVITES_PAR_HEURE_ET_ADRESSE = 1000
print("Compteur et premiere table")
st, ent, corps = get("/places_invite", {"Origin": "http://localhost:8770"})
donnees = json.loads(corps)
verifier("0/15 au depart", donnees == {"prises": 0, "total": 15, "libres": 15}, donnees)
verifier("CORS ouvert a l'origine locale de Play", ent.get("access-control-allow-origin") == "http://localhost:8770", ent)
st, ent, _ = get("/places_invite", {"Origin": "https://pirate.example"})
verifier("CORS refuse a une origine etrangere", "access-control-allow-origin" not in ent)

st, ent, _ = get("/jouer-invite?joueurs=3")
verifier("l'hote invite entre (200, page d'attente)", st == 200, st)
verifier("il recoit un cookie de session", "nc_session=" in ent.get("set-cookie", ""), ent.get("set-cookie"))
verifier("le compteur passe a 1/15", nb_prises() == 1)
ligne = o.compte(next(r["pseudo"] for r in o._cx().execute("SELECT pseudo FROM comptes")))
verifier("la ligne est de role invite_play", ligne["role"] == "invite_play", ligne["role"])
verifier("son emplacement est dans le lot invite (31..45)", 31 <= ligne["emplacement"] <= 45, ligne["emplacement"])
verifier("il ne compte pas dans les comptes valides", o.nb_valides() == 0, o.nb_valides())
verifier("il n'apparait pas dans la liste des joueurs", o.liste_comptes() == [], len(o.liste_comptes()))

print()
print("Les comptes ne prennent jamais une place invite")
with o._cx() as cx:
    for n in range(1, 31):
        cx.execute("INSERT INTO comptes (pseudo,email,sel,empreinte,statut,cree,emplacement,role)"
                   " VALUES (?,?,?,?,?,?,?,?)", ("c%d" % n, "c%d@x.y" % n, "s", "e", "valide", "2026-11-03 10:00", n, "joueur"))
    verifier("30 comptes en place : plus d'emplacement pour un 31e COMPTE", o._prendre_un_emplacement(cx, "nouveau") == -1)
    cx.execute("DELETE FROM comptes WHERE pseudo LIKE 'c%' AND role = 'joueur'")

print()
print("Les 15 places, puis plein")
for _ in range(14):
    get("/jouer-invite")
verifier("15/15", nb_prises() == 15, nb_prises())
emplacements = sorted(r["emplacement"] for r in o._cx().execute("SELECT emplacement FROM comptes WHERE role='invite_play'"))
verifier("15 emplacements distincts, 31 a 45", emplacements == list(range(31, 46)), emplacements)
st, _, corps = get("/jouer-invite")
verifier("la 16e demande est refusee (503)", st == 503, st)
verifier("le compteur reste a 15", nb_prises() == 15)

print()
print("Liberation")
o.nettoyer_invites_perimes(delai_grace_s=10 ** 9)
verifier("dans le delai de grace, rien n'est libere", nb_prises() == 15, nb_prises())
o.nettoyer_invites_perimes(0)
verifier("sans moteur et passe le delai, tout est libere", nb_prises() == 0, nb_prises())
reste = o._cx().execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
verifier("les sessions jetables sont supprimees", reste == 0, reste)
st, _, _ = get("/jouer-invite")
verifier("une place se libere : une nouvelle table est possible", st == 200, st)

print()
print("Freins")
o.nettoyer_invites_perimes(0)
o.INVITES_PAR_HEURE_ET_ADRESSE = 3
o._INVITES_RECENTES.clear()
codes = [get("/jouer-invite")[0] for _ in range(4)]
verifier("la 4e table de la meme adresse en une heure est refusee (429)", codes == [200, 200, 200, 429], codes)
o.INVITES_PAR_HEURE_ET_ADRESSE = 1000
o.nettoyer_invites_perimes(0)


class Vivante:
    def vivant(self):
        return True


for i in range(o.MAX_TABLES_VIVANTES):
    o.PARTIES["x%d" % i] = Vivante()
st, _, _ = get("/jouer-invite")
verifier("trop de moteurs allumes : la table invite est refusee, les comptes sont epargnes", st == 503, st)
o.PARTIES.clear()

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
serveur.shutdown()
sys.exit(1 if echecs else 0)
