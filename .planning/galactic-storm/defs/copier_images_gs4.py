"""Copie les scans du scenario Kree Sentry (gs076-gs090) et du modulaire Imperial Guard (gs091-gs113) vers le depot
PRINCIPAL (20/10/2026). Recette : copier_images_majestrix.py. Paysage (manigances principales et annexes) : rotation 90
degres anti-horaire. Une seule image par card_id (copies : la premiere, scans identiques verifies a l'oeil).
Source : docs/packs/galactic-storm/sources/ (dossier ignore par git), argument 1 si ailleurs."""
import os
import shutil
import sys
from PIL import Image

SOURCES = sys.argv[1] if len(sys.argv) > 1 else "/home/oem/Desktop/Marvel LCG/docs/packs/galactic-storm/sources"
KS = "Scenario Packs/Kree Sentry (Galactic Storm expansion content)"
IG = "Modular Sets/Imperial Guard (Galactic Storm expansion content)"
MAPPING = {
    f"z1/{KS}/Setup cards/01 kree sentry I.png": "gs076",
    f"z2/{KS}/Setup cards/02 kree sentry II.png": "gs077",
    f"z3/{KS}/Setup cards/03 kree sentry III.png": "gs078",
    f"z2/{KS}/Setup cards/04 sentry awakens IA.png": "gs079a",
    f"z1/{KS}/Setup cards/04 sentry awakens IB.png": "gs079b",
    f"z2/{KS}/Setup cards/05 Self-Destruct Protocol IIA.png": "gs080a",
    f"z2/{KS}/Setup cards/05 Self-Destruct Protocol IIB.png": "gs080b",
    f"z2/{KS}/Setup cards/06 rick jones.png": "gs081",
    f"z1/{KS}/Setup cards/08 sentry_s grasp.png": "gs082",
    f"z1/{KS}/Encounter cards/09 optic blast cannon.png": "gs083",
    f"z1/{KS}/Encounter cards/11 repulsor blast unit.png": "gs084",
    f"z1/{KS}/Encounter cards/12 Grip of Annihilation.png": "gs085",
    f"z1/{KS}/Encounter cards/13 Locking on Target.png": "gs086",
    f"z1/{KS}/Encounter cards/15 lair collapse protocol.png": "gs087",
    f"z2/{KS}/Encounter cards/17 Gotcha.png": "gs088",
    f"z2/{KS}/Encounter cards/18 caught in their sights.png": "gs089",
    f"z1/{KS}/Encounter cards/20 intruder elimination.png": "gs090",
    f"z3/{IG}/01 disciplined training.png": "gs091",
    f"z3/{IG}/02 Loyal Devotion.png": "gs092",
    f"z2/{IG}/03 noble bearing.png": "gs093",
    f"z2/{IG}/04 Astra.png": "gs094",
    f"z2/{IG}/05 earthquake.png": "gs095",
    f"z1/{IG}/06 electron.png": "gs096",
    f"z1/{IG}/07 Fang.png": "gs097",
    f"z3/{IG}/08 gladiator.png": "gs098",
    f"z2/{IG}/09 hobgoblin.png": "gs099",
    f"z2/{IG}/10 Hussar.png": "gs100",
    f"z3/{IG}/11 magique.png": "gs101",
    f"z2/{IG}/12 manta.png": "gs102",
    f"z1/{IG}/13 Mentor.png": "gs103",
    f"z3/{IG}/14 neutron.png": "gs104",
    f"z1/{IG}/15 Nightside.png": "gs105",
    f"z2/{IG}/16 oracle.png": "gs106",
    f"z2/{IG}/17 pulsar.png": "gs107",
    f"z3/{IG}/18 smasher.png": "gs108",
    f"z1/{IG}/19 starbolt.png": "gs109",
    f"z3/{IG}/20 titan.png": "gs110",
    f"z1/{IG}/21 warstar.png": "gs111",
    f"z1/{IG}/22 Guard Assembles.png": "gs112",
    f"z3/{IG}/23 imperial formation.png": "gs113",
}
PAYSAGE = {"gs079a", "gs079b", "gs080a", "gs080b", "gs085", "gs086", "gs087"}
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
