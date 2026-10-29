"""Ramene tous les scans au format des cartes officielles.

Pourquoi : les cartes fan-made sont livrees en 1500x2150, bien plus grandes que
les officielles, pour un plateau qui les affiche a 127 px et les agrandit au
survol.

⚠ LA REFERENCE EST LE SCAN FRANCAIS, PAS L'ANGLAIS.

Le jeu se joue en francais : les cartes officielles viennent de assets/pics-fr,
qui font 615x880. Les scans anglais de assets/pics font 300x435, moitie moins.
Aligner les fan-made sur 300 les rendait donc PLUS FLOUES que les officielles
affichees a cote, l'inverse du but recherche. La cible est 615.

⚠ LA REGLE EST SUR LE PETIT COTE, PAS SUR LA LARGEUR.

464 cartes officielles sont en PAYSAGE (435x300) : les complots. Un critere
« largeur > 615 » les aurait toutes ecrasees. On ramene donc le petit
cote a 615 et on laisse le grand suivre, ce qui donne 615x880 en portrait et
880x615 en paysage, sans jamais deformer ni changer l'orientation.

Une image dont le petit cote vaut deja 615 ou moins n'est pas touchee.

    python3 outils/uniformiser-scans.py --etat        # ne modifie rien
    python3 outils/uniformiser-scans.py --sauvegarde  # copie les originaux
    python3 outils/uniformiser-scans.py --appliquer   # redimensionne
"""
import glob
import os
import shutil
import sys

from PIL import Image

# ⚠ CHEMINS RELATIFS AU DEPOT (29/10/2026) : avant, un chemin Windows/WSL en dur
# (/mnt/c/Users/arnau/...) propre a UNE machine. Sur toute autre machine (ce Linux
# compris), `glob` sur un dossier inexistant ne leve rien : --etat/--appliquer
# tournaient en silence sans jamais rien trouver ni rien faire, comme si tout etait
# deja a jour. Repere par l'utilisateur ("j'ai l'impression qu'on a fait une
# regression") en recherchant des scans manquants : voir git log de ce fichier.
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PICS = os.path.join(RACINE, "Fusion", "marvel-lcg-src", "assets", "pics")
SAUVEGARDE = os.path.join(RACINE, "sauvegardes-serveur", "scans-originaux")
PETIT_COTE = 615
QUALITE = 88


def source(chemin):
    """Le fichier a LIRE pour produire `chemin`.

    L'original sauvegarde s'il existe, le fichier en place sinon. Sans cette
    regle, relancer l'outil avec une cible plus haute reagrandirait une image
    deja reduite : le plateau y gagnerait des pixels et pas un detail.
    """
    garde = os.path.join(SAUVEGARDE, os.path.basename(chemin))
    return garde if os.path.exists(garde) else chemin


def a_traiter():
    """Les images dont le petit cote depasse la cible, avec leurs dimensions.

    ⚠ On mesure le fichier EN PLACE (`chemin`), pas `source(chemin)`. Une
    image deja reduite reste en place a 615 px ou moins, mais son original
    sauvegarde, lui, fait toujours 1500x2150 : mesurer l'original aurait
    fait reapparaitre indefiniment les 897 fan-made deja traites (constate
    le 06/09/2026 : --etat en trouvait 1946 alors qu'aucun fichier reel ne
    depassait 615 px). `source()` reste reserve a la LECTURE DES PIXELS au
    moment de redimensionner, dans `appliquer()`.
    """
    sorties = []
    for chemin in sorted(glob.glob(os.path.join(PICS, "*.jpg"))
                         + glob.glob(os.path.join(PICS, "*.png"))):
        try:
            with Image.open(chemin) as im:
                largeur, hauteur = im.size
        except Exception:
            continue
        if min(largeur, hauteur) > PETIT_COTE:
            sorties.append((chemin, largeur, hauteur))
    return sorties


def cible(largeur: int, hauteur: int) -> tuple[int, int]:
    """Nouvelles dimensions : le petit cote a 300, le grand au prorata."""
    facteur = PETIT_COTE / min(largeur, hauteur)
    return (max(1, round(largeur * facteur)), max(1, round(hauteur * facteur)))


def etat():
    liste = a_traiter()
    poids = sum(os.path.getsize(c) for c, _, _ in liste)
    print(f"a traiter : {len(liste)} fichiers, {poids / 1e9:.2f} Go")
    portrait = sum(1 for _, w, h in liste if h >= w)
    print(f"  portrait : {portrait}   paysage : {len(liste) - portrait}")
    print("\nexemples de conversion :")
    for chemin, w, h in liste[:5]:
        nw, nh = cible(w, h)
        print(f"  {os.path.basename(chemin):24} {w}x{h} -> {nw}x{nh}")


def sauvegarder():
    liste = a_traiter()
    os.makedirs(SAUVEGARDE, exist_ok=True)
    faits = 0
    for chemin, _, _ in liste:
        destination = os.path.join(SAUVEGARDE, os.path.basename(chemin))
        # Une sauvegarde deja faite ne doit pas etre ecrasee par une image
        # deja reduite : on ne recopie jamais par-dessus.
        if os.path.exists(destination):
            continue
        shutil.copy2(chemin, destination)
        faits += 1
        if faits % 300 == 0:
            print(f"  {faits} copies...")
    total = sum(os.path.getsize(os.path.join(SAUVEGARDE, f))
                for f in os.listdir(SAUVEGARDE))
    print(f"sauvegarde : {faits} nouveaux fichiers, "
          f"{len(os.listdir(SAUVEGARDE))} au total, {total / 1e9:.2f} Go")
    print(f"dans {SAUVEGARDE}")


def appliquer():
    liste = a_traiter()
    if not liste:
        print("rien a reduire : toutes les images sont deja a "
              f"{PETIT_COTE} px ou moins.")
        return

    # ⚠ Verification FICHIER PAR FICHIER, pas un comptage global. Compter
    # juste `len(os.listdir(SAUVEGARDE)) < len(liste)` laissait passer un
    # pack tout neuf des que la sauvegarde cumulee d'anciens packs suffisait
    # en NOMBRE, sans que les nouveaux fichiers y soient pour autant : la
    # sauvegarde etait "assez grande" sans etre la bonne.
    manquants = [chemin for chemin, _, _ in liste
                 if not os.path.exists(os.path.join(SAUVEGARDE, os.path.basename(chemin)))]
    if manquants:
        print(f"REFUS : {len(manquants)} original(aux) sur {len(liste)} non "
              "sauvegarde(s). Lance --sauvegarde d'abord.", file=sys.stderr)
        raise SystemExit(1)

    avant = sum(os.path.getsize(c) for c, _, _ in liste)
    faits = 0
    for chemin, w, h in liste:
        nw, nh = cible(w, h)
        with Image.open(source(chemin)) as im:
            # LANCZOS : c'est une REDUCTION, le filtre le plus net a ce jeu.
            reduite = im.convert("RGB").resize((nw, nh), Image.Resampling.LANCZOS)
            reduite.save(chemin, "JPEG", quality=QUALITE, optimize=True)
        faits += 1
        if faits % 300 == 0:
            print(f"  {faits} images...")
    apres = sum(os.path.getsize(c) for c, _, _ in liste)
    print(f"termine : {faits} images, {avant / 1e9:.2f} Go -> {apres / 1e9:.2f} Go")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "--etat"
    if mode == "--etat":
        etat()
    elif mode == "--sauvegarde":
        sauvegarder()
    elif mode == "--appliquer":
        appliquer()
    else:
        print(__doc__)
        raise SystemExit(2)
