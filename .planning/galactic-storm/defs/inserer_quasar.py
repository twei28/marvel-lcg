"""Insere (ou REMPLACE) les cartes du heros Quasar (Galactic Storm, Kajislav) dans data/cards.json
(cle `galactic_storm`), declare le heros dans data/sets_info.json (`144. Custom (Galactic Storm)`) puis
recalcule les checksums.

IDEMPOTENT : une carte deja presente est remplacee a sa place (meme card_id), une carte absente est
ajoutee en fin de liste ; la cle de pack et l'entree de sets_info sont creees si elles manquent (le lot
Binary, GS-1, les cree aussi : un second passage ne duplique rien). Source : `defs/quasar_cards.py`.
Usage (depuis n'importe ou) :  python3 .planning/galactic-storm/defs/inserer_quasar.py [racine_du_depot]
"""
import importlib.util
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
PYTHON = os.environ.get("PYTHON_DU_DEPOT", "/home/oem/Desktop/Marvel LCG/.venv-linux/bin/python3.10")
PACK = "galactic_storm"
LIBELLE = "144. Custom (Galactic Storm)"

spec = importlib.util.spec_from_file_location("quasar_cards", os.path.join(ICI, "quasar_cards.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def avec_cle_avant_checksum(d: dict, cle: str, valeur) -> dict:
    """Ajoute `cle` juste avant `checksum` (qui reste la DERNIERE cle du fichier)."""
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
    cartes = avec_cle_avant_checksum(cartes, PACK, [])
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
with open(chemin_cartes, "w", encoding="utf-8") as f:
    json.dump(cartes, f, indent=1, ensure_ascii=False)

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
if LIBELLE not in sets:
    neuf = {}
    for k, v in sets.items():
        neuf[k] = v
        if k == "143. Custom (Skrull Menace)":
            neuf[LIBELLE] = {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": "gs349"}
    if LIBELLE not in neuf:
        neuf = avec_cle_avant_checksum(neuf, LIBELLE,
                                       {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": "gs349"})
    sets = neuf
entree = sets[LIBELLE]
if "quasar" not in entree["heroes"]:
    entree["heroes"].append("quasar")
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"Quasar : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
