"""(Re)insere le lot GS-6 de Galactic Storm dans le depot : scenario 3 HALA ULTIMATUM (gs138-gs155) et
modulaire ACCUSER CORPS (gs156-gs160). IDEMPOTENT. Modele : inserer_gs4.py.

Ce que fait le script, dans l'ordre :
  1. data/cards.json, cle `galactic_storm` : remplace par card_id les cartes de defs/hala_ultimatum_cards.py
     et defs/accuser_corps_cards.py ; ordre existant conserve, cle `checksum` laissee en DERNIER.
  2. data/scenarios/gs_hala_ultimatum.json et gs_hala_ultimatum_expert.json ;
     data/encounter_sets/gs_hala_ultimatum.json et gs_accuser_corps.json (sans random_pick, aucune regle
     « N cartes sur M » n'est imprimee pour Accuser Corps).
  3. data/sets_info.json, entree « 144. Custom (Galactic Storm) » : declare le scenario et les deux sets.
  4. recalcule les checksums de cards.json et sets_info.json AVEC LE MOTEUR.

Usage (a la racine d'une copie du depot, apres `bash outils/preparer-worktree.sh`) :
    /home/oem/Desktop/Marvel\\ LCG/.venv-linux/bin/python3.10 .planning/galactic-storm/defs/inserer_gs6.py
"""
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
sys.path.insert(0, ICI)
import accuser_corps_cards as ACC  # noqa: E402
import hala_ultimatum_cards as HUC  # noqa: E402

PACK = "galactic_storm"
CLE_SET = "144. Custom (Galactic Storm)"
SCENARIO = "gs_hala_ultimatum"
MODULAIRE = "gs_accuser_corps"
CARDS = HUC.CARDS + ACC.CARDS


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
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", SCENARIO + ".json"),
           {"version": "0.5.8", "name": "Hala Ultimatum", "encounters": HUC.ENCOUNTERS}, 2)
    ecrire(os.path.join(MOTEUR, "data", "encounter_sets", MODULAIRE + ".json"),
           {"version": "0.5.8", "name": "Accuser Corps", "encounters": ACC.ENCOUNTERS}, 2)


def scenarios():
    base = {"version": "0.5.8", "name": "Hala Ultimatum",
            "villain": ["gs138a,gs138b", "gs139a,gs139b"], "expert": False,
            "schemes": ["gs141a,gs141b", "gs142a,gs142b"], "set_aside": HUC.SET_ASIDE,
            "encounters": HUC.ENCOUNTERS, "encounter_sets": ["standard"], "modular_sets": [MODULAIRE]}
    ecrire(os.path.join(MOTEUR, "data", "scenarios", f"{SCENARIO}.json"), base, 2)
    expert = dict(base, villain=["gs139a,gs139b", "gs140a,gs140b"], expert=True,
                  encounter_sets=["standard", "expert"])
    ecrire(os.path.join(MOTEUR, "data", "scenarios", f"{SCENARIO}_expert.json"), expert, 2)


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
    for nom in (SCENARIO, MODULAIRE):
        if nom not in s["encounters"]:
            s["encounters"].append(nom)
    s["max_id"] = max(s.get("max_id", "gs000"), "gs160")
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
    print(f"{len(CARDS)} cartes inserees, 2 scenarios et 2 sets de rencontre ecrits")
