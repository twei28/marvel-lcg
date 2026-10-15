"""(Re)insere le bloc SKRULL PANTHEON (sk170-183) + DARD'VAN SECT (sk184-188) dans le depot. IDEMPOTENT.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `skrull_menace` : remplace par card_id les 25 cartes de defs/pantheon_cards.py
     (JSON indent=1, ensure_ascii=False, comme le reste du fichier) ; ordre existant conserve.
  2. data/scenarios/sk_skrull_pantheon.json et sk_skrull_pantheon_expert.json ; data/encounter_sets/sk_skrull_pantheon.json
     et sk_dard_van_sect.json.
  3. data/sets_info.json, entree `143. Custom (Skrull Menace)` : ajoute le scenario et les sets, remonte max_id.
  4. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR (tools/recalculer_checksums.py).

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    python3 .planning/skrull-menace/defs/inserer_pantheon.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
from pantheon_cards import CARDS, ENCOUNTERS_PANTHEON, ENCOUNTERS_DARDVAN  # noqa: E402

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
    # Deux mechants a deux faces : « a,b » = les deux faces d'une MEME carte (modele 60110a,60110b, Typhoid Mary).
    # Dard'van Sect est OBLIGATOIRE avec ce scenario (insert p.14) : set de rencontre fixe, pas modulaire ;
    # Skrull Society est le set modulaire que le livret autorise a retirer.
    base = {"version": "0.5.8", "name": "Skrull Pantheon", "villain": ["sk170a,sk170b", "sk171a,sk171b"], "expert": False,
            "schemes": ["sk173a,sk173b", "sk174a,sk174b"], "set_aside": ["sk175a,sk175b"],
            "encounters": ENCOUNTERS_PANTHEON, "encounter_sets": ["standard", "sk_dard_van_sect"],
            "modular_sets": ["sk_skrull_society"]}
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_skrull_pantheon.json"), base, 2)
    expert = dict(base, villain=["sk171a,sk171b", "sk172a,sk172b"], expert=True,
                  encounter_sets=["standard", "expert", "sk_dard_van_sect"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", "sk_skrull_pantheon_expert.json"), expert, 2)
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "sk_skrull_pantheon.json"),
           {"version": "0.5.8", "name": "Skrull Pantheon", "encounters": ENCOUNTERS_PANTHEON}, 2)
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "sk_dard_van_sect.json"),
           {"version": "0.5.8", "name": "Dard'van Sect", "encounters": ENCOUNTERS_DARDVAN}, 2)


def sets_info():
    chemin = os.path.join(MOTEUR, "data", "sets_info.json")
    d = json.loads(open(chemin, encoding="utf-8", newline="").read())
    s = d[CLE_SET]
    if "sk_skrull_pantheon" not in s["scenarios"]:
        s["scenarios"].append("sk_skrull_pantheon")
    for nom in ("sk_skrull_pantheon", "sk_dard_van_sect"):
        if nom not in s["encounters"]:
            s["encounters"].append(nom)
    s["max_id"] = max(s["max_id"], "sk188")
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
    scenarios()
    sets_info()
    checksums()
    print(f"{len(CARDS)} cartes inserees, scenarios et sets ecrits")
