#!/usr/bin/env python3
"""Importe les combinaisons « meilleurs sets modulaires » de VillainTheory.

Source : la page Google Docs « Every Villain's Best Modular Sets » enregistree en .mht
(Chrome : Enregistrer sous... -> Page Web, fichier unique).

    python3 tools/importer_villaintheory.py CHEMIN/doc.mht

Produit :
  public/js/prepare/villaintheory.js   (donnees lues par la page « Difficulte », NE PAS EDITER A LA MAIN)
  docs/rapports/VILLAINTHEORY-IMPORT.md (couverture : ce qui est garde, ce qui est ecarte, et pourquoi)

Regles (decidees avec le joueur, 30/10/2026) :
  - seules les combinaisons d'un mechant que le jeu possede sont gardees ; les autres vont au rapport ;
  - une combinaison dont un set manque dans le jeu est GARDEE, avec la liste `manquants` : l'ecran la grise
    en disant pourquoi ;
  - les noms de combinaison restent en anglais (noms d'auteur).
"""
import glob
import json
import os
import re
import sys
from html.parser import HTMLParser

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "data")
SORTIE_JS = os.path.join(RACINE, "public", "js", "prepare", "villaintheory.js")
RAPPORT = os.path.join(os.path.dirname(os.path.dirname(RACINE)), "docs", "rapports", "VILLAINTHEORY-IMPORT.md")


class Lecteur(HTMLParser):
    """Suite d'evenements : ('h1'|'h3', texte) et ('row', [cellules]) ; une cellule = liste de paragraphes."""

    def __init__(self):
        super().__init__()
        self.ev, self.row, self.cell, self.buf, self.titre = [], None, None, None, None

    def handle_starttag(self, t, a):
        if t == "tr":
            self.row = []
        elif t == "td":
            self.cell = []
        elif t in ("p", "h1", "h2", "h3"):
            self.buf, self.titre = "", t
        elif t == "br" and self.buf is not None:
            self.buf += "\n"

    def handle_endtag(self, t):
        if t == "td":
            if self.row is not None:
                self.row.append(self.cell or [])
            self.cell = None
        elif t == "tr":
            if self.row:
                self.ev.append(("row", self.row))
            self.row = None
        elif t in ("p", "h1", "h2", "h3"):
            txt = re.sub(r"[ \t\xa0]+", " ", self.buf or "").strip()
            if txt:
                if self.cell is not None:
                    self.cell.append(txt)
                elif t in ("h1", "h3"):
                    self.ev.append((t, txt))
            self.buf = None

    def handle_data(self, d):
        if self.buf is not None:
            self.buf += d


def lire_mht(chemin):
    s = open(chemin, encoding="utf8", errors="ignore").read()
    corps = s[s.index("<body"):s.index("</body>")]
    corps = re.sub(r"<style.*?</style>", "", corps, flags=re.S)
    p = Lecteur()
    p.feed(corps)
    return p.ev


def norm(s):
    s = re.sub(r"[’‘`´]", "'", str(s))
    s = re.sub(r"[*†]+", "", s)
    s = re.sub(r"\(.*?\)", "", s)
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def charger_jeu():
    sets = {}
    for f in glob.glob(os.path.join(DATA, "encounter_sets", "*.json")):
        ident = os.path.basename(f)[:-5]
        nom = json.load(open(f, encoding="utf8")).get("name") or ident
        if ident.startswith(("standard", "expert", "tmnt_standard", "tmnt_expert")) or ident.endswith("_nemesis"):
            continue
        sets.setdefault(norm(nom), ident)
        sets.setdefault(norm(ident), ident)
    scenarios = {}
    for f in glob.glob(os.path.join(DATA, "scenarios", "*.json")):
        ident = os.path.basename(f)[:-5]
        if ident.endswith("_expert"):
            continue
        d = json.load(open(f, encoding="utf8"))
        scenarios[ident] = d.get("name") or ident
    packs = json.load(open(os.path.join(DATA, "sets_info.json"), encoding="utf8"))
    boite_de = {}
    for cle, info in packs.items():
        if not isinstance(info, dict):
            continue
        for e in info.get("encounters", []):
            boite_de.setdefault(e, cle)
    return sets, scenarios, boite_de


# Titres du document qui ne sont pas le nom du scenario du jeu : titre normalise -> identifiants (ou prefixes
# terminant par « * ») de scenarios du jeu.
ALIAS = {
    "kang": ["the_once_and_future_kang"],
    "thesinistersix": ["sinister_six"],
    "wreckingcrew": ["the_wrecking_crew"],
    "thehood": ["the_hood"],
    "projectwideawake": ["project_wideawake"],
    "towerdefense": ["the_tower_defense"],
    "stopthepresses": ["stop_the_presses_*"],
    "protectionracket": ["protection_racket_*"],
    "thegetaway": ["the_getaway_*"],
    "theraftbreakout": ["the_raft_breakout_*"],
}


def nettoyer_titre(t):
    return re.sub(r"\s*\[[^\]]*\]", "", t).strip()


def scenario_du_mechant(nom, scenarios):
    """Les scenarios du jeu dont le nom est ce mechant (« Ultron » ou « Ultron (Age of Ultron) »)."""
    n = norm(nettoyer_titre(nom))
    if n in ALIAS:
        sortie = []
        for a in ALIAS[n]:
            if a.endswith("*"):
                sortie += [i for i in scenarios if i.startswith(a[:-1])]
            elif a in scenarios:
                sortie.append(a)
        return sorted(sortie)
    return sorted(i for i, nm in scenarios.items() if norm(nm) == n or norm(nm.split("(")[0]) == n)


