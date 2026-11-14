"""Insere (ou REMPLACE) les cartes du SCENARIO Lady Deathstrike (Mysteltainn) dans data/cards.json (cle `lady_deathstrike`),
ecrit data/scenarios/lady_deathstrike(.json|_expert.json), data/encounter_sets/lady_deathstrike.json et reaver_resources.json,
declare le tout dans data/sets_info.json (`213. Custom (Lady Deathstrike)`) puis recalcule les checksums. IDEMPOTENT.
Usage : ~/.marvel-venv/bin/python .planning/lady-deathstrike/inserer_lady_deathstrike.py [racine_du_depot]
"""
import importlib.util
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(ICI, "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
PYTHON = os.environ.get("PYTHON_DU_DEPOT", sys.executable)
PACK = "lady_deathstrike"
LIBELLE = "213. Custom (Lady Deathstrike)"

spec = importlib.util.spec_from_file_location("ld_cards", os.path.join(ICI, "ld_cards.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def avant_checksum(d: dict, cle: str, valeur) -> dict:
    """Ajoute `cle` juste avant `checksum` (le fichier garde `checksum` en dernier)."""
    out = {}
    for k, v in d.items():
        if k == "checksum":
            out[cle] = valeur
        out[k] = v
    if cle not in out:
        out[cle] = valeur
    return out


chemin_cartes = os.path.join(MOTEUR, "data", "cards.json")
cartes = json.load(open(chemin_cartes, encoding="utf-8"))
if PACK not in cartes:
    cartes = avant_checksum(cartes, PACK, [])
liste = cartes[PACK]
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
liste.sort(key=lambda c: c.get("card_id", ""))
with open(chemin_cartes, "w", encoding="utf-8") as f:
    json.dump(cartes, f, indent=1, ensure_ascii=False)

# ---- scenario, ensembles de rencontre ----
ENCOUNTERS = (["ld006"] * 2 + ["ld007", "ld008"] + ["ld009"] * 3 + ["ld010"] + ["ld011"] * 2 + ["ld012"] + ["ld013"] * 2 + ["ld014"] * 2)
MODULE = ["ld015", "ld016", "ld017", "ld017", "ld018"]


def ecrire(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, indent=2, ensure_ascii=False)
        f.write("\n")


def scenario(expert):
    return {
        "version": "0.5.8", "name": "Lady Deathstrike",
        "villain": ["ld002", "ld003"] if expert else ["ld001", "ld002"],
        "expert": expert,
        "schemes": ["ld004a,ld004b"],
        # 4 exemplaires de Bleeding Out (cartes 5 a 8) : un par joueur, le reste « mis de cote » par le Setup de ld004a.
        "set_aside": ["ld005"] * 4,
        "encounters": ENCOUNTERS,
        "encounter_sets": ["reavers", "standard", "expert"] if expert else ["reavers", "standard"],
        "modular_sets": ["military_grade"],
    }


ecrire(os.path.join(MOTEUR, "data", "scenarios", "lady_deathstrike.json"), scenario(False))
ecrire(os.path.join(MOTEUR, "data", "scenarios", "lady_deathstrike_expert.json"), scenario(True))
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "lady_deathstrike.json"),
       {"version": "0.5.8", "name": "Lady Deathstrike", "encounters": ENCOUNTERS})
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "reaver_resources.json"),
       {"version": "0.5.8", "name": "Reaver Resources", "encounters": MODULE})

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
if LIBELLE not in sets:
    sets = avant_checksum(sets, LIBELLE, {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": ""})
entree = sets[LIBELLE]
if "lady_deathstrike" not in entree["scenarios"]:
    entree["scenarios"].append("lady_deathstrike")
for e in ("lady_deathstrike", "reaver_resources"):
    if e not in entree["encounters"]:
        entree["encounters"].append(e)
ids = sorted(c["card_id"] for c in cartes[PACK])
entree["max_id"] = max(ids, key=lambda i: (len(i), i)) if ids else ""
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"Lady Deathstrike : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
