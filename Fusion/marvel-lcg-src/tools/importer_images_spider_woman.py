# -*- coding: utf-8 -*-
"""Recette des images du pack SPIDER-WOMAN (Kajislav) : assets/pics/ est
gitignore, donc cette recette est la seule chose reproductible. Source : zip
fan-made 'Spider-Woman (Released)-20260902T070156Z-1-001.zip', extrait par
`python3 -m zipfile -e`.

⚠⚠ LE PACK NE S'APPELLE PAS `spider_woman` : ce nom est celui de la
Spider-Woman OFFICIELLE, Jessica Drew (`04031a`, pack `trors`), dont le deck de
depart existe deja. On suit le precedent `hulk_rainy` (Hulk officiel vs Hulk de
Rainy) : pack, deck et `set_name` portent le nom de l'auteur.

⚠ LES SOURCES SONT DES PNG. On les copie TELLES QUELLES, comme les packs
cameo_compliment, venomized et iron_patriot : le moteur sert les trois
extensions et reencoder en JPG ferait perdre de la qualite pour rien.

⚠⚠ LE PACK NUMEROTE CHAQUE EXEMPLAIRE PHYSIQUE, PAS CHAQUE CARTE. Six paires
ne different que sur le bandeau du numero — mesure du 10/09/2026 par difference
de pixels : 1,9 % a 3,0 % des lignes, TOUTES entre y 2008 et y 2064, soit
exactement la hauteur du bandeau. Les md5 different, et ne prouvent donc RIEN.
Sont dans ce cas : 04/05, 06/07, 08/09, 10/11, 13/14 et 45/46.
36 fichiers de cartes -> 29 cartes distinctes.

⚠⚠ LES NOMS DE FICHIERS NE SONT PAS LES NOMS DES CARTES :
  `01 Cassandra Webb`        -> ** Madame Web ** (Cassandra Webb n'est que son
                                 sous-titre)
  `45/46 interruption nemesis` -> ** Violent Disturbance **
  `03 madame web_s powers`   -> l'apostrophe de « Madame Web's Powers » est
                                 devenue un `_` a l'export.

⚠ LES NUMEROS D'`Aspect Cards` SAUTENT (16-19, 23, 25, 35, 40). Ce ne sont PAS
des cartes manquantes : la decklist de l'auteur montre que les trous
correspondent a des cartes OFFICIELLES qu'il n'avait pas a dessiner (Desperate
Defence, Armored Vest, Unflappable, Avengers Mansion...). Les 8 fichiers
presents SONT ses 8 cartes custom.

⚠⚠ LE ZIP LIVRE DEUX SETS NEMESIS ALTERNATIFS, tous deux numerotes 1/5 a 5/5,
aux bordures differentes :
  A « Man-Bull » (42-46), dont l'OBLIGATION est `41 Separation from the Child`,
    rangee avec le set HEROS — son bandeau dit « SPIDER-WOMAN », pas
    « SPIDER-WOMAN NEMESIS » ;
  B « verze 2 » (47-51, Ms. Marvel), qui a SA PROPRE obligation.
Les deux sont portes. A monte le deck de depart, B est livre en set de
rencontre modulaire (`data/encounter_sets/spider_woman_kajislav_ms_marvel.json`),
le moteur n'acceptant qu'un set nemesis par heros.

⚠ Deux coquilles imprimees de l'auteur, gardees telles quelles dans le NOM des
cartes : « Arachnne Costume » (deux n) et « Misdiiirection » (trois i). Sa
propre decklist ecrit pourtant « Misdirection ».

⚠ Les fichiers d'`extras/` — couverture, image de sortie, compteur de PV et les
trois faces de decklist — sont des visuels de BOITE, pas des cartes. Non
importes. La decklist `52` a servi a ecrire `deck/starter/spider_woman_kajislav.json`.

Usage : python3.10 tools/importer_images_spider_woman.py <dossier extrait>
"""
import os
import shutil
import sys

DST = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "assets", "pics",
)

RACINE = "Spider-Woman (Released)"
HERO = os.path.join(RACINE, "Hero cards")
ASPECT = os.path.join(RACINE, "Aspect Cards")
ENC = os.path.join(RACINE, "Encounter cards")

MAP = {
    # --- identite ---------------------------------------------------------
    "sw001a": os.path.join(RACINE, "000 spider-woman.png"),
    "sw001b": os.path.join(RACINE, "00 julia carpenter.png"),
    # --- set heros, 15 cartes physiques pour 10 titres ---------------------
    "sw002": os.path.join(HERO, "01 Cassandra Webb.png"),      # * Madame Web
    "sw003": os.path.join(HERO, "02 rachel carpenter.png"),
    "sw004": os.path.join(HERO, "03 madame web_s powers.png"),
    "sw005": os.path.join(HERO, "04 swing and kick.png"),
    "sw006": os.path.join(HERO, "06 psi-web trap.png"),
    "sw007": os.path.join(HERO, "08 psionic web blast.png"),
    "sw008": os.path.join(HERO, "10 swinging rescue.png"),
    "sw009": os.path.join(HERO, "12 web formation.png"),
    "sw010": os.path.join(HERO, "13 hold im tight.png"),
    "sw011": os.path.join(HERO, "15 arachne costume.png"),     # * Arachnne Costume
    # --- aspect PROTECTION et basiques ------------------------------------
    "sw012": os.path.join(ASPECT, "16 century.png"),
    "sw013": os.path.join(ASPECT, "17 shroud.png"),
    "sw014": os.path.join(ASPECT, "18 us agent.png"),
    "sw015": os.path.join(ASPECT, "19 blinded sight.png"),
    "sw016": os.path.join(ASPECT, "23 misdirect an enemy.png"),  # Misdiiirection
    "sw017": os.path.join(ASPECT, "25 tactical retreat.png"),
    "sw018": os.path.join(ASPECT, "35 battleworld.png"),
    "sw019": os.path.join(ASPECT, "40 past and future.png"),
    # --- obligation, partagee avec le set nemesis A ------------------------
    "sw020": os.path.join(ENC, "41 separation from the child.png"),
    # --- set nemesis A « Man-Bull » ----------------------------------------
    "sw021": os.path.join(ENC, "42 man-bull nemesis.png"),
    "sw022": os.path.join(ENC, "43 vault breakout nemesis.png"),
    "sw023": os.path.join(ENC, "44 bad inspiration nemesis.png"),
    "sw024": os.path.join(ENC, "45 interruption nemesis.png"),   # Violent Disturbance
    # --- set nemesis B « verze 2 » -----------------------------------------
    "sw025": os.path.join(ENC, "47 ms. marvel nemesis.png"),
    "sw026": os.path.join(ENC, "48 superhuman registration act nemesis verze 2.png"),
    "sw027": os.path.join(ENC, "49 fugitive nemesis verze 2.png"),
    "sw028": os.path.join(ENC, "51 fighting a friend nemesis verze 2.png"),
}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    source = os.path.abspath(sys.argv[1])
    os.makedirs(DST, exist_ok=True)
    copiees, manquantes = 0, []
    for card_id, relatif in sorted(MAP.items()):
        src = os.path.join(source, relatif)
        if not os.path.exists(src):
            manquantes.append(relatif)
            continue
        shutil.copy2(src, os.path.join(DST, card_id + ".png"))
        copiees += 1
    print(f"{copiees} images copiees dans {DST}")
    for m in manquantes:
        print("  MANQUE :", m)
    return 1 if manquantes else 0


if __name__ == "__main__":
    sys.exit(main())
