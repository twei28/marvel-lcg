"""Fabrique des visuels de substitution pour un pack maison, depuis cards.json.

POURQUOI. Un pack transcrit d'un scan arrive avec ses images. Un pack INVENTE
n'en a aucune, et il n'existe nulle part de visuel a recuperer. Le plateau
affiche alors un rectangle avec le nom de la carte, et le pack detonne a cote
des autres. Cet outil dessine une carte lisible a partir des seules donnees :
nom, cout, type, traits, statistiques, texte imprime.

Ce n'est PAS de l'illustration. Le but est qu'on puisse jouer et relire une
carte sans survoler la table. Les vraies images, quand elles existeront, se
posent au meme endroit avec le meme nom de fichier et remplacent tout ceci sans
toucher au code.

Usage
-----
    python3.10 tools/generer_visuels_pack.py <pack> [--sortie assets/pics]
    python3.10 tools/generer_visuels_pack.py squirrel_girl

Les fichiers sont ecrits en `<card_id>.png`. L'extension est obligatoire :
`engine/file/cache.py` la lit explicitement (voir §4 du guide de creation).
"""
import argparse
import html
import json
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

LARGEUR, HAUTEUR = 420, 587          # proportion d'une carte a jouer (1:1.397)
MARGE = 16

POLICES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/mnt/c/Windows/Fonts/arial.ttf",
]
POLICES_GRASSES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/mnt/c/Windows/Fonts/arialbd.ttf",
]

# Couleur de fond par aspect, puis par nature pour les cartes Rencontre.
COULEURS_ASPECT = {
    "Hero":       ((60, 62, 70), (28, 30, 36)),
    "Leadership": ((38, 74, 140), (18, 36, 70)),
    "Justice":    ((150, 122, 26), (74, 60, 12)),
    "Aggression": ((150, 44, 40), (74, 20, 18)),
    "Protection": ((40, 118, 74), (18, 58, 36)),
    "Basic":      ((80, 80, 86), (38, 38, 42)),
}
COULEUR_RENCONTRE = ((92, 30, 30), (40, 12, 12))

# Les cartes Rencontre n'ont pas de Class : on les reconnait a leur type.
TYPES_RENCONTRE = {"Minion", "Treachery", "SideScheme", "Attachment",
                   "Environment", "Villain", "MainScheme", "Obligation"}

# Icones de ressource. Codage du moteur (src/game/element/resources.py,
# RES_TEXT) : R physique, B mentale, Y energie, G wild. Sans elles, impossible
# de savoir ce que la carte rapporte quand on la depense pour en payer une
# autre, ce qui est la moitie des decisions d'un tour.
RESSOURCES = {
    "R": ((176, 58, 52), "physique"),
    "B": ((56, 96, 168), "mentale"),
    "Y": ((198, 158, 44), "energie"),
    "G": ((132, 132, 140), "wild"),
}

STATS_AFFICHEES = [("ATK", (176, 58, 52)), ("THW", (56, 96, 168)),
                   ("DEF", (58, 132, 78)), ("REC", (168, 132, 48)),
                   ("SCH", (140, 70, 150)), ("HP", (196, 196, 200))]


def police(chemins, taille):
    for c in chemins:
        if os.path.exists(c):
            return ImageFont.truetype(c, taille)
    return ImageFont.load_default()


