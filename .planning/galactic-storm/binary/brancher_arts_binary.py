#!/usr/bin/env python3
"""Declare les 19 reskins « art seul » de Binary comme arts alternatifs (code `binary`) dans
data/arts_alternatifs.json, avec une SERIE `binary` qui en fait l'art par defaut du heros Binary
(comme `tmnt` pour les heros TMNT), puis relance tools/generer_arts_cartes.py. Relancable.

Images : importer_images_binary.py. Cartes NON branchees : Avengers Mansion 01091 (le scan imprime
le trait « AVENGERS. » au lieu de « AVENGER. », question Q2 de .planning/todos/2026-10-20-gs1-questions.md).
Usage : python3 brancher_arts_binary.py [racine_de_la_copie]
"""
import importlib.util
import json
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(os.path.join(ICI, "..", "..", ".."))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")
spec = importlib.util.spec_from_file_location("imp", os.path.join(ICI, "importer_images_binary.py"))
imp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp)

CODE = imp.CODE
SERIE = {
    "nom": "Binary (Kajislav)",
    "nom_en": "Binary (Kajislav)",
    "heros_cartes": ["gs001"],
    "heros_ids": ["binary"],
    "sets_exclusifs": [],
}

src = os.path.join(MOTEUR, "data", "arts_alternatifs.json")
d = json.load(open(src, encoding="utf-8"))
d["series"][CODE] = SERIE
for off in imp.ARTS:
    codes = d["cartes"].setdefault(off, [])
    if CODE not in codes:
        codes.append(CODE)
with open(src, "w", encoding="utf-8") as o:
    json.dump(d, o, ensure_ascii=False, indent=1)
    o.write("\n")
subprocess.check_call([sys.executable, os.path.join(MOTEUR, "tools", "generer_arts_cartes.py")])
print(f"{len(imp.ARTS)} arts `{CODE}` declares")
