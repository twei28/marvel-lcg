"""Refait en francais les pages d'un livret de campagne fan-made (texte du PDF remplace).

Le livret est vectoriel : chaque bloc de texte anglais est retire du PDF (redaction,
texte seul, fond et images intacts), puis le francais est ecrit a la meme place, dans
les polices du livret. Les pages sont rendues comme `pages_livret.py` les rend, dans
`public/stories/<code>/fr/`, sous le meme nom que la page anglaise.
L'ecran de campagne ne les cherche que si `data/campagnes/<code>.json` declare `"livret_fr": true`.

    python3 tools/livret_fr.py hunting_season [--pour-de-vrai]

Traductions : `tools/livrets_fr/<code>.json`, une entree par bloc (`p<page>b<bloc>`,
numerotation de PyMuPDF). Un titre sur deux lignes separe ses lignes par « | ».
Polices : le zip « All Marvel Champions Template Fonts.zip » a la racine du depot,
et Lucida Sans Unicode de Windows pour les intertitres (VICTOIRE :, DEFAITE :...).
"""
import argparse
import json
import os
import re
import sys
import tempfile
import zipfile

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_livret import CARTES, COUVERTURE, DEPOT, LARGEUR, RACINE, nom_fichier  # noqa: E402

ZIP_POLICES = os.path.join(DEPOT, "All Marvel Champions Template Fonts.zip")
LUCIDA = "/mnt/c/Windows/Fonts/l_10646.ttf"
POLICES = {
    "regular": "AvenirNextLTPro-Regular.otf",
    "italic": "AvenirNextLTPro-It.otf",
    "bold": "AvenirNextLTPro-Bold.otf",
    "exo": "Exo2Mod-Bold.ttf",
}


def pages_du_livret(carte):
    """Page du PDF -> nom de fichier, avec les memes noms que pages_livret.py."""
    a_rendre = {1: COUVERTURE}
    for rang, page in enumerate(carte["regles_campagne"], 1):
        a_rendre[page] = nom_fichier(0, None, "regles", rang)
    for scenario, numero, intro, regles, epilogue in carte["scenarios"]:
        for role, pages in (("intro", intro), ("regles", regles), ("epilogue", epilogue)):
            pages = pages if isinstance(pages, list) else ([pages] if pages else [])
            for rang, page in enumerate(pages, 1):
                a_rendre[page] = nom_fichier(numero, scenario, role, rang)
    return a_rendre


def texte_span(span):
    return span["text"] if "text" in span else "".join(c["c"] for c in span["chars"])


def couleur(entier):
    return ((entier >> 16) & 255) / 255, ((entier >> 8) & 255) / 255, (entier & 255) / 255


def inclinaisons(page):
    """(x, y) d'origine -> inclinaison horizontale, lue dans les Tm du flux de contenu."""
    flux = page.read_contents().decode("latin-1")
    hauteur = page.rect.height
    sortie = []
    for m in re.finditer(r"(-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) (-?[\d.]+) Tm", flux):
        a, b, c, d, e, f = map(float, m.groups())
        if d:
            sortie.append((e, hauteur - f, c / d))
    return sortie


def inclinaison_de(table, x, y):
    for tx, ty, k in table:
        if abs(tx - x) < 1.5 and abs(ty - y) < 1.5:
            return k
    return 0.0


BORDS = {}


def bord_de_colonne(page, x0):
    """Bord droit de la colonne : le plus a droite qu'atteint le texte anglais de cette colonne."""
    milieu = page.rect.width / 2
    return BORDS.get((page.number, x0 < milieu), milieu + 4 if x0 < milieu else page.rect.width - 20)