def difficulte(txt):
    m = re.match(r"^\s*([+-]?\d+)\s*(\?)?\s*$", txt or "")
    return (int(m.group(1)), bool(m.group(2))) if m else (None, False)


def importer(chemin):
    ev = lire_mht(chemin)
    sets, scenarios, boite_de = charger_jeu()
    section = villain = None
    gardees, ecartees, vus = [], [], set()
    combos_total = 0
    for genre, val in ev:
        if genre == "h1":
            section = val
        elif genre == "h3":
            villain = val
        elif genre == "row" and villain:
            cells = val
            if len(cells) < 5 or cells[0][:1] == ["Name"]:
                continue
            noms = [x for x in cells[0] if not re.search(r"\((1B|2B)\)$", x)]
            nom = " ".join(noms).replace("✔️", "").replace("✔", "").strip()
            recommande = "✔" in " ".join(cells[0])
            defaut = nom.upper() == "DEFAULT MODULAR"
            niveau, incertain = difficulte(cells[2][0] if cells[2] else "")
            bruts = [y.strip() for x in cells[1] if not x.startswith("(") for y in x.split("\n") if y.strip()]
            generique = [b for b in bruts if re.search(r"\b(any|random|mod sets?)\b|^modular set|\)$", b, re.I)]
            if niveau is None or not bruts:
                continue
            combos_total += 1
            if generique:
                ecartees.append((villain, nom or "Default modular", "sets génériques (« " + generique[0] + " »)"))
                continue
            ids, manquants = [], []
            for b in bruts:
                i = sets.get(norm(b))
                (ids if i else manquants).append(i or re.sub(r"[*†]+", "", b).strip())
            ids_sc = scenario_du_mechant(villain, scenarios)
            ligne = {
                "mechant": nettoyer_titre(villain), "speculatif": "SPECULATIVE" in villain.upper(), "scenarios": ids_sc, "nom": nom or "Default modular", "defaut": defaut,
                "recommande": recommande, "difficulte": niveau, "incertain": incertain,
                "sets": ids, "manquants": manquants, "note": " ".join(cells[3]).replace("\n", " ").strip(),
            }
            if not ids_sc:
                ecartees.append((villain, ligne["nom"], "méchant absent du jeu"))
                continue
            cle = (tuple(ids_sc), ligne["nom"], tuple(ids), tuple(manquants))
            if cle in vus:
                continue
            vus.add(cle)
            gardees.append(ligne)
    return gardees, ecartees, combos_total, sets, boite_de


def ecrire(gardees, boite_de):
    sorties = []
    for g in gardees:
        sorties.append({k: g[k] for k in ("scenarios", "nom", "defaut", "recommande", "difficulte", "incertain", "speculatif",
                                          "sets", "manquants", "note")})
    boites = {s: boite_de.get(s, "") for g in gardees for s in g["sets"]}
    corps = json.dumps({"combinaisons": sorties, "boiteDuSet": boites}, ensure_ascii=False, separators=(",", ":"))
    with open(SORTIE_JS, "w", encoding="utf8") as f:
        f.write("// Genere par tools/importer_villaintheory.py — NE PAS EDITER A LA MAIN.\n"
                "// Combinaisons de sets modulaires de VillainTheory (noms en anglais : ce sont des noms d'auteur).\n"
                "export const VILLAINTHEORY = " + corps + ";\n")


def rapport(gardees, ecartees, total):
    par_mechant = {}
    for g in gardees:
        par_mechant.setdefault(g["mechant"], []).append(g)
    jouables = [g for g in gardees if not g["manquants"]]
    grises = [g for g in gardees if g["manquants"]]
    manque = {}
    for g in grises:
        for m in g["manquants"]:
            manque[m] = manque.get(m, 0) + 1
    mech_abs = {}
    for v, n, raison in ecartees:
        mech_abs.setdefault(raison, {})
        mech_abs[raison][v] = mech_abs[raison].get(v, 0) + 1
    L = ["# Import VillainTheory : couverture", "",
         "Généré par `tools/importer_villaintheory.py` (ne pas éditer à la main).", "",
         f"- Combinaisons lues dans le document : **{total}**",
         f"- Gardées (méchant présent dans le jeu) : **{len(gardees)}**, dont **{len(jouables)} jouables** "
         f"et **{len(grises)} grisées** (au moins un set absent du jeu)",
         f"- Écartées (méchant absent du jeu) : **{len(ecartees)}**", "",
         "## Sets absents du jeu (combinaisons grisées)", ""]
    for m, n in sorted(manque.items(), key=lambda x: -x[1]):
        L.append(f"- {m} : {n} combinaison(s)")
    L += ["", "## Combinaisons écartées", ""]
    for raison, d in sorted(mech_abs.items()):
        L.append(f"### {raison}")
        for v, n in sorted(d.items()):
            L.append(f"- {v} : {n}")
        L.append("")
    L += ["", "## Gardées par méchant", ""]
    for v, l in sorted(par_mechant.items()):
        L.append(f"- {v} : {len(l)}")
    os.makedirs(os.path.dirname(RAPPORT), exist_ok=True)
    open(RAPPORT, "w", encoding="utf8").write("\n".join(L) + "\n")
    return len(jouables), len(grises)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    gardees, ecartees, total, _sets, boite_de = importer(sys.argv[1])
    ecrire(gardees, boite_de)
    j, g = rapport(gardees, ecartees, total)
    print(f"{total} lues, {len(gardees)} gardees ({j} jouables, {g} grisees), {len(ecartees)} ecartees")