def texte_lisible(brut):
    """Transforme le texte imprime en texte simple affichable.

    Le champ `text` de cards.json porte du balisage : <b>, <i>, [[TRAIT]],
    [star], et des entites HTML. Rendu tel quel, il est illisible.
    """
    if not brut:
        return ""
    t = brut.replace("\\n", "\n")
    t = re.sub(r"<br\s*/?>", "\n", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = t.replace("[[", "").replace("]]", "")
    t = t.replace("[star]", "*").replace("[wild]", "(wild)")
    return html.unescape(t)


def couleurs(carte):
    if carte.get("type") in TYPES_RENCONTRE and not carte.get("desc", {}).get("Class"):
        return COULEUR_RENCONTRE
    classe = (carte.get("desc") or {}).get("Class", "Basic")
    return COULEURS_ASPECT.get(classe, COULEURS_ASPECT["Basic"])


def degrade(haut, bas):
    img = Image.new("RGB", (LARGEUR, HAUTEUR), haut)
    d = ImageDraw.Draw(img)
    for y in range(HAUTEUR):
        k = y / HAUTEUR
        d.line([(0, y), (LARGEUR, y)],
               fill=tuple(int(haut[i] + (bas[i] - haut[i]) * k) for i in range(3)))
    return img


def dessiner(carte, chemin):
    haut, bas = couleurs(carte)
    img = degrade(haut, bas)
    d = ImageDraw.Draw(img)
    desc = carte.get("desc") or {}

    f_nom = police(POLICES_GRASSES, 26)
    f_petit = police(POLICES, 15)
    f_petit_gras = police(POLICES_GRASSES, 15)
    f_texte = police(POLICES, 15)
    f_cout = police(POLICES_GRASSES, 24)

    d.rectangle([4, 4, LARGEUR - 5, HAUTEUR - 5], outline=(232, 232, 236), width=3)

    # --- nom, sur deux lignes si besoin -------------------------------------
    nom = (carte.get("name") or "").replace("* ", "")
    lignes = textwrap.wrap(nom, width=18) or [""]
    y = MARGE + 6
    for ligne in lignes[:2]:
        d.text((MARGE + 56, y), ligne, font=f_nom, fill=(255, 255, 255))
        y += 30

    # --- cout ---------------------------------------------------------------
    if desc.get("Cost") is not None:
        d.ellipse([MARGE, MARGE, MARGE + 44, MARGE + 44], fill=(248, 248, 250))
        c = str(desc["Cost"])
        bb = d.textbbox((0, 0), c, font=f_cout)
        d.text((MARGE + 22 - (bb[2] - bb[0]) / 2, MARGE + 22 - (bb[3] - bb[1]) / 2 - 3),
               c, font=f_cout, fill=(24, 24, 28))

    # --- bandeau type et traits ---------------------------------------------
    y = max(y, MARGE + 52) + 6
    d.rectangle([MARGE, y, LARGEUR - MARGE, y + 26], fill=(0, 0, 0, 90))
    etiquette = carte.get("type", "")
    traits = ", ".join(carte.get("traits") or [])
    d.text((MARGE + 8, y + 5), etiquette.upper(), font=f_petit_gras, fill=(255, 255, 255))
    if traits:
        d.text((MARGE + 8 + 110, y + 5), traits[:34], font=f_petit, fill=(214, 214, 220))
    y += 34

    # --- zone d'illustration absente : on le DIT, plutot que de faire semblant
    hauteur_illu = 150
    d.rectangle([MARGE, y, LARGEUR - MARGE, y + hauteur_illu],
                fill=(0, 0, 0), outline=(120, 120, 128))
    msg = "illustration a venir"
    bb = d.textbbox((0, 0), msg, font=f_petit)
    d.text((LARGEUR / 2 - (bb[2] - bb[0]) / 2, y + hauteur_illu / 2 - 8),
           msg, font=f_petit, fill=(120, 120, 128))
    y += hauteur_illu + 10

    # --- statistiques --------------------------------------------------------
    presentes = [(cle, coul) for cle, coul in STATS_AFFICHEES if desc.get(cle)]
    if presentes:
        x = MARGE
        for cle, coul in presentes:
            d.ellipse([x, y, x + 46, y + 46], fill=coul, outline=(240, 240, 245), width=2)
            v = str(desc[cle])
            bb = d.textbbox((0, 0), v, font=f_cout)
            d.text((x + 23 - (bb[2] - bb[0]) / 2, y + 20 - (bb[3] - bb[1]) / 2),
                   v, font=f_cout, fill=(255, 255, 255))
            bb = d.textbbox((0, 0), cle, font=f_petit)
            d.text((x + 23 - (bb[2] - bb[0]) / 2, y + 48), cle,
                   font=f_petit, fill=(226, 226, 230))
            x += 58
        y += 74

    # --- texte imprime -------------------------------------------------------
    corps = texte_lisible(carte.get("text"))
    if corps:
        bas_cadre = HAUTEUR - MARGE - 42
        d.rectangle([MARGE, y, LARGEUR - MARGE, bas_cadre],
                    fill=(250, 249, 244), outline=(200, 198, 190))

        # Le texte RETRECIT pour tenir, il ne se coupe pas. Une carte dont la
        # regle est tronquee en silence est pire qu'une carte sans image : on
        # croit la lire alors qu'il en manque un bout.
        for taille, largeur in ((15, 46), (14, 49), (13, 53), (12, 57), (11, 62)):
            f = police(POLICES, taille)
            interligne = taille + 3
            lignes_txt = []
            for paragraphe in corps.split("\n"):
                lignes_txt.extend(textwrap.wrap(paragraphe, width=largeur) or [""])
            if y + 8 + len(lignes_txt) * interligne <= bas_cadre - 4:
                break
        else:
            print(f"  ATTENTION {carte['card_id']} {carte.get('name','')} : "
                  f"texte trop long meme en corps 11, il sera coupe")

        ty = y + 8
        for ligne in lignes_txt:
            if ty > bas_cadre - interligne:
                break
            d.text((MARGE + 8, ty), ligne, font=f, fill=(28, 28, 32))
            ty += interligne

    # --- ressources generees, en bas a gauche comme sur une vraie carte -----
    res = str(desc.get("RES") or "")
    x = MARGE
    for lettre in res:
        coul, _ = RESSOURCES.get(lettre.upper(), ((110, 110, 116), "?"))
        d.ellipse([x, HAUTEUR - MARGE - 34, x + 28, HAUTEUR - MARGE - 6],
                  fill=coul, outline=(244, 244, 248), width=2)
        bb = d.textbbox((0, 0), lettre.upper(), font=f_petit_gras)
        d.text((x + 14 - (bb[2] - bb[0]) / 2, HAUTEUR - MARGE - 28),
               lettre.upper(), font=f_petit_gras, fill=(255, 255, 255))
        x += 34

    # --- pied : rappel que ce visuel est provisoire --------------------------
    pied = f"{carte['card_id']}  ·  visuel provisoire"
    d.text((max(x + 6, MARGE), HAUTEUR - MARGE - 26), pied,
           font=f_petit, fill=(226, 226, 232))

    img.save(chemin, "PNG")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--cartes", default="data/cards.json")
    ap.add_argument("--sortie", default="assets/pics")
    ap.add_argument("--ecraser", action="store_true",
                    help="refaire les visuels deja presents")
    args = ap.parse_args()

    d = json.load(open(args.cartes, encoding="utf-8"))
    assert args.pack in d, f"pack inconnu : {args.pack}"
    os.makedirs(args.sortie, exist_ok=True)

    faits, sautes = 0, 0
    for carte in d[args.pack]:
        if not isinstance(carte, dict) or not carte.get("card_id"):
            continue
        cid = carte["card_id"]
        # Ne jamais ecraser une VRAIE image deja deposee, quelle que soit son
        # extension : ce serait remplacer une illustration par un pis-aller.
        existantes = [e for e in (".png", ".jpg", ".jpeg", ".webp")
                      if os.path.exists(os.path.join(args.sortie, cid + e))]
        if existantes and not args.ecraser:
            sautes += 1
            continue
        dessiner(carte, os.path.join(args.sortie, cid + ".png"))
        faits += 1
    print(f"{faits} visuels ecrits dans {args.sortie}"
          + (f", {sautes} deja presents et conserves" if sautes else ""))


if __name__ == "__main__":
    main()
