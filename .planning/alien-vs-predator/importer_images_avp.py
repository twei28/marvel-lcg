#!/usr/bin/env python3
"""Images du scenario ALIEN VS. PREDATOR (RyCoRan) : 55 card_id.

Usage : python3 importer_images_avp.py <dossier « Alien vs Predator (06-26) » extrait> [racine_du_depot]

Ecrit `assets/pics/<card_id>.jpg` (petit cote ramene a 615 px, LANCZOS ; complots et manigances deja en PAYSAGE dans le zip). L'original reste dans
`sauvegardes-serveur/scans-originaux/`. Les images ne sont pas versionnees.
"""
import os
import sys
from PIL import Image

SRC = sys.argv[1]
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
A, C, X = "Apex Standard/", "Clan Yautja/", "Scout set (expert)/"
CARTES = {
    "ap001a": "01 Alien Queen Villain.png", "ap001b": "01B Alien Queen Villain - defeat.png",
    "ap002a": "02 Predator Villain.png", "ap002b": "02B Predator Villain - defeat.png",
    "ap003a": "03 Alien Queen Villain (B).png", "ap003b": "03 Alien Queen Villain - defeat.png",
    "ap004a": "04 Predator Villain (B).png", "ap004b": "04B Predator Villain - defeat.png",
    "ap005a": "05 Main Scheme 1A.png", "ap005b": "05B Main Scheme 1B.png", "ap006a": "06 Main Scheme 2A.png", "ap006b": "06B Main Scheme 2B.png",
    "ap007a": "07 Main Scheme 3A.png", "ap007b": "07B Main Scheme 3B.png", "ap008a": "08 Main Scheme 4A.png", "ap008b": "08B Main Scheme 4B.png",
    "ap009": "09 Alien Hive Side Scheme.png", "ap010": "10 Ultimate Hunt Side Scheme.png", "ap011": "11 Attach - plasmacaster.png",
    "ap012": "12 Attach - wrist blades.png", "ap013": "13 Attach - Targeted.png", "ap015": "15 Attach - Inner Teeth.png",
    "ap016": "16 Attach - facehugger.png", "ap018": "18 Minion Drone.png", "ap020": "20 Minion Warrior.png", "ap021": "21 Minion Praetorian.png",
    "ap022": "22 Attach - chestburster.png", "ap023": "23 Hive Incursion treach.png", "ap024": "24 - Treachery defeat ally.png",
    "ap025": "25 side scheme ATK.png", "ap026": "26 - Treachery.png", "ap027": "27 - Treachery.png", "ap028": "28 - Treachery.png",
    "ap029": "29 - Treachery.png", "ap030": "30 - Treachery-Trophy.png", "ap031": "31 - Treachery.png", "ap032": "32 side scheme DMG villains.png",
    "ap033": "33 side scheme defeat minions.png",
    "ap101": X + "01-04 Alien Scout minion.png", "ap102": X + "05-08 Alien Scout minion.png", "ap103": X + "09-12 Alien Scout minion.png",
    "ap104": X + "13-16 Alien Scout minion.png",
    "ap201": A + "01 STD Advance.png", "ap202": A + "02 STD Advance.png", "ap203": A + "03 STD Assault.png", "ap204": A + "04 STD cruel.png",
    "ap205": A + "05 STD Over Force.png", "ap206": A + "06 STD Masterplan.png", "ap207": A + "07 STD Shadow.png",
    "ap301": C + "01 Yautja Young Blood.png", "ap302": C + "02 Blooded Predator.png", "ap303": C + "03 Predator Elite.png",
    "ap304": C + "04 Apex Predator.png", "ap305": C + "05 Yautja Side Scheme.png", "ap306": C + "06 Attach - Cloak.png",
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
print(len(CARTES), "images")
