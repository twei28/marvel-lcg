# -*- coding: utf-8 -*-
"""Recette des 13 images du pack JESSICA JONES (set officiel 61) absentes de
MarvelCDB : voir `importer_mc4db.py` pour la source et le format.

Les 30 autres cartes du pack etaient deja en place (previews Hall of Heroes,
300x426). Verifie le 29/09/2026 : les 13 codes ci-dessous sont les seuls du
set `jj` de `data/cards.json` sans fichier dans `assets/pics/`.

    python3 tools/importer_images_jessica_jones.py
    python3 outils/uniformiser-scans.py --sauvegarde && python3 outils/uniformiser-scans.py --appliquer
"""
from importer_mc4db import importer

CODES = [
    "61012",   # "Now I'm Ticked Off!"
    "61013",   # Reluctant Flier
    "61018",   # Lay Down the Law
    "61022",   # Determination
    "61031",   # Purple Man
    "61032",   # Indomitable Will
    "61033a",  # Suggestion (energy)
    "61033b",  # Suggestion (mental)
    "61033c",  # Suggestion (physical)
    "61034",   # Innate Aggression
    "61036",   # Innate Perception
    "61037",   # Innate Inspiration
    "61038",   # Echo
]

if __name__ == "__main__":
    absents = importer(CODES)
    print(len(CODES) - len(absents), "images importees dans assets/pics/",
          ("; SANS IMAGE : " + ", ".join(absents)) if absents else "")
