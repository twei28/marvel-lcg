"""Copie les scans du scenario Secret Invasion vers le depot PRINCIPAL (15/10/2026).
Recette : copier_images_exemple.py. Paysage (complots, complots annexes) : rotation 90 degres anti-horaire.
Une seule image par card_id (copies : on prend la premiere). Paquet Impostor : allie = a, sbire = b."""
import os
import shutil
from PIL import Image

RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
SI = "Scenario Packs/Secret Invasion (Skrull Menace Expansion Content)"
SU = f"{SI}/setup cards"
EN = f"{SI}/encounter cards"
IM = f"{SI}/impostor deck cards"
MAPPING = {
    f"{SU}/000 Spider-Woman I.png": "sk189a",
    f"{SU}/01 queen veranke I.png": "sk189b",
    f"{SU}/00 Spider-Woman II.png": "sk190a",
    f"{SU}/02 queen veranke II.png": "sk190b",
    f"{SU}/0 Spider-Woman III.png": "sk191a",
    f"{SU}/03 queen veranke III.png": "sk191b",
    f"{SU}/04 The Infiltration Has Begun IA.png": "sk192a",
    f"{SU}/04 The Infiltration Has Begun IB.png": "sk192b",
    f"{SU}/05 the skrull invasion IIA.png": "sk193a",
    f"{SU}/05 the skrull invasion IIB.png": "sk193b",
    f"{SU}/06 who do you trust environment.png": "sk194",
    f"{EN}/07 impostor.png": "sk195",
    f"{EN}/08 super skrull enhancement 2.png": "sk196",
    f"{EN}/09 super skrull enhancement 3.png": "sk197",
    f"{EN}/10 super skrull enhancement 1.png": "sk198",
    f"{EN}/11 chaos on the battlefield.png": "sk199",
    f"{EN}/13 Fulfill the prophecy.png": "sk200",
    f"{EN}/14 mistrust and paranoia.png": "sk201",
    f"{EN}/15 arrival of impostors.png": "sk202",
    f"{EN}/16 camouflaged.png": "sk203",
    f"{EN}/19 glory to the Skrull Empire.png": "sk204",
    f"{EN}/21 infiltration ritual.png": "sk205",
    f"{EN}/23 invasion fleet.png": "sk206",
    f"{EN}/24 revelation.png": "sk207",
}
# Paquet Impostor : numero du set (27..46) -> (nom de fichier allie, nom de fichier sbire)
IMPOSTORS = {
    27: ("27 captain america impostor ally.png", "27 captain america impostor minion.png"),
    28: ("28 Mar-vell impostor ally.png", "28 Mar-vell impostor minion.png"),
    29: ("29 carol danvers impostor ally.png", "29 carol danvers impostor minion.png"),
    30: ("30 Carnage impostor ally.png", "30 Carnage impostor minion.png"),
    31: ("31 daredevil impostor ally.png", "31 daredevil impostor minion.png"),
    32: ("32 deathlok impostor ally.png", "32 deathlok impostor minion.png"),
    33: ("33 dugan impostor ally.png", "33 dugan impostor minion.png"),
    34: ("34 elektra impostor ally.png", "34 elektra impostor minion.png"),
    35: ("35 giant-man impostor ally.png", "35 giant-man impostor minion.png"),
    36: ("36 invisible woman impostor ally.png", "36 invisible woman impostor minion.png"),
    37: ("37 iron fist impostor ally.png", "37 iron fist impostor minion.png"),
    38: ("38 iron man impostor ally.png", "38 iron man impostor minion.png"),
    39: ("39 moon knight impostor ally.png", "39 moon knight impostor minion.png"),
    40: ("40 nick fury impostor ally.png", "40 Nick Fury impostor minion.png"),
    41: ("41 phoenix impostor ally.png", "41 phoenix impostor minion.png"),
    42: ("42 spider-man impostor ally.png", "42 spider-man impostor minion.png"),
    43: ("43 thor impostor ally.png", "43 thor impostor minion.png"),
    44: ("44 venom impostor ally.png", "44 Venom impostor minion.png"),
    45: ("45 wolverine impostor ally.png", "45 wolverine impostor minion.png"),
    46: ("46 yellowjacket impostor ally.png", "46 yellowjacket impostor minion.png"),
}
for n, (a, b) in IMPOSTORS.items():
    MAPPING[f"{IM}/{a}"] = f"sk{208 + n - 27}a"
    MAPPING[f"{IM}/{b}"] = f"sk{208 + n - 27}b"
PAYSAGE = {"sk192a", "sk192b", "sk193a", "sk193b", "sk199", "sk200", "sk201"}
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
