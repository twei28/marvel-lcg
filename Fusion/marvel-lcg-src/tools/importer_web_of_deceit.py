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
    # Scenario #2 — Electro. Le set du vilain est celui de DesignHacker
    # (« ELECTRO (2.0) »), les quatre complots et les deux A.I.M. Scientist
    # viennent du dossier de campagne et REMPLACENT ceux du set (livret p.17).
    "wd035": "Scenarios/ELECTRO (2.0)/ELECTRO_",
    "wd036": "Scenarios/ELECTRO (2.0)/ELECTRO_2",
    "wd037": "Scenarios/ELECTRO (2.0)/ELECTRO_3",
    "wd038a": "Scenarios/Electro (Web of Deceit)/scheme-1a",
    "wd038b": "Scenarios/Electro (Web of Deceit)/scheme-1b",
    "wd039a": "Scenarios/Electro (Web of Deceit)/scheme-2a",
    "wd039b": "Scenarios/Electro (Web of Deceit)/scheme-2b",
    "wd040": "Scenarios/ELECTRO (2.0)/ELECTRO_5",
    "wd041": "Scenarios/ELECTRO (2.0)/ELECTRO_6",
    "wd042": "Scenarios/ELECTRO (2.0)/ELECTRO_7",
    "wd043": "Scenarios/ELECTRO (2.0)/ELECTRO_8",
    "wd044": "Scenarios/Electro (Web of Deceit)/aim-scientist-10",
    "wd045": "Scenarios/ELECTRO (2.0)/ELECTRO_11",
    "wd046": "Scenarios/ELECTRO (2.0)/ELECTRO_12",
    "wd047": "Scenarios/ELECTRO (2.0)/ELECTRO_13",
    "wd048": "Scenarios/ELECTRO (2.0)/ELECTRO_14",
    "wd049": "Scenarios/ELECTRO (2.0)/ELECTRO_16",
    "wd050": "Scenarios/ELECTRO (2.0)/ELECTRO_17",
    "wd051": "Scenarios/ELECTRO (2.0)/ELECTRO_19",
    "wd052": "Scenarios/ELECTRO (2.0)/ELECTRO_21",
    "wd053": "Scenarios/ELECTRO (2.0)/ELECTRO_23",
    # Scenario #3 — The Lizard, et le modulaire City Sewers qui l'accompagne.
    "wd054a": "Scenarios/The Lizard/1a", "wd054b": "Scenarios/The Lizard/1b",
    "wd055a": "Scenarios/The Lizard/2a", "wd055b": "Scenarios/The Lizard/2b",
    "wd056a": "Scenarios/The Lizard/3a", "wd056b": "Scenarios/The Lizard/3b",
    "wd057": "Scenarios/The Lizard/4", "wd058": "Scenarios/The Lizard/5",
    "wd059": "Scenarios/The Lizard/6", "wd060": "Scenarios/The Lizard/8",
    "wd061": "Scenarios/The Lizard/9", "wd062": "Scenarios/The Lizard/11",
    "wd063": "Scenarios/The Lizard/15", "wd064": "Scenarios/The Lizard/16",
    "wd065": "Scenarios/The Lizard/17", "wd066": "Scenarios/The Lizard/18",
    "wd067": "Scenarios/The Lizard/19", "wd068": "Scenarios/The Lizard/21",
    "wd069": "Modulars/City Sewers/1", "wd070": "Modulars/City Sewers/2",
    "wd071": "Modulars/City Sewers/3", "wd072": "Modulars/City Sewers/5",
    "wd073": "Modulars/City Sewers/7",
    # Scenario #4 — Vulture. « Wingsuit-v2 » est la version a jour de la carte
    # joueur que la mise en place distribue ; « Wingsuit » est son premier jet.
    "wd074": "Scenarios/Vulture/1", "wd075": "Scenarios/Vulture/2",
    "wd076": "Scenarios/Vulture/3",
    "wd077a": "Scenarios/Vulture/4a", "wd077b": "Scenarios/Vulture/4b",
    "wd078": "Scenarios/Vulture/5", "wd079": "Scenarios/Vulture/7",
    "wd080": "Scenarios/Vulture/9", "wd081": "Scenarios/Vulture/12",
    "wd082": "Scenarios/Vulture/16", "wd083": "Scenarios/Vulture/17",
    "wd084": "Scenarios/Vulture/18", "wd085": "Scenarios/Vulture/19",
    "wd086": "Scenarios/Vulture/20", "wd087": "Scenarios/Vulture/22",
    "wd088": "Scenarios/Vulture/23", "wd089": "Scenarios/Vulture/24",
    "wd090": "Scenarios/Vulture/Wingsuit-v2",
    # Scenario #5 — Kingpin. `wd106` n'a pas d'illustration a lui : c'est le
    # patron des manigances CORROMPUES, qui n'existe pas dans le jeu physique
    # (voir son module). Il emprunte l'art de « Devil's Reign ».
    "wd091": "Scenarios/Kingpin/1", "wd092": "Scenarios/Kingpin/2",
    "wd093": "Scenarios/Kingpin/3",
    "wd094a": "Scenarios/Kingpin/4a", "wd094b": "Scenarios/Kingpin/4b",
    "wd095": "Scenarios/Kingpin/5", "wd096": "Scenarios/Kingpin/6",
    "wd097": "Scenarios/Kingpin/10", "wd098": "Scenarios/Kingpin/14",
    "wd099": "Scenarios/Kingpin/18", "wd100": "Scenarios/Kingpin/19",
    "wd101": "Scenarios/Kingpin/20", "wd102": "Scenarios/Kingpin/21",
    "wd103": "Scenarios/Kingpin/22", "wd104": "Scenarios/Kingpin/23",
    "wd105": "Scenarios/Kingpin/24", "wd106": "Scenarios/Kingpin/22",
    # Le modulaire Kraven the Hunter, qu'aucun scenario n'impose mais qui fait
    # partie du dossier de campagne.
    "wd107": "Modulars/Kraven the Hunter/1", "wd108": "Modulars/Kraven the Hunter/2",
    "wd109": "Modulars/Kraven the Hunter/3", "wd110": "Modulars/Kraven the Hunter/4",
    "wd111": "Modulars/Kraven the Hunter/5",
    # Les 50 cartes des cinq arbres de talents.
    "wd112": "Campaign - Rewards/Multiverse/1",
    "wd113": "Campaign - Rewards/Multiverse/2",
    "wd114": "Campaign - Rewards/Multiverse/3",
    "wd115": "Campaign - Rewards/Multiverse/4",
    "wd116": "Campaign - Rewards/Multiverse/5",
    "wd117": "Campaign - Rewards/Multiverse/6",
    "wd118": "Campaign - Rewards/Multiverse/7",
    "wd119": "Campaign - Rewards/Multiverse/8",
    "wd120": "Campaign - Rewards/Multiverse/9",
    "wd121": "Campaign - Rewards/Multiverse/10",
    "wd122": "Campaign - Rewards/Radioactive/1",
    "wd123": "Campaign - Rewards/Radioactive/2",
    "wd124": "Campaign - Rewards/Radioactive/3",
    "wd125": "Campaign - Rewards/Radioactive/4",
    "wd126": "Campaign - Rewards/Radioactive/5",
    "wd127": "Campaign - Rewards/Radioactive/6",
    "wd128": "Campaign - Rewards/Radioactive/7",
    "wd129": "Campaign - Rewards/Radioactive/8",
    "wd130": "Campaign - Rewards/Radioactive/9",
    "wd131": "Campaign - Rewards/Radioactive/10",
    "wd132": "Campaign - Rewards/Spider-Sense/1",
    "wd133": "Campaign - Rewards/Spider-Sense/2",
    "wd134": "Campaign - Rewards/Spider-Sense/3",
    "wd135": "Campaign - Rewards/Spider-Sense/4",
    "wd136": "Campaign - Rewards/Spider-Sense/5",
    "wd137": "Campaign - Rewards/Spider-Sense/6",
    "wd138": "Campaign - Rewards/Spider-Sense/7",
    "wd139": "Campaign - Rewards/Spider-Sense/8",
    "wd140": "Campaign - Rewards/Spider-Sense/9",
    "wd141": "Campaign - Rewards/Spider-Sense/10",
    "wd152": "Campaign - Rewards/Web-Spinner/1",
    "wd153": "Campaign - Rewards/Web-Spinner/2",
    "wd154": "Campaign - Rewards/Web-Spinner/3",
    "wd155": "Campaign - Rewards/Web-Spinner/4",
    "wd156": "Campaign - Rewards/Web-Spinner/5",
    "wd157": "Campaign - Rewards/Web-Spinner/6",
    "wd158": "Campaign - Rewards/Web-Spinner/7",
    "wd159": "Campaign - Rewards/Web-Spinner/8",
    "wd160": "Campaign - Rewards/Web-Spinner/9",
    "wd161": "Campaign - Rewards/Web-Spinner/10",
    "wd142": "Campaign - Rewards/Symbiosis/1_-_Black_Suit",
    "wd143": "Campaign - Rewards/Symbiosis/2_-_Greater_Power",
    "wd144": "Campaign - Rewards/Symbiosis/3_-_Greater_Responsibility",
    "wd145": "Campaign - Rewards/Symbiosis/4_-_Flee_the_Scene",
    "wd146": "Campaign - Rewards/Symbiosis/5_-_Not_My_Problem",
    "wd147": "Campaign - Rewards/Symbiosis/6_-_Out_of_Patience",
    "wd148": "Campaign - Rewards/Symbiosis/7_-_Monstrous",
    "wd149": "Campaign - Rewards/Symbiosis/8_-_Monstrous",
    "wd150": "Campaign - Rewards/Symbiosis/9_-_Get_it_Off",
    "wd151": "Campaign - Rewards/Symbiosis/10_-_Unity",
    # La variante UNDERLING du set Vulture : seules quatre de ses quatorze
    # cartes sont neuves, les dix autres sont celles du set principal.
    "wd162": "Scenarios/Vulture/Underling/1",
    "wd163": "Scenarios/Vulture/Underling/2",
    "wd164": "Scenarios/Vulture/Underling/3",
    "wd165": "Scenarios/Vulture/Underling/14",
}

