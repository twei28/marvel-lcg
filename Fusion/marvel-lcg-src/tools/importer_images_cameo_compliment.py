# -*- coding: utf-8 -*-
"""Recette des images du pack CAMEO COMPLIMENT : assets/pics/ est gitignore,
donc cette recette est la seule chose reproductible. Source : zip fan-made
'Cameo compliment-20260902T070731Z-1-001.zip' (BlueRiver), extrait par
`python3 -m zipfile -e`.

⚠ LES SOURCES SONT DES PNG, pas des JPG — c'est le seul pack livre ainsi a ce
jour. On les copie TELLES QUELLES en `.png` : le moteur sert les trois
extensions (`mime_type.py:7-27`, `web_server.py:299-301`) et 600 images du
depot sont deja des PNG. Reencoder en JPG ferait perdre de la qualite pour
rien.

⚠ CE N'EST PAS UN PACK DE HEROS : trois cartes d'aspect, aucune identite,
aucun set nemesis. Le nom du zip dit exactement ce qu'elles sont — le
COMPLEMENT, pour les trois autres aspects, de la carte officielle `58031`
Cameo (Meneur).

⚠ « New Suit_.png » porte un SOULIGNE la ou la carte imprime un POINT
D'INTERROGATION (« New Suit? ») : le systeme de fichiers ne l'accepte pas sous
Windows. Le nom de la carte, lui, garde son « ? ».

Usage : python3.10 tools/importer_images_cameo_compliment.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

MAP = {
    "cc001": "Lock It Down.png",      # Justice
    "cc002": "New Suit_.png",         # Protection  (voir l'en-tete)
    "cc003": "Ye Be Worthy.png",      # Agressivite
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Cameo compliment")
    if not os.path.isdir(src):
        print(f"dossier introuvable : {src}")
        return 2

    manquants = []
    for card_id, nom in MAP.items():
        chemin = os.path.join(src, nom)
        if not os.path.isfile(chemin):
            manquants.append(nom)
            continue
        shutil.copyfile(chemin, os.path.join(DST, card_id + ".png"))
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{len(MAP)} images importees dans {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
