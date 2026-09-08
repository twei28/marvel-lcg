"""Les VIGNETTES des scans : la version que le plateau affiche vraiment.

POURQUOI (08/09/2026, « les cartes ne sont pas plus nettes »)
------------------------------------------------------------
Un scan fait 615 px de large ; sur la table, une carte en fait 106 a 127. Le
navigateur reduit donc de 5 pour 1 en une passe, et son filtre ecrase le
texte : « Une fois revelee : cherchez la manigance annexe... » devient une
bouillie grise. Un filtre d'accentuation en CSS n'y change presque rien : ce
qui est perdu a la reduction ne revient pas.

Ce qui marche, mesure sur un banc de comparaison agrandi trois fois : REDUIRE
SUR LE SERVEUR avec un filtre de Lanczos, puis un masque flou, a DEUX FOIS la
taille d'affichage. Le navigateur n'a plus qu'une reduction de moitie a faire,
qu'il reussit bien, et le texte redevient lisible.

CE QUE FAIT L'OUTIL
-------------------
Pour chaque image de assets/pics et assets/pics-fr, ecrit
assets/vignettes/<meme nom>.jpg avec le PETIT COTE a 246 px (le grand suit,
sans deformer ni changer l'orientation : 246x352 en portrait, 352x246 en
paysage). Le moteur sert ces fichiers sous /vignette/<nom>, et retombe sur le
scan complet si la vignette manque.

⚠ INCREMENTAL : une vignette plus recente que sa source n'est pas refaite.
Relancer l'outil apres un ajout de pack ne coute que le pack.

⚠ TOURNE AUSSI SUR LE SERVEUR, a chaque deploiement (deployer.ps1) : les
vignettes ne voyagent pas dans l'archive, elles se recalculent sur place a
partir des scans qui y sont deja.

    python3 tools/generer_vignettes.py            # genere ce qui manque
    python3 tools/generer_vignettes.py --etat     # compte, sans rien ecrire
    python3 tools/generer_vignettes.py --forcer   # refait tout
"""
import os
import sys
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, ImageFilter

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCES = [os.path.join(RACINE, "assets", "pics"), os.path.join(RACINE, "assets", "pics-fr")]
DESTINATION = os.path.join(RACINE, "assets", "vignettes")
PETIT_COTE = 246
QUALITE = 86
EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def cible(largeur: int, hauteur: int) -> tuple[int, int]:
    """Le petit cote a PETIT_COTE, le grand au prorata. Jamais agrandi."""
    facteur = min(1.0, PETIT_COTE / max(1, min(largeur, hauteur)))
    return (max(1, round(largeur * facteur)), max(1, round(hauteur * facteur)))


def a_faire(forcer: bool = False) -> list[tuple[str, str]]:
    """(source, destination) des vignettes manquantes ou perimees."""
    sorties = []
    for dossier in SOURCES:
        if not os.path.isdir(dossier):
            continue
        for nom in sorted(os.listdir(dossier)):
            base, ext = os.path.splitext(nom)
            if ext.lower() not in EXTENSIONS:
                continue
            src = os.path.join(dossier, nom)
            dst = os.path.join(DESTINATION, base + ".jpg")
            if not forcer and os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                continue
            sorties.append((src, dst))
    return sorties


def generer_une(paire: tuple[str, str]) -> str | None:
    """Rend None si tout va bien, sinon le message d'erreur."""
    src, dst = paire
    try:
        with Image.open(src) as im:
            im = im.convert("RGB")
            # LANCZOS : c'est une REDUCTION, le filtre le plus net a ce jeu.
            reduite = im.resize(cible(*im.size), Image.Resampling.LANCZOS)
            # Le masque flou rend aux bords le contraste que la reduction a
            # pris. Reglage retenu sur le banc du 08/09/2026 : plus fort, les
            # lettres blanches prennent un lisere noir.
            nette = reduite.filter(ImageFilter.UnsharpMask(radius=1.0, percent=110, threshold=1))
            tmp = dst + ".tmp"
            nette.save(tmp, "JPEG", quality=QUALITE, optimize=True)
            os.replace(tmp, dst)
        return None
    except Exception as exc:  # une image illisible ne doit pas arreter les 10 000 autres
        return f"{os.path.basename(src)} : {exc}"


def main(arguments: list[str]) -> int:
    forcer = "--forcer" in arguments
    liste = a_faire(forcer)
    if "--etat" in arguments:
        deja = len(os.listdir(DESTINATION)) if os.path.isdir(DESTINATION) else 0
        print(f"vignettes presentes : {deja}   a generer : {len(liste)}   dans {DESTINATION}")
        return 0
    if not liste:
        print("vignettes : rien a faire, tout est a jour.")
        return 0
    os.makedirs(DESTINATION, exist_ok=True)
    erreurs = []
    faites = 0
    with ProcessPoolExecutor() as pool:
        for resultat in pool.map(generer_une, liste, chunksize=16):
            faites += 1
            if resultat:
                erreurs.append(resultat)
            if faites % 500 == 0:
                print(f"  {faites}/{len(liste)}...", flush=True)
    print(f"vignettes : {faites - len(erreurs)} generees, {len(erreurs)} en erreur, dans {DESTINATION}")
    for e in erreurs[:10]:
        print("  ", e, file=sys.stderr)
    return 1 if erreurs else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