# Les cartes PAYSAGE dont le fichier source est stocke debout.
#
# ⚠ Ripper3 exporte TOUTES ses cartes en 1000x1433, y compris les complots et
# les manigances, qui sont des cartes paysage tournees d'un quart de tour. Sans
# cette table, `im.width > im.height` est faux et la carte entre dans le jeu en
# 600x840 avec son texte a la verticale — c'est ce qui est arrive au lot 1.
# Les cartes de DesignHacker, elles, sont deja dans le bon sens (1000x716).
PAYSAGE = {
    "wd002a", "wd002b", "wd003a", "wd003b", "wd004a", "wd004b",  # complots Shocker
    "wd011", "wd015",                                            # manigances Shocker
    "wd020",                                                     # Power Drain II
    "wd038a", "wd038b", "wd039a", "wd039b",                      # complots Electro
    "wd055a", "wd056b",                                          # complots The Lizard
    "wd069",                                                     # City Sewers
    "wd077a", "wd077b", "wd084", "wd085",                        # complot et manigances Vulture
    "wd094a", "wd094b", "wd103", "wd104", "wd106",               # complot et manigances Kingpin
    "wd107",                                                     # Kraven the Hunter
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
        if carte in PAYSAGE:
            im = im.rotate(90, expand=True)
        largeur, hauteur = (840, 600) if im.width > im.height else (600, 840)
        im.resize((largeur, hauteur), Image.LANCZOS).save(
            os.path.join(sortie, carte + ".jpg"), "JPEG", quality=90)
        faits += 1
    print(f"{faits} images ecrites dans {sortie}")
    if manquants:
        print("MANQUANTES :", ", ".join(manquants))

if __name__ == "__main__":
    raise SystemExit(main())
