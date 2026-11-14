#!/usr/bin/env python3
"""Images du heros SILVER SURFER (DesignHacker, MC4 SEALED) : 16 card_id.

Usage : python3 importer_images_silver_surfer.py <dossier « SILVER SURFER (MC4 SEALED) »> [racine_du_depot]

Ecrit `assets/pics/<card_id>.jpg` (petit cote ramene a 615 px, LANCZOS ; la manigance annexe, imprimee
couchee dans un fichier portrait, est tournee de 90 degres anti-horaire) et garde l'original dans
`sauvegardes-serveur/scans-originaux/<card_id>.jpg`. Les images ne sont pas versionnees.
"""
import os
import sys
from PIL import Image

SRC = sys.argv[1]
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
CARTES = {
    "sv001a": "Hero - Silver Surfer.jpg",
    "sv001b": "Alter-Ego - Norrin Radd.jpg",
    "sv002": "HERO DECK/ALLY - DAWN GREENWOOD.jpg",
    "sv003": "HERO DECK/UPGRADE - THE SILVER SURFBOARD.jpg",
    "sv004": "HERO DECK/UPGRADE - ENERGY MANIPULATION.jpg",
    "sv005": "HERO DECK/UPGRADE - RAGE OF RETRIBUTION.jpg",
    "sv006": "HERO DECK/EVENT - COSMIC SPEED 1.jpg",
    "sv007": "HERO DECK/EVENT - COSMIC STRENGTH 1.jpg",
    "sv008": "HERO DECK/EVENT - ABSORB + DISCHARGE 1.jpg",   # fichier mal nomme : la carte est Cosmic Energy
    "sv009": "HERO DECK/EVENT - SILVER UP 1.jpg",
    "sv010": "HERO DECK/RESOURCE - THE POWER COSMIC 1.jpg",
    "sv011": "ENCOUNTER DECK/SS ENCOUNTER - OBLIGATION.jpg",
    "sv012": "ENCOUNTER DECK/SS ENCOUNTER - NEMESIS MINION.jpg",
    "sv013": "ENCOUNTER DECK/SS ENCOUNTER - MINION.jpg",
    "sv014": "ENCOUNTER DECK/SS ENCOUNTER - SIDE SCHEME.jpg",
    "sv015": "ENCOUNTER DECK/SS ENCOUNTER - ATTACHMENT 1.jpg",
}
PAYSAGE = {"sv014"}
os.makedirs(os.path.join(MOTEUR, "assets", "pics"), exist_ok=True)
os.makedirs(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux"), exist_ok=True)
for cid, rel in CARTES.items():
    im = Image.open(os.path.join(SRC, rel)).convert("RGB")
    im.save(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux", cid + ".jpg"), quality=95)
    if cid in PAYSAGE:
        im = im.rotate(90, expand=True)
    w, h = im.size
    k = 615 / min(w, h)
    im = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
    im.save(os.path.join(MOTEUR, "assets", "pics", cid + ".jpg"), quality=92)
    print(cid, im.size)
