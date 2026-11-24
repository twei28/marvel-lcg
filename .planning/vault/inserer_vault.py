"""Insere (ou REMPLACE) les cartes du SCENARIO The Vault (Kajislav) dans data/cards.json (cle `the_vault`),
ecrit data/scenarios/the_vault(.json|_expert.json), data/encounter_sets/the_vault.json,
declare le tout dans data/sets_info.json (`215. Custom (The Vault)`) puis recalcule les checksums. IDEMPOTENT.
Usage : ~/.marvel-venv/bin/python .planning/vault/inserer_vault.py [racine_du_depot]
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
PACK = "the_vault"
LIBELLE = "215. Custom (The Vault)"

spec = importlib.util.spec_from_file_location("vt_cards", os.path.join(ICI, "vt_cards.py"))
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
ENCOUNTERS = (["vt020"] * 2 + ["vt022"] * 4 + ["vt026"] * 2 + ["vt028", "vt029"] + ["vt030"] * 4 + ["vt034"] * 3)
VILAINS_I = [f"vt{n:03d}" for n in (1, 3, 5, 7, 9, 11, 13, 15)]
VILAINS_II = [f"vt{n:03d}" for n in (2, 4, 6, 8, 10, 12, 14, 16)]


def ecrire(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, indent=2, ensure_ascii=False)
        f.write("\n")


def scenario(expert):
    return {
        "version": "0.5.8", "name": "The Vault",
        # Plusieurs vilains : aucun mis en jeu par le moteur, le Setup de vt017a cree le deck de vilains.
        "villain": [],
        "expert": expert,
        "schemes": ["vt017a,vt017b"],
        "set_aside": (VILAINS_II if expert else VILAINS_I) + ["vt018", "vt019"],
        "encounters": ENCOUNTERS,
        "encounter_sets": ["standard", "expert"] if expert else ["standard"],
        "modular_sets": ["sinister_syndicate"],
    }


ecrire(os.path.join(MOTEUR, "data", "scenarios", "the_vault.json"), scenario(False))
ecrire(os.path.join(MOTEUR, "data", "scenarios", "the_vault_expert.json"), scenario(True))
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "the_vault.json"),
       {"version": "0.5.8", "name": "The Vault", "encounters": ENCOUNTERS})

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
if LIBELLE not in sets:
    sets = avant_checksum(sets, LIBELLE, {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": ""})
entree = sets[LIBELLE]
if "the_vault" not in entree["scenarios"]:
    entree["scenarios"].append("the_vault")
for e in ("the_vault",):
    if e not in entree["encounters"]:
        entree["encounters"].append(e)
ids = sorted(c["card_id"] for c in cartes[PACK])
entree["max_id"] = max(ids, key=lambda i: (len(i), i)) if ids else ""
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"The Vault : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
