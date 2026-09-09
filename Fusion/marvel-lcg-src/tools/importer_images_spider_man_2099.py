#!/usr/bin/env python3
"""Copie 18 des 25 scans du zip « Spider-Man 2099 » (Rainy) vers
assets/pics/<card_id>.jpg.

Usage : python3 tools/importer_images_spider_man_2099.py <dossier extrait>/"Spider-Man 2099"

Les doublons IMPRIMES partagent un card_id : on ne copie que le premier scan.
Accelerated Decoy (2 et 3), Rapid Strikes (4 et 5), Shock and Awe (6 et 7),
Wall Crawling (8 et 9), Power Surge (3 et 4 du set nemesis).

⚠ « 0.2 Spider-Man 2099.jpg » est la face HEROS et « 0.1 Miguel O_Hara.jpg »
l'ALTER-EGO, comme pour Ares et Blade : verifie sur le libelle imprime
(« HERO » / « ALTER-EGO »), pas sur le numero de fichier.

⚠ Le zip contient aussi « Alternate Art/14 Spinnerets (alt art).jpg ». Ce n'est
PAS une carte de plus : c'est un art alternatif de sm011, et le depot ne cree
jamais un second card_id pour un art alternatif (PROCESSUS-HEROS etape 10 :
`metadata.hero_alts` pour une IDENTITE, rien du tout pour une carte ordinaire).
Il n'est donc pas importe.
"""
import os
import shutil
import sys

NEMESIS = "Nemesis & obligation"

MAP = {
    "sm001a": "0.2 Spider-Man 2099.jpg",
    "sm001b": "0.1 Miguel O_Hara.jpg",
    "sm002": "1 Ghost Rider.jpg",
    "sm003": "2 Accelerated Decoy.jpg",
    "sm004": "4 Rapid Strikes.jpg",
    "sm005": "6 Shock and Awe.jpg",
    "sm006": "8 Wall Crawling.jpg",
    "sm007": "10 Lyla.jpg",
    "sm008": "11 Accelerated Vision.jpg",
    "sm009": "12 Fangs and Talons.jpg",
    "sm010": "13 Hyper-Agility.jpg",
    "sm011": "14 Spinnerets.jpg",
    "sm012": "15 Web Cape.jpg",
    "sm013": os.path.join(NEMESIS, "Future in Crisis obligation.jpg"),
    "sm014": os.path.join(NEMESIS, "1 Containment Breach.jpg"),
    "sm015": os.path.join(NEMESIS, "2 Electro.jpg"),
    "sm016": os.path.join(NEMESIS, "3 Power Surge.jpg"),
    "sm017": os.path.join(NEMESIS, "5 Charged.jpg"),
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
