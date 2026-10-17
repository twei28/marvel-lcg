# -*- coding: utf-8 -*-
"""Recette des images des six packs TMNT SHINOBI (Inkwire, prefixes sb/sj/sa/sh/sc/se) :
assets/pics/ est gitignore, donc cette recette est la seule chose reproductible.

Source : zip « TMNT Shinobi », dossiers Bushido, Kuji-Kiri, Ninjutsu, Taijutsu,
« Dual Shinobi Cards », « Shinobi Paths » (4 Paths + dos « Cardback ») et
« Shinobi Paths/ Hybrid Shinobi Paths (Advanced) » (7 hybrides + dos ; ATTENTION :
espace en tete du nom du sous-dossier). 103 cartes + 11 dos de Path, 1500x2150.

Le card_id de chaque scan est fixe UNE FOIS POUR TOUTES par
`tools/tmnt_shinobi_numerotation.tsv` (numero du scan : B1 -> sb001 ; duales par
ordre de code BK1.. KT2, NT1, NT2 -> sc001..sc012 ; Paths se001..se011, standards puis
hybrides). Les 11 DOS de Path (inserts de regles de construction, categorie DOS) sont
ecrits `<card_id>_dos.jpg` (ex. se003_dos.jpg pour le dos du Path Samurai) : ce ne sont
pas des cartes jouables, aucun card_id dans cards.json.

Format identique a `outils/uniformiser-scans.py` et aux autres importeurs (petit cote a
615 px, LANCZOS, JPEG qualite 88 optimise).

Usage : python3 tools/importer_images_tmnt_shinobi.py <dossier extrait> [<sortie>] [card_id ...]
  <dossier extrait> contient « TMNT Shinobi/ ». Sortie par defaut : <racine moteur>/assets/pics.
  Des card_id en fin de ligne limitent l'import a ces cartes (ex. `sb001`, `se003_dos`), ou a
  un prefixe entier (ex. `sb`, `se`).
"""
import csv
import os
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
DEFAUT = os.path.join(os.path.dirname(ICI), "assets", "pics")
TABLE = os.path.join(ICI, "tmnt_shinobi_numerotation.tsv")
PETIT_COTE = 615
QUALITE = 88


def lire_table():
    with open(TABLE, encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h, delimiter="\t"))


def dossier_reel(racine, nom):
    """Chemin du dossier (le sous-dossier hybride du zip porte une espace en tete)."""
    chemin = os.path.join(racine, nom)
    return chemin if os.path.isdir(chemin) else None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    racine = os.path.join(os.path.abspath(sys.argv[1]), "TMNT Shinobi")
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
