# -*- coding: utf-8 -*-
"""Recette des images du pack JENNIKA (TMNT Heroes v3, Inkwire) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible.

Source : zip fan-made « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Jennika v3/ » (25 PNG 1500x2150, ou 2150x1500 pour le complot).

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage.

⚠ DOUBLONS : sept fichiers du zip sont des COPIES (ecart moyen < 0,05/255 : seul
le numero imprime « n/16 » ou « n/5 » change). Un seul card_id chacune, on prend
le premier :
  1-3   Composure         -> tj002
  4-5   Apparition        -> tj003
  6-7   Decisive Strike   -> tj004
  8-9   Moonlighting      -> tj005
  10-11 Fearless Resolve  -> tj006
  3-5   Street Phantoms   -> tj015  (dossier Bad Stuff)

⚠ « Sosaiken Cardback.png » (dos de la Voie : regles de construction de deck,
« Advanced Path ») n'est PAS une carte jouable : pas de card_id, pas d'image dans
assets/pics (insert de regles, decision utilisateur du 15/10/2026 : ne rien creer).

Usage : python3 tools/importer_images_jennika.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Heroes/Jennika v3/ ».
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
    "tj001a": "0 Jennika.png",
    "tj001b": "0 Jenny A-E.png",
    # signature
    "tj002": "Jennika Deck/1 Composure.png",
    "tj003": "Jennika Deck/4 Apparition.png",
    "tj004": "Jennika Deck/6 Decisive Strike.png",
    "tj005": "Jennika Deck/8 Moonlighting.png",
    "tj006": "Jennika Deck/10 Fearless Resolve.png",
    "tj007": "Jennika Deck/12 Jenny_s Crib.png",
    "tj008": "Jennika Deck/13 Jennika_s Bow.png",
    "tj009": "Jennika Deck/14 Jennika_s Tekko-Kagi.png",
    "tj010": "Jennika Deck/15 Jennika_s Other Tekko-Kagi flipped.png",
    # la Voie (carte permanente mise de cote)
    "tj011": "Sosaiken.png",
    # obligation : bandeau « JENNIKA », donc set du heros
    "tj012": "Jennika Bad Stuff/Jennika Obligation.png",
    # set nemesis
    "tj013": "Jennika Bad Stuff/1 Jennika Nemesis.png",
    "tj014": "Jennika Bad Stuff/2 Phantasm.png",
    "tj015": "Jennika Bad Stuff/3 Street Phantoms.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Heroes", "Jennika v3")
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
