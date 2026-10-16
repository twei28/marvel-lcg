# -*- coding: utf-8 -*-
"""Recette des images du pack CASEY JONES (TMNT Heroes, Inkwire) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible.

Source : zip fan-made « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Casey Jones v3/ » (24 PNG 1500x2150, ou 2150x1500 pour le complot).

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage. Le script fait lui-meme la reduction
(l'original 1500x2150 n'est PAS copie dans assets/pics, il reste dans le zip).

⚠ DOUBLONS : six fichiers du zip sont des COPIES (ecart moyen < 0,04/255 ; seul le
numero imprime « 1/16 » / « 2/16 » ou « 3/5 » / « 4/5 » / « 5/5 » differe). Un
seul card_id chacune, on prend la premiere :
  1-2   Clap Back             -> tc002
  3-4   Cross Block           -> tc003
  5-6   Face-Off              -> tc004
  7-8   Grand Slam            -> tc005
  3-4-5 Purple Dragon Goons   -> tc017  (dossier Bad Stuff)

⚠ NUMEROTATION : « Casey's Mask » porte « 10/16 » comme « Baseball Bat » et aucune
carte ne porte « 11/16 » : coquille de l'auteur, la Mask est la carte 11.

Usage : python3 tools/importer_images_casey_jones.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Heroes/Casey Jones v3/ ».
  Sortie par defaut : <racine moteur>/assets/pics.
"""
import os
import sys

from PIL import Image

DEFAUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)
PETIT_COTE = 615
QUALITE = 88

MAP = {
    # identite
    "tc001a": "0 Casey Jones Hero.png",
    "tc001b": "0 Casey Jones alter-ego.png",
    # signature
    "tc002": "Casey Jones Deck/1 Clap Back.png",
    "tc003": "Casey Jones Deck/3 Cross Block.png",
    "tc004": "Casey Jones Deck/5 Face-Off.png",
    "tc005": "Casey Jones Deck/7 Grand Slam.png",
    "tc006": "Casey Jones Deck/9 Anything Goes.png",
    "tc007": "Casey Jones Deck/10 Baseball Bat.png",
    "tc008": "Casey Jones Deck/10 Casey_s Mask.png",
    "tc009": "Casey Jones Deck/12 Cricket Willow.png",
    "tc010": "Casey Jones Deck/13 Driving Iron.png",
    "tc011": "Casey Jones Deck/14 Hockey Stick.png",
    "tc012": "Casey Jones Deck/15 Persuader.png",
    "tc013": "Casey Jones Deck/16 Casey_s Bag.png",
    # obligation : bandeau « CASEY JONES », donc set du heros
    "tc014": "Casey Jones Bad Stuff/CJ Obligation.png",
    # set nemesis
    "tc015": "Casey Jones Bad Stuff/1 CJ Nemesis.png",
    "tc016": "Casey Jones Bad Stuff/2 CJ Nemesis.png",
    "tc017": "Casey Jones Bad Stuff/3 CJ Nemesis.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Heroes", "Casey Jones v3")
    dst = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else DEFAUT
    if not os.path.isdir(src):
        print(f"dossier introuvable : {src}")
        return 2
    os.makedirs(dst, exist_ok=True)

    manquants = []
    for card_id, nom in MAP.items():
        chemin = os.path.join(src, nom)
        if not os.path.isfile(chemin):
            manquants.append(nom)
            continue
        with Image.open(chemin) as im:
            largeur, hauteur = im.size
            if min(largeur, hauteur) > PETIT_COTE:
                f = PETIT_COTE / min(largeur, hauteur)
                im = im.convert("RGB").resize(
                    (max(1, round(largeur * f)), max(1, round(hauteur * f))),
                    Image.Resampling.LANCZOS)
            else:
                im = im.convert("RGB")
            im.save(os.path.join(dst, card_id + ".jpg"), "JPEG",
                    quality=QUALITE, optimize=True)
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{len(MAP)} images importees dans {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
