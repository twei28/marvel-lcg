#!/usr/bin/env python3
"""Images du heros SHANG-CHI (DesignHacker, SEALED) : 21 card_id.

Usage : python3 importer_images_shang_chi.py <dossier « SHANG-CHI (SEALED) »> [racine_du_depot]

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
H = "HERO DECK/"
E = "ENCOUNTER DECK/"
CARTES = {
    "shc001a": "~ HERO - SHANG-CHI.png",
    "shc001b": "~ ALTER-EGO - SHANG-CHI.jpg",
    "shc002": "SUPPORT - State of Flow.jpg",
    "shc003": H + "EVENT - Throat Punch 1.jpg",         # 1/15 : physique + mental
    "shc004": H + "EVENT - Throat Punch 2.jpg",         # 2/15 : mental
    "shc005": H + "EVENT - Roundhouse Kick.jpg",        # 3/15 : energie
    "shc006": H + "EVENT - Roundhouse Kick 2.jpg",      # 4/15 : physique + energie
    "shc007": H + "EVENT - Special Delivery.jpg",       # 5/15 : wild
    "shc008": H + "EVENT - Special Delivery copy.jpg",  # 6/15 : mental
    "shc009": H + "EVENT - Dragon Strike.jpg",          # 7/15 : wild
    "shc010": H + "EVENT - Dragon Strike copy.jpg",     # 8/15 : energie
    "shc011": H + "EVENT - Chi Jabs.jpg",               # 9/15 : wild
    "shc012": H + "EVENT - Chi Jabs copy.jpg",          # 10/15 : physique
    "shc013": H + "EVENT - Augmented Blow.jpg",         # 11/15 : energie + mental
    "shc014": H + "EVENT - Augmented Blow copy.jpg",    # 12/15 : physique
    "shc015": H + "UPGRADE - Stark Nunchaku.jpg",
    "shc016": H + "UPGRADE - Golden Bracers.jpg",       # fichier mal nomme : la carte est Metal Bracers
    "shc017": H + "UPGRADE - Martial Mastery.jpg",
    "shc018": E + "SC ENCOUNTER - OBLIGATION.jpg",
    "shc019": E + "SC ENCOUNTER - NEMESIS MINION.jpg",
    "shc020": E + "SC ENCOUNTER - SIDE SCHEME.jpg",
    "shc021": E + "SC ENCOUNTER - TREACHERY.jpg",
}
PAYSAGE = {"shc020"}
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