def ecrire_titre(page, bloc, texte, polices, table):
    """Titre Exo 2 : contour + remplissage, incline comme l'original, retreci pour tenir."""
    lignes = [l for l in bloc["lines"]]
    # Les titres sont poses deux fois (contour puis remplissage) : une ligne sur deux.
    vues, uniques = set(), []
    for l in lignes:
        cle = round(l["spans"][0]["origin"][1], 1)
        if cle not in vues:
            vues.add(cle)
            uniques.append(l)
    morceaux = texte.split("|")
    for i, morceau in enumerate(morceaux):
        ligne = uniques[min(i, len(uniques) - 1)]
        span = ligne["spans"][0]
        x, y = span["origin"]
        if i >= len(uniques):
            y += span["size"] * 1.2 * (i - len(uniques) + 1)
        taille = span["size"]
        police = fitz.Font(fontfile=polices["exo"])
        # Espacement des lettres de l'original (operateur Tc), par point de corps.
        naturel = police.text_length(texte_span(span), fontsize=taille)
        approche = max(0.0, (span["bbox"][2] - span["bbox"][0] - naturel) / max(1, len(texte_span(span)) - 1)) / taille
        place = bord_de_colonne(page, x) - x

        def largeur(t):
            return police.text_length(morceau, fontsize=t) + approche * t * (len(morceau) - 1)
        while largeur(taille) > place and taille > span["size"] * 0.6:
            taille -= 0.25
        k = inclinaison_de(table, x, y)
        pivot = fitz.Point(x, y)
        for car in morceau:
            morph = (pivot, fitz.Matrix(1, 0, k, 1, 0, 0)) if k else None
            page.insert_text((x, y), car, fontsize=taille, fontname="exo", fontfile=polices["exo"],
                             color=couleur(span["color"]), fill=couleur(span["color"]), render_mode=2,
                             border_width=0.05, morph=morph)
            x += police.text_length(car, fontsize=taille) + approche * taille


def ecrire_intertitre(page, bloc, texte):
    """Intertitre Lucida espace (MISE EN PLACE :), a la meme chasse que l'original."""
    span = bloc["lines"][0]["spans"][0]
    x, y = span["origin"]
    taille = span["size"]
    police = fitz.Font(fontfile=LUCIDA)
    largeur_naturelle = police.text_length(texte_span(span), fontsize=taille)
    approche = max(0.0, (span["bbox"][2] - span["bbox"][0] - largeur_naturelle) / max(1, len(texte_span(span)) - 1))
    for car in texte:
        page.insert_text((x, y), car, fontsize=taille, fontname="lucida", fontfile=LUCIDA,
                         color=couleur(span["color"]))
        x += police.text_length(car, fontsize=taille) + approche


def debut_du_texte(ligne):
    """Abscisse du premier caractere visible d'une ligne (apres la fleche d'une liste)."""
    for span in ligne["spans"]:
        for car in span.get("chars", []):
            if car["c"].strip():
                return car["bbox"][0]
    return ligne["bbox"][0]


def ecrire_paragraphe(page, bloc, texte, suivant_y, archive, fonds):
    span = bloc["lines"][0]["spans"][0]
    x0, y0, x1, y1 = bloc["bbox"]
    droite = max(x1, bord_de_colonne(page, x0))
    bas = max(y1, (suivant_y - 1.5) if suivant_y else y1 + 4)
    # Retrait de premiere ligne : une puce (fleche dessinee) precede le texte.
    gauche = bloc["lines"][1]["bbox"][0] if len(bloc["lines"]) > 1 else x0
    premier = debut_du_texte(bloc["lines"][0])
    retrait = max(0.0, premier - gauche)
    # Une image a droite du bloc (l'oeil du Lizard p6) borne la colonne.
    for info in page.get_image_info():
        image = fitz.Rect(info["bbox"])
        if image.x0 > x0 + 10 and image.x0 < droite and image.y0 < bas and image.y1 > y0:
            droite = image.x0 - 4
    # Le prochain encadre gris de la colonne arrete aussi le texte.
    for f in fonds:
        if f.y0 > y1 - 1 and f.x0 < x1 and f.x1 > x0:
            bas = min(bas, f.y0 - 1.5)
    fond = next((f for f in fonds if f.contains(fitz.Rect(bloc["bbox"]))), None)
    if fond is not None:
        droite = min(droite, fond.x1 - 1.5)
        bas = min(bas, fond.y1 - 2)
    # Les lignes du livret sont espacees de 8 pt pour un corps de 6 pt.
    interligne = 1.333
    if len(bloc["lines"]) > 1:
        interligne = (bloc["lines"][1]["spans"][0]["origin"][1] - bloc["lines"][0]["spans"][0]["origin"][1]) / span["size"]
    r, g, b = (int(c * 255) for c in couleur(span["color"]))
    css = (
        "@font-face {font-family: avenir; src: url(%s);}"
        "@font-face {font-family: avenir; src: url(%s); font-style: italic;}"
        "@font-face {font-family: avenir; src: url(%s); font-weight: bold;}"
        "* {font-family: avenir; font-size: %.2fpx; line-height: %.3f; color: rgb(%d,%d,%d); margin: 0; padding: 0;}"
        "body {text-indent: %.2fpx;}"
    ) % (POLICES["regular"], POLICES["italic"], POLICES["bold"], span["size"], interligne, r, g, b, retrait)
    # Le haut de la boite HTML commence a la ligne de tete, pas a la ligne de base.
    rect = fitz.Rect(gauche, y0 - 0.3, droite, bas)
    # Typographie francaise : espace insecable avant « ! ? : ; » et a l'interieur des guillemets.
    texte = re.sub(r" ([!?:;»])", "\u00a0\\1", texte).replace("« ", "«\u00a0")
    # Pas de <p> : sa marge haute d'un cadratin decalait tout d'une ligne.
    reste, echelle = page.insert_htmlbox(rect, texte, css=css + "body {margin: 0;}", archive=archive, scale_low=0.55)
    return echelle


