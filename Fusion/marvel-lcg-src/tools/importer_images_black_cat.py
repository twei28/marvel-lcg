# -*- coding: utf-8 -*-
"""Recette des images du pack BLACK CAT : assets/pics/ est gitignore, donc
cette recette est la seule chose reproductible. Source : zip fan-made
'Black Cat-20260902T073818Z-1-001.zip' (Rainy), extrait par
`python3 -m zipfile -e`.

⚠ LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS, comme tous les packs de Rainy :
« 0.1 Felicia Hardy » est l'ALTER-EGO (bc001b) et « 0.2 Black Cat » le HEROS
(bc001a). Verifie sur les libelles imprimes ALTER-EGO / HERO, pas sur le nom
de fichier.

⚠ « 1 Spider-Man (black) » ET « 1 Spider-Man (red) » NE SONT PAS DEUX
ILLUSTRATIONS DE LA MEME CARTE. Toutes deux numerotees « BLACK CAT (1/15) » et
nommees « * Spider-Man », elles ont des statistiques, des traits et des
capacites DIFFERENTS : PV 4 SYMBIOTE + WEB-WARRIOR pour la noire (bc002),
PV 3 AVENGER pour la rouge (bc003), qui porte en plus le mot-cle Multiverse.
Deux card_id, deux images.

⚠ LES 13 FICHIERS DU ZIP SONT TOUT LE PACK : il n'y a AUCUNE carte de set
nemesis. Ce n'est pas un oubli d'extraction, c'est le pack tel qu'il est
livre.

⚠ « Big Heist.jpg » est la SEULE image en format PAYSAGE (2150x1500) : c'est
une manigance annexe JOUEUR. Les douze autres sont en portrait (1500x2150).

Usage : python3.10 tools/importer_images_black_cat.py <dossier extrait>
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
    "bc001a": "0.2 Black Cat.jpg",
    "bc001b": "0.1 Felicia Hardy.jpg",
    # les DEUX versions de la carte 1/15 (voir l'en-tete)
    "bc002": "1 Spider-Man (black).jpg",
    "bc003": "1 Spider-Man (red).jpg",
    # signature
    "bc004": "Big Heist.jpg",
    "bc005": "Cat Burglary.jpg",
    "bc006": "Lucky Hit.jpg",
    "bc007": "Misfortune.jpg",
    "bc008": "Black Cat_s Claws.jpg",
    "bc009": "Grappling Hook.jpg",
    "bc010": "Ill Gotten Gains.jpg",
    "bc011": "Nine Lives.jpg",
    # obligation : bandeau « BLACK CAT », donc set du heros
    "bc012": "Black Cat obligation.jpg",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Black Cat")
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
