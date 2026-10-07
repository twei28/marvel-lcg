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
    E.Enregistrement.Evenement("c", {"p": 0, "x": 0.5, "y": 0.2, "clic": 3})
    brut = E.Enregistrement.Fichier()
    lignes = [json.loads(x) for x in gzip.decompress(brut).decode("utf-8").splitlines()]
    cas("en-tete en premier", lignes[0]["k"], "entete")
    cas("en-tete garde le scenario", lignes[0]["scenario"], "Rhino")
    cas("partie inachevee", lignes[0]["resultat"], "inachevee")
    cas("rounds", lignes[0]["rounds"], 5)
    cles = [l for l in lignes if l["k"] == "cle"]
    cas("un monde complet tous les 51 rendus", [l["r"] for l in cles], [1, 52, 103])
    cas("curseur rattache au dernier rendu", lignes[-1]["r"], 120)
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

    E.Enregistrement.Rendu("partie-2", {"render_id": 1, "game_over": True, "players_won": True}, entete)
    fin = json.loads(gzip.decompress(E.Enregistrement.Fichier()).decode("utf-8").splitlines()[0])
    cas("nouvelle partie, nouveau fichier, victoire", fin["resultat"], "victoire")
    for n in range(3, 7):
        E.Enregistrement.Rendu("partie-%d" % n, {"render_id": 1}, entete)
    cas("seules les 3 dernieres parties restent", len(os.listdir(dossier)), 3)

print("\n%s" % ("TOUT EST VERT" if echecs == 0 else "%d ECHEC(S)" % echecs))
sys.exit(1 if echecs else 0)
