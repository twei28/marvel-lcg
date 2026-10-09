"""Dictionnaire des TRAITS en francais (« AERIAL » -> « AÉRIEN »).

Sert a la traduction posee sur les scans anglais (plateau, deckbuilder,
galerie) : la ligne des traits est recouverte avec le reste de la zone de
texte, il faut donc la reecrire.

Source : les deux catalogues marvelcdb, francais et anglais. Pour chaque carte
dont les deux listes de traits ont la meme longueur, les traits sont alignes
dans l'ordre ; le vote majoritaire tranche. Complete, et corrige, par
tools/traits_fr_maison.json (traits fan-made ou laisses en anglais par
marvelcdb). Un trait sans traduction connue (nom propre) reste en anglais.

Usage : python3 tools/generer_traits_fr.py
"""
import collections
import json
import re
import urllib.request
from pathlib import Path

ICI = Path(__file__).resolve().parent
SORTIE_TS = ICI.parents[2] / "ui-app" / "src" / "board" / "traits-fr.ts"
SORTIE_JS = ICI.parent / "public" / "js" / "prepare" / "traits-fr.js"
URL_FR = "https://fr.marvelcdb.com/api/public/cards/?encounter=1"
URL_EN = "https://marvelcdb.com/api/public/cards/?encounter=1"


def charger(url):
    with urllib.request.urlopen(url, timeout=120) as reponse:
        return {carte["code"]: carte for carte in json.load(reponse)}


def decouper(traits):
    return [t.strip() for t in re.split(r"\.\s*", traits or "") if t.strip()]


def main():
    francais, anglais = charger(URL_FR), charger(URL_EN)
    votes = collections.defaultdict(collections.Counter)
    for code, carte in anglais.items():
        autre = francais.get(code)
        if not autre:
            continue
        en, fr = decouper(carte.get("traits")), decouper(autre.get("traits"))
        if en and len(en) == len(fr):
            for a, b in zip(en, fr):
                votes[a.upper()][b.upper()] += 1
    table = {en: compte.most_common(1)[0][0] for en, compte in sorted(votes.items())}
    maison = json.loads((ICI / "traits_fr_maison.json").read_text(encoding="utf-8"))
    maison.pop("_lisez_moi", None)
    table.update(maison)
    table = {en: fr for en, fr in sorted(table.items()) if en != fr}
    corps = "".join(f"  {json.dumps(en, ensure_ascii=False)}: {json.dumps(fr, ensure_ascii=False)},\n"
                    for en, fr in table.items())
    entete = ("// Genere par tools/generer_traits_fr.py — NE PAS EDITER A LA MAIN.\n"
              "// Traits anglais (majuscules) -> traits francais officiels, alignes sur\n"
              "// fr.marvelcdb.com et marvelcdb.com, completes par tools/traits_fr_maison.json.\n"
              "// Seuls ceux qui different y figurent.\n")
    SORTIE_TS.write_text(entete + "export const TRAITS_FR: Readonly<Record<string, string | undefined>> = {\n"
                         + corps + "}\n", encoding="utf-8")
    SORTIE_JS.write_text(entete + "export const TRAITS_FR = {\n" + corps + "};\n", encoding="utf-8")
    print(f"{len(table)} traits traduits")


if __name__ == "__main__":
    main()
