"""Recupere les cartes de la campagne fan-made « Web of Deceit » (Drive).

POURQUOI CET OUTIL EXISTE
-------------------------
La source n'est ni un zip ni un site : c'est un dossier Google Drive PARTAGE.
L'API Drive ne sait pas enumerer les enfants d'un dossier qu'on n'a que reçu ;
la PAGE publique, si : chaque entree y porte son identifiant dans un attribut
`ssk` et son nom dans l'`aria-label` voisin. Ce fichier EST la recette de
l'import, comme `importer_images_the_spot.py` l'est pour The Spot.

Le dossier melange des vrais sous-dossiers et des RACCOURCIS vers d'autres
dossiers du meme auteur (les quatre scenarios autres qu'Electro, les heros
maison). Un raccourci s'ouvre comme un dossier, il suffit de le suivre.

CE QU'IL FAIT
-------------
    python3.10 tools/importer_web_of_deceit.py --inventaire <sortie.json>
        Descend l'arbre et ecrit l'inventaire (chemin -> fichiers).

    python3.10 tools/importer_web_of_deceit.py --telecharger <dossier>
        Ecrit chaque carte en JPEG 1000 px de large : assez pour LIRE le texte
        d'une carte (c'est ainsi qu'on la transcrit), et assez pour en tirer
        ensuite le 600x840 du jeu.

Les planches d'impression, les boites et les precons sont ignorees : ce sont
des assemblages, pas des cartes.
"""
import argparse
import io
import json
import os
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor

RACINE = "1K0Q-41Aqy6tgPDMp0K6pYRKdv66IWCIN"
NAVIGATEUR = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/120 Safari/537.36")
ENTREE = re.compile(r'aria-label="([^"]{1,160}?)"[^>]*?ssk=\'5:[^:]+:([-\w]{20,60})-0-\d+\'')
RACCOURCI = re.compile(r'\s*Shortcut to Shared folder$')
SUFFIXE = re.compile(r'\s+(PDF|Image|Video|Audio|Text|Binary|Archive|Word|Excel'
                     r'|PowerPoint|Compressed Archive)?\s*Shared( folder)?$')
IGNORES = ("/Print Files", "/Box", "/Precon Boxes")


def lister(folder_id: str):
    """Les entrees d'un dossier Drive public, lues dans sa page HTML."""
    page = subprocess.run(
        ["curl", "-sL", "--max-time", "120", "-A", NAVIGATEUR,
         f"https://drive.google.com/drive/folders/{folder_id}"],
        capture_output=True, text=True).stdout
    vus, sortie = set(), []
    for trouve in ENTREE.finditer(page):
        libelle, cid = trouve.group(1), trouve.group(2)
        if cid in vus or cid == folder_id:
            continue
        vus.add(cid)
        nom = SUFFIXE.sub('', libelle)
        raccourci = bool(RACCOURCI.search(nom))
        sortie.append({
            "id": cid,
            "nom": RACCOURCI.sub('', nom),
            "dossier": libelle.endswith("Shared folder") and not raccourci,
            "raccourci": raccourci,
        })
    return sortie


def inventorier() -> dict:
    arbre, vus = {}, set()

    def marcher(chemin: str, fid: str, profondeur: int = 0) -> None:
        if fid in vus or profondeur > 4:
            return
        vus.add(fid)
        enfants = lister(fid)
        arbre[chemin] = enfants
        print(f"{chemin} : {len(enfants)}", flush=True)
        for e in enfants:
            if e["dossier"] or e["raccourci"]:
                marcher(f"{chemin}/{e['nom']}", e["id"], profondeur + 1)

    marcher("Web of Deceit", RACINE)
    return arbre