def refaire_page(page, traductions, numero, polices, archive):
    blocs = {i: b for i, b in enumerate(page.get_text("rawdict")["blocks"]) if b["type"] == 0}
    milieu = page.rect.width / 2
    for gauche in (True, False):
        bords = [b["bbox"][2] for b in blocs.values() if (b["bbox"][0] < milieu) == gauche and len(b["lines"]) > 1]
        if bords:
            BORDS[(page.number, gauche)] = max(bords) + 0.5
    fonds = [d["rect"] for d in page.get_drawings()
             if d.get("fill") and d["rect"].width < page.rect.width / 2 + 10 and d["rect"].height < page.rect.height / 2]
    a_traiter = {i: traductions["p%db%d" % (numero, i)] for i in blocs if "p%db%d" % (numero, i) in traductions}
    if not a_traiter:
        return []
    table = inclinaisons(page)  # avant la redaction, qui reecrit le flux
    for i in a_traiter:
        for ligne in blocs[i]["lines"]:
            page.add_redact_annot(fitz.Rect(ligne["bbox"]) + (0.2, 0.4, -0.2, -0.4), fill=False)
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE,
                          text=fitz.PDF_REDACT_TEXT_REMOVE)
    echelles = []
    for i, texte in a_traiter.items():
        if not texte:
            continue
        bloc = blocs[i]
        police = bloc["lines"][0]["spans"][0]["font"]
        if "Exo2" in police:
            ecrire_titre(page, bloc, texte, polices, table)
        elif "Lucida" in police:
            ecrire_intertitre(page, bloc, texte)
        else:
            x0, y0, x1, _ = bloc["bbox"]
            milieu = page.rect.width / 2
            # Un bloc vide (phrase coupee, traduite dans le bloc precedent) laisse sa place.
            meme_colonne = [b["bbox"][1] for j, b in blocs.items()
                            if j != i and a_traiter.get(j, None) != "" and b["bbox"][1] > y0 + 1 and (b["bbox"][0] < milieu) == (x0 < milieu)
                            and b["bbox"][0] < x1 and b["bbox"][2] > x0]
            echelle = ecrire_paragraphe(page, bloc, texte, min(meme_colonne) if meme_colonne else None, archive, fonds)
            echelles.append(("p%db%d" % (numero, i), echelle))
    return echelles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("code")
    ap.add_argument("--pour-de-vrai", action="store_true")
    options = ap.parse_args()
    carte = CARTES[options.code]
    traductions = json.load(open(os.path.join(RACINE, "tools", "livrets_fr", options.code + ".json"), encoding="utf-8"))
    doc = fitz.open(os.path.join(DEPOT, carte["pdf_depot"]))
    zoom = LARGEUR / doc[0].rect.width
    dossier = os.path.join(RACINE, "public", "stories", options.code, "fr")

    tmp = tempfile.mkdtemp()
    with zipfile.ZipFile(ZIP_POLICES) as z:
        for nom in POLICES.values():
            z.extract(nom, tmp)
    polices = {cle: os.path.join(tmp, nom) for cle, nom in POLICES.items()}
    archive = fitz.Archive(tmp)

    os.makedirs(dossier, exist_ok=True)
    for numero, fichier in sorted(pages_du_livret(carte).items()):
        page = doc[numero - 1]
        echelles = refaire_page(page, traductions, numero, polices, archive)
        serres = [(b, round(e, 2)) for b, e in echelles if e < 0.9]
        print("  p%-3d -> fr/%s%s" % (numero, fichier, ("  retrecis : %s" % serres) if serres else ""))
        if options.pour_de_vrai:
            pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
            pix.pil_save(os.path.join(dossier, fichier), format="JPEG", quality=88)
    if not options.pour_de_vrai:
        print("\n  Rien n'a ete ecrit. Relancer avec --pour-de-vrai.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
