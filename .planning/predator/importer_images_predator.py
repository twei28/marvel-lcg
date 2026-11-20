#!/usr/bin/env python3
"""Images du heros PREDATOR (RyCoRan) : 31 card_id.

Usage : python3 importer_images_predator.py <dossier « Predator (5-25 Final) »> [racine_du_depot]

Ecrit `assets/pics/<card_id>.jpg` (petit cote ramene a 615 px, LANCZOS) et garde l'original dans
`sauvegardes-serveur/scans-originaux/<card_id>.jpg`. Les manigances annexes sont deja a l'horizontale dans le zip
(2150x1500) : aucune rotation. Les images ne sont pas versionnees.
"""
import os
import sys
from PIL import Image

SRC = sys.argv[1]
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
N = "Predator Nemesis/"
A = "Predator Alt Nemesis/"
R = "Predator Resources/"
CARTES = {
    "pd001a": "00A - Predator - hero.png",
    "pd001b": "00B - Predator - AE.png",
    "pd002": "01 - Infralocked upgrade.png",
    "pd003": "02 - predator - ally.png",
    "pd004": "03 - pred event THW.png",            # 3/16 (4/16 identique)
    "pd005": "05 - pred event Spine rip.png",      # 5/16 (6/16 identique)
    "pd006": "07 - pred event DEF.png",
    "pd007": "08 - pred event-blurred.png",        # 8/16 (9/16 identique)
    "pd008": "10 - pred event FIND-HEAL.png",
    "pd009": "11 - Predator side scheme.png",
    "pd010": "12 - support trophy.png",
    "pd011": "13 - pred upgrade - destruct.png",
    "pd012": "14 - pred upgrade - wrist blades.png",
    "pd013": "15 - pred upgrade - plasma.png",
    "pd014": "16 - pred upgrade - helmet.png",
    "pd015": N + "N00 - Predator - obligation.png",
    "pd016": N + "N01 - Pred - Side Scheme.png",
    "pd017": N + "N02 - Pred Minion Queen.png",
    "pd018": N + "N03 - Pred Minion Drone.png",
    "pd019": N + "N04 - Pred - Treach.png",
    "pd020": N + "N05 - Pred-Attach.png",
    "pd021": R + "Predator (R) - Energy.png",
    "pd022": R + "Predator (R) - Genius.png",
    "pd023": R + "Predator (R) - Strength2.png",
    "pd024": "Predator-Wolverine  TeamUp.png",
    "pd025": "Pred - Spidey Aspect - Event.png",
    "pd026": A + "N01 - Side Scheme-Chopper.png",
    "pd027": A + "N02 - Dutch - Minion.png",
    "pd028": A + "N03 - Dillon - Minion.png",
    "pd029": A + "N04 - pred - Attach.png",
    "pd030": A + "N05 - Treachery (GET).png",
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
