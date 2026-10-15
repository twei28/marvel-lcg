"""Super-Skrull + Kree-Skrull War (15/10/2026) : copie les scans de l'archive vers le depot PRINCIPAL
(recette de copier_images_exemple.py). Une seule image par card_id (copies : on prend la premiere).
Paysage (complots) : rotation 90 degres anti-horaire avant de ramener le petit cote a 615 px."""
import os, shutil
from PIL import Image
RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
SS = "Scenario Packs/Super-Skrull (Skrull Menace Expansion Content)"
KW = "Modular Sets/Kree-Skrull War (Skrull Menace Expansion Content)"
MAPPING = {
    f"{SS}/Setup Cards/01 super-skrull I.png": "sk117",
    f"{SS}/Setup Cards/02 super-skrull II.png": "sk118",
    f"{SS}/Setup Cards/03 super-skrull III.png": "sk119",
    f"{SS}/Setup Cards/04 Searching for the Heir IA.png": "sk120a",
    f"{SS}/Setup Cards/04 Seraching for the Heir IB.png": "sk120b",
    f"{SS}/Setup Cards/05 Heir to the Throne IIA.png": "sk121a",
    f"{SS}/Setup Cards/05 Heir to the Throne IIB.png": "sk121b",
    f"{SS}/Superpower Deck/06 flexibility.png": "sk122",
    f"{SS}/Superpower Deck/07 invisibility.png": "sk123",
    f"{SS}/Superpower Deck/08 pyrokinesis.png": "sk124",
    f"{SS}/Superpower Deck/09 rock mimicry.png": "sk125",
    f"{SS}/Encounter Cards/10 invisible forcefield.png": "sk126",
    f"{SS}/Encounter Cards/13 lord kl_rt.png": "sk127",
    f"{SS}/Encounter Cards/14 mt_nox.png": "sk128",
    f"{SS}/Encounter Cards/15 praxagora.png": "sk129",
    f"{SS}/Encounter Cards/16 R_kin.png": "sk130",
    f"{SS}/Encounter Cards/17 galactic council.png": "sk131",
    f"{SS}/Encounter Cards/18 skrull warlords.png": "sk132",
    f"{SS}/Encounter Cards/19 hypnotic gaze.png": "sk133",
    f"{SS}/Encounter Cards/22 power multiplying.png": "sk134",
    f"{SS}/Encounter Cards/26 villain_s versatility.png": "sk135",
    f"{KW}/01 bel-dann.png": "sk136",
    f"{KW}/02 raksor.png": "sk137",
    f"{KW}/03 earth involvement.png": "sk138",
    f"{KW}/04 kree fleet.png": "sk139",
    f"{KW}/05 skrull fleet.png": "sk140",
}
PAYSAGE = {"sk120a", "sk120b", "sk121a", "sk121b", "sk131", "sk132", "sk138"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"
os.makedirs(ORIG, exist_ok=True)
os.makedirs(PICS, exist_ok=True)
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
