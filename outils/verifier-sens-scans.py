"""Une carte de type paysage doit etre stockee en PAYSAGE.

    python3 outils/verifier-sens-scans.py            # controle
    python3 outils/verifier-sens-scans.py --details  # nomme chaque carte

⚠ POURQUOI CE CONTROLE EXISTE. Le 15/09/2026, TRENTE manigances annexes
s'affichaient a l'envers en jeu. Constat de l'utilisateur, capture a l'appui :
« et cette carte est a l'envers ». Aucun outil ne pouvait l'attraper : il
fallait un oeil, carte par carte.

⚠ LA REGLE, MESUREE ET NON DEDUITE. Le moteur ne tourne un scan QUE s'il est en
paysage sur le disque (`ImageCreator.TryRotateImage`, `engine/lib/image_creator.py`) :

    if width > height:
        img_io = img_io.rotate(90, expand=True)

Le plateau applique ensuite un quart de tour en CSS, dans l'autre sens, et la
carte retombe a l'endroit. Un fichier deja en portrait n'est donc PAS tourne par
le moteur : il arrive couche a l'ecran.

D'ou la regle : ce que le jeu affiche en paysage (MainScheme, SideScheme,
Status — la meme liste que `paysageSelonTypePapier` cote plateau) doit etre
stocke en paysage, largeur > hauteur.

⚠ LES SEPT EXCEPTIONS SONT CONNUES ET ASSUMEES. Sept scans sont en portrait et
s'affichent pourtant correctement : ils ont ete verifies a l'oeil le
15/09/2026 et ne doivent PAS etre convertis sans la meme verification. Les
convertir a l'aveugle les mettrait a l'envers a leur tour.
"""
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JEU = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
TYPES_PAYSAGE = ("MainScheme", "SideScheme", "Status")

# ⚠ EN PORTRAIT SUR LE DISQUE, ET CORRECTS A L'ECRAN. Verifies a l'oeil le
# 15/09/2026, lors de la correction des trente manigances a l'envers. Les
# convertir A L'AVEUGLE les mettrait a l'envers a leur tour : toute modification
# de cette liste demande la meme verification, carte par carte, dans le jeu.
EXCEPTIONS = {
    # Une carte SANS ART, rendue en texte par le moteur : son fichier n'est pas
    # un scan de carte et la regle ne s'y applique pas (fiche du 15/09/2026).
    "57039a",   # Choosing Sides
    # Cinq scans fan-made livres en portrait et corrects en jeu.
    "ab013",    # Crack in the Multiverse
    "sg020",    # Discord in the Branches
    "nt014",    # Cemented
    "ip017",    # Reign's End
    "ip035",    # "You're in My World"
}


def dossiers_images():
    for nom in ("assets/pics", "assets/pics-fr"):
        chemin = os.path.join(JEU, nom)
        if os.path.isdir(chemin):
            yield chemin


def scans_connus():
    """Le chemin de chaque image, par identifiant (sans extension)."""
    par_id = {}
    for dossier in dossiers_images():
        for racine, _, fichiers in os.walk(dossier):
            for f in fichiers:
                base, ext = os.path.splitext(f)
                if ext.lower() in (".jpg", ".jpeg", ".png", ".webp"):
                    par_id.setdefault(base, os.path.join(racine, f))
    return par_id


def cartes_paysage():
    with open(os.path.join(JEU, "data", "cards.json"), encoding="utf-8") as f:
        catalogue = json.load(f)
    for lot in catalogue.values():
        if not isinstance(lot, list):
            continue
        for carte in lot:
            if isinstance(carte, dict) and carte.get("type") in TYPES_PAYSAGE:
                yield carte


def main() -> int:
    details = "--details" in sys.argv[1:]
    try:
        from PIL import Image
    except ImportError:
        print("Pillow manquant : python3 -m pip install Pillow", file=sys.stderr)
        return 2

    par_id = scans_connus()
    a_lenvers, sans_scan, vus = [], 0, 0
    for carte in cartes_paysage():
        identifiant = str(carte.get("card_id") or "")
        chemin = par_id.get(identifiant)
        if not chemin:
            sans_scan += 1
            continue
        try:
            with Image.open(chemin) as image:
                largeur, hauteur = image.size
        except Exception:
            continue
        vus += 1
        if largeur <= hauteur and identifiant not in EXCEPTIONS:
            a_lenvers.append((identifiant, carte.get("name") or "?", largeur, hauteur))

    print(f"cartes de type paysage avec un scan : {vus}")
    print(f"  (sans scan en local, ignorees : {sans_scan})")
    if not a_lenvers:
        print("  ok   toutes sont stockees en paysage")
        return 0

    print(f"\nECHEC : {len(a_lenvers)} scan(s) en portrait, donc a l'envers en jeu.")
    for identifiant, nom, largeur, hauteur in (a_lenvers if details else a_lenvers[:15]):
        print(f"  - {identifiant:14} {nom[:40]:40} {largeur}x{hauteur}")
    if not details and len(a_lenvers) > 15:
        print(f"  ... et {len(a_lenvers) - 15} autres (--details pour tout voir)")
    print("\nLe moteur ne tourne que ce qui est en paysage sur le disque.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
