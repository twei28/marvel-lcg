#!/usr/bin/env python3
"""Tests du format de puzzle v2 et de sa validation (docs/puzzle/FORMAT-V2.md).

Lancement : python3 outils/test_puzzle_format.py
Aucune partie n'est démarrée : on charge seulement les modules du moteur.
"""
import glob
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, os.path.join(MOTEUR, "src"))

from engine import Engine  # noqa: E402,F401  (l'ordre d'import du moteur l'exige)
from engine.lib.json import Json  # noqa: E402
from game.puzzle.puzzle import RunPuzzle  # noqa: E402
from game.puzzle.puzzle_data import PuzzleData, PuzzleObjective  # noqa: E402
from game.puzzle.puzzle_validation import validate_command, validate_puzzle  # noqa: E402

METHODES = {n for n in dir(RunPuzzle) if n[:1].isupper()}
echecs = []


def verifie(condition, message):
    if not condition:
        echecs.append(message)
        print("ECHEC :", message)


def charge(chemin):
    return Json.LoadsAs(open(chemin, encoding="utf-8").read(), PuzzleData)


# 1. Les fichiers v1 existants se lisent, restent en format 1 et sont valides.
fichiers = sorted(glob.glob(os.path.join(MOTEUR, "puzzle", "**", "*.json"), recursive=True))
verifie(fichiers, "aucun puzzle v1 trouvé")
for f in fichiers:
    p = charge(f)
    nom = os.path.relpath(f, MOTEUR)
    verifie(p.format == 1, f"{nom} : format v1 attendu")
    verifie(p.objectives == [] and p.title == "", f"{nom} : défauts v2 attendus")
    erreurs = validate_puzzle(p, METHODES)
    verifie(not erreurs, f"{nom} : {erreurs}")

# 2. Commandes valides.
for c in ["Puzzle.Damage(c3, 12)", "Puzzle.PutIntoPlay('Iron Man');", "Puzzle.PlaceThreat(c5, -3)",
          "Puzzle.End('Let\\'s go!')", "Puzzle.MoveTo(c4, 'Hand', player=1)",
          "Puzzle.InstallerVille([['a','b'],['c','d']], (1, 1))", "Puzzle.End()",
          # E2 (23/10/2026) : PV absolus, et gain / pioche d'un siege precis
          "Puzzle.SetHealth('01094', 9)", "Puzzle.Draw(1, siege=2)", "Puzzle.Gain('01072', siege=1)"]:
    verifie(validate_command(c, METHODES) is None, f"commande valide refusée : {c} -> {validate_command(c, METHODES)}")

# 3. Commandes hostiles ou mal formées : toutes doivent être refusées.
hostiles = [
    "import os", "Puzzle.world.rule = 1", "x = 1", "Puzzle.Damage(c3, 1); Puzzle.Damage(c3, 1)",
    "__import__('os').system('ls')", "os.system('ls')", "Puzzle.Damage(c3, 1).foo()",
    "Puzzle.world.x()", "Puzzle._Hidden()", "Puzzle.damage(c3, 1)", "Puzzle.Nope()",
    "Puzzle.Damage(c3, [x for x in ()])", "Puzzle.Damage(c3, lambda: 1)", "Puzzle.Damage(*a)",
    "Puzzle.Damage(**a)", "Puzzle.Damage(c3, 10**9)", "Puzzle.Damage(c3, 99999999)",
    "Puzzle.Damage(c3, 'x' * 5)", "Puzzle.Damage(c3, Puzzle.world)", "Puzzle.Damage(c3, evil)",
    "Puzzle.Damage(c3, 1.5)", "Puzzle.Damage(c3, b'x')", "Puzzle.Damage(c3, f'{1}')",
    "", "   ;", "Puzzle.Damage(", "@Puzzle.Damage\ndef f(): pass", "with open('x') as f: pass",
    "Puzzle.Damage(c3, 1) if True else 0", "A" * 500, "Puzzle.End('" + "x" * 300 + "')",
    "Puzzle.Damage(c3, [[[[1]]]])", 123, None,
]
for c in hostiles:
    verifie(validate_command(c, METHODES) is not None, f"commande hostile acceptée : {c!r}")

# 4. Un puzzle v2 complet : aller-retour JSON puis validation.
p = charge(os.path.join(MOTEUR, "puzzle", "puzzle-01071.json"))
p.format = 2
p.title = "Défaite du Rhino"
p.description = "Vous avez 3 cartes."
p.difficulty = 2
p.hints = ["Regardez la défausse."]
p.objectives = [PuzzleObjective(kind="defeat_villain"), PuzzleObjective(kind="free_text", text="Sans perdre de PV")]
p.objectives_mode = "all"
p.first_player = 0
p.solution_visibility = "always"
copie = Json.LoadsAs(Json.Dumps(p), PuzzleData)
verifie(copie.title == p.title and copie.difficulty == 2 and copie.hints == p.hints, "aller-retour des métadonnées")
verifie(len(copie.objectives) == 2 and copie.objectives[1].text == "Sans perdre de PV", "aller-retour des objectifs")
verifie(isinstance(copie.objectives[0], PuzzleObjective), "objectif reconverti en dataclass")
verifie(validate_puzzle(copie, METHODES) == [], f"puzzle v2 valide refusé : {validate_puzzle(copie, METHODES)}")

# 5. Un puzzle v2 invalide : chaque défaut doit être signalé.
def defaut(modif, motif):
    q = Json.LoadsAs(Json.Dumps(copie), PuzzleData)
    modif(q)
    erreurs = validate_puzzle(q, METHODES)
    verifie(any(motif in e for e in erreurs), f"défaut non signalé ({motif}) : {erreurs}")

defaut(lambda q: setattr(q, "difficulty", 9), "difficulté")
defaut(lambda q: setattr(q, "title", "x" * 200), "titre")
defaut(lambda q: setattr(q, "hints", ["a"] * 50), "indices")
defaut(lambda q: setattr(q, "objectives_mode", "xor"), "mode d'objectifs")
defaut(lambda q: setattr(q, "objectives", [PuzzleObjective(kind="magie")]), "inconnu")
defaut(lambda q: setattr(q, "objectives", [PuzzleObjective(kind="free_text")]), "texte est obligatoire")
defaut(lambda q: setattr(q, "objectives", [PuzzleObjective(kind="complete_scheme")]), "cible est obligatoire")
defaut(lambda q: setattr(q, "start_phase", "nuit"), "phase de départ")
defaut(lambda q: setattr(q, "solution_visibility", "x"), "visibilité")
defaut(lambda q: setattr(q, "first_player", 5), "premier joueur")
defaut(lambda q: setattr(q, "players", []), "joueurs")
defaut(lambda q: setattr(q, "players", q.players * 5), "joueurs")
defaut(lambda q: setattr(q.players[0], "hand_cards", ["../../etc"]), "identifiant de carte")
defaut(lambda q: setattr(q.players[0], "player_deck", ["01001a"] * 500), "plus de")
defaut(lambda q: setattr(q, "puzzle_command", ["import os"]), "commande 1")
defaut(lambda q: setattr(q, "puzzle_command", ["Puzzle.End()"] * 3000), "commandes")
defaut(lambda q: setattr(q, "format", 7), "format")

print("OK" if not echecs else f"{len(echecs)} échec(s)")
sys.exit(1 if echecs else 0)
