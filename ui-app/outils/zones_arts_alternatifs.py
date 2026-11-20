#!/usr/bin/env python3
"""Zones de texte des arts alternatifs de héros (cb, rog, rog2, m3t) : point d'entrée.

    cd ui-app && python3 outils/zones_arts_alternatifs.py [--planches <dossier>]

Décode les scans (300 x 420), fait tourner le détecteur du plateau par
outils/zones-arts-alternatifs.mjs, qui applique src/board/zones-arts-alternatifs.corrections.json
et écrit src/board/zones-arts-alternatifs.ts. Avec --planches : planches-contact,
zone retenue en rouge, pour vérifier chaque image à l'œil.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

ICI = os.path.dirname(os.path.abspath(__file__))
UI = os.path.dirname(ICI)
PICS = os.path.join(UI, "..", "Fusion", "marvel-lcg-src", "assets", "pics")
SERIES = re.compile(r"^(.+_(cb|rog|rog2|m3t|mcdc26))\.(jpg|jpeg|png|webp)$")
L, H = 300, 420



def proposition_blanche(image):
    """Plus grande tache presque blanche du bas de la carte (encadre des arts « Comic »)."""
    largeur, hauteur = image.size
    px = image.load()
    blanc = [[False] * largeur for _ in range(hauteur)]
    for y in range(hauteur // 2, hauteur):
        for x in range(largeur):
            r, g, b = px[x, y][:3]
            blanc[y][x] = min(r, g, b) >= 205 and max(r, g, b) - min(r, g, b) <= 35
    vu = [[False] * largeur for _ in range(hauteur)]
    meilleure = None
    for y0 in range(hauteur // 2, hauteur):
        for x0 in range(largeur):
            if not blanc[y0][x0] or vu[y0][x0]:
                continue
            pile, n = [(x0, y0)], 0
            vu[y0][x0] = True
            bx0, by0, bx1, by1 = x0, y0, x0, y0
            while pile:
                x, y = pile.pop()
                n += 1
                bx0, by0, bx1, by1 = min(bx0, x), min(by0, y), max(bx1, x), max(by1, y)
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if hauteur // 2 <= ny < hauteur and 0 <= nx < largeur and blanc[ny][nx] and not vu[ny][nx]:
                        vu[ny][nx] = True
                        pile.append((nx, ny))
            # Un encadre est plein : la tache couvre l'essentiel de sa boite.
            if n >= 0.45 * (bx1 - bx0 + 1) * (by1 - by0 + 1) and (meilleure is None or n > meilleure[0]):
                meilleure = (n, bx0, by0, bx1, by1)
    if not meilleure or meilleure[0] < 0.04 * largeur * hauteur:
        return None
    _, bx0, by0, bx1, by1 = meilleure
    return [round(bx0 / largeur, 3), round(by0 / hauteur, 3), round((bx1 + 1) / largeur, 3), round((by1 + 1) / hauteur, 3)]


fichiers = sorted(f for f in os.listdir(PICS) if SERIES.match(f))
# Dans ui-app : le Node du poste (binaire Windows) lit ce chemin relatif.
travail = tempfile.mkdtemp(prefix=".zones-", dir=UI)
try:
    propositions = {}
    with open(os.path.join(travail, "pixels.bin"), "wb") as sortie:
        for f in fichiers:
            image = Image.open(os.path.join(PICS, f)).convert("RGBA").resize((L, H), Image.LANCZOS)
            sortie.write(image.tobytes())
            propositions[SERIES.match(f).group(1)] = proposition_blanche(image)
    with open(os.path.join(travail, "propositions.json"), "w") as sortie:
        json.dump(propositions, sortie)
    with open(os.path.join(travail, "fichiers.json"), "w") as sortie:
        json.dump(fichiers, sortie)
    subprocess.run(["node", "outils/zones-arts-alternatifs.mjs", os.path.basename(travail)], cwd=UI, check=True)
    if "--planches" in sys.argv:
        dossier = sys.argv[sys.argv.index("--planches") + 1]
        os.makedirs(dossier, exist_ok=True)
        donnees = json.load(open(os.path.join(travail, "zones.json")))
        W, HH, PAR = 200, 280, 12
        for p in range(0, len(fichiers), PAR):
            planche = Image.new("RGB", (W * 6, (HH + 16) * 2), "white")
            dessin = ImageDraw.Draw(planche)
            for k, f in enumerate(fichiers[p:p + PAR]):
                cle = SERIES.match(f).group(1)
                x, y = (k % 6) * W, (k // 6) * (HH + 16)
                planche.paste(Image.open(os.path.join(PICS, f)).convert("RGB").resize((W, HH)), (x, y))
                z = donnees["zones"].get(cle)
                if z:
                    dessin.rectangle([x + z["x0"] * W, y + z["y0"] * HH, x + z["x1"] * W, y + z["y1"] * HH], outline="red", width=3)
                dessin.text((x + 2, y + HH + 2), ("" if z else "SANS ") + cle, fill="black")
            planche.save(os.path.join(dossier, f"planche-{p // PAR:02d}.jpg"), quality=80)
finally:
    shutil.rmtree(travail, ignore_errors=True)
