#!/usr/bin/env python3
"""Copie 18 des 26 scans du zip « Blade » (Rainy) vers assets/pics/<card_id>.jpg.

Usage : python3 tools/importer_images_blade.py <dossier extrait>/Blade

Les doublons imprimes (Gear Up 1 et 2, Go for the Heart 3 a 5, On the Hunt
6 et 7, Vampire Bite 8 et 9, Vampiric Reflexes 10 et 11, Vampire 3 et 4,
Embraced 6 et 7) partagent un card_id : on ne copie que le premier scan.
⚠ « 0.2 Blade.jpg » est la face HEROS et « 0.1 Eric Brooks.jpg » l'ALTER-EGO,
comme pour Ares : verifie sur le libelle imprime, pas sur le numero.
"""
import os
import shutil
import sys

MAP = {
    "bl001a": "0.2 Blade.jpg",
    "bl001b": "0.1 Eric Brooks.jpg",
    "bl002": "1 Gear Up.jpg",
    "bl003": "3 Go for the Heart.jpg",
    "bl004": "6 On the Hunt.jpg",
    "bl005": "8 Vampire Bite.jpg",
    "bl006": "10 Vampiric Reflexes.jpg",
    "bl007": "12 Bandolier of Stakes.jpg",
    "bl008": "13 Blade_s Sword.jpg",
    "bl009": "14 Daywalker.jpg",
    "bl010": "15 Predatory Instincts.jpg",
    "bl011": os.path.join("Nemesis & obligation", "Blade obligation.jpg"),
    "bl012": os.path.join("Nemesis & obligation", "1 Blood Hunt.jpg"),
    "bl013": os.path.join("Nemesis & obligation", "2 Dracula.jpg"),
    "bl014": os.path.join("Nemesis & obligation", "3 Vampire.jpg"),
    "bl015": os.path.join("Nemesis & obligation", "5 Bandolier of Stakes.jpg"),
    "bl016": os.path.join("Nemesis & obligation", "6 Embraced.jpg"),
    "bl017": os.path.join("Nemesis & obligation", "8 Turned.jpg"),
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
