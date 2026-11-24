#!/usr/bin/env python3
"""Decoupe le CODE du projet en TOMES Markdown a donner un par un a une IA (20/10/2026).

    python3 outils/construire-tomes-code.py --cible moteur [--taille-ko 600] [--sortie kit-code-tomes]
    python3 outils/construire-tomes-code.py --cible plateau lanceur outils
    python3 outils/construire-tomes-code.py --cible cartes --pack web_of_deceit --pack mts
    python3 outils/construire-tomes-code.py --liste            # n'ecrit rien : taille de chaque cible

POURQUOI DES TOMES
------------------
Tout le code du projet pese ≈ 72 Mo (≈ 18 M de tokens) : aucune IA ne le lit d'un coup. Ce script en tire des tomes
de taille reglable, un par morceau de code COHERENT (le moteur, le plateau, les pages du lanceur, les outils, les
scripts d'un pack de cartes). Il n'inclut JAMAIS : les donnees (`data/*.json`, 33 Mo), les images, les fichiers GENERES
(`textes-fr-complets.*`, `public/js/traduction/*`, bundles), les secrets (`deploiement/`, `site/`, `.env`, cles).
Chaque tome commence par la liste de ses fichiers ; les tomes d'une meme cible se suivent (`TOME-moteur-01-sur-05.md`).

CIBLES
------
  moteur   src/engine, src/game, src/core, src/editor, src/cards/*.py, src/cards/pack/__init__.py
  plateau  ui-app/src (sans tests par defaut) + ui-app/styles
  lanceur  public/js, public/css, public/*.html (sans stories, app, fixtures, traduction generee)
  outils   Fusion/marvel-lcg-src/tools/*.py (sans tools/cas par defaut) + outils/
  cartes   les scripts Python d'un ou plusieurs packs de cartes (--pack <cle>, repetable)
"""
import argparse
import io
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")

EXCLUS_NOMS = re.compile(r"(textes-fr-complets|textes-fr-fanmade|textes-fr\.|noms-fr\.ts|\.min\.|\.map$|package-lock|"
                         r"arts-cartes-table|zones-arts-alternatifs|scans-fr-liste|\.d\.ts$)")
EXCLUS_DOSSIERS = {"__pycache__", "node_modules", "dist", ".game", ".game-src", "fixtures", "__fixtures__", "stories",
                   "img", "fonts", "effects", "pwa", ".git"}
EXT_CODE = {".py", ".ts", ".tsx", ".js", ".mjs", ".css", ".html", ".sh"}
LANG = {".py": "python", ".ts": "typescript", ".tsx": "tsx", ".js": "javascript", ".mjs": "javascript", ".css": "css",
        ".html": "html", ".sh": "bash"}


def lire(p):
    with io.open(p, encoding="utf-8", errors="replace", newline="") as f:
        return f.read()


def fichiers_de(racine, avec_tests=False, ext=EXT_CODE, profondeur_max=None, sauf_dossiers=()):
    sortie = []
    for d, ds, fs in os.walk(racine):
        ds[:] = sorted(x for x in ds if x not in EXCLUS_DOSSIERS and x not in sauf_dossiers)
        if profondeur_max is not None and os.path.relpath(d, racine).count(os.sep) >= profondeur_max:
            ds[:] = []
        for f in sorted(fs):
            if os.path.splitext(f)[1] not in ext or EXCLUS_NOMS.search(f):
                continue
            if not avec_tests and re.search(r"\.(test|spec)\.", f):
                continue
            sortie.append(os.path.join(d, f))
    return sortie


