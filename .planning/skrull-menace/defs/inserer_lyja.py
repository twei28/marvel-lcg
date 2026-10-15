"""Insere (ou REmplace) les 26 cartes du heros Lyja dans data/cards.json (cle `skrull_menace`),
declare le heros dans data/sets_info.json (`143. Custom (Skrull Menace)`) puis recalcule les checksums.

IDEMPOTENT : une carte deja presente est remplacee a sa place (meme card_id), une carte absente
est ajoutee en fin de liste. Source des valeurs : `defs/lyja_cards.py` (liste `CARDS`).
Usage (depuis n'importe ou) :  python3 .planning/skrull-menace/defs/inserer_lyja.py [racine_du_depot]
La racine par defaut est celle de la copie qui contient ce script.
"""
import importlib.util
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
PYTHON = os.environ.get("PYTHON_DU_DEPOT", sys.executable)

spec = importlib.util.spec_from_file_location("lyja_cards", os.path.join(ICI, "lyja_cards.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

chemin_cartes = os.path.join(MOTEUR, "data", "cards.json")
cartes = json.load(open(chemin_cartes, encoding="utf-8"))
liste = cartes["skrull_menace"]
index = {c.get("card_id"): i for i, c in enumerate(liste) if isinstance(c, dict)}
ajoutees = remplacees = 0
for carte in mod.CARDS:
    if carte["card_id"] in index:
        liste[index[carte["card_id"]]] = carte
        remplacees += 1
    else:
        liste.append(carte)
        index[carte["card_id"]] = len(liste) - 1
        ajoutees += 1
with open(chemin_cartes, "w", encoding="utf-8") as f:
    json.dump(cartes, f, indent=1, ensure_ascii=False)

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
entree = sets["143. Custom (Skrull Menace)"]
if "lyja" not in entree["heroes"]:
    entree["heroes"].append("lyja")
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"Lyja : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
