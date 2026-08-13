"""Refabrique les 21 illustrations du scenario The Spot depuis son zip.

POURQUOI CET OUTIL EXISTE
-------------------------
`assets/pics/` est dans le `.gitignore` : les images ne sont pas versionnees.
Sans recette ecrite, les 21 illustrations de ce scenario ne seraient donc
reproductibles que de memoire. Ce fichier EST la recette.

CE QU'IL FAIT
-------------
Il lit le zip d'origine et ecrit `assets/pics/sp0XX.jpg` en 600x840 (840x600
pour les cartes paysage). Ce format est celui de l'aspect Determination, le
precedent import fan-made, et c'est EXACTEMENT le ratio natif de ces cartes
(1488/2079 = 1,397) : aucune deformation. 26 Mo d'origine deviennent 2,8 Mo.

Usage :
    python3.10 tools/importer_images_the_spot.py "<chemin du zip>"
"""
import os, sys, zipfile, tempfile
from PIL import Image

# La carte 1 est recto-verso, la 6 aussi. Les cartes 17, 18, 20, 21, 23 et 25
# sont des EXEMPLAIRES : elles ne different de leur jumelle que par le numero
# imprime en bas a gauche (verifie pixel a pixel), donc une seule image suffit.
IMAGES = {
    "sp001a": "Double Sided Cards/1. Heightened Threat - 1A.jpg",
    "sp001b": "Double Sided Cards/1. Heightened Threat - 1B.jpg",
    "sp002":  "2. The Spot.jpg",
    "sp003":  "3. The Spot.jpg",
    "sp004":  "4. The Spot.jpg",
    "sp005":  "5. The Spot.jpg",
    "sp006a": "Double Sided Cards/6. What Goes Around... A.jpg",
    "sp006b": "Double Sided Cards/6. What Goes Around... B.jpg",
    "sp007":  "7. Rocket Racer.jpg",
    "sp008":  "8 Puma.jpg",
    "sp009":  "9. Anywhere and Everywhere.jpg",
    "sp010":  "10. Chameleon.jpg",
    "sp011":  "11. Penchant for Pilfery.jpg",
    "sp012":  "12. Living Laser.jpg",
    "sp013":  "13. Spotty Pasts.jpg",
    "sp014":  "14. Warp Hole.jpg",
    "sp015":  "15. The Hypernova.jpg",
    "sp016":  "16. ...Comes Around!.jpg",
    "sp017":  "19. Distributed Presence.jpg",
    "sp018":  "22. Oddballs.jpg",
    "sp019":  "24. Target Spotted.jpg",
}
RACINE_ZIP = "THE SPOT (3.0)"


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    chemin_zip = sys.argv[1]
    sortie = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "pics")
    sortie = os.path.normpath(sortie)
    os.makedirs(sortie, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(chemin_zip) as z:
            z.extractall(tmp)
        base = os.path.join(tmp, RACINE_ZIP)
        assert os.path.isdir(base), f"racine introuvable dans le zip : {RACINE_ZIP}"
        poids = 0
        for card_id, rel in IMAGES.items():
            src = os.path.join(base, rel)
            assert os.path.isfile(src), f"image absente du zip : {rel}"
            im = Image.open(src).convert("RGB")
            cible = (600, 840) if im.height >= im.width else (840, 600)
            dst = os.path.join(sortie, f"{card_id}.jpg")
            im.resize(cible, Image.LANCZOS).save(dst, quality=85, optimize=True)
            poids += os.path.getsize(dst)
    print(f"{len(IMAGES)} images ecrites dans {sortie} ({poids/1024:.0f} Ko)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