def telecharger(arbre: dict, sortie: str) -> None:
    from PIL import Image

    taches = []
    for chemin, enfants in arbre.items():
        if any(x in chemin for x in IGNORES):
            continue
        for e in enfants:
            if e["dossier"] or e["raccourci"]:
                continue
            taches.append((chemin, e["nom"], e["id"]))
    print(len(taches), "fichiers")

    def prendre(tache):
        chemin, nom, fid = tache
        dossier = os.path.join(sortie, chemin)
        os.makedirs(dossier, exist_ok=True)
        cible = os.path.join(dossier, os.path.splitext(nom)[0] + ".jpg")
        if os.path.exists(cible) and os.path.getsize(cible) > 5000:
            return "deja"
        for _ in range(3):
            r = subprocess.run(
                ["curl", "-sL", "--max-time", "120",
                 f"https://drive.google.com/thumbnail?id={fid}&sz=w1000"],
                capture_output=True)
            if r.returncode == 0 and len(r.stdout) > 5000:
                try:
                    Image.open(io.BytesIO(r.stdout)).convert("RGB").save(
                        cible, "JPEG", quality=88)
                    return "ok"
                except Exception as exc:
                    dernier = f"image illisible : {exc}"
            else:
                dernier = f"curl {r.returncode}, {len(r.stdout)} octets"
        return f"ECHEC {chemin}/{nom} : {dernier}"

    with ThreadPoolExecutor(max_workers=8) as pool:
        resultats = list(pool.map(prendre, taches))
    rates = [r for r in resultats if r.startswith("ECHEC")]
    print(f"{len(resultats) - len(rates)} ok, {len(rates)} rates")
    for r in rates:
        print(" ", r)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--inventaire", default="")
    ap.add_argument("--telecharger", default="")
    ap.add_argument("--images", default="",
                    help="dossier des cartes deja telechargees "
                         "(medias/web-of-deceit-source, celui qui contient Scenarios/)")
    args = ap.parse_args()
    if not args.inventaire and not args.telecharger and not args.images:
        raise SystemExit(__doc__)

    if args.images:
        ecrire_images(args.images)
        if not args.inventaire and not args.telecharger:
            return 0

    arbre = inventorier()
    if args.inventaire:
        with open(args.inventaire, "w", encoding="utf-8") as f:
            json.dump(arbre, f, ensure_ascii=False, indent=1)
        print("inventaire ecrit :", args.inventaire)
    if args.telecharger:
        telecharger(arbre, args.telecharger)
    return 0



################################################################################
# Les images du jeu : assets/pics/wdXXX.jpg en 600x840
#
# Meme format que l'aspect Determination et The Spot, et meme raison : c'est le
# ratio natif de ces cartes, aucune deformation. `assets/pics/` est ignore par
# git, donc cette table EST la recette.
IMAGES = {
    # Scenario #1 — Shocker
    "wd001a": "Scenarios/Shocker/1a", "wd001b": "Scenarios/Shocker/1b",
    "wd002a": "Scenarios/Shocker/2a", "wd002b": "Scenarios/Shocker/2b",
    "wd003a": "Scenarios/Shocker/3a", "wd003b": "Scenarios/Shocker/3b",
    "wd004a": "Scenarios/Shocker/4a", "wd004b": "Scenarios/Shocker/4b",
    "wd005": "Scenarios/Shocker/5", "wd006": "Scenarios/Shocker/6",
    "wd007": "Scenarios/Shocker/7", "wd008": "Scenarios/Shocker/8",
    "wd009": "Scenarios/Shocker/9", "wd010": "Scenarios/Shocker/10",
    "wd011": "Scenarios/Shocker/11", "wd012": "Scenarios/Shocker/12",
    "wd013": "Scenarios/Shocker/13", "wd014": "Scenarios/Shocker/14",
    "wd015": "Scenarios/Shocker/16",
    # Crime Wave
    "wd016": "Modulars/Crime Wave/1", "wd017": "Modulars/Crime Wave/3",
    "wd018": "Modulars/Crime Wave/5", "wd019": "Modulars/Crime Wave/6",
    # Power Drain II
    "wd020": "Modulars/Power Drain II/1", "wd021": "Modulars/Power Drain II/2",
    "wd022": "Modulars/Power Drain II/3", "wd023": "Modulars/Power Drain II/4",
    "wd024": "Modulars/Power Drain II/5", "wd025": "Modulars/Power Drain II/6",
    # Bodyguard
    "wd026": "Campaign Setup Cards/Bodyguard/1", "wd027": "Campaign Setup Cards/Bodyguard/2",
    "wd028": "Campaign Setup Cards/Bodyguard/3", "wd029": "Campaign Setup Cards/Bodyguard/4",
    # Mise en place de la campagne
    "wd030": "Campaign Setup Cards/vote_for_fisk_standard",
    "wd031": "Campaign Setup Cards/vote_for_fisk_expert",
    "wd032": "Campaign Setup Cards/the-great-web-env",
    "wd033": "Campaign Setup Cards/expert-mode-ii-green-goblin-minion",
    "wd034": "Campaign Setup Cards/expert-mode-hobgoblin-minion",
}


def ecrire_images(source: str) -> None:
    """Ecrit assets/pics/wdXXX.jpg depuis les cartes telechargees."""
    from PIL import Image

    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sortie = os.path.join(racine, "assets", "pics")
    os.makedirs(sortie, exist_ok=True)

    faits, manquants = 0, []
    for carte, chemin in IMAGES.items():
        origine = os.path.join(source, chemin + ".jpg")
        if not os.path.exists(origine):
            manquants.append(carte)
            continue
        im = Image.open(origine).convert("RGB")
        largeur, hauteur = (840, 600) if im.width > im.height else (600, 840)
        im.resize((largeur, hauteur), Image.LANCZOS).save(
            os.path.join(sortie, carte + ".jpg"), "JPEG", quality=90)
        faits += 1
    print(f"{faits} images ecrites dans {sortie}")
    if manquants:
        print("MANQUANTES :", ", ".join(manquants))

if __name__ == "__main__":
    raise SystemExit(main())
