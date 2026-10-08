"""Enregistrement d'une partie (« Revoir sa partie ») : difference, fichier, purge.

Usage: RELEASE=1 python3.10 tools/test_enregistrement.py
"""
import gzip
import json
import os
import sys
import tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
os.environ.setdefault("RELEASE", "1")

from engine import enregistrement as E

echecs = 0


def cas(nom, obtenu, attendu):
    global echecs
    if obtenu == attendu:
        print("  ok    %s" % nom)
    else:
        echecs += 1
        print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))


a = {"render_id": 1, "phase": "P", "players": [{"hand": [1, 2], "hp": 10}], "vieux": 1}
b = {"render_id": 2, "phase": "P", "players": [{"hand": [1, 2, 3], "hp": 9}], "neuf": True}
d = E.difference(a, b)
cas("aller-retour", E.appliquer(a, d), b)
cas("egal = rien", E.difference(a, a), None)
cas("cle retiree", d.get("x"), ["vieux"])
cas("liste de meme longueur par indice", "i" in d["o"]["players"], True)
cas("a n'est pas modifie", a["players"][0]["hand"], [1, 2])
cas("type qui change", E.appliquer(1, E.difference(1, [1])), [1])

with tempfile.TemporaryDirectory() as dossier:
    E.Enregistrement.dossier = staticmethod(lambda: dossier)
    entete = lambda: {"scenario": "Rhino", "joueurs": ["Spider-Man"]}
    mondes = [{"render_id": i, "round_id": 1 + i // 30, "x": i % 7} for i in range(1, 121)]
    for m in mondes:
        E.Enregistrement.Rendu("partie-1", m, entete)
    E.Enregistrement.Rendu("partie-1", {"render_id": 121, "round_id": 5, "x": 0}, entete, {13: "Y", 14: "RR"})
    E.Enregistrement.Rendu("partie-1", {"render_id": 122, "round_id": 5, "x": 1}, entete, {13: "Y", 15: "B"})
    mondes += [{"render_id": 121, "round_id": 5, "x": 0}, {"render_id": 122, "round_id": 5, "x": 1}]
    E.Enregistrement.Evenement("c", {"p": 0, "x": 0.5, "y": 0.2, "clic": 3})
    brut = E.Enregistrement.Fichier()
    lignes = [json.loads(x) for x in gzip.decompress(brut).decode("utf-8").splitlines()]
    cas("en-tete en premier", lignes[0]["k"], "entete")
    cas("en-tete garde le scenario", lignes[0]["scenario"], "Rhino")
    cas("partie inachevee", lignes[0]["resultat"], "inachevee")
    cas("rounds", lignes[0]["rounds"], 5)
    cles = [l for l in lignes if l["k"] == "cle"]
    cas("un monde complet tous les 51 rendus", [l["r"] for l in cles], [1, 52, 103])
    cas("curseur rattache au dernier rendu", lignes[-1]["r"], 122)
    res = [l["m"] for l in lignes if l["k"] == "res"]
    cas("ressources des mains, chaque carte une seule fois", res, [{"13": "Y", "14": "RR"}, {"15": "B"}])
    monde = None
    rejoues = []
    for l in lignes:
        if l["k"] == "cle":
            monde = l["m"]
        elif l["k"] == "d":
            monde = E.appliquer(monde, l["d"])
        else:
            continue
        rejoues.append(monde)
    cas("tous les mondes se reconstruisent", rejoues, mondes)

    # L'en-tete se complete au round 1 : au premier rendu, le heros n'est pas pose.
    appels = []
    def entete_qui_change():
        appels.append(1)
        return {"joueurs": [{"heros": "rule" if len(appels) == 1 else "Spider-Man"}]}
    E.Enregistrement.Rendu("partie-x", {"render_id": 1, "round_id": 0}, entete_qui_change)
    E.Enregistrement.Rendu("partie-x", {"render_id": 2, "round_id": 1}, entete_qui_change)
    x = json.loads(gzip.decompress(E.Enregistrement.Fichier()).decode("utf-8").splitlines()[0])
    cas("en-tete complete au round 1", x["joueurs"], [{"heros": "Spider-Man"}])
    E.Enregistrement.Rendu("partie-2", {"render_id": 1, "game_over": True, "players_won": True}, entete)
    fin = json.loads(gzip.decompress(E.Enregistrement.Fichier()).decode("utf-8").splitlines()[0])
    cas("nouvelle partie, nouveau fichier, victoire", fin["resultat"], "victoire")
    for n in range(3, 7):
        E.Enregistrement.Rendu("partie-%d" % n, {"render_id": 1}, entete)
    cas("seules les 3 dernieres parties restent", len(os.listdir(dossier)), 3)

# Les parties TERMINEES de l'hote, rangees pour l'administrateur et pour lui.
import threading  # noqa: E402
class _Fil:
    def __init__(self, target, args=(), daemon=None):
        self.f, self.a = target, args
    def start(self):
        self.f(*self.a)
E.threading.Thread = _Fil
with tempfile.TemporaryDirectory() as racine:
    chez = os.path.join(racine, "arnaud")
    E.Enregistrement.DossierDeLHote = staticmethod(lambda: chez)
    with tempfile.TemporaryDirectory() as enreg:
        E.Enregistrement.dossier = staticmethod(lambda: enreg)
        for n in range(5):
            E.Enregistrement.Rendu("fin-%d" % n, {"render_id": 1, "round_id": 2}, entete)
            E.Enregistrement.Rendu("fin-%d" % n, {"render_id": 2, "round_id": 2, "game_over": True, "players_won": True}, entete)
            E.Enregistrement.Rendu("fin-%d" % n, {"render_id": 3, "round_id": 2, "game_over": True, "players_won": True}, entete)
            import time as _t; _t.sleep(1.05)
        E.Enregistrement.Rendu("inachevee", {"render_id": 1, "round_id": 1}, entete)
    cas("une partie terminee est rangee chez l'hote, ses 3 dernieres gardees", len(E.Enregistrement.PartiesDeLHote()), 3)
    premiere = os.path.join(chez, E.Enregistrement.PartiesDeLHote()[0])
    cas("le fichier rangé est une partie gagnee", json.loads(gzip.decompress(open(premiere, "rb").read()).decode("utf-8").splitlines()[0])["resultat"], "victoire")

# CE QUE LE JOUEUR VOIT (08/10/2026) : /set_vu enregistre une ligne « v »,
# relayee au spectateur par /get_vus. Genre inconnu et valeur trop longue refuses.
import asyncio
from engine.device.web.server.server_get import GameServerGet


class _Requete:
    def __init__(self, donnees):
        self.donnees = donnees

    async def json(self):
        return self.donnees


class _Table:
    GENRES_VUS = GameServerGet.GENRES_VUS
    TAILLE_VU_MAX = GameServerGet.TAILLE_VU_MAX
    TAILLE_REGLAGES_MAX = GameServerGet.TAILLE_REGLAGES_MAX


with tempfile.TemporaryDirectory() as enreg:
    E.Enregistrement.dossier = staticmethod(lambda: enreg)
    E.Enregistrement.Rendu("vus", {"render_id": 7, "round_id": 1}, entete)
    table = _Table()
    poster = lambda d: asyncio.run(GameServerGet.set_vu(table, _Requete(d))).status
    cas("une selection est acceptee", poster({"p": 0, "g": "sel", "v": {"e": "x", "o": 3, "c": [12], "r": []}}), 200)
    cas("un genre inconnu est refuse", poster({"p": 0, "g": "n_importe_quoi", "v": 1}), 400)
    cas("une valeur trop longue est refusee", poster({"p": 0, "g": "loupe", "v": "x" * 5000}), 413)
    cas("les reglages ont droit a plus", poster({"p": 0, "g": "regl", "v": {"mc_a": "x" * 5000}}), 200)
    relayes = json.loads(asyncio.run(GameServerGet.get_vus(table, None)).text)
    cas("le spectateur lit la derniere valeur de chaque genre", relayes["0"]["sel"]["c"], [12])
    lignes = [json.loads(x) for x in gzip.decompress(E.Enregistrement.Fichier()).decode("utf-8").splitlines()]
    vus = [l for l in lignes if l["k"] == "v"]
    cas("deux lignes v enregistrees (les refus n'en laissent pas)", [l["g"] for l in vus], ["sel", "regl"])
    cas("rattachees au dernier rendu", vus[0]["r"], 7)

print("\n%s" % ("TOUT EST VERT" if echecs == 0 else "%d ECHEC(S)" % echecs))
sys.exit(1 if echecs else 0)
