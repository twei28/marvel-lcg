# -*- coding: utf-8 -*-
"""Recette des images du pack SUNFIRE : assets/pics/ est gitignore, donc cette
recette est la seule chose reproductible. Source : zip fan-made
'Sunfire-20260902T073636Z-1-001.zip' (Rainy), extrait par
`python3 -m zipfile -e`.

⚠ LES DEUX FACES PORTENT LE MEME NUMERO « 0.1 » dans le zip, contrairement aux
autres packs de Rainy qui numerotent « 0.1 » et « 0.2 ». Ce n'est donc pas le
numero qui tranche mais le LIBELLE IMPRIME sur la carte : « 0.1 Sunfire.jpg »
porte HERO, « 0.1 Shiro Yoshida.jpg » porte ALTER-EGO. Verifie sur les cartes,
pas sur les noms de fichier.

⚠ QUATRE CARTES SONT LIVREES EN PLUSIEURS EXEMPLAIRES et n'ont donc qu'UN
card_id. On prend le premier de chaque serie :
  1-2      Atomic Fire   -> sf002
  3-4-5    Burning Hands -> sf003
  6-7-8-9  Hot Pursuit   -> sf004
  10-11-12 Solar Blast   -> sf005
  1..6     Burning       -> sf009  (dossier « Setup - Burning »)

⚠ LES SIX « BURNING » SONT UN SEUL card_id, `sf009`. Ce sont les six
exemplaires MIS DE COTE par `sf001b` a la mise en place, pas six cartes
differentes : le bandeau imprime « BURNING (1/6) ... (6/6) » numerote des
copies, pas des variantes.

Usage : python3.10 tools/importer_images_sunfire.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

MAP = {
    # identite : les deux fichiers sont numerotes « 0.1 », voir l'en-tete
    "sf001a": "0.1 Sunfire.jpg",
    "sf001b": "0.1 Shiro Yoshida.jpg",
    # signature
    "sf002": "1 Atomic Fire.jpg",
    "sf003": "3 Burning Hands.jpg",
    "sf004": "6 Hot Pursuit.jpg",
    "sf005": "10 Solar Blast.jpg",
    "sf006": "13 Atomic Samurai.jpg",
    "sf007": "14 Sunfire_s Mask.jpg",
    "sf008": "15 Sunfire_s Suit.jpg",
    # les six exemplaires mis de cote, un seul card_id
    "sf009": "Setup - Burning/1 Burning.jpg",
    # obligation : bandeau « SUNFIRE », donc set du heros
    "sf010": "Nemesis & obligation/obligation Shame.jpg",
    # set nemesis
    "sf011": "Nemesis & obligation/1 Hand Ambush.jpg",
    "sf012": "Nemesis & obligation/2 Silver Samurai.jpg",
    "sf013": "Nemesis & obligation/3 Hand Ninja.jpg",
    "sf014": "Nemesis & obligation/4 Silver Samurai_s Katana.jpg",
    "sf015": "Nemesis & obligation/5 Tachyon Whip.jpg",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Sunfire")
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
