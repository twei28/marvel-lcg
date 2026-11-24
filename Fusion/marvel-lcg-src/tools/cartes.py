#!/usr/bin/env python3
"""Cherche des cartes joueur dans data/cards.json (aide a la construction de decks).

    python3 tools/cartes.py [--classe Justice] [--set "TMNT Basic"] [--type Ally] [--trait NINJA] [--texte regex]
                            [--nom regex] [--id ub012] [--max 80]

Sans filtre : rien (trop gros). Une ligne par carte : id | nom | classe | type | cout | ressource | PV/ATQ/CTR | texte court.
"""
import argparse, json, os, re

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--classe"); ap.add_argument("--set"); ap.add_argument("--type"); ap.add_argument("--trait")
ap.add_argument("--texte"); ap.add_argument("--nom"); ap.add_argument("--id"); ap.add_argument("--max", type=int, default=80)
ap.add_argument("--long", action="store_true", help="texte complet")
a = ap.parse_args()
if not any([a.classe, a.set, a.type, a.trait, a.texte, a.nom, a.id]):
    ap.error("au moins un filtre")
d = json.load(open(os.path.join(RACINE, "data", "cards.json"), encoding="utf8"))
# Noms francais officiels des cartes (generes par tools/importer_scans_fr.py) : « 01003 -> Salto Arriere ».
FR = dict(re.findall(r"'([0-9a-z]+)':\s*\"((?:[^\"\\]|\\.)*)\"",
                     open(os.path.join(RACINE, "public", "js", "prepare", "noms-fr.js"), encoding="utf8").read()))
vus, n = set(), 0
for liste in d.values():
    for c in liste if isinstance(liste, list) else []:
        if not isinstance(c, dict) or c.get("card_id") in vus:
            continue
        ds = c.get("desc") or {}
        if a.id and c["card_id"] != a.id: continue
        if a.classe and ds.get("Class", "").lower() != a.classe.lower(): continue
        if a.set and a.set.lower() not in str(c.get("set_name", "")).lower(): continue
        if a.type and str(c.get("type", "")).lower() != a.type.lower(): continue
        if a.trait and a.trait.lower() not in [str(t).lower() for t in c.get("traits", [])]: continue
        if a.nom and not re.search(a.nom, str(c.get("name", "")), re.I): continue
        if a.texte and not re.search(a.texte, str(c.get("text", "")), re.I): continue
        vus.add(c["card_id"])
        txt = re.sub(r"<[^>]+>", "", str(c.get("text", ""))).replace("\n", " ")
        if not a.long: txt = txt[:170]
        stats = "/".join(str(ds.get(k, "")) for k in ("HP", "ATK", "THW"))
        fr = FR.get(c['card_id'])
        nom = c.get('name','') + (f" ({fr})" if fr and fr != c.get('name') else '')
        print(f"{c['card_id']} | {nom} | {ds.get('Class','')} | {c.get('type','')} | {ds.get('Cost','')} | {ds.get('RES','')} | {stats} | {txt}")
        n += 1
        if n >= a.max:
            print(f"... ({a.max} premiers)"); raise SystemExit
