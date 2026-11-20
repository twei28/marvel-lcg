# -*- coding: utf-8 -*-
"""Recette des 13 allies de la campagne fan-made « Galactic Storm Campaign »
(pack `galactic_storm`, codes gs224 a gs236), sans scan ni sur marvelcdb.com ni
sur mc4db (contenu communautaire, pas des codes FFG a cinq chiffres).

Source donnee par l'utilisateur le 29/10/2026 : dossier public Google Drive
https://drive.google.com/drive/folders/1QOZJh8ZWEyQXlrLx2caCNA6V8HzdIS07
  Campaigns/Galactic Storm/Campaign allies/                    (3 allies generiques)
  Campaigns/Galactic Storm/Identity-specific campaign allies/   (10 allies par heros)
Fichiers PNG 1500x2150 (meme format « bleed » que les autres scans fan-made de
ce depot, voir outils/uniformiser-scans.py) ; mention au bas de chaque carte
« MC Custom Content By: Kajislav », coherente avec le numero imprime (ex. 224
pour gs224) : verifie visuellement sur Rick Jones avant d'ecrire cette recette.

Comme le dossier n'a que 13 fichiers repartis sur deux sous-dossiers (jamais
plus de 50, pas besoin d'enumeration recursive comme make_determination_pics.py),
les identifiants Drive sont lus une fois et gardes ici en dur : un dossier
public peut changer de contenu sans le signaler.

    python3 tools/importer_images_galactic_storm_campaign.py
    python3 outils/uniformiser-scans.py --sauvegarde && python3 outils/uniformiser-scans.py --appliquer
"""
import os
import urllib.request

from PIL import Image

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DST = os.path.join(RACINE, "assets", "pics")

# code -> (id du fichier Drive, nom, pour verification)
CARTES = {
    "gs224": ("14QpD1M2JNdhpYJ9DmVAIbZYBzJ09Ct0v", "Rick Jones"),
    "gs225": ("1d3KWcVAwrZezevaVKvP3ZTpeh_SPeE_w", "Gladiator"),
    "gs226": ("1pLK09zJXRopyTMtTwpA2LmYsjHHkZacJ", "Lauri-Ell"),
    "gs227": ("1TQoDQ-F5faXaNbUHm05xGDA4k2deFI-q", "Binary"),
    "gs228": ("1xoO04xjv4lIKTZZtPN4eh_gmrZNBdp8m", "Captain Marvel"),
    "gs229": ("1oQL_wh-FCxYIImXHoYHvFQnDlY2ZJjC6", "Crystal"),
    "gs230": ("1JEbvIlEuoNQ_B07ssYo6fVZQ_r2xqj8k", "Doctor Pym"),
    "gs231": ("1Nnw_CYJtdDGf8UWLXkDBpbQETycKZMWf", "Goliath"),
    "gs232": ("1QMbkfwP9vazw2ydoYuDrpAAq23zy7mhG", "Her"),
    "gs233": ("1tb0qIxorpTS8XXVKV6Rpq-Z-Fs1-ldod", "Living Lightning"),
    "gs234": ("1oFrgpItIHIM6A0QTQoKnl8XOXs69o-6H", "Sersi"),
    "gs235": ("1gj8GwpZhxD-q9GLPa11xnFLSXVW0dmfC", "Spider-Woman"),
    "gs236": ("15g68zy5pTwTRlzL8nviOQAf0Bzn8NJw7", "Thor"),
}


def importer() -> list[str]:
    """Telecharge chaque carte vers `assets/pics/<code>.jpg`. Rend les codes
    dont le telechargement a echoue."""
    echecs = []
    for code, (fid, nom) in CARTES.items():
        url = f"https://drive.google.com/uc?export=download&id={fid}"
        requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            brut = urllib.request.urlopen(requete, timeout=60).read()
            image = Image.open(__import__("io").BytesIO(brut)).convert("RGB")
        except Exception as e:
            echecs.append(code)
            print(f"  {code} ({nom}) : ECHEC - {e}")
            continue
        chemin = os.path.join(DST, code + ".jpg")
        image.save(chemin, "JPEG", quality=92)
        print(f"  {code} ({nom}) : {image.size[0]}x{image.size[1]}")
    return echecs


if __name__ == "__main__":
    echecs = importer()
    print(len(CARTES) - len(echecs), "images importees dans assets/pics/",
          ("; ECHEC : " + ", ".join(echecs)) if echecs else "")
