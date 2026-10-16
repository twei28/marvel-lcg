# -*- coding: utf-8 -*-
"""Recette des images du pack ALOPEX (TMNT Heroes, Inkwire) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible.

Source : zip fan-made « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Alopex v3/ » (24 PNG 1500x2150, ou 2150x1500 pour le complot).

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage (voir importer_images_raphael.py).

⚠ DOUBLONS : onze fichiers du zip sont des COPIES (comparees a l'image : seul le
numero de collection imprime change, ecart moyen < 0,05/255). Un seul card_id
chacune, on prend le premier :
  2-3-4  Bold Strategy      -> ta003
  5-6    Pounce             -> ta004
  7-8-9  Prowl              -> ta005
  10-11  Sniff Out Trouble  -> ta006
  Treachery 1-2-3 (Curse of Nine Tales, 3/5 4/5 5/5) -> ta015

⚠ PAIRE 14/15 (ta009 Alopex's Kama / ta010 Alopex's Other Kama) : l'illustration
est CONTINUE d'une carte a l'autre (la lame traverse les deux). Rien n'est
declare ici : voir .planning/tmnt/alopex-questions.md et la memoire
`tmnt-cartes-jumelles-panorama`.

Usage : python3 tools/importer_images_alopex.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Heroes/Alopex v3/ ».
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
    "ta001a": "0 Alopex Hero.png",
    "ta001b": "0 Alopex AE.png",
    # signature
    "ta002": "Alopex Deck/1 Nobody.png",
    "ta003": "Alopex Deck/2 Bold Strategy.png",
    "ta004": "Alopex Deck/5 Pounce.png",
    "ta005": "Alopex Deck/7 Prowl.png",
    "ta006": "Alopex Deck/10 Sniff Out Trouble.png",
    "ta007": "Alopex Deck/12 Mutant Shelter.png",
    "ta008": "Alopex Deck/13 Kitsune Kabuki.png",
    "ta009": "Alopex Deck/14 Alopex_s Kama.png",
    "ta010": "Alopex Deck/15 Alopex_s Other Kama flipped.png",
    "ta011": "16 Prey.png",
    # obligation : bandeau « ALOPEX », donc set du heros
    "ta012": "Alopex Bad Stuff/Alopex obligation.png",
    # set nemesis
    "ta013": "Alopex Bad Stuff/Kitsune Side Scheme.png",
    "ta014": "Alopex Bad Stuff/Alopex Kitsune.png",
    "ta015": "Alopex Bad Stuff/Alopex Treachery 1.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Heroes", "Alopex v3")
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
