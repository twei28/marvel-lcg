#!/usr/bin/env python3
"""Classe les cartes d'aspect TMNT qui ont une officielle d'origine.

Regle de l'utilisateur (17/10/2026) : si SEULE l'image change, la carte est un
ART ALTERNATIF de l'officielle (propose a tous) ; si quoi que ce soit change
(nom, sous-titre, unicite, traits, texte, cout/ressource/stats, type, bandeau),
c'est une carte EXCLUSIVE TMNT (heros TMNT seulement).

Lit data/cards.json et tools/tmnt_aspects_numerotation.tsv (colonne
card_id_origine). Usage :
    python3 tools/classer_reskins_tmnt.py             # resume
    python3 tools/classer_reskins_tmnt.py --json      # [[id, nom, origine, [ecarts]], ...]
    python3 tools/classer_reskins_tmnt.py --art-seul  # ids "art seul" (un par ligne)
"""
import csv
import json
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
CARTES = RACINE / "data" / "cards.json"
TSV = RACINE / "tools" / "tmnt_aspects_numerotation.tsv"


def charger_cartes(chemin=CARTES):
    d = json.load(open(chemin, encoding="utf-8"))
    cartes = {}
    for v in d.values():
        if isinstance(v, list):
            for c in v:
                if isinstance(c, dict) and c.get("card_id"):
                    cartes[c["card_id"]] = c
    return cartes


def lire_origines(chemin=TSV):
    """[(card_id TMNT, card_id officielle)] pour les lignes qui ont une origine."""
    with open(chemin, encoding="utf-8") as f:
        return [(r["card_id"], r["card_id_origine"].strip())
                for r in csv.DictReader(f, delimiter="\t") if r["card_id_origine"].strip()]


def _texte_sans_citation(t):
    # La citation est une ligne qui COMMENCE par <i> (avec ou sans « —Auteur »).
    t = "\n".join(l for l in (t or "").split("\n") if not l.lstrip().startswith("<i>"))
    return re.sub(r"\s+", " ", t.replace("[[", "").replace("]]", "")).strip().lower()


def _nom(c):
    return re.sub(r"^\*\s*", "", c.get("name", "")).strip()


def ecarts(tmnt, off):
    """Liste des aspects qui different entre la carte TMNT et l'officielle."""
    e = []
    if _nom(tmnt) != _nom(off):
        e.append("nom")
    if (tmnt.get("subtitle") or "") != (off.get("subtitle") or ""):
        e.append("sous-titre")
    if tmnt.get("name", "").startswith("*") != off.get("name", "").startswith("*"):
        e.append("unicité")
    if sorted(tmnt.get("traits") or []) != sorted(off.get("traits") or []):
        e.append("traits")
    if _texte_sans_citation(tmnt.get("text")) != _texte_sans_citation(off.get("text")):
        e.append("texte")
    if (tmnt.get("desc") or {}) != (off.get("desc") or {}):
        e.append("desc")
    if tmnt.get("type") != off.get("type"):
        e.append("type")
    if sorted(tmnt.get("unique_also") or []) != sorted(off.get("unique_also") or []):
        e.append("bandeau")
    return e


def classer(cartes=None, origines=None):
    cartes = cartes or charger_cartes()
    origines = origines or lire_origines()
    res = []
    for cid, oid in origines:
        t, o = cartes.get(cid), cartes.get(oid)
        if not t or not o:
            continue
        res.append([cid, t["name"], oid, ecarts(t, o)])
    return res


def main():
    res = classer()
    if "--json" in sys.argv:
        print(json.dumps(res, ensure_ascii=False))
    elif "--art-seul" in sys.argv:
        print("\n".join(r[0] for r in res if not r[3]))
    else:
        seul = [r for r in res if not r[3]]
        print(f"{len(res)} cartes avec officielle : {len(seul)} art seul, {len(res) - len(seul)} exclusives")
        for r in res:
            if r[3]:
                print(f"  exclusive {r[0]} {r[1]} (<- {r[2]}) : {', '.join(r[3])}")


if __name__ == "__main__":
    main()
