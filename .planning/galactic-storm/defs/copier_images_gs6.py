"""Copie les scans du scenario Hala Ultimatum (gs138-gs155) et du modulaire Accuser Corps (gs156-gs160)
vers CETTE copie (worktree isole, 20/10/2026). Recette : copier_images_gs4.py. Paysage (manigances
principales et annexes) : rotation 90 degres anti-horaire. Une seule image par card_id (copies : la
premiere, scans identiques verifies sur la transcription). Source : sources/, argument 1 si ailleurs."""
import os
import shutil
import sys
from PIL import Image

SOURCES = sys.argv[1] if len(sys.argv) > 1 else (
    "/home/oem/Desktop/Marvel LCG/.claude/worktrees/agent-a1a3ae99d214abd96/docs/packs/galactic-storm/sources")
HU = "Scenario Packs/Hala Ultimatum (Galactic Storm expansion content)"
AC = "Modular Sets/Accuser Corps (Galactic Storm expansion content)"
MAPPING = {
    f"z3/{HU}/Setup cards/01 Kree Ruler I.png": "gs138a",
    f"z3/{HU}/Setup cards/01 tanalth I.png": "gs138b",
    f"z3/{HU}/Setup cards/02 Kree Ruler II.png": "gs139a",
    f"z4/{HU}/Setup cards/02 tanalth II.png": "gs139b",
    f"z3/{HU}/Setup cards/03 Kree Ruler III.png": "gs140a",
    f"z4/{HU}/Setup cards/03 tanalth III.png": "gs140b",
    f"z3/{HU}/Setup cards/04 Hidden on hala IA.png": "gs141a",
    f"z4/{HU}/Setup cards/04 Hidden on hala IB.png": "gs141b",
    f"z4/{HU}/Setup cards/05 reckoning begins IIA.png": "gs142a",
    f"z3/{HU}/Setup cards/05 reckoning begins IIB.png": "gs142b",
    f"z3/{HU}/Setup cards/06 Hala.png": "gs143",
    f"z1/{HU}/Encounter cards/07 grand-high pursuer.png": "gs144",
    f"z2/{HU}/Encounter cards/08 kree plasma rifle.png": "gs145",
    f"z3/{HU}/Encounter cards/09 kree resilience.png": "gs146",
    f"z2/{HU}/Encounter cards/11 kree assassin.png": "gs147",
    f"z2/{HU}/Encounter cards/13 kree pursuer.png": "gs148",
    f"z1/{HU}/Encounter cards/15 kree soldier.png": "gs149",
    f"z2/{HU}/Encounter cards/19 House of Fiero.png": "gs150",
    f"z1/{HU}/Encounter cards/21 War Academies of Hala.png": "gs151",
    f"z3/{HU}/Encounter cards/22 detention facility of hala.png": "gs152",
    f"z1/{HU}/Encounter cards/23 advanced arsenal.png": "gs153",
    f"z1/{HU}/Encounter cards/26 battle cry.png": "gs154",
    f"z1/{HU}/Encounter cards/28 bloodthirst of hala.png": "gs155",
    f"z3/{AC}/01 the accused.png": "gs156",
    f"z1/{AC}/02 universal weapon.png": "gs157",
    f"z1/{AC}/03 unwavering.png": "gs158",
    f"z1/{AC}/05 kree accuser.png": "gs159",
    f"z3/{AC}/07 judgement day.png": "gs160",
}
# Manigances principales et annexes : carte pivotee de 90 degres sur le scan (lue en tournant l'image).
PAYSAGE = {"gs141a", "gs141b", "gs142a", "gs142b", "gs150", "gs151", "gs152"}
RACINE_WORKTREE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
ORIG = f"{RACINE_WORKTREE}/sauvegardes-serveur/scans-originaux"
PICS = f"{RACINE_WORKTREE}/Fusion/marvel-lcg-src/assets/pics"

if __name__ == "__main__":
    os.makedirs(ORIG, exist_ok=True)
    os.makedirs(PICS, exist_ok=True)
    manquantes = []
    for fichier, cid in MAPPING.items():
        src = os.path.join(SOURCES, fichier)
        if not os.path.exists(src):
            manquantes.append(src)
            continue
        shutil.copy(src, f"{ORIG}/{cid}.png")
        im = Image.open(src).convert("RGB")
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    if manquantes:
        print(len(manquantes), "sources introuvables :")
        for m in manquantes:
            print(" ", m)
    print(len(MAPPING) - len(manquantes), "images copiees sur", len(MAPPING))
