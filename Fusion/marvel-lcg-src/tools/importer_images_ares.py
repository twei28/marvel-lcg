# -*- coding: utf-8 -*-
"""Recette des images du pack ARES : assets/pics/ est gitignore, donc cette
recette est la seule chose reproductible. Source : zip fan-made
'Ares-20260902T073810Z-1-001.zip' (Rainy), dossier « A creer », extrait par
`python3 -m zipfile -e`.

⚠ LES DEUX FACES SONT NUMEROTEES « 0.1 » ET « 0.2 » MAIS PORTENT LE MEME NOM
« Ares ». Ce n'est pas le numero qui tranche mais le LIBELLE IMPRIME :
« 0.1 Ares.jpg » porte ALTER-EGO (REC 4, main 5), « 0.2 Ares.jpg » porte HERO
(THW 1 / ATK 3 / DEF 2, main 4). Verifie sur les cartes, pas sur les noms.
Donc 0.2 -> ar001a (heros) et 0.1 -> ar001b (alter-ego), a l'INVERSE de
l'ordre des fichiers.

⚠ CINQ CARTES SONT LIVREES EN PLUSIEURS EXEMPLAIRES et n'ont donc qu'UN
card_id. On prend le premier de chaque serie :
  1-2        Spray and Pray  -> ar002
  3-4-5      To Battle!      -> ar003
  8-9-10     Feint           -> ar006
  12-13      Reeling         -> ar008
  14-15      Sundered        -> ar009
  nemesis 4-5 Lead the Charge -> ar014

Usage : python3 tools/importer_images_ares.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

MAP = {
    # identite : 0.2 est le HEROS, 0.1 l'ALTER-EGO, voir l'en-tete
    "ar001a": "0.2 Ares.jpg",
    "ar001b": "0.1 Ares.jpg",
    # signature
    "ar002": "1 Spray and Pray.jpg",
    "ar003": "3 To Battle.jpg",
    "ar004": "6 Ares_ Axe.jpg",
    "ar005": "7 Ares_ Battle Helm.jpg",
    "ar006": "8 Feint.jpg",
    "ar007": "11 God of War.jpg",
    "ar008": "12 Reeling.jpg",
    "ar009": "14 Sundered.jpg",
    # obligation : bandeau « ARES », donc set du heros
    "ar010": "Nemesis & obligation/Ire of Athena obligation.jpg",
    # set nemesis
    "ar011": "Nemesis & obligation/1 Athena_s Guidance.jpg",
    "ar012": "Nemesis & obligation/2 Athena.jpg",
    "ar013": "Nemesis & obligation/3 Aegis Breastplate.jpg",
    "ar014": "Nemesis & obligation/4 Lead The Charge.jpg",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Ares")
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
