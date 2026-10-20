"""Copie les scans du scenario Earth Under Siege (gs161-gs194, gsr01-gsr10) vers le depot PRINCIPAL
(21/10/2026). Recette : copier_images_gs4.py. Paysage (manigance principale, manigances annexes de
scenario et d'ensemble) : rotation 90 degres anti-horaire. Une seule image par card_id (copies/doublons
scannes plusieurs fois : la premiere trouvee, textes identiques verifies sur les deux transcriptions
earth-under-siege.md / earth-under-siege-ensembles.md). Source : docs/packs/galactic-storm/sources/
(dossier ignore par git), argument 1 si ailleurs."""
import os
import shutil
import sys
from PIL import Image

SOURCES = sys.argv[1] if len(sys.argv) > 1 else (
    "/home/oem/Desktop/Marvel LCG/.claude/worktrees/agent-a1a3ae99d214abd96/docs/packs/galactic-storm/sources")
EUS = "Scenario Packs/Earth Under Siege (Galactic Storm expansion content)"
MAPPING = {
    f"z3/{EUS}/Setup Cards/00 Earthfall 1A.png": "gs161a",
    f"z3/{EUS}/Setup Cards/00 Earthfall 1B ALT.png": "gs161b",
    f"z3/{EUS}/Setup Cards/00 enemies at surge standard ALT.png": "gs162a",
    f"z3/{EUS}/Setup Cards/00 enemies at surge expert ALT.png": "gs162b",
    f"z2/{EUS}/Encounter Cards/03 main concern.png": "gs163",
    f"z2/{EUS}/Encounter Cards/04 observe the perimeter.png": "gs164",
    f"z3/{EUS}/Encounter Cards/05 threat on the horizon.png": "gs165",
    f"z2/{EUS}/Setup Cards/01 annihilus.png": "gs166",
    f"z2/{EUS}/Setup Cards/02 annihilus II.png": "gs167",
    f"z1/{EUS}/Annihilus encounter cards/03 portal to the negative zone.png": "gs168",
    f"z1/{EUS}/Annihilus encounter cards/06 annihilation wave.png": "gs169",
    f"z3/{EUS}/Setup Cards/01 attuma.png": "gs170",
    f"z2/{EUS}/Setup Cards/02 attuma II.png": "gs171",
    f"z3/{EUS}/Attuma encounter cards/03 Atlantean Amulet.png": "gs172",
    f"z3/{EUS}/Attuma encounter cards/04 Atlantean Battle Gear.png": "gs173",
    f"z1/{EUS}/Attuma encounter cards/05 andromeda.png": "gs174",
    f"z3/{EUS}/Attuma encounter cards/06 rising sea levels.png": "gs175",
    f"z3/{EUS}/Setup Cards/01 destroyer.png": "gs176",
    f"z1/{EUS}/Setup Cards/02 destroyer II.png": "gs177",
    f"z3/{EUS}/Destroyer encounter cards/03 uru armor plating.png": "gs178",
    f"z1/{EUS}/Destroyer encounter cards/04 programmed to obliterate.png": "gs179",
    f"z2/{EUS}/Destroyer encounter cards/05 pure destruction.png": "gs180",
    f"z2/{EUS}/Setup Cards/01 doctor minerva.png": "gs181",
    f"z2/{EUS}/Setup Cards/02 doctor minerva II.png": "gs182",
    f"z1/{EUS}/Doctor Minerva encounter cards/03 induced mutation.png": "gs183",
    f"z3/{EUS}/Doctor Minerva encounter cards/05 captain atlas.png": "gs184",
    f"z1/{EUS}/Doctor Minerva encounter cards/05 kree secret laboratory.png": "gs185",
    f"z3/{EUS}/Setup Cards/01 mole man.png": "gs186",
    f"z2/{EUS}/Setup Cards/02 mole man II.png": "gs187",
    f"z1/{EUS}/Mole Man encounter cards/04 moloid.png": "gs188",
    f"z3/{EUS}/Mole Man encounter cards/06 underground tremor.png": "gs189",
    f"z1/{EUS}/Setup Cards/01 veranke.png": "gs190",
    f"z3/{EUS}/Setup Cards/02 veranke II.png": "gs191",
    f"z1/{EUS}/Veranke encounter cards/03 arch enemy_s face.png": "gs192",
    f"z2/{EUS}/Veranke encounter cards/04 replaced.png": "gs193",
    f"z3/{EUS}/Veranke encounter cards/06 Secret Invasion.png": "gs194",
    f"z1/{EUS}/Standard-Expert reskins/03 assault.png": "gsr01",
    f"z1/{EUS}/Standard-Expert reskins/04 assault.png": "gsr02",
    f"z1/{EUS}/Standard-Expert reskins/07 shadows of the past.png": "gsr03",
    f"z1/{EUS}/Standard-Expert reskins/08 exhaustion.png": "gsr04",
    f"z3/{EUS}/Standard-Expert reskins/01 advance.png": "gsr05",
    f"z2/{EUS}/Standard-Expert reskins/05 Caught Off Guard.png": "gsr06",
    f"z2/{EUS}/Standard-Expert reskins/09 masterplan.png": "gsr07",
    f"z2/{EUS}/Standard-Expert reskins/02 advance.png": "gsr08",
    f"z3/{EUS}/Standard-Expert reskins/06 Gang-up.png": "gsr09",
    f"z3/{EUS}/Standard-Expert reskins/10 under fire.png": "gsr10",
}
# Manigance principale, manigances annexes de scenario et d'ensemble : carte pivotee de 90 degres sur
# le scan (transcriptions : "Carte dessinee en paysage (pivotee de 90 degres)").
PAYSAGE = {"gs161a", "gs161b", "gs162a", "gs162b", "gs168", "gs175", "gs179", "gs185", "gs194"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"

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
