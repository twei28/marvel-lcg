# -*- coding: utf-8 -*-
"""Recette des images du pack IRON PATRIOT : assets/pics/ est gitignore, donc
cette recette est la seule chose reproductible. Source : zip fan-made
'Iron Patriot-20260829T085900Z-1-001.zip' (Neptune), extrait par
`python3 -m zipfile -e`.

⚠ LE ZIP S'APPELAIT « OneDrive_2026-08-29.zip » a son arrivee. Renomme le
05/09/2026 quand son vrai contenu a ete identifie (voir le plan fan-made).

⚠ LES SOURCES SONT DES PNG. On les copie TELLES QUELLES, comme les packs
cameo_compliment et venomized : le moteur sert les trois extensions et
reencoder en JPG ferait perdre de la qualite pour rien.

⚠⚠ LE PACK NUMEROTE CHAQUE EXEMPLAIRE PHYSIQUE, PAS CHAQUE CARTE. « Deceptive
Guard (9/16) » et « (10/16) » sont LA MEME CARTE en deux exemplaires. Mesure du
09/09/2026, par difference de pixels : les fichiers homonymes ne different que
sur la bande y 2015..2063, soit 1,8 % de la hauteur — exactement le bandeau du
numero. Les md5 different, et ne prouvent donc RIEN.
Sont dans ce cas : 09/10, 11/12, 13/14, R01-R03, R04-R06, R07-R09, N04/N05 et
MM04-MM06. 53 fichiers de cartes -> 37 cartes distinctes.

⚠⚠ EXCEPTION, ET C'EST L'INVERSE : « (06) H.A.M.M.E.R. Helicarrier.png » et
« (6) H.A.M.M.E.R. Helicarrier.png » portent le MEME numero imprime (6/16) et
different sur 96 % de l'image. Ce sont DEUX VERSIONS du texte :
  (06) « **Action**   : Exhaust this card and spend 1 resource... »
  (6)  « **Response** : Exhaust this card and spend 1 resource... »
On retient (06), la version ACTION, pour deux raisons : le fichier suit la
numerotation zero-padee de tout le dossier, et surtout un « Response » sans
clause « After... » n'est pas une Reponse valide dans les regles du jeu. (6)
est un brouillon laisse dans le zip.

⚠ « Seige » (16/16) est la COQUILLE IMPRIMEE de l'auteur pour « Siege ». Le nom
de la carte la garde, c'est ce qui est imprime.

⚠ Les deux fichiers a la racine du Hero Pack — « (00PAE) Norman Osborn.png » et
« (00PH) Iron Patriot.png » — sont les visuels de la BOITE, pas des cartes :
memes personnages, sans cadre de jeu. Non importes.

Usage : python3.10 tools/importer_images_iron_patriot.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

HERO = os.path.join("Hero Pack", "Hero Set")
NEM = os.path.join("Hero Pack", "Nemesis Set")
MM = os.path.join("Hero Pack", "Molecule Man Encounter Set")

MAP = {
    # --- identite ---------------------------------------------------------
    "ip001a": os.path.join(HERO, "(00H) Iron Patriot.png"),
    "ip001b": os.path.join(HERO, "(00AE) Norman Osborn.png"),
    # --- set heros, 16 cartes physiques pour 13 titres --------------------
    "ip002a": os.path.join(HERO, "(01) Registration Act.png"),
    "ip002b": os.path.join(HERO, "(01) Dark Reign.png"),
    "ip003":  os.path.join(HERO, "(02) Absolute Power.png"),
    "ip004":  os.path.join(HERO, "(03) Corrupt Absolutely.png"),
    "ip005":  os.path.join(HERO, "(04) Sentry.png"),
    "ip006":  os.path.join(HERO, "(05) Victoria Hand.png"),
    "ip007":  os.path.join(HERO, "(06) H.A.M.M.E.R. Helicarrier.png"),
    "ip008":  os.path.join(HERO, "(07) Director of Security.png"),
    "ip009":  os.path.join(HERO, "(08) Total Authority.png"),
    "ip010":  os.path.join(HERO, "(09) Deceptive Guard.png"),
    "ip011":  os.path.join(HERO, "(11) Foreboding Influence.png"),
    "ip012":  os.path.join(HERO, "(13) Repulsor Bombard.png"),
    "ip013":  os.path.join(HERO, "(15) Call to Arms.png"),
    "ip014":  os.path.join(HERO, "(16) Seige.png"),
    "ip015":  os.path.join(HERO, "(Obl) Exposed Insanity.png"),
    # --- set nemesis ------------------------------------------------------
    "ip016":  os.path.join(NEM, "(N01) Doctor Doom.png"),
    "ip017":  os.path.join(NEM, "(N02) Reign's End.png"),
    "ip018":  os.path.join(NEM, "(N03) Cabal Obligations.png"),
    "ip019":  os.path.join(NEM, "(N04) Assembled Resistance.png"),
    # --- deck REGISTERED, 20 cartes physiques pour 14 titres --------------
    "ip020":  os.path.join(HERO, "(R01) H.A.M.M.E.R. Agents.png"),
    "ip021":  os.path.join(HERO, "(R04) H.A.M.M.E.R. Commandos.png"),
    "ip022":  os.path.join(HERO, "(R07) H.A.M.M.E.R. Operatives.png"),
    "ip023":  os.path.join(HERO, "(R10) Bullseye.png"),
    "ip024":  os.path.join(HERO, "(R11) Daken.png"),
    "ip025":  os.path.join(HERO, "(R12) Ghost.png"),
    "ip026":  os.path.join(HERO, "(R13) Madame Masque.png"),
    "ip027":  os.path.join(HERO, "(R14) Moonstone.png"),
    "ip028":  os.path.join(HERO, "(R15) Taskmaster.png"),
    "ip029":  os.path.join(HERO, "(R16) Venom.png"),
    "ip030":  os.path.join(HERO, "(R17) Ares.png"),
    "ip031":  os.path.join(HERO, "(R18) Loki.png"),
    "ip032":  os.path.join(HERO, "(R19) Penance.png"),
    "ip033":  os.path.join(HERO, "(R20) The Hood.png"),
    # --- set modulaire Molecule Man ---------------------------------------
    "ip034":  os.path.join(MM, "(MM01) Molecule Man.png"),
    "ip035":  os.path.join(MM, "(MM02) You're in My World.png"),
    "ip036":  os.path.join(MM, "(MM03) Master of Molecules.png"),
    "ip037":  os.path.join(MM, "(MM04) Manipulate Realities.png"),
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    src = os.path.join(os.path.abspath(sys.argv[1]), "Iron Patriot")
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
