# -*- coding: utf-8 -*-
"""Recette des images du pack d'aspect Starjammers (Phenexian et Mysteltainn, prefixe `sy`, pack starjammers_aspects).

assets/pics/ est gitignore : cette recette est la seule chose reproductible.
Source : zip `Starjammers-20261025T195726Z-1-001.zip`, dossier `Starjammers/Aspect and Basic Cards/` (50 PNG 1500x2150, 2150x1500 pour
la manigance joueur Skillful Execution). Format identique a `outils/uniformiser-scans.py` et aux autres importeurs : petit cote a 615 px,
LANCZOS, JPEG qualite 88 optimise.

La table nom de fichier -> card_id suit docs/packs/starjammers-aspects/TRANSCRIPTIONS.md (numero imprime moins 76).
Le FICHIER « Rogue Tactics » porte la carte imprimee « Rogue Heroics » (sy048).

Usage : python3 tools/importer_images_starjammers_aspects.py <dossier « Aspect and Basic Cards » extrait> [<sortie>] [card_id ...]
"""
import os
import sys

from PIL import Image

ICI = os.path.dirname(os.path.abspath(__file__))
DEFAUT = os.path.join(os.path.dirname(ICI), "assets", "pics")
PETIT_COTE = 615
QUALITE = 88

# (aspect dans le nom du fichier, fragment du titre du fichier) -> card_id
TABLE = {
    "sy001": ("Basic", "Ch_od"), "sy002": ("Basic", "Corsair (Christopher Summers)"), "sy003": ("Basic", "Hepzibah"),
    "sy004": ("Basic", "Sikorsky"), "sy005": ("Basic", "Waldo"), "sy006": ("Basic", "Raza Longknife"),
    "sy007": ("Basic", "Life-Bonded Crewmates"), "sy008": ("Basic", "Steadfast Companions"),
    "sy009": ("Basic", "Skillful Execution"), "sy010": ("Basic", "Center Section Garden"), "sy011": ("Basic", "Standing Still"),
    "sy012": ("Basic", "The Starjammer"), "sy013": ("Basic", "Honorary Starjammer"), "sy014": ("Basic", "Pirate_s Rapier"),
    "sy015": ("Basic", "Stolen Goods"),
    "sy016": ("Aggression", "Binary"), "sy017": ("Aggression", "Korvus Rook_shir (Ally)"),
    "sy018": ("Aggression", "Korvus Rook_shir (Blade of the Phoenix)"), "sy019": ("Aggression", "Marvel Girl"),
    "sy020": ("Aggression", "Critical Blow"), "sy021": ("Aggression", "Outlaw Justice"), "sy022": ("Aggression", "Reckless Attack"),
    "sy023": ("Aggression", "Energy Cannon"), "sy024": ("Aggression", "Longarm Blaster"),
    "sy025": ("Justice", "Havok"), "sy026": ("Justice", "Polaris"), "sy027": ("Justice", "Freedom Fighters"),
    "sy028": ("Justice", "Masterstroke"), "sy029": ("Justice", "Reckless Maneuver"), "sy030": ("Justice", "Helek"),
    "sy031": ("Justice", "Disruptor Ray"), "sy032": ("Justice", "Tactical Teleporter"),
    "sy033": ("Leadership", "Cyclops"), "sy034": ("Leadership", "Keeyah"), "sy035": ("Leadership", "Lilandra"),
    "sy036": ("Leadership", "Decisive Action"), "sy037": ("Leadership", "Far Flung Family"),
    "sy038": ("Leadership", "Reckless Charge"), "sy039": ("Leadership", "Targeting Station"),
    "sy040": ("Leadership", "Captain of the Starjammer"), "sy041": ("Leadership", "Jet Bike"),
    "sy042": ("Protection", "Kalyx (Ally)"), "sy043": ("Protection", "Kalyx (Thorn Crew)"), "sy044": ("Protection", "K-Zzat"),
    "sy045": ("Protection", "Tolo Hawk"), "sy046": ("Protection", "Ready for Anything"), "sy047": ("Protection", "Reckless Defense"),
    "sy048": ("Protection", "Rogue Tactics"), "sy049": ("Protection", "Armored Space Suit"), "sy050": ("Protection", "Plasnet Launcher"),
}


def trouver(dossier, aspect, titre):
    """Le PNG dont le nom contient « (Aspect) » et le titre (apres le dernier « - »)."""
    for nom in sorted(os.listdir(dossier)):
        if not nom.endswith(".png") or f"({aspect})" not in nom:
            continue
        reste = nom.split(f"({aspect})", 1)[1].lstrip(" -").rsplit(".png", 1)[0]
        if reste == titre or (titre.endswith(")") is False and reste.startswith(titre) and "(" not in reste[len(titre):]
                              and reste == titre) or reste.startswith(titre + " ("):
            return os.path.join(dossier, nom)
    return None


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    dossier = os.path.abspath(sys.argv[1])
    dst = os.path.abspath(sys.argv[2]) if len(sys.argv) > 2 and os.path.isdir(sys.argv[2]) else DEFAUT
    filtres = [a for a in sys.argv[2:] if a.startswith("sy")]
    os.makedirs(dst, exist_ok=True)
    manquants, faits = [], 0
    for cid, (aspect, titre) in TABLE.items():
        if filtres and cid not in filtres:
            continue
        chemin = trouver(dossier, aspect, titre)
        if not chemin:
            manquants.append(f"{cid} ({aspect}) {titre}")
            continue
        with Image.open(chemin) as im:
            largeur, hauteur = im.size
            im = im.convert("RGB")
            if min(largeur, hauteur) > PETIT_COTE:
                f = PETIT_COTE / min(largeur, hauteur)
                im = im.resize((max(1, round(largeur * f)), max(1, round(hauteur * f))), Image.Resampling.LANCZOS)
            im.save(os.path.join(dst, cid + ".jpg"), "JPEG", quality=QUALITE, optimize=True)
        faits += 1
    if manquants:
        print("MANQUANTS dans le zip :")
        for nom in manquants:
            print("   ", nom)
        return 1
    print(f"{faits} images importees dans {dst}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
