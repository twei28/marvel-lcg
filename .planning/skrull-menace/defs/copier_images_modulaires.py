"""Copie les scans des sets modulaires (Shaper of Worlds, elites, Standard/Expert Skrull) vers le depot PRINCIPAL.
Recette : copier_images_exemple.py. Paysage (complots annexes) : rotation 90 degres anti-horaire.
Une seule image par card_id (copies : on prend la premiere). Les cartes `ability_link` ont leur propre image."""
import os
import shutil
from PIL import Image

RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav/Modular Sets")
SW = "Shaper of Worlds (Skrull Menace Expansion Content)"
CR = "Crusader (Skrull Elite) (Skrull Menace Expansion Content)"
JA = "Jazinda (Skrull Elite) (Skrull Menace Expansion Content)"
SK = "Skymax (Skrull Menace Expansion Content)"
WS = "War Skrull (Skrull Menace Expansion Content)"
XA = "Xavin (Skrull Menace Expansion Content)"
ST = "Standard Skrull-Expert Skrull (Skrull Menace Expansion Content)"
MAPPING = {
    f"{SW}/1 shaper of worlds.png": "sk228", f"{SW}/2 cosmic cube creation.png": "sk229",
    f"{SW}/3 cosmic cube fragment.png": "sk230a", f"{SW}/4 cosmic cube fragment.png": "sk230b",
    f"{SW}/5 cosmic cube fragment.png": "sk230c", f"{SW}/6 cosmic cube fragment.png": "sk230d",
    f"{CR}/1 crusader minion.png": "sk231", f"{CR}/2 enemy adaptation.png": "sk232", f"{CR}/3 freedom ring.png": "sk233",
    f"{CR}/4 spy training.png": "sk234", f"{CR}/5 rivals to the end.png": "sk235",
    f"{JA}/1 jazinda minion.png": "sk236", f"{JA}/2 skrull energy gun.png": "sk237", f"{JA}/3 sy-torak gem.png": "sk238",
    f"{JA}/4 stealing for the empire.png": "sk239", f"{JA}/6 skrull of royal blood.png": "sk240",
    f"{SK}/1 skymax minion.png": "sk241", f"{SK}/2 changing appearance.png": "sk242",
    f"{SK}/4 surprising alliance.png": "sk243", f"{SK}/5 shape alteration.png": "sk244",
    f"{WS}/1 war skrull minion.png": "sk245", f"{WS}/2 impostor.png": "sk246", f"{WS}/3 skrull commander.png": "sk247",
    f"{WS}/4 skrull geneticist.png": "sk248", f"{WS}/5 cloning program.png": "sk249",
    f"{XA}/1 xavin minion.png": "sk250", f"{XA}/2 invisible forcefield.png": "sk251",
    f"{XA}/4 skrull training program.png": "sk252", f"{XA}/5 going nova.png": "sk253",
    f"{ST}/01 impostor.png": "sk254", f"{ST}/02 curced by the past.png": "sk255", f"{ST}/03 subject of experiment.png": "sk256",
    f"{ST}/04 Forge Ahead.png": "sk257", f"{ST}/05 Mobilization.png": "sk258", f"{ST}/06 stick to the plan.png": "sk259",
    f"{ST}/11 replaced archenemy.png": "sk260", f"{ST}/12 focused attention.png": "sk261", f"{ST}/13 tricky assault.png": "sk262",
}
PAYSAGE = {"sk229", "sk234", "sk239", "sk243", "sk249", "sk252"}
DEPOT = "/home/oem/Desktop/Marvel LCG"
ORIG = f"{DEPOT}/sauvegardes-serveur/scans-originaux"
PICS = f"{DEPOT}/Fusion/marvel-lcg-src/assets/pics"

if __name__ == "__main__":
    os.makedirs(ORIG, exist_ok=True)
    for fichier, cid in MAPPING.items():
        src = os.path.join(RACINE, fichier)
        shutil.copy(src, f"{ORIG}/{cid}.png")
        im = Image.open(src).convert("RGB")
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    print(len(MAPPING), "images copiees")
