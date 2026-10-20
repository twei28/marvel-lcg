"""(Re)insere le scenario 2 MAJESTRIX'S VERDICT de Galactic Storm (gs114-gs137) dans le depot. IDEMPOTENT.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `galactic_storm` (creee si absente) : remplace par card_id les 27 cartes de
     defs/majestrix_cards.py (JSON indent=1, ensure_ascii=False) ; ordre existant conserve, les autres cartes
     du pack (heros, autres scenarios, ecrits par d'autres lots) ne sont pas touchees.
  2. data/scenarios/gs_majestrix_verdict.json et gs_majestrix_verdict_expert.json ;
     data/encounter_sets/gs_majestrix_verdict.json.
  3. data/sets_info.json, entree `144. Custom (Galactic Storm)` (creee si absente) : ajoute le scenario et le
     set, remonte max_id.
  4. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    python3 .planning/galactic-storm/defs/inserer_majestrix.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from majestrix_cards import CARDS, ENCOUNTERS, SET_ASIDE  # noqa: E402

CLE_SET = "144. Custom (Galactic Storm)"
PACK = "galactic_storm"
SCENARIO = "gs_majestrix_verdict"
# Le set modulaire du livret, Imperial Guard, appartient au lot GS-4 (pas encore porte) : en attendant, un set
# officiel au theme Kree-Shi'ar (question Q1 de .planning/todos/2026-10-20-gs5-questions.md).
MODULAIRE = "kree_militants"


def ecrire(chemin, obj, indent):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def cartes():
    chemin = os.path.join(MOTEUR, "data", "cards.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    neuves = {x["card_id"]: x for x in CARDS}
    liste = [neuves.pop(x["card_id"], x) for x in d.get(PACK, [])]
    d[PACK] = liste + list(neuves.values())
    ecrire(chemin, d, 1)


def scenarios():
    base = {"version": "0.5.8", "name": "Majestrix's Verdict", "villain": ["gs114", "gs115"], "expert": False,
            "schemes": ["gs117a,gs117b", "gs118a,gs118b"], "set_aside": SET_ASIDE, "encounters": ENCOUNTERS,
            "encounter_sets": ["standard"], "modular_sets": [MODULAIRE]}
    ecrire(os.path.join(MOTEUR, "data", "scenarios", f"{SCENARIO}.json"), base, 2)
    expert = dict(base, villain=["gs115", "gs116"], expert=True, encounter_sets=["standard", "expert"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", f"{SCENARIO}_expert.json"), expert, 2)
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", f"{SCENARIO}.json"),
           {"version": "0.5.8", "name": "Majestrix's Verdict", "encounters": ENCOUNTERS}, 2)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    if CLE_SET not in d:
        # Insere avant la cle « checksum » (toujours la derniere du fichier).
        somme = d.pop("checksum", None)
        d[CLE_SET] = {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": "gs000"}
        if somme is not None:
            d["checksum"] = somme
    s = d[CLE_SET]
    if SCENARIO not in s["scenarios"]:
        s["scenarios"].append(SCENARIO)
    if SCENARIO not in s["encounters"]:
        s["encounters"].append(SCENARIO)
    s["max_id"] = max(s["max_id"], "gs137")
    ecrire(chemin, d, 1)


def checksums():
    pyenv = os.environ.copy()
    pyenv["PYTHONPATH"] = os.path.join(MOTEUR, ".game-src")
    py = "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python"
    subprocess.run([py, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                    os.path.join(MOTEUR, "data", "cards.json"), os.path.join(MOTEUR, "data", "sets_info.json")],
                   cwd=MOTEUR, env=pyenv, check=True)


if __name__ == "__main__":
    cartes()
    scenarios()
    sets_info()
    checksums()
    print(f"{len(CARDS)} cartes inserees, scenarios et set ecrits")
