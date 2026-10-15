"""(Re)insere les sets MODULAIRES restants (sk228-sk262) dans le depot. IDEMPOTENT.

Sets : Shaper of Worlds, Skrull Elite (Crusader, Jazinda, Skymax, War Skrull, Xavin), Standard Skrull, Expert Skrull.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `skrull_menace` : remplace par card_id les cartes de defs/modulaires_cards.py
     (JSON indent=1, ensure_ascii=False, ordre existant conserve, nouvelles cartes a la suite).
  2. data/encounter_sets/sk_<set>.json (un fichier par set, `ENCOUNTERS`).
  3. data/scenarios/sk_essai_*.json : scenarios d'ESSAI (non declares dans sets_info.json, donc invisibles de
     l'ecran de choix) qui montent un Rhino avec ces sets en modulaires, pour la batterie `[modulaires]`.
  4. data/sets_info.json, entree `143. Custom (Skrull Menace)` : declare les sets, remonte max_id.
  5. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    python3 .planning/skrull-menace/defs/inserer_modulaires.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from modulaires_cards import ANCIENS_NOMS, CARDS, ENCOUNTERS  # noqa: E402

CLE_SET = "143. Custom (Skrull Menace)"
TOUS_LES_MODULAIRES = ["sk_shaper_of_worlds", "sk_skrull_elite_crusader", "sk_skrull_elite_jazinda",
                       "sk_skrull_elite_skymax", "sk_skrull_elite_war_skrull", "sk_skrull_elite_xavin"]


def ecrire(chemin, obj, indent):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def cartes():
    chemin = os.path.join(MOTEUR, "data", "cards.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    neuves = {x["card_id"]: x for x in CARDS}
    liste = [neuves.pop(x["card_id"], x) for x in d["skrull_menace"]]
    d["skrull_menace"] = liste + list(neuves.values())
    ecrire(chemin, d, 1)


def sets_de_rencontre():
    for ancien in ANCIENS_NOMS:
        chemin = os.path.join(MOTEUR, "data", "encounter_sets", ancien + ".json")
        if os.path.exists(chemin):
            os.remove(chemin)
    for fichier, (nom, ids) in ENCOUNTERS.items():
        ecrire(os.path.join(MOTEUR, "data", "encounter_sets", fichier + ".json"),
               {"version": "0.5.8", "name": nom, "encounters": ids}, 2)


def scenarios_d_essai():
    rhino = json.loads(open(os.path.join(MOTEUR, "data", "scenarios", "rhino.json"), encoding="utf-8").read())
    base = dict(rhino, name="Rhino (essai modulaires Skrull Menace)", modular_sets=TOUS_LES_MODULAIRES)
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_essai_modulaires.json"), base, 2)
    # Standard Skrull REMPLACE Standard ; Expert Skrull REMPLACE Expert (livret : « you may replace them »).
    standard = dict(base, name="Rhino (essai Standard Skrull)", encounter_sets=["standard_skrull"], modular_sets=[])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_essai_skrull_standard.json"), standard, 2)
    expert_rhino = json.loads(open(os.path.join(MOTEUR, "data", "scenarios", "rhino_expert.json"), encoding="utf-8").read())
    expert = dict(expert_rhino, name="Rhino expert (essai Standard + Expert Skrull)",
                  encounter_sets=["standard_skrull", "expert_skrull"], modular_sets=[])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_essai_skrull_expert.json"), expert, 2)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    s = d[CLE_SET]
    s["encounters"] = [n for n in s["encounters"] if n not in ANCIENS_NOMS]
    for nom in ENCOUNTERS:
        if nom not in s["encounters"]:
            s["encounters"].append(nom)
    s["max_id"] = max(s["max_id"], "sk262")
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
    sets_de_rencontre()
    scenarios_d_essai()
    sets_info()
    checksums()
    print(f"{len(CARDS)} cartes inserees, {len(ENCOUNTERS)} sets et 3 scenarios d'essai ecrits")
