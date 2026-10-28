"""Fabrique `public/createur-cartes/donnees/types.json` a partir des MESURES prises sur le Card Maker de Landstander
(`mesurer-landstander.mjs` -> mesures.json) : pour chacun des 23 types, la pile de calques, les couleurs par defaut de
chaque calque teinte, et la geometrie / police de chaque element de texte. Rien du code de Landstander n'est repris :
ce sont des positions, des tailles et des noms de fichiers.

    python3 tools/createur-cartes/generer-specs.py <mesures.json>
"""
import json
import re
import sys
import urllib.parse
from pathlib import Path

ENTREE = Path(sys.argv[1])
SORTIE = Path(__file__).resolve().parents[2] / "public/createur-cartes/donnees/types.json"
mesures = json.loads(ENTREE.read_text(encoding="utf-8"))
etiquettes = {t: n for t, n in json.loads((ENTREE.parent / "types-options.json").read_text(encoding="utf-8"))}

POLICE_PROPS = ["fontFamily", "fontSize", "fontWeight", "fontStyle", "color", "textAlign", "lineHeight", "letterSpacing",
                "textShadow", "webkitTextStroke", "textTransform", "fontVariant", "transform", "opacity", "mixBlendMode",
                "paddingTop", "paddingLeft", "whiteSpace", "justifyContent", "alignItems", "zIndex"]


def srgb(lin):
    lin = max(0.0, min(1.0, lin))
    v = 12.92 * lin if lin <= 0.0031308 else 1.055 * (lin ** (1 / 2.4)) - 0.055
    return round(v * 255)


def couleur_du_filtre(filtre):
    """Un calque teinte = une couleur PLEINE (feFuncX slope=0, intercept=couleur, en lineaire) qui garde l'alpha du calque."""
    f = urllib.parse.unquote(filtre)
    ch = []
    for canal in "RGB":
        m = re.search(r'feFunc%s[^>]*intercept="([-0-9.eE]+)"' % canal, f)
        if not m:
            return None
        ch.append(srgb(float(m.group(1))))
    return "#%02x%02x%02x" % tuple(ch)


def dernier_segment(url):
    return urllib.parse.unquote(url.split("pages.dev/")[-1].rstrip('")')).strip('"')


ARBRE = json.loads((ENTREE.parent / "arbre.json").read_text(encoding="utf-8"))
PX = re.compile(r"(-?[0-9.]+)px")
STYLE_GARDE = ["clipPath", "fontFamily", "fontSize", "fontWeight", "fontStyle", "color", "textAlign", "lineHeight", "letterSpacing", "textShadow",
               "webkitTextStroke", "textTransform", "fontVariant", "opacity", "mixBlendMode", "whiteSpace", "justifyContent",
               "alignItems", "flexDirection", "display", "paddingTop", "paddingRight", "paddingBottom", "paddingLeft", "zIndex", "textIndent", "wordSpacing"]


def deg(valeur):
    m = re.match(r"(-?[0-9.]+)deg", valeur or "")
    return float(m.group(1)) if m else 0.0


def nombres(valeur, n):
    return [float(x) for x in re.findall(r"-?[0-9.]+", valeur or "")][:n]


def arbre_de(t):
    """Tous les noeuds visibles de la carte (sauf les calques), avec boite SANS transformation, matrice propre et origine."""
    rows = ARBRE[t]["rows"]
    garde = {}
    for r in rows:
        if r["i"] == 0 or not r["vis"] or r["tag"] == "IMG" and "headshot" not in r["cls"]:
            continue
        if r["x"] > 5000 or r["x"] < -5000 or r["y"] > 5000 or r["y"] < -5000 or r["w"] < 1 and r["h"] < 1:
            continue
        garde[r["i"]] = r
    elements = []
    for r in garde.values():
        o = PX.findall(r["org"])
        m = nombres(r["tr"], 6) if r["tr"] != "none" else None
        e = {"i": r["i"], "parent": r["parent"] if r["parent"] in garde else -1, "tag": r["tag"], "cls": r["cls"],
             "boite": [r["x"], r["y"], r["w"], r["h"]], "origine": [float(o[0]), float(o[1])] if len(o) == 2 else [r["w"] / 2, r["h"] / 2],
             "style": {k: r["style"][k] for k in STYLE_GARDE if k in r["style"]}}
        rot, scl, trn = deg(r.get("rot")), nombres(r.get("scl"), 2), nombres(r.get("trn"), 2)
        if rot:
            e["rot"] = rot
        if scl and r.get("scl") not in ("none", None):
            e["scl"] = scl if len(scl) == 2 else [scl[0], scl[0]]
        if trn and r.get("trn") not in ("none", None):
            e["trn"] = trn
        if m:
            e["m"] = m
        if r.get("text"):
            e["texte"] = r["text"]
        elements.append(e)
    return elements


types = {}
for t, v in mesures.items():
    calques, couleurs, photos = [], {}, 0
    for r in v["rows"]:
        if r["tag"] != "IMG" or r["depth"] != 0:
            continue
        cls = [c for c in r["cls"].split() if c not in ("background", "photoimg")]
        if "photoimg" in r["cls"] and "headshot" not in r["cls"]:
            photos += 1
            calques.append({"role": "photo" if "photofront" not in r["cls"] else "photofront"})
            continue
        if not r["vis"] or not cls:
            continue
        s = r["style"]
        bg = s["backgroundImage"]
        if bg == "none":
            continue
        role = cls[0] if cls[0] != "shadow_upper" else "shadow_upper"
        if "url(" not in bg:
            # `gradient` : un degrade CSS (du bas-gauche au haut-droit : bas -> haut) decoupe par le masque `<type>/gradient.png`.
            rgb = re.findall(r"rgb\((\d+), (\d+), (\d+)\)", bg)
            c = {"role": "gradient", "src": t + "/gradient.png",
                 "degrade": ["#%02x%02x%02x" % tuple(int(x) for x in m) for m in rgb[:2]]}
            calques.append(c)
            continue
        c = {"role": role, "src": dernier_segment(bg.split('url(')[1].split(')')[0])}
        if s["filter"] != "none":
            col = couleur_du_filtre(s["filter"])
            if col:
                c["teinte"] = role
                couleurs[role] = col
        if s["mixBlendMode"] not in ("normal", ""):
            c["melange"] = s["mixBlendMode"]
        calques.append(c)
    elements = arbre_de(t)
    types[t] = {
        "id": t, "etiquette": etiquettes.get(t, t), "famille": v["attrs"].get("data-family", "hero"),
        "paysage": bool(v.get("tournee")), "largeur": 2150 if v.get("tournee") else 1500, "hauteur": 1500 if v.get("tournee") else 2150,
        "calques": calques, "couleursParDefaut": couleurs, "elements": elements,
    }
SORTIE.write_text(json.dumps(types, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(len(types), "types ->", SORTIE, SORTIE.stat().st_size // 1024, "Ko")
