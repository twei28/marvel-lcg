# -*- coding: utf-8 -*-
"""Recette des images des six packs d'aspect TMNT (Inkwire, prefixes ua/ub/uj/ul/up/ud) :
assets/pics/ est gitignore, donc cette recette est la seule chose reproductible.

Source : zip « TMNT Aspect », six dossiers (Aggression, Basic, Justice, Leadership,
Protection, « Dual-Aspect » AVEC une espace finale dans le nom du dossier), 235 PNG
1500x2150 (2150x1500 pour la manigance joueur Weasel In).

Le card_id de chaque scan est fixe UNE FOIS POUR TOUTES par
`tools/tmnt_aspects_numerotation.tsv` (ordre alphabetique des noms de fichier, sans
tenir compte de la casse, 001 a N dans chaque dossier). Les cinq agents de portage
lisent la meme table : aucun ne choisit ses numeros.

Format identique a `outils/uniformiser-scans.py` et aux autres importeurs (petit cote a
615 px, LANCZOS, JPEG qualite 88 optimise).

Usage : python3 tools/importer_images_tmnt_aspects.py <dossier extrait> [<sortie>] [card_id ...]
  <dossier extrait> contient « TMNT Aspect/ ». Sortie par defaut : <racine moteur>/assets/pics.
  Des card_id en fin de ligne limitent l'import a ces cartes (ex. `ua015`), ou a un
  prefixe entier (ex. `ua`).
"""
import csv
import os
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
DEFAUT = os.path.join(os.path.dirname(ICI), "assets", "pics")
TABLE = os.path.join(ICI, "tmnt_aspects_numerotation.tsv")
PETIT_COTE = 615
QUALITE = 88


def lire_table():
    with open(TABLE, encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h, delimiter="\t"))


def dossier_reel(racine, nom):
    """Le dossier « Dual-Aspect » du zip porte une espace finale."""
    for d in os.listdir(racine):
        if d.strip() == nom:
            return os.path.join(racine, d)
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    racine = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Aspect")
    dst = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else DEFAUT
    filtres = sys.argv[3:]
    if not os.path.isdir(racine):
        print(f"dossier introuvable : {racine}")
        return 2
    os.makedirs(dst, exist_ok=True)

    manquants, faits = [], 0
    for ligne in lire_table():
        cid = ligne["card_id"]
        if filtres and not any(cid == f or (len(f) == 2 and cid.startswith(f)) for f in filtres):
            continue
        dossier = dossier_reel(racine, ligne["dossier"])
        chemin = os.path.join(dossier or "", ligne["fichier_scan"])
        if not dossier or not os.path.isfile(chemin):
            manquants.append(f"{cid} {ligne['dossier']}/{ligne['fichier_scan']}")
            continue
        with Image.open(chemin) as im:
            largeur, hauteur = im.size
            im = im.convert("RGB")
            if min(largeur, hauteur) > PETIT_COTE:
                f = PETIT_COTE / min(largeur, hauteur)
                im = im.resize((max(1, round(largeur * f)), max(1, round(hauteur * f))),
                               Image.Resampling.LANCZOS)
            im.save(os.path.join(dst, cid + ".jpg"), "JPEG", quality=QUALITE, optimize=True)
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
