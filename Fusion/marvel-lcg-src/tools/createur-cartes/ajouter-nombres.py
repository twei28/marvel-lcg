"""Ajoute a `public/createur-cartes/donnees/types.json` la geometrie des NOMBRES, a partir des releves de `mesures/mesurer-nombres.mjs`
(Card Maker de Landstander, tous les champs remplis, etoiles comprises).

    python3 tools/createur-cartes/ajouter-nombres.py <dossier ref-nombres> <dossier ref-nombres-sans>   (ETOILE=0 SUFFIXE=-sans)

Pour chaque element « ... cost » (fond flex centre, filtre `codeshadow` = contour noir + ombres), on retient la police de l'etoile qui
suit le nombre : `etoile = {fs, dy, ecart, dx}` ; `dx` = decalage du CENTRE du nombre quand l'etoile est la (le groupe nombre + etoile
est centre dans la boite, ou la boite est deplacee par la page : on mesure le resultat), `dy` = centre de l'etoile - centre de la boite,
`ecart` = espace entre le nombre et l'etoile. Les autres elements (menace, boosts, ressources...) sont copies tels quels dans `nombres`.
"""
import json
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
        if not el["cls"].endswith(" cost"):
            continue
        r = next((x for x in rows if x["cls"] == el["cls"] and x["y"] > -5000), None)
        if not r:
            continue
        enfants = [x for x in rows if x["parent"] == r["i"]]
        sp = next((x for x in enfants if x["tag"] == "SPAN"), None)
        co = next((x for x in enfants if x["tag"] == "CODE"), None)
        el.pop("etoile", None)
        if not co:
            continue
        r0 = next((x for x in json.loads((SANS / f"{tid}.json").read_text(encoding="utf-8")) if x["cls"] == el["cls"] and x["y"] > -5000), None)
        cx0 = (r0 or r)["x"] + (r0 or r)["w"] / 2  # centre de la boite SANS etoile
        cy = r["y"] + r["h"] / 2
        if sp and sp.get("text"):
            el["etoile"] = {"fs": px(co["style"]["fontSize"]), "dy": round(co["y"] + co["h"] / 2 - cy, 1),
                            "ecart": round(co["x"] - (sp["x"] + sp["w"]), 1), "dx": round(sp["x"] + sp["w"] / 2 - cx0, 1)}
        else:  # etoile seule (pas de valeur) : elle remplace le nombre
            el["etoileSeule"] = {"fs": px(co["style"]["fontSize"]), "dx": round(co["x"] + co["w"] / 2 - cx0, 1),
                                 "dy": round(co["y"] + co["h"] / 2 - cy, 1)}
TYPES.write_text(json.dumps(types, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print("types.json mis a jour")
