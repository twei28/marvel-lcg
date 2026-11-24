"""(Re)insere le lot GS-8 de Galactic Storm dans le depot. IDEMPOTENT.

Contenu : scenario 5 Supreme Intelligence (gs195-gs208) et les sets modulaires Starforce (gs209-gs217),
Seeds of Corruption (gs218-gs221), Nega-Bomb (gs222a/gs222b, gs223).

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `galactic_storm` (creee si absente) : remplace par card_id les cartes de
     defs/supreme_intelligence_cards.py (JSON indent=1, ensure_ascii=False, ordre existant conserve, nouvelles
     cartes a la suite, cle `checksum` laissee en DERNIER).
  2. data/encounter_sets/gs_<set>.json (un fichier par set modulaire).
  3. data/scenarios/gs_supreme_intelligence.json (+ _expert) : scenario jouable seul, hors campagne.
     data/scenarios/gs_essai_modulaires_gs8.json : scenario d'ESSAI (non declare dans sets_info, donc
     invisible) qui monte Rhino avec Seeds of Corruption + Nega-Bomb pour les cas `[gs8]`.
  4. data/sets_info.json, entree `144. Custom (Galactic Storm)` (creee si absente) : declare le scenario et
     les sets, remonte max_id.
  5. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    /home/oem/Desktop/Marvel\\ LCG/.venv-linux/bin/python3.10 .planning/galactic-storm/defs/inserer_supreme_intelligence.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from supreme_intelligence_cards import CARDS, ENCOUNTERS, ENCOUNTERS_SCENARIO, STARFORCE  # noqa: E402

PACK = "galactic_storm"
CLE_SET = "144. Custom (Galactic Storm)"
SCENARIO = "gs_supreme_intelligence"


def ecrire(chemin, obj, indent):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def cartes():
    chemin = os.path.join(MOTEUR, "data", "cards.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    neuves = {x["card_id"]: x for x in CARDS}
    existantes = d.get(PACK, [])
    liste = [neuves.pop(x["card_id"], x) for x in existantes]
    nouveau = {}
    for k, v in d.items():
        if k == "checksum":
            continue
        nouveau[k] = v
    nouveau[PACK] = liste + list(neuves.values())
    if "checksum" in d:
        nouveau["checksum"] = d["checksum"]
    ecrire(chemin, nouveau, 1)


def sets_de_rencontre():
    for fichier, (nom, ids) in ENCOUNTERS.items():
        ecrire(os.path.join(MOTEUR, "data", "encounter_sets", fichier + ".json"),
               {"version": "0.5.8", "name": nom, "encounters": ids}, 2)


def scenarios():
    base = {
        "version": "0.5.8",
        "name": "Supreme Intelligence",
        "villain": ["gs195", "gs196"],
        "expert": False,
        "schemes": ["gs198a,gs198b", "gs199a,gs199b"],
        "set_aside": ["gs200"],
        "encounters": ENCOUNTERS_SCENARIO + STARFORCE,
        "encounter_sets": ["standard"],
        "modular_sets": ["gs_seeds_of_corruption"],
    }
    ecrire(os.path.join(MOTEUR, "data", "scenarios", SCENARIO + ".json"), base, 2)
    expert = dict(base, villain=["gs196", "gs197"], expert=True, encounter_sets=["standard", "expert"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", SCENARIO + "_expert.json"), expert, 2)
    rhino = json.loads(open(os.path.join(MOTEUR, "data", "scenarios", "rhino.json"), encoding="utf-8").read())
    essai = dict(rhino, name="Rhino (essai modulaires Galactic Storm GS-8)",
                 modular_sets=["gs_seeds_of_corruption", "gs_nega_bomb", "gs_starforce"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "gs_essai_modulaires_gs8.json"), essai, 2)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    if CLE_SET not in d:
        nouveau = {}
        for k, v in d.items():
            if k == "checksum":
                continue
            nouveau[k] = v
        nouveau[CLE_SET] = {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": "gs000"}
        if "checksum" in d:
            nouveau["checksum"] = d["checksum"]
        d = nouveau
    s = d[CLE_SET]
    if SCENARIO not in s["scenarios"]:
        s["scenarios"].append(SCENARIO)
    for nom in ENCOUNTERS:
        if nom not in s["encounters"]:
            s["encounters"].append(nom)
    s["max_id"] = max(s.get("max_id", "gs000"), "gs223")
    ecrire(chemin, d, 1)


def checksums():
    pyenv = os.environ.copy()
    pyenv["PYTHONPATH"] = os.path.join(MOTEUR, ".game-src")
    py = "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python3.10"
    subprocess.run([py, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                    os.path.join(MOTEUR, "data", "cards.json"), os.path.join(MOTEUR, "data", "sets_info.json")],
                   cwd=MOTEUR, env=pyenv, check=True)


if __name__ == "__main__":
    cartes()
    sets_de_rencontre()
    scenarios()
    sets_info()
    checksums()
    print(f"{len(CARDS)} cartes inserees, {len(ENCOUNTERS)} sets, 2 scenarios + 1 scenario d'essai ecrits")
