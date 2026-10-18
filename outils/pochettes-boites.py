#!/usr/bin/env python3
"""Pochettes des boites de scenarios, toutes recadrees au meme format (18/10/2026).

Les images de `assets/textures/sets/` sont de quatre sortes (pochette de pack portrait, illustration plate
carree, boite 3D en biais, pochette fan-made) : affichees telles quelles, elles ont l'air de quatre tailles.
Ce script en tire, pour chaque boite du choix du mechant, le meme cadre portrait 0,72 : l'illustration
seule, de face, sans le liseré du pack ni la perspective de la boite.

    python3 outils/pochettes-boites.py     # ecrit public/img/prepare/boites/<numero>.webp

Les rectangles sont (x, y, largeur) dans l'image d'origine ; la hauteur se deduit du ratio. Une nouvelle boite
sans entree ici garde son image d'origine (voir `pochetteBoite` dans public/js/prepare/app.js).
"""
import os
from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "assets", "textures", "sets")
SORTIE = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "img", "prepare", "boites")
RATIO = 0.72
LARGEUR, HAUTEUR = 288, 400

RECTS = {
    "1. Core Set": (72, 4, 160),
    "2. The Green Goblin": (10, 48, 159),
    "4. The Rise of Red Skull": (42, 0, 216),
    "7. The Wrecking Crew": (10, 48, 159),
    "11. The Once and Future Kang": (10, 48, 159),
    "16. Galaxy's Most Wanted": (42, 0, 216),
    "21. The Mad Titan's Shadow": (42, 0, 216),
    "24. The Hood": (18, 44, 166),
    "27. Sinister Motives": (42, 0, 216),
    "32. Mutant Genesis": (42, 0, 216),
    "39. Mojo Mania": (25, 40, 165),
    "40. NeXt Evolution": (42, 0, 216),
    "45. Age of Apocalypse": (42, 0, 216),
    "50. Agents of S.H.I.E.L.D.": (42, 0, 216),
    "55. Trickster Takeover": (70, 42, 160),
    "56. Civil War": (20, 0, 216),
    "57. Synthezoid Smackdown": (22, 36, 166),
    "60. Fear No Evil": (42, 0, 216),
    "119. Custom (The Spot)": (0, 5, 209),
    "120. Custom (Web of Deceit)": (0, 5, 209),
    "136. Custom (Gorr the God Butcher)": (0, 10, 183),
    "143. Custom (Skrull Menace)": (28, 0, 216),
    "178. Custom (Hunting Season)": (8, 0, 216),
}

os.makedirs(SORTIE, exist_ok=True)
for nom, (x, y, w) in RECTS.items():
    im = Image.open(os.path.join(SOURCE, nom + ".webp")).convert("RGB")
    h = round(w / RATIO)
    h = min(h, im.height - y)
    w = round(h * RATIO)
    boite = im.crop((x, y, x + w, y + h)).resize((LARGEUR, HAUTEUR), Image.LANCZOS)
    boite.save(os.path.join(SORTIE, nom.split(".")[0] + ".webp"), quality=90, method=6)
    print(nom, (x, y, w, h))
