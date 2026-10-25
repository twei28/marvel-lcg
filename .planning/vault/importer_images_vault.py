#!/usr/bin/env python3
"""Images du scenario THE VAULT (Kajislav) : 27 card_id.

Usage : python3 importer_images_vault.py <dossier « The Vault (Sealed) » extrait> [racine_du_depot]

Ecrit `assets/pics/<card_id>.jpg` (petit cote ramene a 615 px, LANCZOS). Les cartes COUCHEES dans un PNG portrait
(complot principal 17A/17B et manigances 26-29, texte tourne de 90° vers la droite) sont REDRESSEES en paysage
(rotation de 90° anti-horaire), comme `ld004a`. L'original reste dans `sauvegardes-serveur/scans-originaux/`.
Les images ne sont pas versionnees.
"""
import os
import sys
from PIL import Image

SRC = sys.argv[1]
RACINE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
V = "Villain deck/"
S = "Setup cards/"
E = "Encounter cards/"
# (fichier, couchee ?)
CARTES = {
    "vt001": (V + "01 batroc.png", False), "vt002": (V + "02 batroc II.png", False),
    "vt003": (V + "03 mentallo.png", False), "vt004": (V + "04 mentallo II.png", False),
    "vt005": (V + "05 grey Gargoyle.png", False), "vt006": (V + "06 grey Gargoyle II.png", False),
    "vt007": (V + "07 hydro-man.png", False), "vt008": (V + "08 hydro-man villain II.png", False),
    "vt009": (V + "09 mad Thinker villain.png", False), "vt010": (V + "10 mad Thinker villain II.png", False),
    "vt011": (V + "11 nekra villain.png", False), "vt012": (V + "12 nekra villain II.png", False),
    "vt013": (V + "13 vapor.png", False), "vt014": (V + "14 vapor II.png", False),
    "vt015": (V + "15 venom villain.png", False), "vt016": (V + "16 venom villain II.png", False),
    "vt017a": (S + "17 vault breakout IA.png", True), "vt017b": (S + "17 vault breakout IB.png", True),
    "vt018": (S + "18 vault.png", False), "vt019": (S + "19 inspection.png", False),
    "vt020": (E + "20 craven escape.png", False), "vt022": (E + "22 corrupted guardsman.png", False),
    "vt026": (E + "26 burglary.png", True), "vt028": (E + "28 backup plan.png", True),
    "vt029": (E + "29 schemeing from within.png", True), "vt030": (E + "30 enemy encounter.png", False),
    "vt034": (E + "34 cause a stir.png", False),
}
os.makedirs(os.path.join(MOTEUR, "assets", "pics"), exist_ok=True)
os.makedirs(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux"), exist_ok=True)
for cid, (rel, couchee) in CARTES.items():
    im = Image.open(os.path.join(SRC, rel)).convert("RGB")
    im.save(os.path.join(MOTEUR, "sauvegardes-serveur", "scans-originaux", cid + ".jpg"), quality=95)
    if couchee:
        im = im.rotate(90, expand=True)
    w, h = im.size
    k = 615 / min(w, h)
    im = im.resize((round(w * k), round(h * k)), Image.LANCZOS)
    im.save(os.path.join(MOTEUR, "assets", "pics", cid + ".jpg"), quality=92)
    print(cid, im.size)
