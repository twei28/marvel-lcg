# -*- coding: utf-8 -*-
"""Recette des images du pack VENUS (TMNT Heroes, Inkwire) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible.

Source : zip fan-made « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Venus v3/ » (21 PNG 1500x2150, ou 2150x1500 pour le complot annexe).

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage. Le script fait lui-meme la reduction,
parce que `uniformiser-scans.py` a ses chemins en dur sous /mnt/c/... ; l'original
1500x2150 n'est donc PAS copie dans assets/pics (il reste dans le zip).

⚠ DOUBLONS : trois paires de fichiers du zip sont des COPIES (seul le numero imprime
« 3/15 » / « 4/15 » differe). Un seul card_id chacune, on prend la premiere :
  3-4   Brain Burn  -> tv004
  7-8   Resistance  -> tv007
  4-5   Salvaged Scales (dossier Bad Stuff) -> tv019

⚠ « 2 Arc Nova » imprime « VENUS (2/16) » : coquille de l'auteur (les 15 scans sont
numerotes 1 a 15) ; sans consequence, un seul card_id.

Usage : python3 tools/importer_images_venus.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Heroes/Venus v3/ ».
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
    "tv001a": "0 Venus Hero.png",
    "tv001b": "0 Venus AE.png",
    # signature
    "tv002": "Venus Deck/1 Bludgeon.png",
    "tv003": "Venus Deck/2 Arc Nova.png",
    "tv004": "Venus Deck/3 Brain Burn.png",
    "tv005": "Venus Deck/5 Eldritch Lance.png",
    "tv006": "Venus Deck/6 Quantanucleic Acid.png",
    "tv007": "Venus Deck/7 Resistance.png",
    "tv008": "Venus Deck/9 Evanescence.png",
    "tv009": "Venus Deck/10 Arcane Emitting Diode.png",
    "tv010": "Venus Deck/11 Cosmic Requiem.png",
    "tv011": "Venus Deck/12 Dragon Scale.png",
    "tv012": "Venus Deck/13 Dream Weaver.png",
    "tv013": "Venus Deck/14 Reanimator Engine.png",
    "tv014": "Venus Deck/15 Turtle Shell.png",
    # obligation : bandeau « VENUS », donc set du heros
    "tv015": "Venus Bad Stuff/Venus Obligation.png",
    # set nemesis
    "tv016": "Venus Bad Stuff/1 Venus Nemesis.png",
    "tv017": "Venus Bad Stuff/2 Venus Nemesis.png",
    "tv018": "Venus Bad Stuff/3 Venus Nemesis.png",
    "tv019": "Venus Bad Stuff/4 Nemesis.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Heroes", "Venus v3")
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
