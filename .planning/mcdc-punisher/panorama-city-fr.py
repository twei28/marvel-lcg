"""Recolle les scans FRANCAIS de The City (pu005) et Never Sleeps (pu006) en un panorama continu.

Pendant de panorama-city.py (images EN 532x740). Ici les scans de l'equipe MC×DC sont en 750x1075 (pleine page) : chaque
illustration deborde sur sa voisine de D = 152 px (mesure : ecart quadratique ~47 sur 290 lignes, decalage vertical 0).
Panorama = A[:, :750] fondue avec B[:, 152:], etire a 1500 px de large, redecoupe en deux moities de 750 px. Seule la zone
d'illustration est remplacee (cadre, titre, etiquette et boite de texte restent ceux de chaque scan).
Usage : python3 panorama-city-fr.py <6005.jpg> <6006.jpg> <dossier de sortie>
"""
import sys
import numpy as np
from PIL import Image

D, F = 152, 80          # chevauchement mesure, largeur du fondu
W, H = 750, 1075


def haut_a(x):
    # bord haut de l'illustration de The City : coin coupe a gauche, sous l'etiquette ENVIRONNEMENT, encoche du centre
    if x < 145: return int(190 - 0.566 * x) + 4
    if x < 535: return 110
    if x < 690: return 154
    return 192


def haut_b(x):
    if x < 60: return 192
    if x < 220: return 154
    if x < 695: return 110
    return int(110 + (x - 695) * 80 / 55) + 4
FONDU_V = 12            # fondu vertical aux bords haut et bas de la zone remplacee
# bord haut de la boite de texte, relu sur les scans : (x=0, x=750)
BAS_A = (598, 585)
BAS_B = (603, 588)

a = np.asarray(Image.open(sys.argv[1]).convert('RGB'), dtype=float)
b = np.asarray(Image.open(sys.argv[2]).convert('RGB'), dtype=float)
assert a.shape == (H, W, 3) and b.shape == (H, W, 3)

y0, y1 = 100, 600
w = np.linspace(0, 1, F)[None, :, None]
fondu = a[y0:y1, W - F:W] * (1 - w) + b[y0:y1, D - F:D] * w
pano = np.concatenate([a[y0:y1, :W - F], fondu, b[y0:y1, D:]], axis=1)          # 750 + 598 = 1348 de large
pano = np.asarray(Image.fromarray(pano.clip(0, 255).astype('uint8')).resize((2 * W, y1 - y0), Image.LANCZOS), dtype=float)


def pose(src, moitie, bas, haut):
    out = src.copy()
    for x in range(W):
        y_bas = int(bas[0] + (bas[1] - bas[0]) * x / (W - 1)) - 6
        y_haut = haut(x)
        for y in range(y_haut, y_bas + 1):
            t = max(0.0, min(1.0, (y - y_haut) / FONDU_V, (y_bas - y) / FONDU_V))
            out[y, x] = src[y, x] * (1 - t) + pano[y - y0, moitie * W + x] * t
    return out


na, nb = pose(a, 0, BAS_A, haut_a), pose(b, 1, BAS_B, haut_b)
sortie = sys.argv[3]
Image.fromarray(na.clip(0, 255).astype('uint8')).save(sortie + '/pu005_pano.jpg', quality=93)
Image.fromarray(nb.clip(0, 255).astype('uint8')).save(sortie + '/pu006_pano.jpg', quality=93)
o = Image.new('RGB', (2 * W, H)); o.paste(Image.open(sortie + '/pu005_pano.jpg'), (0, 0)); o.paste(Image.open(sortie + '/pu006_pano.jpg'), (W, 0))
o.save(sortie + '/pano.png')
