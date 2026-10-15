"""Exemple (Lyja, 15/10/2026) : copie les scans de l'archive vers le depot PRINCIPAL.
Adapte MAPPING (chemin relatif dans le dossier du bloc -> card_id) et DOSSIER.
Paysage : mets le card_id dans PAYSAGE (rotation 90 degres anti-horaire)."""
import os, shutil
from PIL import Image
RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
DOSSIER = "Hero Packs/Lyja (Skrull Menace Expansion Content)"
MAPPING = {"00 lyja hero.png": "sk037a", "Encounter Cards/43 punish the defector nemesis.png": "sk067"}
PAYSAGE = {"sk067"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"
for fichier, cid in MAPPING.items():
    src = os.path.join(RACINE, DOSSIER, fichier)
    shutil.copy(src, f"{ORIG}/{cid}.png")
    im = Image.open(src).convert("RGB")
    if cid in PAYSAGE:
        im = im.rotate(90, expand=True)
    w, h = im.size
    k = 615 / min(w, h)
    im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
