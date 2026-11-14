"""Images du heros Quasar (Galactic Storm, Kajislav, lot GS-2), lues DIRECTEMENT dans les quatre archives
« MC custom content by Kajislav-20261014T200011Z-1-00N.zip » (racine du depot principal). Relancable.

1. Cartes du pack : `assets/pics/<card_id>.png` (petit cote 615, LANCZOS ; manigance annexe pivotee de 90 degres
   anti-horaire), original dans `sauvegardes-serveur/scans-originaux/<card_id>.png`. Une image par card_id
   (copies : la premiere).
2. Reskins des officielles (decision G-D4 : arts alternatifs) : `assets/pics/<officielle>_quasar.jpg`
   (615x882 JPEG, comme `_tmnt` / `_mcdc26`), code « quasar » ajoute a la carte dans `data/arts_alternatifs.json`
   (16 cartes) ; les trois ressources Energy / Genius / Strength forment la collection de ressources « quasar »
   (`01088_quasar` ...), declaree dans `ui-app/src/board/variantes.ts` et `public/js/prepare/app.js`.
   Puis `tools/generer_arts_cartes.py`.
Usage : python3 copier_images_quasar.py [depot_principal] [copie_de_travail]
  (images ecrites dans le depot PRINCIPAL, non versionnees ; JSON et tables dans la copie de travail).
"""
import io
import json
import os
import subprocess
import sys
import zipfile
from PIL import Image

PRINCIPAL = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "/home/oem/Desktop/Marvel LCG"
ICI = os.path.dirname(os.path.abspath(__file__))
COPIE = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
ZIP = PRINCIPAL + "/MC custom content by Kajislav-20261014T200011Z-1-00{}.zip"
BASE = "MC custom content by Kajislav/Hero Packs/Quasar (Galactic Storm expansion content)/"
PICS = PRINCIPAL + "/Fusion/marvel-lcg-src/assets/pics"
ORIG = PRINCIPAL + "/sauvegardes-serveur/scans-originaux"
CODE = "quasar"

CARTES = {  # card_id -> (zip, chemin sous BASE)
    "gs300a": (3, "00 quasar 2.png"),
    "gs300b": (3, "0 Wendell Vaughn.png"),
    "gs301": (2, "01 quantum Bands.png"),
    "gs302": (2, "Hero cards/02 epoch.png"),
    "gs303": (2, "Hero cards/03 flight of light.png"),
    "gs305": (3, "Hero cards/05 No Holding Back.png"),
    "gs307": (3, "Hero cards/07 Righteous Fury.png"),
    "gs309": (3, "Hero cards/09 Unbreakable Guard.png"),
    "gs311": (2, "Hero cards/11 quantum enegry.png"),
    "gs313": (1, "Hero cards/13 Quantum Absorption.png"),
    "gs315": (1, "Hero cards/15 Quantum Jump.png"),
    "gs316": (3, "Hero cards/16 quantum Weapon.png"),
    "gs349": (3, "Hero cards/14 Quantum Bubble.png"),
    "gs065": (2, "Encounter cards/43 protector of the universe.png"),
    "gs099q": (1, "Encounter cards/44 Maelstrom nemesis.png"),
    "gs239q": (1, "Encounter cards/45 Entropy Ascendant.png"),
    "gs237q": (3, "Encounter cards/46 avatar of oblivion.png"),
    "gs240q": (1, "Encounter cards/47 distant manipulation.png"),
}
PAYSAGE = {"gs239q"}

RESKINS = {  # officielle -> (zip, fichier sous « Starter deck_s reskins/ »)
    "56046": (1, "Defensive Conditioning.png"), "21065": (1, "Martinex.png"),
    "22035": (1, "honorary guardian.png"), "17022": (1, "knowhere.png"),
    "48014": (2, "Change of Fortune.png"), "16012": (2, "Starhawk.png"), "09020": (2, "Unflappable.png"),
    "17020": (2, "cosmo.png"), "18019": (2, "drax.png"), "47021": (2, "multitalented.png"),
    "32014": (2, "powerful punch.png"), "54033": (2, "shield deputy.png"),
    "19012": (3, "Martyr.png"), "09015": (3, "desperate defense.png"), "10031": (3, "electrostatic armor.png"),
    "19020": (3, "gamora.png"),
}
RESSOURCES = {"01088": (1, "energy.png"), "01089": (1, "genius.png"), "01090": (3, "strength.png")}


def lire(n, chemin):
    with zipfile.ZipFile(ZIP.format(n)) as z:
        data = z.read(chemin)
    return data, Image.open(io.BytesIO(data)).convert("RGB")


def main():
    for cid, (n, f) in CARTES.items():
        data, im = lire(n, BASE + f)
        assert im.size == (1500, 2150), (cid, im.size)
        open(f"{ORIG}/{cid}.png", "wb").write(data)
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(f"{PICS}/{cid}.png")
    for cid, (n, f) in {**RESKINS, **RESSOURCES}.items():
        _, im = lire(n, BASE + "Starter deck_s reskins/" + f)
        assert im.size == (1500, 2150), (cid, im.size)
        im.resize((615, 882), Image.LANCZOS).save(f"{PICS}/{cid}_{CODE}.jpg", "JPEG", quality=88, optimize=True)
    src = COPIE + "/Fusion/marvel-lcg-src/data/arts_alternatifs.json"
    d = json.load(open(src, encoding="utf-8"))
    for cid in RESKINS:
        codes = d["cartes"].setdefault(cid, [])
        if CODE not in codes:
            codes.append(CODE)
    # Serie « quasar » : sans choix enregistre, le joueur QUASAR voit les illustrations de l'auteur sur ces
    # 16 officielles (meme mecanisme que la serie TMNT pour un heros TMNT : `serieDuHeros`, arts-cartes.ts) ;
    # aucun set exclusif (les reskins ne sont que de l'art).
    d["series"][CODE] = {"nom": "Quasar (Kajislav)", "nom_en": "Quasar (Kajislav)", "heros_cartes": ["gs300"],
                         "heros_ids": ["quasar"], "sets_exclusifs": []}
    with open(src, "w", encoding="utf-8") as o:
        json.dump(d, o, ensure_ascii=False, indent=1)
        o.write("\n")
    subprocess.check_call([sys.executable, COPIE + "/Fusion/marvel-lcg-src/tools/generer_arts_cartes.py"])
    print(f"{len(CARTES)} cartes, {len(RESKINS)} arts « {CODE} », {len(RESSOURCES)} ressources « {CODE} »")


main()
