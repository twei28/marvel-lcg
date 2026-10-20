"""Copie les scans du scenario Majestrix's Verdict (gs114-gs137) vers le depot PRINCIPAL (20/10/2026).
Recette : .planning/skrull-menace/defs/copier_images_exemple.py. Paysage (manigances) : rotation 90 degres
anti-horaire. Une seule image par card_id (copies : la premiere, scans identiques verifies a l'oeil).
Source : docs/packs/galactic-storm/sources/ (dossier ignore par git), argument 1 si ailleurs."""
import os
import shutil
import sys
from PIL import Image

SOURCES = sys.argv[1] if len(sys.argv) > 1 else "/home/oem/Desktop/Marvel LCG/docs/packs/galactic-storm/sources"
MV = "Scenario Packs/Majestrix_s Verdict (Galactic Storm expansion content)"
MAPPING = {
    f"z3/{MV}/Setup cards/01 Deathbird I.png": "gs114",
    f"z4/{MV}/Setup cards/02 Deathbird II.png": "gs115",
    f"z4/{MV}/Setup cards/03 Deathbird III.png": "gs116",
    f"z3/{MV}/Setup cards/04 Earn the People’s Favor IA.png": "gs117a",
    f"z4/{MV}/Setup cards/04 Earn the People’s Favor IB.png": "gs117b",
    f"z3/{MV}/Setup cards/05 Majestrix_s Verdict IIA.png": "gs118a",
    f"z4/{MV}/Setup cards/05 Majestrix_s Verdict IIB.png": "gs118b",
    f"z3/{MV}/Setup cards/06 Imprisoned on Chandilar.png": "gs119",
    f"z3/{MV}/Setup cards/07 Shi_ar Throne side scheme.png": "gs120a",
    f"z4/{MV}/Setup cards/07 Shi_ar Throne support.png": "gs120b",
    f"z3/{MV}/Starjammers/08 lilandra ally.png": "gs121",
    f"z1/{MV}/Starjammers/09 Ch_od.png": "gs122",
    f"z2/{MV}/Starjammers/10 corsair.png": "gs123",
    f"z3/{MV}/Starjammers/11 hepzibah.png": "gs124",
    f"z1/{MV}/Starjammers/12 korvus.png": "gs125",
    f"z3/{MV}/Starjammers/13 raza.png": "gs126",
    f"z3/{MV}/Encounter cards/14 Royal Cape of the Shi_ar.png": "gs127",
    f"z2/{MV}/Encounter cards/15 Shi_ar crest.png": "gs128",
    f"z1/{MV}/Encounter cards/16 Shi_ar Javelin.png": "gs129",
    f"z1/{MV}/Encounter cards/18 araki.png": "gs130",
    f"z3/{MV}/Encounter cards/19 Jailor of Chandilar.png": "gs131",
    f"z2/{MV}/Encounter cards/23 Private Audience.png": "gs132",
    f"z1/{MV}/Encounter cards/24 Tapping the M_kraan Force.png": "gs133",
    f"z1/{MV}/Encounter cards/25 Tortured Prisoners.png": "gs134",
    f"z2/{MV}/Encounter cards/26 Birthright to the Throne.png": "gs135",
    f"z1/{MV}/Encounter cards/28 Exemplar Punishment.png": "gs136",
    f"z1/{MV}/Encounter cards/31 Sister_s Deception.png": "gs137",
}
PAYSAGE = {"gs117a", "gs117b", "gs118a", "gs118b", "gs119", "gs120a", "gs132", "gs133", "gs134"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"

if __name__ == "__main__":
    os.makedirs(ORIG, exist_ok=True)
    for fichier, cid in MAPPING.items():
        src = os.path.join(SOURCES, fichier)
        shutil.copy(src, f"{ORIG}/{cid}.png")
        im = Image.open(src).convert("RGB")
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    print(len(MAPPING), "images copiees")
