"""Copie les scans du scenario Paibok et du set New Revengers vers le depot PRINCIPAL (15/10/2026).
Recette : copier_images_exemple.py. Paysage (complots, complots annexes) : rotation 90 degres anti-horaire.
Une seule image par card_id (copies : on prend la premiere)."""
import os
import shutil
from PIL import Image

RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
PAIBOK = "Scenario Packs/Paibok (Skrull Menace Expansion Content)"
NEWREV = "Modular Sets/New Revengers (Skrull Menace Expansion Content)"
MAPPING = {
    f"{PAIBOK}/Setup cards/01 paibok I.png": "sk141",
    f"{PAIBOK}/Setup cards/02 paibok II.png": "sk142",
    f"{PAIBOK}/Setup cards/03 paibok III.png": "sk143",
    f"{PAIBOK}/Setup cards/04 power skrull engineering IA.png": "sk144a",
    f"{PAIBOK}/Setup cards/04 power skrull engineering IB.png": "sk144b",
    f"{PAIBOK}/Setup cards/05 mastering superpowers IIA.png": "sk145a",
    f"{PAIBOK}/Setup cards/05 mastering supoerpowers IIB.png": "sk145b",
    f"{PAIBOK}/Encounter cards/06 captain Paibok.png": "sk146",
    f"{PAIBOK}/Encounter cards/07 distracted.png": "sk147",
    f"{PAIBOK}/Encounter cards/09 electricity projection.png": "sk148",
    f"{PAIBOK}/Encounter cards/10 hypnotized.png": "sk149",
    f"{PAIBOK}/Encounter cards/12 ice control (1).png": "sk150",
    f"{PAIBOK}/Encounter cards/13 metalic transformation.png": "sk151",
    f"{PAIBOK}/Encounter cards/14 shapeshifting.png": "sk152",
    f"{PAIBOK}/Encounter cards/15 trapped in ice.png": "sk153",
    f"{PAIBOK}/Encounter cards/17 devos.png": "sk154",
    f"{PAIBOK}/Encounter cards/18 general Kalamari.png": "sk155",
    f"{PAIBOK}/Encounter cards/19 galactic Ambassador.png": "sk156",
    f"{PAIBOK}/Encounter cards/20 settling scores.png": "sk157",
    f"{PAIBOK}/Encounter cards/22 council manipulation.png": "sk158",
    f"{PAIBOK}/Encounter cards/23 getting ruthless.png": "sk159",
    f"{PAIBOK}/Encounter cards/25 power demonstration.png": "sk160",
    f"{NEWREV}/01 O.M.N.I.T.R.O.N.I.C.U.S..png": "sk161",
    f"{NEWREV}/02 angar.png": "sk162",
    f"{NEWREV}/03 asti.png": "sk163",
    f"{NEWREV}/04 skar.png": "sk164",
    f"{NEWREV}/05 maker.png": "sk165",
    f"{NEWREV}/06 vermin.png": "sk166",
    f"{NEWREV}/07 white tiger.png": "sk167",
    f"{NEWREV}/08 the revenge time.png": "sk168",
    f"{NEWREV}/09 forming the revengers.png": "sk169",
}
PAYSAGE = {"sk144a", "sk144b", "sk145a", "sk145b", "sk156", "sk157", "sk168"}
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
