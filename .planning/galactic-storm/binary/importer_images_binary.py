#!/usr/bin/env python3
"""Images du heros BINARY (Galactic Storm, Kajislav) : cartes du pack et arts alternatifs.

Relancable. Usage :
    python3 importer_images_binary.py <dossier_sources> [racine_du_depot_principal] [--sec]

<dossier_sources> contient z1/ z2/ z3/ (extraits des quatre zips « MC custom content by Kajislav »,
parties « Hero Packs/Binary (Galactic Storm expansion content) » ; voir docs/packs/galactic-storm/INVENTAIRE.md).

Ecrit, dans le depot PRINCIPAL (les images ne sont pas versionnees, regle du brief Skrull Menace) :
  1. `assets/pics/<card_id>.png` pour les 17 card_id du pack : petit cote ramene a 615 px (LANCZOS),
     carte paysage (Goin' Rogue) tournee de 90 degres dans le sens anti-horaire ; une image par card_id
     (premier exemplaire) ; l'original dans `sauvegardes-serveur/scans-originaux/<card_id>.png` ;
  2. `assets/pics/<officielle>_binary.jpg` (615x882 JPEG, 882x615 pour une manigance de joueur) pour les
     reskins « art seul » (code d'art `binary`, data/arts_alternatifs.json) ;
  3. `assets/pics/0108[89]_binary.jpg`, `01090_binary.jpg` : collection de ressources doubles « binary ».
Les cartes en QUESTION (Avengers Mansion, trait « AVENGERS ») ne sont PAS branchees (voir
.planning/todos/2026-10-20-gs1-questions.md) : leur image n'est pas copiee.
"""
import os
import sys
from PIL import Image

BIN = "Hero Packs/Binary (Galactic Storm expansion content)"
RACINE_ZIP = "MC custom content by Kajislav"

CARTES = {
    "gs001a": ("z3", "00 binary hero.png"),
    "gs001b": ("z3", "0 carol danvers.png"),
    "gs002": ("z3", "Hero Cards/01 cosmic influx.png"),
    "gs003": ("z3", "Hero Cards/03 fuel the fire.png"),
    "gs004": ("z1", "Hero Cards/05 Pursued by the Flame.png"),
    "gs005": ("z2", "Hero Cards/07 Solar Flare.png"),
    "gs006": ("z2", "Hero Cards/09 energy torrent.png"),
    "gs007": ("z2", "Hero Cards/10 prophet singer.png"),
    "gs008": ("z1", "Hero Cards/11 white hole.png"),
    "gs009": ("z3", "Hero Cards/12 body in flames.png"),
    "gs010": ("z3", "Hero Cards/13 Energy Conversion.png"),
    "gs011": ("z1", "Hero Cards/15 light radiation heat.png"),
    "gs031": ("z1", "Encounter Cards/41 forgotten life.png"),
    "gs032": ("z3", "Encounter Cards/42 rogue nemesis 2.png"),
    "gs237": ("z2", "Encounter Cards/44 touched 2.png"),
    "gs239": ("z2", "Encounter Cards/43 Going Rogue.png"),
    "gs240": ("z3", "Encounter Cards/45 energy transfer.png"),
}
PAYSAGE = {"gs239"}

R = "Starter deck_s reskins/"
# officielle -> (zip, fichier). Comparees au texte, au cout, a la ressource, aux traits, aux stats et a
# l'unicite de l'officielle (planches du 20/10/2026, gabarit « reskins » de BINARY-GABARITS.md).
ARTS = {
    "43035": ("z1", R + "Defense Specialist.png"),
    "49022": ("z1", R + "Face the Past.png"),
    "16045": ("z1", R + "Follow Through.png"),
    "43018": ("z1", R + "Keep Them Busy.png"),
    "42023": ("z1", R + "Soaring Acrobatics.png"),
    "54016": ("z1", R + "Spoiling for a Fight.png"),
    "43037": ("z1", R + "Surveillance Specialist.png"),
    "06017": ("z1", R + "hall of heroes.png"),
    "16024": ("z2", R + "Deft Focus.png"),
    "41019": ("z2", R + "Directed Force.png"),
    "33032": ("z2", R + "Marked.png"),
    "56013": ("z2", R + "aggressive conditioning.png"),
    "43036": ("z3", R + "Front Line Specialist.png"),
    "13013": ("z3", R + "Into the Fray.png"),
    "12030": ("z3", R + "Moment of Triumph.png"),
    "43034": ("z3", R + "combat specialist.png"),
    "40204": ("z3", R + "hope summers.png"),
    "01084": ("z3", R + "nick fury.png"),
    "43021": ("z3", R + "specialized training.png"),
}
ARTS_PAYSAGE = {"43018", "43021"}
RESSOURCES = {
    "01088": ("z1", R + "energy.png"),
    "01089": ("z2", R + "genius.png"),
    "01090": ("z3", R + "strength.png"),
}
CODE = "binary"


def ouvrir(src, z, rel):
    return Image.open(os.path.join(src, z, RACINE_ZIP, BIN, rel)).convert("RGB")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sec = "--sec" in sys.argv
    src = os.path.abspath(args[0])
    principal = os.path.abspath(args[1]) if len(args) > 1 else "/home/oem/Desktop/Marvel LCG"
    pics = os.path.join(principal, "Fusion", "marvel-lcg-src", "assets", "pics")
    originaux = os.path.join(principal, "sauvegardes-serveur", "scans-originaux")
    os.makedirs(originaux, exist_ok=True)
    for cid, (z, rel) in CARTES.items():
        im = ouvrir(src, z, rel)
        assert im.size == (1500, 2150), (cid, im.size)
        if sec:
            print(cid, "<-", rel)
            continue
        im.save(os.path.join(originaux, f"{cid}.png"))
        if cid in PAYSAGE:
            im = im.rotate(90, expand=True)
        w, h = im.size
        k = 615 / min(w, h)
        im.resize((round(w * k), round(h * k)), Image.LANCZOS).save(os.path.join(pics, f"{cid}.png"), optimize=True)
    for table, paysage in ((ARTS, ARTS_PAYSAGE), (RESSOURCES, set())):
        for off, (z, rel) in table.items():
            im = ouvrir(src, z, rel)
            if sec:
                print(f"{off}_{CODE}", "<-", rel)
                continue
            if off in paysage:
                im = im.rotate(90, expand=True)
                taille = (882, 615)
            else:
                taille = (615, 882)
            im.resize(taille, Image.LANCZOS).save(os.path.join(pics, f"{off}_{CODE}.jpg"), "JPEG", quality=88, optimize=True)
    print("ok" if not sec else "sec")


if __name__ == "__main__":
    main()
