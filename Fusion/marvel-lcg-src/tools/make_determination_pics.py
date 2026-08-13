"""Les scans de l'aspect Determination, telecharges et remis a la taille du jeu.

    python3.10 tools/make_determination_pics.py [dt001 dt002 ...]

Sans argument : toutes les cartes du pack `determination` de data/cards.json.

POURQUOI CE SCRIPT EXISTE
-------------------------
assets/pics/ n'est pas suivi par git (.gitignore) : les scans ne sont pas du
source. Sans un script, la seule facon de retrouver une image perdue serait de
refaire a la main un enchainement que personne n'aurait ecrit.

CE QU'IL FAIT
-------------
1. Telecharge `D-<n>.jpg` depuis le dossier public du Drive de designhacker.ca.
   Le numero vient du card_id : dt007 -> D-7.jpg. Le dossier s'enumere par
   `embeddedfolderview` (la recherche du connecteur Drive n'indexe que ce qui a
   deja ete ouvert, et la page du dossier s'arrete a 50 entrees).
2. ROGNE LE FOND PERDU. Les fichiers du Drive sont des BLEED : 1638x2229, soit
   69,5 x 94 mm, quand une carte finie mesure 63,5 x 88 mm. Sans ce rognage, le
   jeu afficherait 3 mm de debord tout autour.
3. Ramene a 600x840, la taille des variantes `_m3t` du jeu. Les originaux pesent
   ~1,5 Mo piece : les garder tels quels ajouterait 200 Mo a l'archive livrable,
   la dette exacte mesuree le 12/08 sur les scans deja presents (577 Ko de
   moyenne, contre 220 Ko un mois plus tot).
4. Depose dans les DEUX installations : le depot et la copie WSL. `.game/assets`
   est un lien symbolique vers la seconde, donc le jeu voit l'image aussitot,
   sans relance.
"""
import io
import json
import os
import re
import subprocess
import sys
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER_DRIVE = "1Hkb4FLbt5R5E8PfVuFAARAuxZvN0NL1I"   # DETERMINATION (3.0)/BLEED
DESTINATIONS = [
    os.path.join(RACINE, "assets", "pics"),
    os.path.expanduser("~/marvel-work/fusion/marvel-lcg-src/assets/pics"),
]

# Carte finie 63,5 x 88 mm ; fichier livre avec 3 mm de fond perdu sur chaque bord.
BLEED_MM = 3.0
LARGEUR_AVEC_BLEED_MM = 69.5
HAUTEUR_AVEC_BLEED_MM = 94.0
TAILLE_FINALE = (600, 840)
QUALITE = 85


def index_du_dossier():
    """{ 'D-7.jpg': '<id Drive>' } pour tout le dossier, pas seulement 50."""
    url = "https://drive.google.com/embeddedfolderview?id=%s#list" % DOSSIER_DRIVE
    requete = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(requete).read().decode("utf-8", "replace")
    paires = re.findall(r'id="entry-([A-Za-z0-9_\-]+)".*?flip-entry-title">([^<]+)<', html, re.S)
    return {titre: ident for ident, titre in paires}


def main():
    from PIL import Image

    voulues = sys.argv[1:]
    if not voulues:
        cartes = json.load(io.open(os.path.join(RACINE, "data", "cards.json"), encoding="utf-8"))
        voulues = [c["card_id"] for c in cartes.get("determination", [])]
    if not voulues:
        print("aucune carte determination dans cards.json")
        return 1

    index = index_du_dossier()
    print("dossier Drive : %d fichiers" % len(index))

    for card_id in voulues:
        numero = int(card_id[2:])
        nom = "D-%d.jpg" % numero
        if nom not in index:
            print("ABSENT du Drive : %s (%s)" % (nom, card_id))
            continue
        brut = "/tmp/%s" % nom
        if not os.path.exists(brut) or os.path.getsize(brut) < 100000:
            url = "https://drive.google.com/uc?export=download&id=" + index[nom]
            subprocess.run(["curl", "-sL", "-o", brut, url], check=True)

        im = Image.open(brut)
        largeur, hauteur = im.size
        marge_x = (BLEED_MM / LARGEUR_AVEC_BLEED_MM) * largeur
        marge_y = (BLEED_MM / HAUTEUR_AVEC_BLEED_MM) * hauteur
        carte = im.crop((int(marge_x), int(marge_y),
                         int(largeur - marge_x), int(hauteur - marge_y)))
        carte = carte.resize(TAILLE_FINALE, Image.LANCZOS)

        for dossier in DESTINATIONS:
            if not os.path.isdir(dossier):
                print("destination absente, ignoree : %s" % dossier)
                continue
            chemin = os.path.join(dossier, "%s.jpg" % card_id)
            carte.save(chemin, quality=QUALITE)
        print("%s <- %s  (%d Ko)" % (card_id, nom,
              os.path.getsize(os.path.join(DESTINATIONS[0], "%s.jpg" % card_id)) // 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
