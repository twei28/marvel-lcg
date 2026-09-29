# -*- coding: utf-8 -*-
"""Import d'images de cartes OFFICIELLES depuis mc4db (clone de MarvelCDB,
images de Cerebro) : `assets/pics/` est gitignore, les recettes
`importer_images_*.py` sont la seule chose reproductible du depot.

Source : https://mc4db.merlindumesnil.net (donnee par l'utilisateur le
29/09/2026). MarvelCDB (.com et .fr) n'a AUCUNE image pour les cartes 61xxx
ni pour une partie des 60xxx (`imagesrc` null) ; Hall of Heroes ne montre que
les previews. mc4db, lui, sert `/bundles/cards/EN/<pack>/<code>.webp` en
738x1048.

⚠ ON LIT `imagesrc` DANS L'API, ON NE DEVINE PAS LE CHEMIN : un code absent
rend `imagesrc` null et l'import le dit, au lieu de rapporter un 404 muet.

Format en place : JPEG RGB, extension `.jpg`, comme les autres 6xxxx (les
tailles varient, 300x426 pour les previews, 615x892 apres
`outils/uniformiser-scans.py`, a lancer apres cet import : il ramene le petit
cote a 615).
"""
import io
import json
import os
import urllib.request

from PIL import Image

SITE = "https://mc4db.merlindumesnil.net"
DST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "assets", "pics")


def _lire(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "narwhalchampions-import/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def importer(codes: list[str]) -> list[str]:
    """Telecharge chaque code vers `assets/pics/<code>.jpg`. Rend les codes
    SANS image (imagesrc null), pour que l'appelant les affiche."""
    absents = []
    for code in codes:
        fiche = json.loads(_lire(f"{SITE}/api/public/card/{code}"))
        src = fiche.get("imagesrc")
        if not src:
            absents.append(code)
            print(f"  {code} : pas d'image sur mc4db ({fiche.get('name')})")
            continue
        image = Image.open(io.BytesIO(_lire(SITE + src))).convert("RGB")
        chemin = os.path.join(DST, code + ".jpg")
        image.save(chemin, "JPEG", quality=92)
        print(f"  {code} : {image.size[0]}x{image.size[1]} <- {src} ({fiche.get('name')})")
    return absents
