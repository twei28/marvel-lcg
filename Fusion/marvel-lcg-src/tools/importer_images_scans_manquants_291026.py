# -*- coding: utf-8 -*-
"""Recette des 10 scans officiels retrouves manquants le 29/10/2026 (audit complet
des 8545 entrees de data/cards.json contre assets/pics, apres resolution des
reimpressions `full_link`/`ability_link` et exclusion des jetons `Status`, qui
vivent dans assets/textures/, pas ici).

Tous les dix sont des cartes OFFICIELLES FFG dont marvelcdb.com n'a plus (ou pas)
le scan ; mc4db (clone de marvelcdb, voir importer_mc4db.py) les a tous les dix.

    python3 tools/importer_images_scans_manquants_291026.py
    python3 outils/uniformiser-scans.py --sauvegarde && python3 outils/uniformiser-scans.py --appliquer

Deux groupes signales par le meme audit, VOLONTAIREMENT laisses de cote :
  * 13 allies de `gs224` a `gs236` (Galactic Storm Campaign) et `2425_boss_rush`
    (Challenge) : absents de mc4db aussi -- contenu de campagne non standard,
    pas des codes FFG a cinq chiffres, aucune source officielle connue pour eux.
  * Les cartes de type `Status` (Confused, Stunned, Tough...) : leurs images sont
    dans assets/textures/, pas assets/pics/ -- l'audit les avait d'abord signalees
    a tort avant que ce filtre soit ajoute.
"""
from importer_mc4db import importer

CODES = [
    "62003",  # Harlem's Hero (Luke Cage)
    "62007",  # Fogwell's Gym (Luke Cage)
    "62009",  # Cruisin' for a Bruisin' (Luke Cage) -- signalee par l'utilisateur
    "01144a",  # Android Efficiency (Ultron, core) -- servent aussi 01144/01144b/01144c (ability_link)
    "54031",  # Hydra Mercenary (Winter Soldier Nemesis)
    "56097a",  # Pro-Registration Tactics (Civil War)
    "56123a",  # Pro-Registration Tactics (Civil War)
    "56124a",  # Pro-Registration Tactics (Civil War)
    "56142a",  # Resistance Tactics (Civil War)
    "56173a",  # Resistance Tactics (Civil War)
]

if __name__ == "__main__":
    absents = importer(CODES)
    print(len(CODES) - len(absents), "images importees dans assets/pics/",
          ("; SANS IMAGE : " + ", ".join(absents)) if absents else "")
