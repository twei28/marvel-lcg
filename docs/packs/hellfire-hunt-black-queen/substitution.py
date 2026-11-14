#!/usr/bin/env python3
"""Preuve par SUBSTITUTION du pack hellfire_hunt_black_queen (hf361-hf366, hf401-hf422) dans MA plage de ports (10100-10199).

`tools/substituer_pack.py` espace ses cartes de 60 ports : trop pour une plage de 100. Meme principe, un module a la fois : on remplace
`hfNNN.py` par un stub `GetAbilities -> []`, on rejoue les cas dont le NOM contient « hfNNN » (+ espace), on compte les rouges, on RESTAURE.
SAUVEGARDE preable obligatoire (rien n'est commite) : le script sauvegarde lui-meme le pack dans <sortie>/sauvegarde et verifie l'empreinte a la fin.

Usage : python3 substitution.py <racine_moteur> <python> <sortie_dir>
"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys

RACINE, PYTHON, SORTIE = sys.argv[1], sys.argv[2], sys.argv[3]
SEULEMENT = sys.argv[4:]   # optionnel : ids a rejouer (sortie dans SUBSTITUTION-<ids>.txt)
PACK = os.path.join(RACINE, "src", "cards", "pack", "hellfire_hunt_black_queen")
GAME = os.path.join(RACINE, ".game-src-hfq")
STUB = 'from . import *\n\ndef GetAbilities() -> Sequence["Ability"]:\n    return []\n'


def empreinte():
    h = hashlib.md5()
    for f in sorted(glob.glob(os.path.join(PACK, "*.py"))):
        h.update(open(f, "rb").read())
    return h.hexdigest()


def purger():
    for d in glob.glob(os.path.join(PACK, "__pycache__")):
        shutil.rmtree(d, ignore_errors=True)


def jouer(filtre):
    rapport = os.path.join(SORTIE, "rapport.json")
    if os.path.exists(rapport):
        os.remove(rapport)
    env = dict(os.environ, PARALLELES="3", CAS_PREFIX="hfq")
    subprocess.run([PYTHON, "tools/test_capacites.py", GAME, "10100", rapport, filtre], cwd=RACINE, env=env, capture_output=True, timeout=900)
    if not os.path.exists(rapport):
        return None
    r = json.load(open(rapport))
    return r["total"], [c["nom"] for c in r["cas"] if not c["ok"]]


def main():
    os.makedirs(SORTIE, exist_ok=True)
    sauve = os.path.join(SORTIE, "sauvegarde")
    shutil.rmtree(sauve, ignore_errors=True)
    shutil.copytree(PACK, sauve, ignore=shutil.ignore_patterns("__pycache__"))
    avant = empreinte()
    lignes = []
    try:
        for f in sorted(glob.glob(os.path.join(PACK, "hf*.py"))):
            cid = os.path.basename(f)[:-3]
            if SEULEMENT and cid not in SEULEMENT:
                continue
            contenu = open(f, encoding="utf-8").read()
            try:
                open(f, "w", encoding="utf-8").write(STUB)
                purger()
                res = jouer("[hf] %s " % cid)
            finally:
                open(f, "w", encoding="utf-8").write(contenu)
                purger()
            if res is None:
                lignes.append("%-8s RAPPORT ABSENT (processus mort ?)" % cid)
            elif res[0] == 0:
                lignes.append("%-8s AUCUN CAS" % cid)
            else:
                verts = res[0] - len(res[1])
                lignes.append("%-8s rouges %d/%d%s" % (cid, len(res[1]), res[0], ("   restent VERTS : %d" % verts) if verts else ""))
            print(lignes[-1], flush=True)
    finally:
        for f in glob.glob(os.path.join(sauve, "*.py")):
            shutil.copy(f, os.path.join(PACK, os.path.basename(f)))
        purger()
    apres = empreinte()
    lignes.append("empreinte avant/apres : %s %s %s" % (avant, apres, "IDENTIQUES" if avant == apres else "DIFFERENTES !!"))
    open(os.path.join(SORTIE, "SUBSTITUTION%s.txt" % (("-" + "-".join(SEULEMENT)) if SEULEMENT else "")), "w", encoding="utf-8").write("\n".join(lignes) + "\n")
    print(lignes[-1])


main()
