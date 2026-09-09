#!/usr/bin/env python3
"""Copie 21 des 28 scans du zip « Superior Spider-Man » (Rainy) vers
assets/pics/<card_id>.jpg.

Usage : python3 tools/importer_images_superior_spider_man.py <dossier extrait>/"Superior Spider-Man"

Les doublons IMPRIMES partagent un card_id : Agility (2 et 3), Brutal
Efficiency (4 a 6), Webbed Up (7 et 8), Spider-Bot (13 et 14).

⚠ CE PACK A DEUX ALTER-EGOS, donc TROIS faces d'identite : su001a la face
heros, su001b Peter Parker et su001c Elliot Tolliver. Le zip nomme les DEUX
alter-egos « 0.1 » — c'est le libelle imprime (ALTER-EGO / HERO) qui tranche,
jamais le numero de fichier.

⚠ « 1 Spiderlings (alt art).jpg » n'est PAS une carte de plus : art alternatif
de su002, non importe (PROCESSUS-HEROS etape 10).
"""
import os
import shutil
import sys

NEM = "Nemesis & Obligation"

MAP = {
    "su001a": "0.2 Spider-Man.jpg",
    "su001b": "0.1 Peter Parker.jpg",
    "su001c": "0.1 Elliot Tolliver.jpg",
    "su002": "1 Spiderlings.jpg",
    "su003": "2 Agility.jpg",
    "su004": "4 Brutal Efficiency.jpg",
    "su005": "7 Webbed Up.jpg",
    "su006": "9 Anna Maria Marconi.jpg",
    "su007": "10 Facial Recognition Uplink.jpg",
    "su008": "11 Mastermind.jpg",
    "su009": "12 Mechanical Arms.jpg",
    "su010": "13 Spider-Bot.jpg",
    "su011": "15 Web-Shooters.jpg",
    "su012": "16 Contingency Plan.jpg",
    "su013": os.path.join(NEM, "Ghost of a Conscience.jpg"),
    "su014": os.path.join(NEM, "Crisis of Conscience.jpg"),
    "su015": os.path.join(NEM, "1 Goblin Protocol.jpg"),
    "su016": os.path.join(NEM, "2 Hobgoblin.jpg"),
    "su017": os.path.join(NEM, "3 Lunatic Laugh.jpg"),
    "su018": os.path.join(NEM, "4 Goblin Glider.jpg"),
    "su019": os.path.join(NEM, "5 Pumpkin Bombs.jpg"),
}


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    source = sys.argv[1]
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cible = os.path.join(racine, "assets", "pics")
    for card_id, nom in MAP.items():
        chemin = os.path.join(source, nom)
        if not os.path.exists(chemin):
            sys.exit(f"manquant : {chemin}")
        shutil.copyfile(chemin, os.path.join(cible, card_id + ".jpg"))
        print(f"{card_id} <- {nom}")
    print(f"{len(MAP)} images copiees dans {cible}")


if __name__ == "__main__":
    main()
