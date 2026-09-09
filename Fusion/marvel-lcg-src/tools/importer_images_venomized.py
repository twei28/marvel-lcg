# -*- coding: utf-8 -*-
"""Recette des images du pack VENOMIZED : assets/pics/ est gitignore, donc
cette recette est la seule chose reproductible. Source : zip fan-made
'[1] Venomized-20260902T070736Z-1-001.zip' (ekAugust), extrait par
`python3 -m zipfile -e`.

⚠ CE N'EST PAS UN PACK DE HEROS : c'est un SIXIEME ASPECT de deckbuilding
(noir), 35 cartes d'aspect plus 2 cartes du set « Venomized Weakness ».
Aucune identite, aucun set nemesis. Precedent : l'aspect Determination
(`dt`, set 118).

⚠ LES SOURCES SONT DES PNG. On les copie TELLES QUELLES en `.png`, comme le
pack Cameo compliment : le moteur sert les trois extensions
(`mime_type.py`, `web_server.py`) et 600 images du depot sont deja des PNG.
Reencoder en JPG ferait perdre de la qualite pour rien.

⚠ « 9 - Can_t Escape Us.png » porte un SOULIGNE la ou la carte imprime une
APOSTROPHE (« "Can't Escape Us!" ») : le systeme de fichiers ne l'accepte pas
sous Windows. Le nom de la carte, lui, garde son apostrophe.

⚠ LE NUMERO DE FICHIER N'EST PAS LE NUMERO IMPRIME. Le pied de carte affiche
`numero de fichier + 18` (l'auteur numerote a la suite de ses autres packs).
Les `card_id` suivent le NUMERO DE FICHIER, qui est le seul ordre stable.

⚠ MATERIEL INCOMPLET. La decklist de l'auteur cite « Symbiotic Healing
Factor », marquee « custom Aspect card designed by ekAugust ». Elle n'est PAS
dans le zip : 37 fichiers pour 37 cartes, aucune de ce nom. Elle n'a donc ni
card_id ni image, et n'est pas portee.

Usage : python3.10 tools/importer_images_venomized.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

ASPECT = "Aspect Cards"
FAIB = "Weakness Cards"

MAP = {
    "vz001": os.path.join(ASPECT, "1 - Agent Anti-Venom.png"),
    "vz002": os.path.join(ASPECT, "2 - Codex.png"),
    "vz003": os.path.join(ASPECT, "3 - Mania.png"),
    "vz004": os.path.join(ASPECT, "4 - Red Goblin.png"),
    "vz005": os.path.join(ASPECT, "5 - Sleeper.png"),
    "vz006": os.path.join(ASPECT, "6 - Venom.png"),
    "vz007": os.path.join(ASPECT, "7 - Backed into a Corner.png"),
    "vz008": os.path.join(ASPECT, "8 - Black Webbing.png"),
    "vz009": os.path.join(ASPECT, "9 - Can_t Escape Us.png"),
    "vz010": os.path.join(ASPECT, "10 - Dive into Danger.png"),
    "vz011": os.path.join(ASPECT, "11 - Feed the Hunger.png"),
    "vz012": os.path.join(ASPECT, "12 - Forceful Bonding.png"),
    "vz013": os.path.join(ASPECT, "13 - Inner Strength.png"),
    "vz014": os.path.join(ASPECT, "14 - Scared of the Dark.png"),
    "vz015": os.path.join(ASPECT, "15 - Stronger Together.png"),
    "vz016": os.path.join(ASPECT, "16 - Symbiotic Drop Kick.png"),
    "vz017": os.path.join(ASPECT, "17 - Symbiotic For Justice!.png"),
    "vz018": os.path.join(ASPECT, "18 - Symbiotic Go All Out.png"),
    "vz019": os.path.join(ASPECT, "19 - Symbiotic Multitasking.png"),
    "vz020": os.path.join(ASPECT, "20 - Symbiotic Not Today!.png"),
    "vz021": os.path.join(ASPECT, "21 - Symbiotic One by One.png"),
    "vz022": os.path.join(ASPECT, "22 - Symbiotic Perseverance.png"),
    "vz023": os.path.join(ASPECT, "23 - Symbiotic Sneak Attack.png"),
    "vz024": os.path.join(ASPECT, "24 - In the Thick of It.png"),
    "vz025": os.path.join(ASPECT, "25 - Gluttony.png"),
    "vz026": os.path.join(ASPECT, "26 - Symbiote Infusion.png"),
    "vz027": os.path.join(ASPECT, "27 - The Power of the Bond.png"),
    "vz028": os.path.join(ASPECT, "28 - Alchemax.png"),
    "vz029": os.path.join(ASPECT, "29 - Doctor Steven.png"),
    "vz030": os.path.join(ASPECT, "30 - Durable Physiology.png"),
    "vz031": os.path.join(ASPECT, "31 - First Contact.png"),
    "vz032": os.path.join(ASPECT, "32 - Klyntar Tendrils.png"),
    "vz033": os.path.join(ASPECT, "33 - Symbiotic Bond.png"),
    "vz034": os.path.join(ASPECT, "34 - Urban Camouflage.png"),
    "vz035": os.path.join(ASPECT, "35 - You Are What You Eat.png"),
    "vz036": os.path.join(FAIB, "36 - Flash Fire.png"),
    "vz037": os.path.join(FAIB, "37 - Sensory Overload.png"),
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "[1] Venomized")
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
