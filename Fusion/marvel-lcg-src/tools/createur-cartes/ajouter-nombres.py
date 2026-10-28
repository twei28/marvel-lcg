"""Ajoute a `public/createur-cartes/donnees/types.json` la geometrie des NOMBRES, a partir des releves de `mesures/mesurer-nombres.mjs`
(Card Maker de Landstander, tous les champs remplis, etoiles comprises).

    python3 tools/createur-cartes/ajouter-nombres.py <dossier ref-nombres> <dossier ref-nombres-sans>   (ETOILE=0 SUFFIXE=-sans)

Pour chaque element « ... cost » (fond flex centre, filtre `codeshadow` = contour noir + ombres), on retient la police de l'etoile qui
suit le nombre : `etoile = {fs, dy, ecart, dx}` ; `dx` = decalage du CENTRE du nombre quand l'etoile est la (le groupe nombre + etoile
est centre dans la boite, ou la boite est deplacee par la page : on mesure le resultat), `dy` = centre de l'etoile - centre de la boite,
`ecart` = espace entre le nombre et l'etoile. Les autres elements (menace, boosts, ressources...) sont copies tels quels dans `nombres`.
"""
import json
import re
import sys
from pathlib import Path

REF = Path(sys.argv[1])
SANS = Path(sys.argv[2])
TYPES = Path(__file__).resolve().parents[2] / "public/createur-cartes/donnees/types.json"
types = json.loads(TYPES.read_text(encoding="utf-8"))


def px(v):
    return float(str(v).replace("px", "") or 0)


for tid, spec in types.items():
    f = REF / f"{tid}.json"
    if not f.exists():
        continue
    rows = json.loads(f.read_text(encoding="utf-8"))
    for el in spec["elements"]:
        if not (el["cls"].endswith(" cost") or el["cls"] == "startingthreatwrap"):
            continue
        r = next((x for x in rows if x["cls"] == el["cls"] and x["y"] > -5000), None)
        if not r:
            continue
        enfants = [x for x in rows if x["parent"] == r["i"]]
        sp = next((x for x in enfants if x["tag"] == "SPAN" or x["cls"] == "startingthreat"), None)
        co = next((x for x in enfants if x["tag"] == "CODE"), None)
        el.pop("etoile", None)
        if sp:
            el["fsNombre"] = px(sp["style"]["fontSize"])
        if not co:
            continue
        r0 = next((x for x in json.loads((SANS / f"{tid}.json").read_text(encoding="utf-8")) if x["cls"] == el["cls"] and x["y"] > -5000), None)
        if r0:  # la boite et l'origine de rotation de l'etat REMPLI font foi (a vide, certaines boites mesurent 0 de haut)
            el["boite"] = [r0["x"], r0["y"], r0["w"], r0["h"]]
            el["origine"] = [px(v) for v in r0["org"].split()]
        cx0 = (r0 or r)["x"] + (r0 or r)["w"] / 2  # centre de la boite SANS etoile
        cy = r["y"] + r["h"] / 2
        if sp and sp.get("text"):
            el["etoile"] = {"fs": px(co["style"]["fontSize"]), "dy": round(co["y"] + co["h"] / 2 - cy, 1),
                            "ecart": round(co["x"] - (sp["x"] + sp["w"]), 1), "dx": round(sp["x"] + sp["w"] / 2 - cx0, 1)}
        else:  # etoile seule (pas de valeur) : elle remplace le nombre
            el["etoileSeule"] = {"fs": px(co["style"]["fontSize"]), "dx": round(co["x"] + co["w"] / 2 - cx0, 1),
                                 "dy": round(co["y"] + co["h"] / 2 - cy, 1)}
    # phase de la manigance principale : numero + lettre, groupe centre dans la boite
    for el in spec["elements"]:
        if el["cls"] != "mainschemephase cost":
            continue
        r = next((x for x in rows if x["cls"] == el["cls"] and x["y"] > -5000), None)
        num = next((x for x in rows if r and x["cls"] == "mainschemephasenumber" and x["y"] > -5000), None)
        let = next((x for x in rows if r and x["cls"] == "mainschemephaseletter" and x["y"] > -5000), None)
        if num and let:
            el["phase"] = {"fsNum": px(num["style"]["fontSize"]), "fsLettre": px(let["style"]["fontSize"]), "ecart": round(let["x"] - (num["x"] + num["w"]), 1)}
    # bulle de PV (promos) : image 256 x 256 posee a l'endroit de la bulle, pas pleine carte
    hb = next((x for x in rows if x["cls"] == "background hp_bubble" and (x["x"], x["y"]) != (0, 0)), None)
    for c in spec["calques"]:
        if c.get("role") == "hp_bubble":
            c.pop("pos", None)
            if hb and hb["w"] > 400 and "promo" in tid:
                c["pos"] = [hb["x"], hb["y"]]
    # icones de renfort : ancre = la derniere icone (boost1), pas de 95 px, etoile 90 px a gauche ; ressources : 3 emplacements fixes
    b1 = next((x for x in rows if x["cls"].startswith("boost1") and x["y"] > -5000), None)
    if b1:
        spec["renforts"] = {"x": b1["x"], "y": b1["y"], "taille": b1["w"]}
        fond = next((re.search(r"/(\w+)/boostbox\d\.png", x["style"]["backgroundImage"]) for x in rows if x["cls"] == "boostbox" and "boostbox" in x["style"]["backgroundImage"]), None)
        if fond:  # fond noir en pilule derriere les icones (une image pleine carte par nombre d'emplacements)
            spec["renforts"]["fond"] = fond.group(1)
    else:
        spec.pop("renforts", None)
    res = [next((x for x in rows if x["cls"] == f"resource{k}" and x["y"] > -5000), None) for k in (1, 2, 3)]
    if all(res):
        spec["ressources"] = [[x["x"], x["y"]] for x in res]
    else:
        spec.pop("ressources", None)
# tete (headshot) : les types qui ont la case « Show corner headshot? » ; l'eclat (splash) accompagne la tete sauf sur les promos
AVEC_TETE = json.loads((Path(__file__).parent / "mesures/types-avec-tete.json").read_text(encoding="utf-8"))
for tid, spec in types.items():
    if tid in AVEC_TETE:
        spec["tete"] = {"splash": "promo" not in tid}
    else:
        spec.pop("tete", None)
TYPES.write_text(json.dumps(types, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("types.json mis a jour")
