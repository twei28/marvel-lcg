"""Passe les calques PNG du createur (public/createur-cartes/img) en WebP SANS PERTE (alpha compris) : ~2 fois plus leger.
Les PNG d'origine sont supprimes (ils se re-telechargent avec les sondes) et types.json pointe sur les .webp.

    python3 tools/createur-cartes/optimiser-images.py
"""
import re
from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parents[2] / "public/createur-cartes"
avant = apres = 0
for png in sorted((RACINE / "img").rglob("*.png")):
    webp = png.with_suffix(".webp")
    Image.open(png).save(webp, "WEBP", lossless=True, method=6, quality=100)
    avant += png.stat().st_size
    apres += webp.stat().st_size
    png.unlink()
types = RACINE / "donnees/types.json"
texte = types.read_text(encoding="utf-8")
types.write_text(re.sub(r'("src":\s*"[^"]+)\.png"', r'\1.webp"', texte), encoding="utf-8")
print(f"{avant / 1e6:.1f} Mo -> {apres / 1e6:.1f} Mo")
