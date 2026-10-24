"""Insere (ou REMPLACE) les cartes du heros Shang-Chi (DesignHacker) dans data/cards.json (cle `shang_chi`),
declare le heros dans data/sets_info.json (`212. Custom (Shang-Chi)`) puis recalcule les checksums. IDEMPOTENT.
Usage : ~/.marvel-venv/bin/python .planning/shang-chi/inserer_shang_chi.py [racine_du_depot]
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
PACK = "shang_chi"
LIBELLE = "212. Custom (Shang-Chi)"

spec = importlib.util.spec_from_file_location("shc_cards", os.path.join(ICI, "shc_cards.py"))
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

chemin_sets = os.path.join(MOTEUR, "data", "sets_info.json")
sets = json.load(open(chemin_sets, encoding="utf-8"))
if LIBELLE not in sets:
    sets = avant_checksum(sets, LIBELLE, {"name": PACK, "scenarios": [], "heroes": [], "encounters": [], "max_id": ""})
entree = sets[LIBELLE]
if "shang_chi" not in entree["heroes"]:
    entree["heroes"].append("shang_chi")
ids = sorted(c["card_id"] for c in cartes[PACK])
entree["max_id"] = max(ids, key=lambda i: (len(i), i)) if ids else ""
with open(chemin_sets, "w", encoding="utf-8") as f:
    json.dump(sets, f, indent=1, ensure_ascii=False)

env = dict(os.environ, PYTHONPATH=os.path.join(MOTEUR, "src"))
subprocess.run([PYTHON, "tools/recalculer_checksums.py", os.path.join(MOTEUR, ".game-src"),
                "data/cards.json", "data/sets_info.json"], cwd=MOTEUR, env=env, check=True)
print(f"Shang-Chi : {ajoutees} carte(s) ajoutee(s), {remplacees} remplacee(s)")
