"""Releve, dans NOTRE catalogue (data/cards.json = texte anglais, public/js/traduction/textes-fr-complets.js = texte francais officiel),
les mots que les vraies cartes emploient : declencheurs en gras (Action, Reaction forcee...), mots-cles (Toughness / Tenacite...) avec leur
rappel en italique. Rien n'est devine : une paire n'est retenue que si elle revient sur plusieurs cartes. Ecrit
`public/createur-cartes/donnees/styles-texte.json`.

    python3 tools/createur-cartes/extraire-styles.py
"""
import collections
import json
import re
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
cartes = json.loads((RACINE / "data/cards.json").read_text(encoding="utf-8"))
en = {c["card_id"]: c["text"] for v in cartes.values() for c in v if isinstance(c, dict) and c.get("text")}
src = (RACINE / "public/js/traduction/textes-fr-complets.js").read_text(encoding="utf-8")
fr = json.loads(re.sub(r",\s*}$", "}", re.search(r"TEXTES_FR_COMPLETS\s*=\s*(\{.*\})", src, re.S).group(1)))

# ---- declencheurs : <b>Mot</b> de part et d'autre (meme nombre de gras)
decl = collections.defaultdict(collections.Counter)
for k, t in en.items():
    f = fr.get(k)
    if not f:
        continue
    be = [x.strip().rstrip(":").strip() for x in re.findall(r"<b>(.*?)</b>", t)]
    bf = [x.strip().rstrip(":").strip() for x in re.findall(r"<b>(.*?)</b>", f)]
    if be and len(be) == len(bf):
        for a, b in zip(be, bf):
            decl[a][b] += 1
DECLENCHEURS = ["Action", "Hero Action", "Alter-Ego Action", "Response", "Hero Response", "Alter-Ego Response", "Interrupt", "Hero Interrupt",
                "Alter-Ego Interrupt", "Forced Response", "Forced Interrupt", "Forced Action", "When Revealed", "When Defeated", "Setup", "Resource",
                "Hero Resource", "Alter-Ego Resource", "Special", "Boost", "First Player Action"]
declencheurs = []
for mot in DECLENCHEURS:
    choix = decl[mot].most_common()
    if not choix:
        continue
    # « When Defeated » a deux traductions selon le genre (vaincu / dejouee) : on garde les deux, si elles sont frequentes
    garde = [c for c in choix if c[1] >= max(5, choix[0][1] // 3) and c[0].lower() == c[0].lower()]
    declencheurs.append({"en": mot, "fr": [g[0] for g in garde[:2]] if mot == "When Defeated" else [garde[0][0] if garde else choix[0][0]]})

# ---- mots-cles : premiere ligne de la carte, « Mot. Autre mot 1. <i>(rappel)</i> »
MOTS = ["Toughness", "Guard", "Retaliate", "Permanent", "Surge", "Quickstrike", "Overkill", "Piercing", "Ranged", "Restricted", "Peril", "Patrol",
        "Incite", "Hinder", "Crisis", "Hazard", "Acceleration", "Amplify", "Villainous", "Steady", "Stalwart", "Vulnerable", "Assault", "Victory"]
def decouper(ligne):
    """« Guard. Retaliate 1. <i>(rappel)</i> » -> ([« Guard. », « Retaliate 1. »], « <i>(rappel)</i> »)."""
    rappel = ""
    m = re.search(r"\s*(<i>\(.*?\)</i>)", ligne)
    if m:
        rappel = m.group(1).strip()
        ligne = ligne[: m.start()] + ligne[m.end():]
    return [p.strip() for p in re.findall(r"[^.]+\.", ligne) if p.strip()], rappel
paires = collections.defaultdict(collections.Counter)
for k, t in en.items():
    f = fr.get(k)
    if not f:
        continue
    le, rae = decouper(t.split("\n")[0])
    lf, raf = decouper(f.split("\n")[0])
    if not le or len(le) != len(lf):
        continue
    for i, (a, b) in enumerate(zip(le, lf)):
        base = re.sub(r"\s*(\d+|X)\.?$", "", a.rstrip(".")).strip()
        if base in MOTS:
            avec_nombre = bool(re.search(r"\s(\d+|X)\.$", a))
            # le rappel suit le dernier mot-cle de la ligne
            r = (rae, raf) if i == len(le) - 1 and rae and raf else ("", "")
            paires[base][(re.sub(r"\d+", "X", a), re.sub(r"\d+", "X", b), re.sub(r"\d+", "X", r[0]), re.sub(r"\d+", "X", r[1]))] += 1
mots = []
for mot in MOTS:
    if not paires[mot]:
        continue
    total = collections.Counter()
    for (a, b, ra, rb), n in paires[mot].items():
        total[(a, b)] += n
    (a, b), _ = total.most_common(1)[0]
    # le rappel le plus frequent parmi les cartes qui en ont un (avec ce mot)
    rap = collections.Counter({(ra, rb): n for (aa, bb, ra, rb), n in paires[mot].items() if aa == a and bb == b and ra})
    ra, rb = rap.most_common(1)[0][0] if rap else ("", "")
    mots.append({"en": mot, "motEn": a, "motFr": b, "rappelEn": ra, "rappelFr": rb, "nb": sum(total.values())})
sortie = RACINE / "public/createur-cartes/donnees/styles-texte.json"
sortie.write_text(json.dumps({"declencheurs": declencheurs, "motsCles": mots}, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(declencheurs), "declencheurs,", len(mots), "mots-cles ->", sortie)
for m in mots:
    print(f"{m['nb']:3d} {m['motEn']:18} | {m['motFr']:18} | {m['rappelEn'][:60]} | {m['rappelFr'][:60]}")
for d in declencheurs:
    print(d)
