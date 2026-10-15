"""Copie les scans du scenario Skrull Pantheon et du set Dard'van Sect vers le depot PRINCIPAL (15/10/2026).
Recette : copier_images_exemple.py. Paysage (complots principaux, complots annexes) : rotation 90 degres anti-horaire.
Une seule image par card_id (copies : on prend la premiere). Les deux faces d'une carte double face ont chacune
leur image (sk170a = Kly'bn, sk170b = Sl'gur't ; sk175a = Stronghold, sk175b = Destroyed)."""
import os
import shutil
from PIL import Image

RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
PANTHEON = "Scenario Packs/Skrull Pantheon (Skrull Menace Expansion Content)"
DARDVAN = "Modular Sets/Dard_van Sect (Skrull Menace Expansion Content)"
MAPPING = {
    f"{PANTHEON}/Setup cards/01 kly_bn I.png": "sk170a",
    f"{PANTHEON}/Setup cards/01 sl_gur_t I.png": "sk170b",
    f"{PANTHEON}/Setup cards/02 kly_bn II.png": "sk171a",
    f"{PANTHEON}/Setup cards/02 sl_gur_t II.png": "sk171b",
    f"{PANTHEON}/Setup cards/03 kly_bn III.png": "sk172a",
    f"{PANTHEON}/Setup cards/03 sl_gur_t III.png": "sk172b",
    f"{PANTHEON}/Setup cards/04 protect the pantheon 1A.png": "sk173a",
    f"{PANTHEON}/Setup cards/04 protect the pantheon 1B.png": "sk173b",
    f"{PANTHEON}/Setup cards/05 Slaying the False Gods 2A.png": "sk174a",
    f"{PANTHEON}/Setup cards/05 Slaying the False Gods 2B.png": "sk174b",
    f"{PANTHEON}/Setup cards/06 skrull partheon.png": "sk175a",
    f"{PANTHEON}/Setup cards/06 skrull partheon damaged.png": "sk175b",
    f"{PANTHEON}/Encounter cards/07 blessed by Kly_bn.png": "sk176",
    f"{PANTHEON}/Encounter cards/09 blessed by Sl_gur_t.png": "sk177",
    f"{PANTHEON}/Encounter cards/11 nogor minion.png": "sk178",
    f"{PANTHEON}/Encounter cards/12 Shapeless Wastes.png": "sk179",
    f"{PANTHEON}/Encounter cards/13 streighten the faith.png": "sk180",
    f"{PANTHEON}/Encounter cards/15 prayer to kly_bn.png": "sk181",
    f"{PANTHEON}/Encounter cards/18 prayer to Sl_gur_t.png": "sk182",
    f"{PANTHEON}/Encounter cards/21 talisman of the skrulls.png": "sk183",
    f"{DARDVAN}/01 dardvan fanatic.png": "sk184",
    f"{DARDVAN}/03 dardvan priest.png": "sk185",
    f"{DARDVAN}/04 dard_van sect side scheme.png": "sk186",
    f"{DARDVAN}/05 collective prayers.png": "sk187",
    f"{DARDVAN}/06 sectarian practices.png": "sk188",
}
PAYSAGE = {"sk173a", "sk173b", "sk174a", "sk174b", "sk179", "sk180", "sk186"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"

if __name__ == "__main__":
    os.makedirs(ORIG, exist_ok=True)
    for fichier, cid in MAPPING.items():
        src = os.path.join(RACINE, fichier)
        shutil.copy(src, f"{ORIG}/{cid}.png")
        im = Image.open(src).convert("RGB")
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    print(len(MAPPING), "images copiees")
