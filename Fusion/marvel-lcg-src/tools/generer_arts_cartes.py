#!/usr/bin/env python3
"""Genere les deux tables d'arts alternatifs de cartes depuis data/arts_alternatifs.json.

    python3 tools/generer_arts_cartes.py             # ecrit les deux fichiers
    python3 tools/generer_arts_cartes.py --verifier  # code 1 si l'un est en retard

Sorties (alignees par construction, comme le demande GUIDE-CREATION-CONTENU §12 bis) :
  - public/js/prepare/arts-cartes-table.js     (preparation + deck-builder)
  - ui-app/src/board/arts-cartes-table.ts      (plateau)
"""
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "data" / "arts_alternatifs.json"
SORTIE_JS = RACINE / "public" / "js" / "prepare" / "arts-cartes-table.js"
SORTIE_TS = RACINE.parent.parent / "ui-app" / "src" / "board" / "arts-cartes-table.ts"
if not (RACINE.parent.parent / "ui-app").is_dir():
    SORTIE_TS = RACINE.parent / "ui-app" / "src" / "board" / "arts-cartes-table.ts"

ENTETE = ("GENERE par tools/generer_arts_cartes.py depuis data/arts_alternatifs.json : "
          "ne pas modifier a la main.")


def reimpressions(cartes):
    """Reimpression identique (`full_link`) -> officielle, pour les cartes a art alternatif.

    Le moteur sert l'image de l'officielle pour ses reimpressions : l'art alternatif
    et le choix du joueur valent donc pour toutes les impressions."""
    donnees = json.load(open(RACINE / "data" / "cards.json", encoding="utf-8"))
    out = {}
    for v in donnees.values():
        if isinstance(v, list):
            for c in v:
                if isinstance(c, dict) and c.get("full_link") in cartes and c.get("card_id"):
                    out[c["card_id"]] = c["full_link"]
    return dict(sorted(out.items()))


def lire():
    d = json.load(open(SOURCE, encoding="utf-8"))
    cartes = dict(sorted(d["cartes"].items()))
    return {"series": d["series"], "cartes": cartes, "origines": reimpressions(cartes)}


def _js(d):
    return json.dumps(d, ensure_ascii=False, indent=2)


def contenu_js(d):
    return (f"// {ENTETE}\n"
            "\"use strict\";\n\n"
            "/** Officielle -> codes d'art alternatif (image `assets/pics/<id>_<code>.jpg`). */\n"
            f"export const ARTS_CARTES = {_js(d['cartes'])};\n\n"
            "/** Reimpression identique -> officielle (meme image, meme choix). */\n"
            f"export const ORIGINES_CARTES = {_js(d['origines'])};\n\n"
            "/** Series d'art : heros qui l'ont par defaut, sets exclusifs. */\n"
            f"export const SERIES_ARTS = {_js(d['series'])};\n")


def contenu_ts(d):
    return (f"// {ENTETE}\n\n"
            "/** Officielle -> codes d'art alternatif (image `<id>_<code>`). */\n"
            f"export const ARTS_CARTES: Record<string, string[]> = {_js(d['cartes'])}\n\n"
            "/** Reimpression identique -> officielle (meme image, meme choix). */\n"
            f"export const ORIGINES_CARTES: Record<string, string> = {_js(d['origines'])}\n\n"
            "export type SerieArt = {\n"
            "  nom: string\n  nom_en: string\n  heros_cartes: string[]\n  heros_ids: string[]\n  sets_exclusifs: string[]\n}\n\n"
            "/** Series d'art : heros qui l'ont par defaut, sets exclusifs. */\n"
            f"export const SERIES_ARTS: Record<string, SerieArt> = {_js(d['series'])}\n")


def main():
    d = lire()
    sorties = [(SORTIE_JS, contenu_js(d)), (SORTIE_TS, contenu_ts(d))]
    if "--verifier" in sys.argv:
        en_retard = [str(p) for p, c in sorties if not p.exists() or p.read_text(encoding="utf-8") != c]
        if en_retard:
            print("EN RETARD (relancer tools/generer_arts_cartes.py) :", *en_retard, sep="\n  ")
            sys.exit(1)
        print("tables alignees")
        return
    for p, c in sorties:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(c, encoding="utf-8")
        print("ecrit", p)


if __name__ == "__main__":
    main()
