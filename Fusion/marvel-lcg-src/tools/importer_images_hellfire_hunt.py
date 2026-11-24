# -*- coding: utf-8 -*-
"""Recette des images des cartes de campagne et d'aspect de Hellfire Hunt (Dipsome, prefixe `hf`, pack hellfire_hunt).

assets/pics/ est gitignore : cette recette est la seule chose reproductible.
Source : zip `Hellfire Hunt Campaign-20261025T195712Z-1-001.zip` (PNG 1500x2150, 2150x1500 pour les manigances annexes). Format identique
a tools/importer_images_starjammers_aspects.py : petit cote a 615 px, LANCZOS, JPEG qualite 88 optimise.

Usage : python3 tools/importer_images_hellfire_hunt.py <dossier « Hellfire Hunt Campaign » extrait> [<sortie>] [card_id ...]
"""
import os
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
DEFAUT = os.path.join(os.path.dirname(ICI), "assets", "pics")
PETIT_COTE = 615
QUALITE = 88

ASPECTS = "Hero/Aspect Cards"
ALLIES = "Campaign Card/allies"
POTENTIELS = "Campaign Card/ally side scheme"
CAMPAGNE = "Campaign Card/Campaign"

TABLE = {
    "hf001": f"{ASPECTS}/013.png", "hf002": f"{ASPECTS}/014.png", "hf003": f"{ASPECTS}/015.png", "hf004": f"{ASPECTS}/016.png",
    "hf005": f"{ASPECTS}/017.png", "hf006": f"{ASPECTS}/018.png", "hf007": f"{ASPECTS}/019.png", "hf008": f"{ASPECTS}/023.png",
    "hf009": f"{ASPECTS}/024.png", "hf010": f"{ASPECTS}/025.png", "hf011": f"{ASPECTS}/026.png", "hf012": f"{ASPECTS}/027.png",
}
TABLE.update({f"hf{12 + n:03d}": f"{ALLIES}/{n}.png" for n in range(1, 17)})       # hf013-hf028
TABLE.update({f"hf{28 + n:03d}": f"{POTENTIELS}/{n}.png" for n in range(1, 13)})   # hf029-hf040
TABLE.update({f"hf{40 + n:03d}": f"{CAMPAGNE}/{n}.png" for n in range(1, 8)})      # hf041-hf047
TABLE["hf048"] = f"{CAMPAGNE}/xav.png"


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    racine = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 and os.path.isdir(sys.argv[2]) else DEFAUT
    filtres = [a for a in sys.argv[2:] if a.startswith("hf")]
    os.makedirs(dst, exist_ok=True)
    manquants, faits = [], 0
    for cid, rel in TABLE.items():
        if filtres and cid not in filtres:
            continue
        chemin = os.path.join(racine, rel)
        if not os.path.exists(chemin):
            manquants.append(f"{cid} {rel}")
            continue
        with Image.open(chemin) as im:
            largeur, hauteur = im.size
            im = im.convert("RGB")
            if min(largeur, hauteur) > PETIT_COTE:
                f = PETIT_COTE / min(largeur, hauteur)
                im = im.resize((max(1, round(largeur * f)), max(1, round(hauteur * f))), Image.Resampling.LANCZOS)
            cible = os.path.join(dst, cid + ".jpg")
            if os.path.islink(cible):
                os.remove(cible)
            im.save(cible, "JPEG", quality=QUALITE, optimize=True)
        faits += 1
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{faits} images importees dans {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
