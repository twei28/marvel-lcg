# -*- coding: utf-8 -*-
"""Recette des images du pack RAPHAEL (TMNT Heroes, Inkwire) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible.

Source : zip fan-made « TMNT Heroes-20261014T200300Z-1-001.zip », dossier
« TMNT Heroes/Raphael v3/ » (24 PNG 1500x2150, ou 2150x1500 pour le complot).

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage. Le script fait lui-meme la reduction,
parce que `uniformiser-scans.py` a ses chemins en dur sous /mnt/c/... et ne
sait travailler que sur assets/pics en place ; l'original 1500x2150 n'est donc
PAS copie dans assets/pics (rien a sauvegarder cote depot, il reste dans le zip).

⚠ DOUBLONS : cinq fichiers du zip sont des COPIES (comparees a l'image, ecart
moyen < 0,05/255 ; seule « 10 Seething Rage » differe un peu, par le numero
imprime « 9/15 » / « 10/15 »). Un seul card_id chacune, on prend le premier :
  2-3   Disarm           -> tr003
  4-5   Headbutt         -> tr004
  7-8   Unbridled Fury   -> tr006
  9-10  Seething Rage    -> tr007
  3-4   Insurrection     -> tr016  (dossier Bad Stuff)

⚠ L'ENCART « Raphael Insert.png » (regles des Sai) n'est PAS une carte : pas de
card_id, pas d'image dans assets/pics. Il est resume dans le bloc
`insert_note` du deck de depart et dans .planning/tmnt/raphael-phase-a.md.

Usage : python3 tools/importer_images_raphael.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Heroes/Raphael v3/ ».
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
    "tr001a": "0 Raphael Hero.png",
    "tr001b": "0 Raph alter-ego.png",
    # signature
    "tr002": "Raphael Deck/1 Casey Jones.png",
    "tr003": "Raphael Deck/2 Disarm.png",
    "tr004": "Raphael Deck/4 Headbutt.png",
    "tr005": "Raphael Deck/6 Savage Assault.png",
    "tr006": "Raphael Deck/7 Unbridled Fury.png",
    "tr007": "Raphael Deck/9 Seething Rage.png",
    "tr008": "Raphael Deck/11 Shell Cycle.png",
    "tr009": "Raphael Deck/12 Raph_s Punching Bag.png",
    "tr010": "Raphael Deck/13 Gekido.png",
    "tr011": "Raphael Deck/14 Raphael_s Sai.png",
    "tr012": "Raphael Deck/15 Raphael_s Other Sai Flipped.png",
    # obligation : bandeau « RAPHAEL », donc set du heros
    "tr013": "Raphael Bad Stuff/Raphael Obligation.png",
    # set nemesis
    "tr014": "Raphael Bad Stuff/1 Mutagen Bomb.png",
    "tr015": "Raphael Bad Stuff/2 Old Hob.png",
    "tr016": "Raphael Bad Stuff/3 Insurrection.png",
    "tr017": "Raphael Bad Stuff/5 Prepare to Rally.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Heroes", "Raphael v3")
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
