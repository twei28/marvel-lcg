# -*- coding: utf-8 -*-
"""Recette des images du pack MICHELANGELO (TMNT Heroes v3, Inkwire).

assets/pics/ est gitignore : cette recette est la seule chose reproductible.
Source : zip « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Michelangelo v3/ » (24 PNG), extrait SEUL dans un repertoire
neuf, JAMAIS dans le depot.

⚠ LE NOM DE FICHIER « 0 Michelangelo Hero Spin.png » EST LA FACE HEROS, pas une
variante : le dossier ne contient AUCUNE autre face heros (« Hero Spin » = le
heros « en rotation », verifie a la lecture du scan : stats THW 1 / ATK 1 /
DEF 2, libelle HERO). Pas d'art alternatif, pas de `hero_alts`.

⚠ DEUX FICHIERS PAR CARTE DOUBLE. Les exemplaires multiples n'ont qu'UN
card_id ; on prend le premier de chaque serie. Une comparaison pixel a pixel
(PIL ImageChops, 15/10/2026) a prouve que les doublons ne different que par le
numero « n/15 » du bandeau :
  3-4      Impulsive -> tm004
  5-6      Kaiten    -> tm005
  7-8      Majime    -> tm006
  9-10     Optimism  -> tm007
  Bad Stuff 3-4-5 Smash -> tm016

⚠ « 15 Michelangelo_s Other Nunchuck FLIPPED.png » : la mise en page est
MIROIR (texte a gauche, cout en haut a droite), c'est voulu par l'auteur.
⚠ MANIGANCES = PAYSAGE (882x615 dans le jeu, comme ls013 / sf011).
« 12 I_m Here To Help.png » est livre en paysage (2150x1500). « 1 Sewer
Problems.png » est livre en PORTRAIT (1500x2150) avec la carte tournee de 90 :
le titre est a gauche, le texte monte. On la remet a l'endroit par une rotation
de 90 degres dans le sens horaire (ROTATION ci-dessous).

Mise au format : meme regle que outils/uniformiser-scans.py (petit cote ramene
a 615, qualite JPEG 88, jamais d'agrandissement). L'outil lui-meme ecrit en dur
dans /mnt/c/... et sauvegarde les originaux la-bas : il n'est donc pas lance ;
cette recette en reproduit la regle, sans sauvegarde des originaux (le zip
reste la source).

Usage : python3 tools/importer_images_michelangelo.py <dossier "Michelangelo v3">
"""
import os
import sys

from PIL import Image

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)
PETIT_COTE = 615
QUALITE = 88

MAP = {
    "tm001a": "0 Michelangelo Hero Spin.png",
    "tm001b": "0 Mikey alter-ego.png",
    "tm002": "Michelangelo Deck/1 Slash.png",
    "tm003": "Michelangelo Deck/2 Call for Help.png",
    "tm004": "Michelangelo Deck/3 Impulsive.png",
    "tm005": "Michelangelo Deck/5 Kaiten.png",
    "tm006": "Michelangelo Deck/7 Majime.png",
    "tm007": "Michelangelo Deck/9 Optimism.png",
    "tm008": "Michelangelo Deck/11 Mikey_s Couch.png",
    "tm009": "Michelangelo Deck/12 I_m Here To Help.png",
    "tm010": "Michelangelo Deck/13 Mikey_s Skateboard.png",
    "tm011": "Michelangelo Deck/14 Michelangelo_s Nunchuck.png",
    "tm012": "Michelangelo Deck/15 Michelangelo_s Other Nunchuck FLIPPED.png",
    "tm013": "Mikelangelo Bad Stuff/Michelangelo Obligation.png",
    "tm014": "Mikelangelo Bad Stuff/1 Sewer Problems.png",
    "tm015": "Mikelangelo Bad Stuff/2 Wyrm.png",
    "tm016": "Mikelangelo Bad Stuff/3 Smash.png",
}
ROTATION = {"tm014": -90}  # degres PIL (negatif = sens horaire)
# « Michelangelo Insert.png » (regles du Nunchuck et de la manigance) n'est PAS
# une carte : pas de card_id, pas d'image.


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.abspath(sys.argv[1])
    manquants = []
    os.makedirs(DST, exist_ok=True)
    for card_id, nom in MAP.items():
        chemin = os.path.join(src, nom)
        if not os.path.isfile(chemin):
            manquants.append(nom)
            continue
        im = Image.open(chemin).convert("RGB")
        if card_id in ROTATION:
            im = im.rotate(ROTATION[card_id], expand=True)
        w, h = im.size
        petit = min(w, h)
        if petit > PETIT_COTE:
            echelle = PETIT_COTE / petit
            im = im.resize((round(w * echelle), round(h * echelle)), Image.LANCZOS)
        im.save(os.path.join(DST, card_id + ".jpg"), "JPEG", quality=QUALITE)
    if manquants:
        print("MANQUANTS :")
        for nom in manquants:
            print("  ", nom)
        return 1
    print(len(MAP), "images ecrites dans", DST)
    return 0


if __name__ == "__main__":
    sys.exit(main())
