# -*- coding: utf-8 -*-
"""Recette des images du scenario BAXTER STOCKMAN v3 (TMNT Enemies, Inkwire).

assets/pics/ est gitignore : cette recette est la seule chose reproductible.
Source : zip « TMNT Enemies-20261014T200338Z-1-001.zip », dossier
« TMNT Enemies /Baxter Stockman v3/ » (42 PNG), extrait SEUL dans un repertoire
neuf, JAMAIS dans le depot.

Contenu du dossier (prefixe de card_id `tx`) :
  1-3 Baxter.png                    -> tx001 / tx002 / tx003 (vilain, stades I a III)
  4 Baxter_s Laboratory A / B.png   -> tx004a / tx004b (manigance principale, PAYSAGE)
  Baxter_s Lab Deck/ (5 a 22)       -> tx005 a tx011 (18 exemplaires, 7 cartes distinctes)
  Cyber Swarm v3/ (1 a 6)           -> tx012 a tx014 (set modulaire, 6 exemplaires)
  High Speed v3/ (1 a 5)            -> tx015, tx016 (set modulaire, 5 exemplaires)
  Security Protocol v3/ (1 a 7)     -> tx017, tx018 (set modulaire, 7 exemplaires)
  Dazed (1).png                     -> la CARTE D'ETAT Dazed : assets/textures/dazed.webp
                                       (meme mecanique que cloaked.webp), pas un card_id
  Dazed Rules Insert.png            -> encart de regles : AUCUNE carte, la regle vit dans
                                       src/cards/pack/status/dazed.py

⚠ DOUBLONS : les exemplaires multiples n'ont qu'UN card_id ; on prend le premier de
chaque serie. Une comparaison pixel a pixel (PIL ImageChops, 16/10/2026) a prouve qu'ils ne
different que par le numero « n/22 » (n/6, n/5, n/7) du bandeau :
  8-11 Plague of M.O.U.S.E.R.S. -> tx007      12-14 Radical Ingenuity -> tx008
  15-17 Rapid Replication -> tx009            18-20 Robotics Facility -> tx010
  21-22 Mad Lab -> tx011                      6-7 Swarm Superiority -> tx006
  Cyber 1-3 Flight of Flyborgs -> tx012       Cyber 5-6 Buzz Off -> tx014
  High Speed 1-3 Roadkill Rodneys -> tx015    High Speed 4-5 Wrapped Up -> tx016
  Security 1-4 Auto Defense Bots -> tx017     Security 5-7 Intruder Alert! -> tx018

⚠ MANIGANCES (4A/4B, Robotics Facility, Mad Lab) = PAYSAGE (livrees en 2150x1500).

Mise au format : meme regle que outils/uniformiser-scans.py (petit cote ramene a 615,
qualite JPEG 88, jamais d'agrandissement), comme les recettes des tortues.

Usage : python3 tools/importer_images_baxter_stockman.py <dossier "Baxter Stockman v3">
        [--copie-versionnee <dossier>]   (defaut : .planning/tmnt/pics-baxter a la racine du depot)
"""
import os
import sys

from PIL import Image

RACINE_MOTEUR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(RACINE_MOTEUR, "assets", "pics")
TEXTURES = os.path.join(RACINE_MOTEUR, "assets", "textures")
VERSIONNEE = os.path.join(os.path.dirname(os.path.dirname(RACINE_MOTEUR)), ".planning", "tmnt", "pics-baxter")
PETIT_COTE = 615
QUALITE = 88

MAP = {
    "tx001": "1 Baxter.png",
    "tx002": "2 Baxter.png",
    "tx003": "3 Baxter.png",
    "tx004a": "4 Baxter_s Laboratory A.png",
    "tx004b": "4 Baxter_s Laboratory B.png",
    "tx005": "Baxter_s Lab Deck/5 Baxter Blaster.png",
    "tx006": "Baxter_s Lab Deck/6 Swarm Superiority.png",
    "tx007": "Baxter_s Lab Deck/8 Plague of MOUSERS.png",
    "tx008": "Baxter_s Lab Deck/12 Radical Ingenuity.png",
    "tx009": "Baxter_s Lab Deck/15 Rapid Replication.png",
    "tx010": "Baxter_s Lab Deck/18 Robotics Facility.png",
    "tx011": "Baxter_s Lab Deck/21 Mad Lab.png",
    "tx012": "Cyber Swarm v3/1 Flight of Flyborgs.png",
    "tx013": "Cyber Swarm v3/4 Superfly.png",
    "tx014": "Cyber Swarm v3/5 Buzz Off.png",
    "tx015": "High Speed v3/1 Roadkill Rodneys.png",
    "tx016": "High Speed v3/4 Wrapped Up.png",
    "tx017": "Security Protocol v3/1 Auto Defense Bots.png",
    "tx018": "Security Protocol v3/5 Intruder Alert.png",
}


def reduire(im):
    w, h = im.size
    petit = min(w, h)
    if petit > PETIT_COTE:
        echelle = PETIT_COTE / petit
        im = im.resize((round(w * echelle), round(h * echelle)), Image.LANCZOS)
    return im


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    src = os.path.abspath(args[0])
    versionnee = VERSIONNEE
    if "--copie-versionnee" in sys.argv:
        versionnee = os.path.abspath(sys.argv[sys.argv.index("--copie-versionnee") + 1])
    manquants = []
    os.makedirs(DST, exist_ok=True)
    os.makedirs(versionnee, exist_ok=True)
    for card_id, nom in MAP.items():
        chemin = os.path.join(src, nom)
        if not os.path.isfile(chemin):
            manquants.append(nom)
            continue
        im = reduire(Image.open(chemin).convert("RGB"))
        for dossier in (DST, versionnee):
            im.save(os.path.join(dossier, card_id + ".jpg"), "JPEG", quality=QUALITE)
    # La carte d'etat Dazed : texture, au meme format que cloaked.webp (952 x 614).
    dazed = os.path.join(src, "Dazed (1).png")
    if os.path.isfile(dazed):
        os.makedirs(TEXTURES, exist_ok=True)
        Image.open(dazed).convert("RGB").save(os.path.join(TEXTURES, "dazed.webp"), "WEBP", quality=90)
    else:
        manquants.append("Dazed (1).png")
    if manquants:
        print("MANQUANTS :")
        for nom in manquants:
            print("  ", nom)
        return 1
    print(len(MAP), "images ecrites dans", DST, "et", versionnee, "+ assets/textures/dazed.webp")
    return 0


if __name__ == "__main__":
    sys.exit(main())
