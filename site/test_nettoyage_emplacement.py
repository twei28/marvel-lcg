"""Recycler un emplacement efface TOUT ce qui suit le compte (14/11/2026).

Avant : la fiche Legacy, les arts de heros et les preferences (reglages, puzzles
crees, brouillons) restaient sur le disque, et le nouvel occupant les heritait.

Usage : python3 site/test_nettoyage_emplacement.py
"""
import os
import sys
import tempfile

_base = os.path.join(tempfile.gettempdir(), "nc-nettoyage-emplacement.db")
for _suffixe in ("", "-wal", "-shm"):
    try:
        os.remove(_base + _suffixe)
    except FileNotFoundError:
        pass
os.environ["BASE"] = _base
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + str(detail) if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


with tempfile.TemporaryDirectory() as racine:
    o.RACINE_JEU = racine
    game = os.path.join(racine, ".game")
    os.makedirs(game)
    du_compte = ["legacy-serveur-3.json", "arts-heros-serveur-3.json", "preferences-serveur-3.json",
                 "achievements-serveur-3.json", "games_history-serveur-3.json", "statistics-serveur-3.json"]
    autre_place = ["legacy-serveur-4.json", "preferences-serveur-4.json"]
    for nom in du_compte + autre_place:
        with open(os.path.join(racine, nom), "w") as f:
            f.write("{}")
    o._nettoyer_emplacement(3)
    for nom in du_compte:
        verifier(f"{nom} effacé", not os.path.exists(os.path.join(racine, nom)))
    for nom in autre_place:
        verifier(f"{nom} (autre place) intact", os.path.exists(os.path.join(racine, nom)))

print(f"\n{'ECHEC : ' + ', '.join(echecs) if echecs else 'tout est vert'}")
sys.exit(1 if echecs else 0)
