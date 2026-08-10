"""Fabrique les vignettes manquantes des boites, pour le gestionnaire de decks.

`public/deck.html` affiche une vignette par boite, chargee depuis
`/sets/<nom de la boite>` et resolue en `assets/textures/sets/<nom>.webp`.
Vingt-cinq boites sur 82 n'en avaient aucune et s'affichaient en RECTANGLE
GRIS : les trois dernieres boites officielles, le set modulaire Ronan, et
TOUS les packs maison, qui n'auront jamais de photo de boite officielle.

Faute de photo, on prend l'art le plus representatif du pack : la carte
d'identite du heros, a defaut le vilain, a defaut la premiere carte illustree.
Mise a la hauteur des vignettes existantes (300 px) en gardant les proportions
de la carte, ce qui donne une tuile un peu plus etroite que les photos de
boite mais de la meme hauteur, donc alignee dans la grille.

    ~/marvel-work/python/bin/python3.10 tools/vignettes_boites.py [--forcer]

Sans `--forcer`, une boite qui a deja sa vignette n'est jamais touchee : les
photos officielles ne doivent pas etre ecrasees par de l'art de carte.
"""
import argparse
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETS = os.path.join(RACINE, "assets", "textures", "sets")
PICS = os.path.join(RACINE, "assets", "pics")
HAUTEUR = 300

# L'ordre dit quelle carte represente le mieux un pack. Un heros d'abord :
# c'est lui qu'on cherche des yeux dans la grille.
#
# « Leader » vient juste apres le vilain, et pas par gout du detail : la boite
# 57 Synthezoid Smackdown n'a NI heros NI vilain, c'est un affrontement entre
# deux camps menes par des Leaders (She-Hulk et Vision). Sans ce type, l'outil
# tombait sur le premier sbire venu et affichait un « S.H.I.E.L.D. Operator »
# en guise de boite, ce qui ne dit rien a personne. Signale en jeu le
# 10/8/2026 : « le visuel de synthezoid smackdown n'est pas le bon ».
PRIORITE = ("Hero", "AlterEgo", "Villain", "Leader", "MainScheme", "Ally", "Minion")


def image_de(card_id):
    for ext in (".jpg", ".png", ".webp"):
        chemin = os.path.join(PICS, card_id + ext)
        if os.path.exists(chemin):
            return chemin
    return None


def carte_representative(cartes):
    """La carte dont l'art servira de vignette, ou None si le pack n'en a aucune."""
    def rang(carte):
        type_carte = carte.get("type")
        return PRIORITE.index(type_carte) if type_carte in PRIORITE else len(PRIORITE)

    for carte in sorted(cartes, key=lambda c: (rang(c), c.get("card_id", ""))):
        chemin = image_de(carte.get("card_id", ""))
        if chemin:
            return carte, chemin
    return None, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--forcer", action="store_true",
                    help="refabrique aussi les vignettes deja presentes")
    options = ap.parse_args()

    from PIL import Image

    info = json.load(open(os.path.join(RACINE, "data", "sets_info.json"), encoding="utf-8"))
    # Les deux catalogues, pas seulement le principal : le pack « homebrew »
    # (Stan Lee) ne vit que dans cards_custom.json, et sa boite restait grise.
    cards = {}
    for fichier in ("cards.json", "cards_custom.json"):
        chemin = os.path.join(RACINE, "data", fichier)
        if not os.path.exists(chemin):
            continue
        for pack, liste in json.load(open(chemin, encoding="utf-8")).items():
            if isinstance(liste, list):
                cards.setdefault(pack, []).extend(liste)
    existantes = {os.path.splitext(f)[0] for f in os.listdir(SETS)}

    faites, ignorees, sans_carte = 0, 0, []
    for boite, definition in info.items():
        if not isinstance(definition, dict):
            continue
        fichier = boite.replace("/", "")
        if fichier in existantes and not options.forcer:
            ignorees += 1
            continue
        pack = definition.get("name")
        # « homebrew » cote sets_info, « stanlee » cote catalogue : on retombe
        # sur le nom du heros declare quand la cle directe ne donne rien.
        cartes = cards.get(pack)
        if not cartes:
            for heros in definition.get("heroes") or []:
                cartes = cards.get(heros.replace("_", ""))
                if cartes:
                    break
        if not cartes:
            sans_carte.append((boite, "aucun pack « %s » dans cards.json" % pack))
            continue
        carte, source = carte_representative([c for c in cartes if isinstance(c, dict)])
        if not source:
            sans_carte.append((boite, "aucune carte illustree"))
            continue

        image = Image.open(source).convert("RGB")
        largeur = max(1, round(image.width * HAUTEUR / image.height))
        image = image.resize((largeur, HAUTEUR), Image.LANCZOS)
        image.save(os.path.join(SETS, fichier + ".webp"), "WEBP", quality=82, method=6)
        print("  %-36s <- %s %s" % (boite[:36], carte.get("card_id"),
                                    (carte.get("name") or "")[:24]))
        faites += 1

    print()
    print("  %d vignette(s) fabriquee(s), %d deja presente(s)" % (faites, ignorees))
    for boite, raison in sans_carte:
        print("  IGNOREE : %-34s %s" % (boite[:34], raison))
    return 0 if not sans_carte else 0


if __name__ == "__main__":
    sys.exit(main())
