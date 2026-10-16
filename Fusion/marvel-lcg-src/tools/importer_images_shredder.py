# -*- coding: utf-8 -*-
"""Recette des images des packs SHREDDER (`ts`) et TMNT STANDARD-EXPERT (`te`)
(TMNT Enemies, Inkwire) : assets/pics/ est gitignore, donc cette recette est la
seule chose reproductible. Meme reduction que importer_images_raphael.py
(petit cote a 615 px, LANCZOS, JPEG qualite 88 optimise).

Source : zip « TMNT Enemies-20261014T200338Z-1-001.zip », dossiers
« TMNT Enemies /Shredder v3/ », « TMNT Enemies /TMNT Standard-Expert (Status Card
Standard-Expert)/ » et « TMNT Enemies /Normal Standard-Expert Reskins/ »
(PNG 1500x2150, ou 2150x1500 pour les complots et les manigances annexes).

DOUBLONS (comparaison pixel a pixel : seul le numero de collection imprime
differe, zone de ~20x45 px du coin bas) : un seul card_id par carte, plusieurs
exemplaires dans le set de rencontre :
  8-9 Elite Guard -> ts008 ; 10-11 Foot Ninja -> ts010 ; 13-14 Cloak of Shadows
  -> ts013 ; 15-16 Disarming Assault -> ts015 ; 17-18-19 Shred -> ts017 ;
  20-21 Foot Rikugon -> ts020 ; Chunin 4-5 Doroppuin -> ts104 ;
  Shadow 1-2 Foot Assassin -> ts301 ; 3-4 Foot Soldiers -> ts303 ;
  5-6 Foothold -> ts305 ; TMNT Standard 2-3 Outmatched -> te002 ; 6-7 Skulk -> te006 ;
  reskins S1-S2 Advance -> te021 ; S3-S4 Assault -> te023.

L'ENCART « Shredder Insert.png » n'est PAS une carte (decision phase B) : pas de
card_id, pas d'image dans assets/pics. La carte d'etat « Cloaked.png » existe deja.

Usage : python3 tools/importer_images_shredder.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Enemies /» ; sortie par defaut assets/pics.
"""
import os
import sys

from PIL import Image

DEFAUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "pics")
PETIT_COTE = 615
QUALITE = 88
SH = "Shredder v3/"
SE = "TMNT Standard-Expert (Status Card Standard-Expert)/"
RS = "Normal Standard-Expert Reskins/"

MAP = {
    "ts001": SH + "1 Shredder 1.png", "ts002": SH + "2 Shredder 2.png", "ts003": SH + "3 Shredder 3.png",
    "ts004a": SH + "4 Main Scheme 1A.png", "ts004b": SH + "4 Main Scheme 1B.png",
    "ts005a": SH + "5 Main Scheme 2A.png", "ts005b": SH + "5 Main Scheme 2B.png",
    "ts006": SH + "Shredder Deck/6 Bladed Armor.png", "ts007": SH + "Shredder Deck/7 Kuro Kabuto.png",
    "ts008": SH + "Shredder Deck/8 Elite Guard.png", "ts010": SH + "Shredder Deck/10 Foot Ninja.png",
    "ts012": SH + "Shredder Deck/12 Mongo.png", "ts013": SH + "Shredder Deck/13 Cloak of Shadows.png",
    "ts015": SH + "Shredder Deck/15 Disarming Assault.png", "ts017": SH + "Shredder Deck/17 Shred.png",
    "ts020": SH + "Shredder Deck/20 Foot Rikugon.png", "ts022": SH + "Shredder Deck/22 Throne of the Jonin.png",
    "ts101": SH + "Chunin v3/1 Karai.png", "ts102": SH + "Chunin v3/2 Ocho.png",
    "ts103": SH + "Chunin v3/3 Kira no Ken.png", "ts104": SH + "Chunin v3/4 Doroppuin.png",
    "ts201": SH + "Foot Goon Squad v3/1 Bebop.png", "ts202": SH + "Foot Goon Squad v3/2 Bludgeon.png",
    "ts203": SH + "Foot Goon Squad v3/3 Hun.png", "ts204": SH + "Foot Goon Squad v3/4 Koya.png",
    "ts205": SH + "Foot Goon Squad v3/5 Rocksteady.png", "ts206": SH + "Foot Goon Squad v3/6 Send out the Goons.png",
    "ts301": SH + "Shadow of the Foot v3/1 Foot Assassin.png", "ts303": SH + "Shadow of the Foot v3/3 Foot Soldiers.png",
    "ts305": SH + "Shadow of the Foot v3/5 Foothold.png",
    "te001": SE + "Standard/S1 No Quarter.png", "te002": SE + "Standard/S2 Outmatched.png",
    "te004": SE + "Standard/S4 Pursued by Shadows.png", "te005": SE + "Standard/S5 Shadow of the Past.png",
    "te006": SE + "Standard/S6 Skulk.png",
    "te101": SE + "Expert/E1 Annihilation.png", "te102": SE + "Expert/E2 Haunted by the Past.png",
    "te103": SE + "Expert/E3 Sinister Plan.png",
    "te201": SE + "Optional Intense Version/X1 Intense Combatants.png",
    "te021": RS + "S1 Advance.png", "te023": RS + "S3 Assault.png", "te025": RS + "S5 Caught Off Guard.png",
    "te026": RS + "S6 Gang-Up.png", "te027": RS + "S7 Shadow of the Past.png",
    "te121": RS + "E1 Exhaust.png", "te122": RS + "E2 Masterplan.png", "te123": RS + "E3 Under Fire.png",
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Enemies ")
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
            im = im.convert("RGB")
            if min(largeur, hauteur) > PETIT_COTE:
                f = PETIT_COTE / min(largeur, hauteur)
                im = im.resize((max(1, round(largeur * f)), max(1, round(hauteur * f))), Image.Resampling.LANCZOS)
            im.save(os.path.join(dst, card_id + ".jpg"), "JPEG", quality=QUALITE, optimize=True)
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{len(MAP)} images importees dans {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
