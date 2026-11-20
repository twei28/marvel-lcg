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
from PIL import Image, ImageDraw, ImageFont

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "assets", "textures", "sets")
SORTIE = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "img", "prepare", "boites")
RATIO = 0.72
LARGEUR, HAUTEUR = 288, 400

# ⚠ 1, 56, 57, 120, 143, 178 RETIRÉES le 29/10/2026 : nouvelles images d'origine recues
# (Core Set, Civil War, Synthezoid Smackdown, Web of Deceit, Skrull Menace, Hunting Season),
# affichees entieres (pochette carree en "contain" cote CSS) : plus besoin de ce recadrage
# manuel pour elles. 119 (The Spot) et 192 (Bebop & Rocksteady) n'avaient jamais ete ici
# (elles etaient composees depuis assets/pics, voir plus bas) : memes nouvelles images,
# posees directement dans assets/textures/sets/.
RECTS = {
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
    "60. Fear No Evil": (42, 0, 216),
    "136. Custom (Gorr the God Butcher)": (0, 10, 183),
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


# Les trois boites fan-made TMNT n'ont pas de pochette : on en tire une de l'illustration de leur méchant
# (assets/pics), recadrée sur le personnage, avec le titre en Bangers comme sur les autres couvertures.
PICS = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "assets", "pics")
POLICE = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "public", "fonts", "Bangers-Regular.ttf")
Y0, Y1 = 98, 488   # la fenêtre de l'illustration sur une carte de méchant (615 x 882)
LARGE = round((Y1 - Y0) * RATIO)
# 192 (Bebop & Rocksteady) et 119 (The Spot) RETIRÉS le 29/10/2026 : vraies pochettes recues,
# posees directement dans assets/textures/sets/ (plus besoin de les composer depuis une carte).
DE_CARTES = {
    "190": ("SHREDDER", [("ts001.jpg", 215)]),
    "195": ("BAXTER STOCKMAN", [("tx001.jpg", 130)]),
}
for numero, (titre, morceaux, *fenetre) in DE_CARTES.items():
    y0, y1 = fenetre if fenetre else (Y0, Y1)
    large = round((y1 - y0) * RATIO)
    toile = Image.new("RGB", (large, y1 - y0))
    part = large // len(morceaux)
    for i, (fichier, x) in enumerate(morceaux):
        carte = Image.open(os.path.join(PICS, fichier)).convert("RGB")
        toile.paste(carte.crop((x, y0, x + part, y1)), (i * part, 0))
    toile = toile.resize((LARGEUR, HAUTEUR), Image.LANCZOS)
    d = ImageDraw.Draw(toile)
    taille = 46
    while True:
        police = ImageFont.truetype(POLICE, taille)
        if d.textlength(titre, font=police) <= LARGEUR - 24 or taille <= 20:
            break
        taille -= 2
    d.text((LARGEUR / 2, HAUTEUR - 34), titre, font=police, fill="white", anchor="mm", stroke_width=4, stroke_fill="black")
    toile.save(os.path.join(SORTIE, numero + ".webp"), quality=90, method=6)
    print(numero, titre)
