"""(Re)insere le bloc SECRET INVASION (sk189-227) dans le depot. IDEMPOTENT.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `skrull_menace` : remplace par card_id les 64 cartes de defs/secret_invasion_cards.py
     (JSON indent=1, ensure_ascii=False, comme le reste du fichier) ; ordre existant conserve.
  2. data/scenarios/sk_secret_invasion.json et sk_secret_invasion_expert.json ; data/encounter_sets/sk_secret_invasion.json.
  3. data/sets_info.json, entree `143. Custom (Skrull Menace)` : ajoute le scenario et le set, remonte max_id.
  4. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    python3 .planning/skrull-menace/defs/inserer_secret_invasion.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from secret_invasion_cards import CARDS, ENCOUNTERS_SI, SET_ASIDE  # noqa: E402

CLE_SET = "143. Custom (Skrull Menace)"


def ecrire(chemin, obj, indent):
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        json.dump(obj, f, indent=indent, ensure_ascii=False)


def cartes():
    chemin = os.path.join(MOTEUR, "data", "cards.json")
    texte = open(chemin, encoding="utf-8", newline="").read()
    d = json.loads(texte)
    # Ordre existant CONSERVE (pas de tri : les autres blocs ajoutent a la suite, un tri ferait un diff
    # geant) : une carte deja presente est remplacee en place, les nouvelles sont ajoutees a la fin.
    neuves = {x["card_id"]: x for x in CARDS}
    liste = [neuves.pop(x["card_id"], x) for x in d["skrull_menace"]]
    d["skrull_menace"] = liste + list(neuves.values())
    ecrire(chemin, d, 1)


def scenarios():
    base = {"version": "0.5.8", "name": "Secret Invasion",
            "villain": ["sk189a,sk189b", "sk190a,sk190b"], "expert": False,
            "schemes": ["sk192a,sk192b", "sk193a,sk193b"], "set_aside": SET_ASIDE, "encounters": ENCOUNTERS_SI,
            "encounter_sets": ["standard"], "modular_sets": ["sk_army_of_skrulls"]}
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_secret_invasion.json"), base, 2)
    expert = dict(base, villain=["sk190a,sk190b", "sk191a,sk191b"], expert=True, encounter_sets=["standard", "expert"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_secret_invasion_expert.json"), expert, 2)
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "sk_secret_invasion.json"),
           {"version": "0.5.8", "name": "Secret Invasion", "encounters": ENCOUNTERS_SI}, 2)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    s = d[CLE_SET]
    if "sk_secret_invasion" not in s["scenarios"]:
        s["scenarios"].append("sk_secret_invasion")
    if "sk_secret_invasion" not in s["encounters"]:
        s["encounters"].append("sk_secret_invasion")
    s["max_id"] = max(s["max_id"], "sk227")
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
