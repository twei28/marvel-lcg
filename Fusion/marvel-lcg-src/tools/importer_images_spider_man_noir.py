# -*- coding: utf-8 -*-
"""Recette des images du pack SPIDER-MAN NOIR : assets/pics/ est gitignore,
donc cette recette est la seule chose reproductible. Source : zip fan-made
'Spider-Man Noir-20260902T073956Z-1-001.zip' (Rainy), extrait par
`python3 -m zipfile -e`.

⚠ LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS, comme tous les packs de Rainy :
« 0.1 Peter Parker » est l'ALTER-EGO (sn001b) et « 0.2 Spider-Man Noir » le
HEROS (sn001a). Verifie sur les libelles imprimes ALTER-EGO / HERO.

⚠ CINQ CARTES SONT LIVREES EN PLUSIEURS EXEMPLAIRES et n'ont donc qu'UN
card_id. Les scans ont ete compares au pixel (cout haut-gauche, icone de
ressource bas-gauche, bloc de texte) : ecart maximal 0 partout.
  1-2-3   Guns Blazing            -> sn002
  4-5     Webs Within Webs        -> sn003
  6-7     Web Shot                -> sn004
  8-9-10  Web Swinging            -> sn005
  3-4 (N) Lightning Strikes Twice -> sn014

Usage : python3.10 tools/importer_images_spider_man_noir.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

MAP = {
    # identite (numerotation du zip inversee, voir l'en-tete)
    "sn001a": "0.2 Spider-Man Noir.jpg",
    "sn001b": "0.1 Peter Parker.jpg",
    # signature
    "sn002": "1 Guns Blazing.jpg",
    "sn003": "4 Webs Within Webs.jpg",
    "sn004": "6 Web Shot.jpg",
    "sn005": "8 Web Swinging.jpg",
    "sn006": "11 The Black Cat Club.jpg",
    "sn007": "12 Dual Pistols.jpg",
    "sn008": "13 Enhanced Spider-Sense.jpg",
    "sn009": "14 Fancy Fedora.jpg",
    "sn010": "15 Organic Webbing.jpg",
    # obligation : bandeau « SPIDER-MAN NOIR », donc set du heros
    "sn011": "Nemesis & Obligation/obligation In Walks Trouble.jpg",
    # set nemesis
    "sn012": "Nemesis & Obligation/1 Power Struggle.jpg",
    "sn013": "Nemesis & Obligation/2 Electro Noir.jpg",
    "sn014": "Nemesis & Obligation/3 Lightning Strikes Twice.jpg",
    "sn015": "Nemesis & Obligation/5 Thunderstorm.jpg",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Spider-Man Noir")
    if not os.path.isdir(src):
        print(f"dossier introuvable : {src}")
        return 2

    manquants = []
    for card_id, nom in MAP.items():
        chemin = os.path.join(src, nom)
        if not os.path.isfile(chemin):
            manquants.append(nom)
            continue
        shutil.copyfile(chemin, os.path.join(DST, card_id + ".jpg"))
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{len(MAP)} images importees dans {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
