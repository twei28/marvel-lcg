"""Insere (ou REMPLACE) les cartes du SCENARIO Alien vs. Predator (RyCoRan) dans data/cards.json (cle `alien_vs_predator`), ecrit
data/scenarios/alien_vs_predator(.json|_expert.json) et les ensembles alien_vs_predator, standard_apex, clan_yautja, declare le tout dans
data/sets_info.json (`216. Custom (Alien vs. Predator)`) puis recalcule les checksums. IDEMPOTENT.
Usage : ~/.marvel-venv/bin/python .planning/alien-vs-predator/inserer_avp.py [racine_du_depot]
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
PACK = "alien_vs_predator"
LIBELLE = "216. Custom (Alien vs. Predator)"

spec = importlib.util.spec_from_file_location("ap_cards", os.path.join(ICI, "ap_cards.py"))
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
SCOUTS = ["ap101"] * 4 + ["ap102"] * 4 + ["ap103"] * 4 + ["ap104"] * 4
ENCOUNTERS = (["ap011", "ap012"] + ["ap013"] * 2 + ["ap015"] + ["ap016"] * 2 + ["ap018"] * 2 + ["ap020", "ap021", "ap022", "ap023", "ap024", "ap025",
              "ap026", "ap027", "ap028", "ap029", "ap030", "ap031", "ap032", "ap033"])
APEX = ["ap201", "ap202", "ap203", "ap204", "ap205", "ap206", "ap207"]
CLAN = ["ap301", "ap302", "ap303", "ap304", "ap305", "ap306"]


def ecrire(chemin, contenu):
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(contenu, f, indent=2, ensure_ascii=False)
        f.write("\n")


def scenario(expert):
    return {
        "version": "0.5.8", "name": "Alien vs. Predator",
        # Deux mechants : aucun mis en jeu par le moteur, le Setup de ap005a les met en jeu (modele bebop_rocksteady / tk005a).
        "villain": [],
        "expert": expert,
        "schemes": ["ap005a,ap005b", "ap006a,ap006b", "ap007a,ap007b", "ap008a,ap008b"],
        "set_aside": (["ap003a,ap003b", "ap004a,ap004b"] if expert else ["ap001a,ap001b", "ap002a,ap002b"]) + ["ap009", "ap010"] + SCOUTS,
        "encounters": ENCOUNTERS,
        # Apex Standard REMPLACE le Standard (insert) ; prefixe « standard » pour que le moteur le melange comme un standard.
        "encounter_sets": ["standard_apex"],
        "modular_sets": ["clan_yautja"],
    }


ecrire(os.path.join(MOTEUR, "data", "scenarios", "alien_vs_predator.json"), scenario(False))
ecrire(os.path.join(MOTEUR, "data", "scenarios", "alien_vs_predator_expert.json"), scenario(True))
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "alien_vs_predator.json"),
       {"version": "0.5.8", "name": "Alien vs. Predator", "encounters": ENCOUNTERS})
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "standard_apex.json"),
       {"version": "0.5.8", "name": "Apex Standard", "encounters": APEX})
ecrire(os.path.join(MOTEUR, "data", "encounter_sets", "clan_yautja.json"),
       {"version": "0.5.8", "name": "Clan Yautja", "encounters": CLAN})

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
if LIBELLE not in sets:
    sets = avant_checksum(sets, LIBELLE, {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": ""})
entree = sets[LIBELLE]
if "alien_vs_predator" not in entree["scenarios"]:
    entree["scenarios"].append("alien_vs_predator")
for e in ("alien_vs_predator", "standard_apex", "clan_yautja"):
    if e not in entree["encounters"]:
        entree["encounters"].append(e)
ids = sorted(c["card_id"] for c in cartes[PACK])
entree["max_id"] = max(ids, key=lambda i: (len(i), i)) if ids else ""
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"Alien vs Predator : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
