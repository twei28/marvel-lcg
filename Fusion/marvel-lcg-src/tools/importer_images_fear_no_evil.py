# -*- coding: utf-8 -*-
"""Recette des 5 images de FEAR NO EVIL (set officiel 60) absentes de
MarvelCDB : voir `importer_mc4db.py` pour la source et le format.

Les autres cartes du pack viennent de Hall of Heroes (18/09/2026). Verifie le
29/09/2026 : ces cinq codes etaient les seuls sans fichier dans `assets/pics/`.

    python3 tools/importer_images_fear_no_evil.py
    python3 outils/uniformiser-scans.py --sauvegarde && python3 outils/uniformiser-scans.py --appliquer
"""
from importer_mc4db import importer

CODES = [
    "60051",  # Powerful Punch
    "60056",  # Superpower Training
    "60057",  # Energy
    "60058",  # Genius
    "60059",  # Strength
]

if __name__ == "__main__":
    absents = importer(CODES)
    print(len(CODES) - len(absents), "images importees dans assets/pics/",
          ("; SANS IMAGE : " + ", ".join(absents)) if absents else "")
