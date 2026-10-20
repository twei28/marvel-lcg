#!/usr/bin/env python3
"""Branche les « Full Art Reprints » MC/DC 2026 comme arts alternatifs de cartes de deck.

Relancable. Pour chaque ligne de CARTES (carte officielle du jeu -> image de la galerie) :
  1. redimensionne l'image 1500x2150 vers 615x882 (la taille des arts TMNT,
     `assets/pics/<id>_tmnt.jpg`) et l'ecrit dans `assets/pics/<id>_mcdc26.jpg` ;
  2. ajoute le code « mcdc26 » a la carte dans `data/arts_alternatifs.json` ;
  3. relance `tools/generer_arts_cartes.py` (tables du plateau et de la preparation).
Les images viennent de `sources/galerie/` (voir `telecharger-galerie.py`).
Usage : python3 importer-full-art.py [--sec]   (--sec : n'ecrit rien, liste seulement)
Les cartes NON branchees (doute) sont dans `.planning/todos/2026-10-20-mcdc-full-art-questions.md`.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image

ICI = Path(__file__).resolve().parent
RACINE = ICI.parent.parent.parent
MOTEUR = RACINE / "Fusion" / "marvel-lcg-src"
GALERIE = ICI / "sources" / "galerie"
CODE = "mcdc26"
TAILLE = (615, 882)

# card_id officiel -> (dossier de la galerie, nom du fichier, MC/DC n°)
CARTES = {
    # Basic
    "49022": ("basic", "B - face the past - RP.jpg", 6144),
    "29027": ("basic", "B - ingenuity - RP.jpg", 6149),
    "13018": ("basic", "B - ironheart - RP.jpg", 6145),
    "32019": ("basic", "B - professor x - RP.jpg", 6146),
    "30021": ("basic", "B - spdr - RP.jpg", 6148),
    "31022": ("basic", "B - spider man otto - RP.jpg", 6147),
    # Aggression
    "13016": ("aggression", "A - boot camp - RP.jpg", 6157),
    "17028": ("aggression", "A - dive bomb - RP.jpg", 6155),
    "28017": ("aggression", "A - honed technique - RP.jpg", 6152),
    "10018": ("aggression", "A - martial prowess - RP.jpg", 6156),
    "35014": ("aggression", "A - sunfire - RP.jpg", 6151),
    "25014": ("aggression", "A - throg - RP.jpg", 6150),
    "32041": ("aggression", "A - wolverine - RP.jpg", 6154),
    # Justice
    "41012": ("justice", "J - captain britain - RP.jpg", 6163),
    "04049": ("justice", "J - CTA - RP.jpg", 6160),
    "15012": ("justice", "J - crisis averted - RP.jpg", 6161),
    "22011": ("justice", "J - eros - RP.jpg", 6164),
    "27044": ("justice", "J - field agent - RP.jpg", 6165),
    "30013": ("justice", "J - spider man pavitr - RP.jpg", 6162),
    # Leadership
    "23012": ("leadership", "L - black panther - RP.jpg", 6172),
    "49015": ("leadership", "L - cyclops - RP.jpg", 6167),
    "08031": ("leadership", "L - rapid response - RP.jpg", 6170),
    "45016": ("leadership", "L - side by side - RP.jpg", 6173),
    "03017": ("leadership", "L - strength in numbers - RP.jpg", 6166),
    # Protection
    "38012": ("protection", "P - armor - RP.jpg", 6179),
    "52017": ("protection", "P - dr sinclair - RP.jpg", 6176),
    "10031": ("protection", "P - electrostatic armor - RP.jpg", 6181),
    "52019": ("protection", "P - ready for a fight - RP.jpg", 6175),
    "48012": ("protection", "P - rogue - RP.jpg", 6178),
    "27012": ("protection", "P - spider UK - RP.jpg", 6177),
    "27016": ("protection", "P - what doesnt kill me - RP.jpg", 6174),
}


def main():
    sec = "--sec" in sys.argv
    src = MOTEUR / "data" / "arts_alternatifs.json"
    d = json.load(open(src, encoding="utf-8"))
    for cid, (dossier, nom, _num) in CARTES.items():
        f = GALERIE / dossier / nom
        if not f.is_file():
            sys.exit(f"image absente : {f} (lancer telecharger-galerie.py)")
        sortie = MOTEUR / "assets" / "pics" / f"{cid}_{CODE}.jpg"
        codes = d["cartes"].setdefault(cid, [])
        if CODE not in codes:
            codes.append(CODE)
        if sec:
            print(cid, "<-", nom)
            continue
        im = Image.open(f).convert("RGB")
        assert im.size == (1500, 2150), (nom, im.size)
        im.resize(TAILLE, Image.LANCZOS).save(sortie, "JPEG", quality=88, optimize=True)
    if sec:
        return
    with open(src, "w", encoding="utf-8") as o:
        json.dump(d, o, ensure_ascii=False, indent=1)
        o.write("\n")
    subprocess.check_call([sys.executable, str(MOTEUR / "tools" / "generer_arts_cartes.py")])


main()
