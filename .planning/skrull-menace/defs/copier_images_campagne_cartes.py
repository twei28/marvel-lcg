"""Copie les scans des CARTES DE CAMPAGNE (sk263-sk289b) vers le depot PRINCIPAL (15/10/2026).
Recette : copier_images_exemple.py. Complots annexes de joueur (paysage, stockes pivotes) : rotation
90 degres anti-horaire. Petit cote ramene a 615 px (LANCZOS) ; original dans scans-originaux."""
import os
import shutil
from PIL import Image

RACINE = os.path.expanduser("~/Desktop/Marvel LCG-contenu/kajislav/MC custom content by Kajislav")
CAMP = "Campaigns/Skrull Menace (Released)"
MAPPING = {
    f"{CAMP}/campaign allies/crusader.png": "sk263",
    f"{CAMP}/campaign allies/jazinda.png": "sk264",
    f"{CAMP}/campaign allies/paibok ally.png": "sk265",
    f"{CAMP}/campaign allies/skymax.png": "sk266",
    f"{CAMP}/campaign allies/super-skrull ally.png": "sk267",
    f"{CAMP}/campaign allies/War Skrull.png": "sk268",
    f"{CAMP}/campaign allies/xavin.png": "sk269",
    f"{CAMP}/campaign player side schemes/buddy training program.png": "sk270",
    f"{CAMP}/campaign player side schemes/cloning faux pas.png": "sk271",
    f"{CAMP}/campaign player side schemes/fickle alliance.png": "sk272",
    f"{CAMP}/campaign player side schemes/newbie training.png": "sk273",
    f"{CAMP}/campaign player side schemes/searching for powers.png": "sk274",
    f"{CAMP}/campaign player side schemes/skrull military training.png": "sk275",
    f"{CAMP}/campaign player side schemes/stealing for good.png": "sk276",
    f"{CAMP}/campaign supports/antalya.png": "sk277",
    f"{CAMP}/campaign supports/cadre K.png": "sk278",
    f"{CAMP}/campaign supports/pool-o-vision.png": "sk279",
    f"{CAMP}/campaign supports/princess anelle.png": "sk280",
    f"{CAMP}/campaign supports/skrull battleship.png": "sk281",
    f"{CAMP}/campaign supports/skrull kill krew.png": "sk282",
    f"{CAMP}/campaign upgrades/3-D man_s googles upgrade.png": "sk283",
    f"{CAMP}/campaign upgrades/inhibitor mask upgrade.png": "sk284",
    f"{CAMP}/campaign upgrades/nullifier.png": "sk285",
    f"{CAMP}/campaign upgrades/reverting device upgrade.png": "sk286",
    f"{CAMP}/campaign upgrades/skrull shapeshifter.png": "sk287",
    f"{CAMP}/campaign upgrades/Sy-Torak Gem upgrade.png": "sk288",
    f"{CAMP}/rulebook/cooperation progress reminder.png": "sk289a",
    f"{CAMP}/rulebook/cooperation progress reminder back.png": "sk289b",
}
PAYSAGE = {"sk270", "sk271", "sk272", "sk273", "sk274", "sk275", "sk276"}
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
