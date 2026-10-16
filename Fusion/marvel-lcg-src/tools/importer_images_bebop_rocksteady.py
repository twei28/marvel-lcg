# -*- coding: utf-8 -*-
"""Recette des images du scenario BEBOP & ROCKSTEADY (TMNT Villains, Inkwire,
prefixe `tk`) : assets/pics/ est gitignore, donc cette recette est la seule
chose reproductible.

Source : zip fan-made « TMNT Enemies-20261014T200338Z-1-001.zip », dossier
« TMNT Enemies /Bebop & Rocksteady v3/ » (PNG 1500x2150, ou 2150x1500 pour les
manigances et le complot principal). Attention : le dossier racine du zip
s'appelle « TMNT Enemies » AVEC UN ESPACE FINAL ; le script le retrouve par
motif et n'en depend pas.

Les scans sont reduits AU MEME FORMAT que `outils/uniformiser-scans.py` (petit
cote a 615 px, grand cote au prorata, LANCZOS, JPEG qualite 88 optimise) :
615x882 en portrait, 882x615 en paysage.

DOUBLONS : onze fichiers du zip sont des COPIES (compares a l'image, ecart
moyen < 0,05/255 ; seul le numero imprime « 22/28 » / « 23/28 » change). Un
seul card_id chacune, on prend la premiere :
  16-17 Collision Course  -> tk016        18-19 Ole!            -> tk018
  20-21 Toro! Toro!       -> tk020        22-23 Lay the Beatdown -> tk022
  24-25 Pummel            -> tk024        26-27 Trample          -> tk026
  Concrete Jungle 2-3 Road to Ruin -> tk102 ; 4-5 Fallen Empires -> tk104
  Rock the Block  1-2 Hittin' the Town -> tk201 ; 3-4 Jagerbombs -> tk203
En revanche les TROIS « Bumbling Buffoons » (13, 14, 15) ont TROIS illustrations
differentes : trois card_id (tk013, tk014, tk015), meme texte.

L'encart « Bebop and Rocksteady Insert.png » (regles : plusieurs vilains, FAQ,
mot-cle Dodgy) n'est PAS une carte : pas de card_id, pas d'image dans
assets/pics. Il est applique dans les scripts et resume dans
.planning/tmnt/bebop-phase-a.md.

« Shredder v3/Foot Goon Squad v3/1 Bebop.png » (le SBIRE Bebop du scenario
Shredder, prefixe `ts`) n'est PAS importe ici.

Usage : python3 tools/importer_images_bebop_rocksteady.py <dossier extrait> [<dossier de sortie>]
  <dossier extrait> contient « TMNT Enemies /Bebop & Rocksteady v3/ ».
  Sortie par defaut : <racine moteur>/assets/pics.
"""
import glob
import os
import sys

from PIL import Image

DEFAUT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)
PETIT_COTE = 615
QUALITE = 88

SETUP = "Setup & Double Sided Cards/"
RENC = "Bebop & Rocksteady Encounter Deck/"
CJ = "Concrete Jungle v3/"
RB = "Rock the Block v3/"

MAP = {
    # villains : A1/A2 et B1/B2 sont les deux FACES (ALERT / K.O.) d'une meme carte
    "tk001a": SETUP + "1A1 Bebop.png",
    "tk001b": SETUP + "1A2 Bebop.png",
    "tk002a": SETUP + "2B1 Bebop.png",
    "tk002b": SETUP + "2B2 Bebop.png",
    "tk003a": SETUP + "3A1 Rocksteady.png",
    "tk003b": SETUP + "3A2 Rocksteady.png",
    "tk004a": SETUP + "4B1 Rocksteady.png",
    "tk004b": SETUP + "4B2 Rocksteady.png",
    # complot principal (un seul stade)
    "tk005a": SETUP + "5 Main Scheme 1A.png",
    "tk005b": SETUP + "5 Main Scheme 1B.png",
    # cartes recto/verso du set
    "tk006a": SETUP + "6a Destructive Dunderheads.png",
    "tk006b": SETUP + "6b Gone Berserk.png",
    "tk007a": SETUP + "7a Hog Wild.png",
    "tk007b": SETUP + "7b Headfirst.png",
    "tk008a": SETUP + "8a Rhino Rage.png",
    "tk008b": SETUP + "8b Headstrong.png",
    # deck de rencontre
    "tk009": RENC + "9 Shutter Shades.png",
    "tk010": RENC + "10 Aviator Cap.png",
    "tk011": RENC + "11 Roberta.png",
    "tk012": RENC + "12 Juniper.png",
    "tk013": RENC + "13 Bumbling Buffoons.png",
    "tk014": RENC + "14 Bumbling Buffoons.png",
    "tk015": RENC + "15 Bumbling Buffoons.png",
    "tk016": RENC + "16 Collision Course.png",
    "tk018": RENC + "18 Ole.png",
    "tk020": RENC + "20 Toro Toro.png",
    "tk022": RENC + "22 Lay the Beatdown.png",
    "tk024": RENC + "24 Pummel.png",
    "tk026": RENC + "26 Trample.png",
    "tk028": RENC + "28 Anchovy.png",
    # Concrete Jungle (module fixe du scenario)
    "tk101": CJ + "1 Welcome to the Jungle.png",
    "tk102": CJ + "2 Road to Ruin.png",
    "tk104": CJ + "4 Fallen Empires.png",
    "tk106": CJ + "6 Channel 6 News.png",
    "tk107": CJ + "7 Eastman Theater.png",
    "tk108": CJ + "8 Powder Keg.png",
    "tk109": CJ + "9 Power Play.png",
    # Rock the Block (module recommande)
    "tk201": RB + "1 Hittin the Town.png",
    "tk203": RB + "3 Jagerbombs.png",
    "tk205": RB + "5 Get Your Swell On.png",
}


def trouver_racine(extrait: str) -> str:
    candidats = glob.glob(os.path.join(extrait, "TMNT Enemies*", "Bebop & Rocksteady v3"))
    if not candidats:
        raise SystemExit(f"« TMNT Enemies*/Bebop & Rocksteady v3 » introuvable sous {extrait}")
    return candidats[0]


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = trouver_racine(os.path.abspath(sys.argv[1]))
    dst = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else DEFAUT
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
