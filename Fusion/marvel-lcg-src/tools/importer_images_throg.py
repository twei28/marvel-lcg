# -*- coding: utf-8 -*-
"""Recette des images du pack THROG : assets/pics/ est gitignore, donc cette
recette est la seule chose reproductible. Source : zip fan-made
'Throg-20260902T074023Z-1-001.zip' (Rainy), extrait par
`python3 -m zipfile -e`.

⚠ LE ZIP NUMEROTE LES DEUX FACES A L'ENVERS : « 0.1 Puddlegulp » est
l'ALTER-EGO (tg001b) et « 0.2 Throg » le HEROS (tg001a). Verifie sur les
libelles imprimes ALTER-EGO / HERO et sur les statistiques (REC 4 d'un cote,
ATQ/CTR/DEF de l'autre), pas sur le nom de fichier. Meme piege que br001a/b.

⚠ CINQ CARTES SONT LIVREES EN PLUSIEURS EXEMPLAIRES et n'ont donc qu'UN
card_id. Les scans ont ete compares au pixel (cout haut-gauche, icone de
ressource bas-gauche, bloc de texte) : ecart maximal 0 partout. Ce n'est PAS
le cas de figure `bt007a/b` Multi-Tasking, ou deux scans de meme nom
differaient par l'icone.
  1-2-3 Airborne Amphibian -> tg002
  4-5   Great Courage      -> tg003
  6-7   Hammer Throw       -> tg004
  8-9   Lightning Leap     -> tg005
  10-11 Thunderous Charge  -> tg006

Le dossier `PSDs/` du zip (17 fichiers) n'est PAS importe : ce sont les
sources d'illustration de l'auteur, pas des cartes.

Usage : python3.10 tools/importer_images_throg.py <dossier extrait>
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
    "tg001a": "0.2 Throg.jpg",
    "tg001b": "0.1 Puddlegulp.jpg",
    # signature
    "tg002": "1 Airborne Amphibian.jpg",
    "tg003": "4 Great Courage.jpg",
    "tg004": "6 Hammer Throw.jpg",
    "tg005": "8 Lightning Leap.jpg",
    "tg006": "10 Thunderous Charge.jpg",
    "tg007": "12 Foreverglade.jpg",
    "tg008": "13 Frog of Thunder.jpg",
    "tg009": "14 Frogjolnir.jpg",
    "tg010": "15 Throg_s Armor.jpg",
    # obligation : bandeau « THROG », donc set du heros
    "tg011": "Nemesis & obligation/obligation Trouble in Central Park.jpg",
    # set nemesis
    "tg012": "Nemesis & obligation/1 Adorable Distraction.jpg",
    "tg013": "Nemesis & obligation/2 Alligator Loki.jpg",
    "tg014": "Nemesis & obligation/3 Causing a Commotion.jpg",
    "tg015": "Nemesis & obligation/4 Lost Property.jpg",
    "tg016": "Nemesis & obligation/5 Chomped.jpg",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Throg")
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