def cible_fichiers(cible, args):
    if cible == "moteur":
        src = os.path.join(MOTEUR, "src")
        out = []
        for sous in ("engine", "game", "core", "editor"):
            out += fichiers_de(os.path.join(src, sous), ext={".py"})
        out += [os.path.join(src, "cards", f) for f in sorted(os.listdir(os.path.join(src, "cards"))) if f.endswith(".py")]
        out.append(os.path.join(src, "cards", "pack", "__init__.py"))
        out += [os.path.join(src, f) for f in ("main.py", "build.py") if os.path.exists(os.path.join(src, f))]
        return out
    if cible == "plateau":
        return fichiers_de(os.path.join(RACINE, "ui-app", "src"), args.avec_tests, ext={".ts", ".tsx", ".css"}) \
            + fichiers_de(os.path.join(RACINE, "ui-app", "styles"), ext={".css"})
    if cible == "lanceur":
        out = fichiers_de(os.path.join(MOTEUR, "public", "js"), args.avec_tests, ext={".js", ".mjs"}, sauf_dossiers=("traduction", "marvel", "module"))
        out += fichiers_de(os.path.join(MOTEUR, "public", "css"), ext={".css"})
        out += [os.path.join(MOTEUR, "public", f) for f in sorted(os.listdir(os.path.join(MOTEUR, "public"))) if f.endswith(".html")]
        return out
    if cible == "outils":
        out = [os.path.join(MOTEUR, "tools", f) for f in sorted(os.listdir(os.path.join(MOTEUR, "tools"))) if f.endswith(".py")]
        if args.avec_tests:
            out += fichiers_de(os.path.join(MOTEUR, "tools", "cas"), ext={".py"})
        out += fichiers_de(os.path.join(RACINE, "outils"), ext={".py", ".mjs", ".sh"})
        return out
    if cible == "cartes":
        out = []
        for pack in args.pack or []:
            d = os.path.join(MOTEUR, "src", "cards", "pack", pack)
            if not os.path.isdir(d):
                raise SystemExit("pack inconnu : %s" % pack)
            out += fichiers_de(d, ext={".py"})
        return out
    raise SystemExit("cible inconnue : %s" % cible)


def bloc(code, langage):
    plus_long = max([len(m) for m in re.findall(r"`+", code)] + [2])
    cloture = "`" * max(3, plus_long + 1)
    if not code.endswith("\n"):
        code += "\n"
    return "%s%s\n%s%s\n" % (cloture, langage, code, cloture)


def tomes(cible, fichiers, taille_max):
    lots, courant, taille = [], [], 0
    for f in fichiers:
        t = os.path.getsize(f)
        if courant and taille + t > taille_max:
            lots.append(courant)
            courant, taille = [], 0
        courant.append(f)
        taille += t
    if courant:
        lots.append(courant)
    return lots


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cible", nargs="+", choices=["moteur", "plateau", "lanceur", "outils", "cartes"])
    ap.add_argument("--pack", action="append")
    ap.add_argument("--taille-ko", type=int, default=600, help="taille maximale d'un tome (Ko de code, defaut 600 ≈ 150 000 tokens)")
    ap.add_argument("--sortie", default=os.path.join(RACINE, "kit-code-tomes"))
    ap.add_argument("--avec-tests", action="store_true")
    ap.add_argument("--liste", action="store_true")
    args = ap.parse_args()
    cibles = args.cible or ["moteur", "plateau", "lanceur", "outils"]
    if args.liste:
        for c in cibles:
            fs = cible_fichiers(c, args)
            o = sum(os.path.getsize(f) for f in fs)
            print("%-8s %5d fichiers  %7.1f Mo  ≈ %5.1f M tokens  ≈ %d tomes de %d Ko"
                  % (c, len(fs), o / 1e6, o / 4e6, len(tomes(c, fs, args.taille_ko * 1024)), args.taille_ko))
        return 0
    os.makedirs(args.sortie, exist_ok=True)
    for c in cibles:
        fs = cible_fichiers(c, args)
        lots = tomes(c, fs, args.taille_ko * 1024)
        nom_c = c if c != "cartes" else "cartes-" + "-".join(args.pack or [])
        for i, lot in enumerate(lots, 1):
            chemin = os.path.join(args.sortie, "TOME-%s-%02d-sur-%02d.md" % (nom_c, i, len(lots)))
            taille = sum(os.path.getsize(f) for f in lot)
            sortie = ["# TOME %s %d/%d" % (nom_c, i, len(lots)), "",
                      "Code du projet « Narwhal Champions » (Marvel Champions LCG) : cible **%s**, tome %d sur %d, %d fichiers, "
                      "%.0f Ko (≈ %d tokens). Chemins relatifs a la racine du depot." % (c, i, len(lots), len(lot), taille / 1024, taille // 4),
                      "", "## Fichiers de ce tome", ""]
            sortie += ["- `%s`" % os.path.relpath(f, RACINE).replace("\\", "/") for f in lot]
            sortie.append("")
            for f in lot:
                rel = os.path.relpath(f, RACINE).replace("\\", "/")
                sortie.append("## `%s`" % rel)
                sortie.append("")
                sortie.append(bloc(lire(f), LANG.get(os.path.splitext(f)[1], "")))
            with io.open(chemin, "w", encoding="utf-8", newline="") as fh:
                fh.write("\n".join(sortie))
            print("%s : %d fichiers, %.0f Ko" % (chemin, len(lot), taille / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
