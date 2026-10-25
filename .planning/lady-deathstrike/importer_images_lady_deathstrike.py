#!/usr/bin/env python3
"""Images du scenario LADY DEATHSTRIKE (Mysteltainn) : 19 card_id.

Usage : python3 importer_images_lady_deathstrike.py <dossier « LadyDeathstrike » extrait> [racine_du_depot]

Ecrit `assets/pics/<card_id>.jpg` (petit cote ramene a 615 px, LANCZOS ; les manigances annexes et la face A du complot
principal, imprimees en PAYSAGE dans un PNG deja couche, restent telles quelles) et garde l'original dans
`sauvegardes-serveur/scans-originaux/<card_id>.jpg`. Les images ne sont pas versionnees.
"""
import os
import sys
from PIL import Image

SRC = sys.argv[1]
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
E = "EncounterCards/"
M = "CustomModular_ReaverResources/"
CARTES = {
    "ld001": "1_LadyDeathstrike.v2.png",
    "ld002": "2_LadyDeathstrike2.v2.png",
    "ld003": "3_LadyDeathstrike3.v2.png",
    "ld004a": "4A_MutantHuntingSeason.v3.png",
    "ld004b": "4B_MutantHuntingSeason.v3.png",
    "ld005": "5_BleedingOut.png",
    "ld006": E + "9_AdamantiumNanoskeleton.v3.png",
    "ld007": E + "11_ReaverCommander.v3.png",
    "ld008": E + "12_ReinforcedAdamantiumClaws.v4.png",
    "ld009": E + "13_ReaverTracker.v2.png",
    "ld010": E + "16_DeepWound.v3.png",
    "ld011": E + "17_BideTime.v2.png",
    "ld012": E + "19_StalkingPrey.v2.png",
    "ld013": E + "20_LashOut.v4.png",
    "ld014": E + "22_MutantHunter.v2.png",
    "ld015": M + "1_IntegratedAugmentations.png",
    "ld016": M + "2_TitaniumExoskeleton.png",
    "ld017": M + "3_InhibitorCollar.png",
    "ld018": M + "5_ChopShopCybernetics.png",
}
os.makedirs(os.path.join(MOTEUR, "assets", "pics"), exist_ok=True)
os.makedirs(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux"), exist_ok=True)
for cid, rel in CARTES.items():
    im = Image.open(os.path.join(SRC, rel)).convert("RGB")
    im.save(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux", cid + ".jpg"), quality=95)
    w, h = im.size
    k = 615 / min(w, h)
    im = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
    im.save(os.path.join(MOTEUR, "assets", "pics", cid + ".jpg"), quality=92)
    print(cid, im.size)
