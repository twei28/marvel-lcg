#!/usr/bin/env python3
"""Prepare les scans pour un hebergement STATIQUE : le moteur redresse en portrait toute image plus large que
haute (engine/file/cache.py, TryRotateImage) et le plateau la remet a plat par CSS. Un hebergeur statique ne
peut pas le faire a la volee : ce script ecrit UNIQUEMENT les versions tournees des scans paysage, a servir
AVANT les originaux sous /scan/<id> (dans Caddy : try_files vers ce dossier d'abord).

    python3 navigateur/preparer-scans.py --compter            # combien, sans rien ecrire
    python3 navigateur/preparer-scans.py <dossier-de-sortie>  # ecrit <sortie>/pivotes/<dossier>/<fichier>
"""
import os, sys
from PIL import Image, ImageOps
ASSETS = os.environ.get("ASSETS", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Fusion", "marvel-lcg-src", "assets"))
DOSSIERS = ("pics-fr", "pics", "textures", "cache", "vignettes")
compter = "--compter" in sys.argv
sortie = None if compter else sys.argv[1]
n = tot = octets = 0
for d in DOSSIERS:
    base = os.path.join(ASSETS, d)
    if not os.path.isdir(base):
        continue
    for nom in sorted(os.listdir(base)):
        if not nom.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            continue
        tot += 1
        p = os.path.join(base, nom)
        try:
            im = ImageOps.exif_transpose(Image.open(p))
        except Exception:
            continue
        if im.width <= im.height:
            continue
        n += 1
        if sortie:
            os.makedirs(os.path.join(sortie, "pivotes", d), exist_ok=True)
            dest = os.path.join(sortie, "pivotes", d, nom)
            im.rotate(90, expand=True).save(dest, quality=90)
            octets += os.path.getsize(dest)
print(f"{n} scans paysage sur {tot}" + (f", {octets/1e6:.0f} Mo ecrits" if sortie else ""))
