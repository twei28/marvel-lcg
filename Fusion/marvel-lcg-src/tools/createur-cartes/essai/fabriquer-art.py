"""Fabrique les images d'essai du banc (dans public/createur-cartes/_essai/) a partir d'un scan de NOTRE catalogue :
l'illustration de Valkyrie (25001a), sa tete d'angle, et la version paysage. Rien ne vient du site de reference.

    python3 tools/createur-cartes/essai/fabriquer-art.py
"""
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parents[3]
SCAN = RACINE / "assets/pics-hd/25001a.jpg"
SORTIE = RACINE / "public/createur-cartes/_essai"
SORTIE.mkdir(exist_ok=True)
scan = Image.open(SCAN).convert("RGB")  # 710 x 1030, carte entiere
# l'illustration : la zone entre le titre et le panneau de texte, agrandie pour couvrir une carte 1500 x 2150
art = scan.crop((0, 120, 710, 640))
art.resize((1500, int(1500 * art.height / art.width)), Image.LANCZOS).save(SORTIE / "valkyrie-photo.png")
art.resize((2150, int(2150 * art.height / art.width)), Image.LANCZOS).save(SORTIE / "valkyrie-photo-paysage.png")
scan.crop((628, 912, 710, 1030)).resize((300, 300), Image.LANCZOS).save(SORTIE / "valkyrie-head.png")
print("images d'essai ecrites dans", SORTIE)
