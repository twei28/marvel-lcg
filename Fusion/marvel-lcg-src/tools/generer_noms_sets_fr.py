#!/usr/bin/env python3
"""Deduit le nom FRANCAIS des sets de rencontre a partir des textes FR des cartes de scenario.

Le texte d'un schema principal dit par exemple :
  « Les sets de rencontre Rhino et Standard. Un set de rencontre modulaire (recommande : Alerte a la Bombe). »
On rapproche ces noms, DANS L'ORDRE, des `encounter_sets` et `modular_sets` du fichier du scenario. Un rapprochement
n'est retenu que si le nombre de noms francais egale le nombre de sets du jeu : sinon, on ne devine pas.

    python3 tools/generer_noms_sets_fr.py

Produit public/js/prepare/noms-sets-fr.js (NE PAS EDITER A LA MAIN) et docs/rapports/NOMS-SETS-FR.md (couverture).
Un set sans nom francais deduit s'affiche sous son nom anglais.
"""
import glob
import json
import os
import re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "data")
SORTIE_JS = os.path.join(RACINE, "public", "js", "prepare", "noms-sets-fr.js")
RAPPORT = os.path.join(os.path.dirname(os.path.dirname(RACINE)), "docs", "rapports", "NOMS-SETS-FR.md")
TEXTES = os.path.join(RACINE, "public", "js", "traduction", "textes-fr-complets.js")


def textes():
    out = {}
    src = open(TEXTES, encoding="utf8").read()
    for m in re.finditer(r'^\s*"([0-9a-z]+)":\s*"((?:[^"\\]|\\.)*)",?\s*$', src, re.M):
        out[m.group(1)] = json.loads('"' + m.group(2) + '"')
    return out


def decouper(liste):
    liste = re.sub(r"\s+", " ", liste).strip().strip(".")
    parts = re.split(r",\s*| et | ou ", liste)
    return [p.strip() for p in parts if p.strip()]


def main():
    tx = textes()
    fr = {}
    conflits = {}
    scenarios_lus = rapproches = 0
    for f in sorted(glob.glob(os.path.join(DATA, "scenarios", "*.json"))):
        d = json.load(open(f, encoding="utf8"))
        if d.get("expert") or not d.get("schemes"):
            continue
        t = tx.get(d["schemes"][0].split(",")[0])
        if not t:
            continue
        plain = re.sub(r"<[^>]+>", "", t)
        scenarios_lus += 1
        paires = []
        m = re.search(r"sets? de rencontre (.+?)\.\s*(?:Un|Deux|Trois|Quatre|\d)\b", plain) or \
            re.search(r"sets? de rencontre (.+?)\.", plain)
        if m:
            noms = [n for n in decouper(m.group(1)) if n.lower() != "standard"]
            ids = [i for i in d.get("encounter_sets", []) if not i.startswith(("standard", "expert"))]
            if noms and len(noms) == len(ids):
                paires += list(zip(ids, noms))
        r = re.search(r"recommand[ée]s?\s*:\s*([^)]+)\)", plain)
        if r:
            noms = decouper(r.group(1))
            ids = d.get("modular_sets", [])
            if noms and len(noms) == len(ids):
                paires += list(zip(ids, noms))
        if paires:
            rapproches += 1
        for i, n in paires:
            n = n.strip(" .")
            if re.match(r"(du|de|des|d'|le|la|les|l')\b", n):  # un morceau de phrase, pas un titre (« du Caïd »)
                continue
            if i in fr and fr[i] != n:
                conflits.setdefault(i, {fr[i]}).add(n)
            else:
                fr[i] = n
    for i in conflits:
        fr.pop(i, None)
    tous = {os.path.basename(f)[:-5]: json.load(open(f, encoding="utf8")).get("name") or "" for f in
            glob.glob(os.path.join(DATA, "encounter_sets", "*.json"))}
    corps = json.dumps(dict(sorted(fr.items())), ensure_ascii=False, indent=1)
    with open(SORTIE_JS, "w", encoding="utf8") as f:
        f.write("// Genere par tools/generer_noms_sets_fr.py — NE PAS EDITER A LA MAIN.\n"
                "// Nom francais des sets de rencontre, deduit des textes FR des cartes de scenario.\n"
                "// Un set absent d'ici s'affiche sous son nom anglais.\n"
                "export const NOMS_SETS_FR = " + corps + ";\n")
    L = ["# Noms français des sets de rencontre : couverture", "",
         "Généré par `tools/generer_noms_sets_fr.py` (ne pas éditer à la main).", "",
         f"- Scénarios dont le texte FR a été lu : **{scenarios_lus}**, dont **{rapproches}** avec un rapprochement fiable",
         f"- Sets avec un nom français déduit : **{len(fr)}** sur {len(tous)} fichiers de sets",
         f"- Conflits (deux noms différents pour un même set, ignorés) : **{len(conflits)}**", ""]
    if conflits:
        L += ["## Conflits", ""] + [f"- {i} : {sorted(v)}" for i, v in sorted(conflits.items())] + [""]
    L += ["## Noms déduits", ""] + [f"- `{i}` → {n}" for i, n in sorted(fr.items())]
    os.makedirs(os.path.dirname(RAPPORT), exist_ok=True)
    open(RAPPORT, "w", encoding="utf8").write("\n".join(L) + "\n")
    print(f"{len(fr)} noms FR deduits ({len(conflits)} conflits) sur {len(tous)} sets")


if __name__ == "__main__":
    main()
