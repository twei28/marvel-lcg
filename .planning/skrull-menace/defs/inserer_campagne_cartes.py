"""(Re)insere les CARTES DE CAMPAGNE (sk263-sk289b + 2 gabarits techniques) dans le depot. IDEMPOTENT.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `skrull_menace` : remplace par card_id les cartes de
     defs/campagne_cartes_cards.py (JSON indent=1, ensure_ascii=False, comme le reste du fichier) ;
     ordre existant conserve, les nouvelles cartes sont ajoutees a la fin.
  2. data/sets_info.json, entree `143. Custom (Skrull Menace)` : remonte `max_id` (« sk289b » > « sk262 »
     en comparaison de chaines). Aucun scenario ni ensemble de rencontre : les cartes de campagne
     n'entrent dans un deck que par la Cooperation Area.
  3. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    python3 .planning/skrull-menace/defs/inserer_campagne_cartes.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from campagne_cartes_cards import CARDS  # noqa: E402

CLE_SET = "143. Custom (Skrull Menace)"


def ecrire(chemin, obj, indent):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def cartes():
    chemin = os.path.join(MOTEUR, "data", "cards.json")
    texte = open(chemin, encoding="utf-8", newline="").read()
    d = json.loads(texte)
    neuves = {x["card_id"]: x for x in CARDS}
    liste = [neuves.pop(x["card_id"], x) for x in d["skrull_menace"]]
    d["skrull_menace"] = liste + list(neuves.values())
    ecrire(chemin, d, 1)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    s = d[CLE_SET]
    s["max_id"] = max(s["max_id"], "sk289b")
    ecrire(chemin, d, 1)


def checksums():
    pyenv = os.environ.copy()
    pyenv["PYTHONPATH"] = os.path.join(MOTEUR, ".game-src")
    py = os.path.join(os.path.dirname(RACINE), "..", "..", ".venv-linux", "bin", "python")
    if not os.path.exists(py):
        py = "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"
    subprocess.run([py, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                    os.path.join(MOTEUR, "data", "cards.json"), os.path.join(MOTEUR, "data", "sets_info.json")],
                   cwd=MOTEUR, env=pyenv, check=True)


if __name__ == "__main__":
    cartes()
    sets_info()
    checksums()
    print(f"{len(CARDS)} cartes inserees")
