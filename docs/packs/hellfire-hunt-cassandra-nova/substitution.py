#!/usr/bin/env python3
"""Preuve par substitution du pack hellfire_hunt_cassandra_nova, dans la plage de ports 10500-10599 (tools/substituer_pack.py avance de 60 ports par
carte : 38 cartes sortiraient de la plage). Meme principe : pour chaque module, le stub vide remplace le fichier, les cas dont le nom contient
`<card_id> ` sont rejoues, on compte les rouges, on restaure. SAUVEGARDE d'abord (rien n'est commite) ; empreinte avant/apres.
Usage : python3 substitution.py <racine_moteur> <game_dir> [prefixe_de_card_id ...]      (a lancer depuis la racine du moteur, avec le python du venv)"""
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys

RACINE = os.path.abspath(sys.argv[1])
GAME_DIR = os.path.abspath(sys.argv[2])
PREFIXES = sys.argv[3:] or ["hf6", "hf37", "hf38"]
PACK = os.path.join(RACINE, "src", "cards", "pack", "hellfire_hunt_cassandra_nova")
SAUV = "/tmp/sauvegarde_pack_hfn"
STUB = 'from . import *\n\ndef GetAbilities() -> Sequence["Ability"]:\n    return []\n'
BASES = [10500, 10520, 10540, 10560, 10580]


def empreinte() -> str:
    h = hashlib.md5()
    for f in sorted(glob.glob(os.path.join(PACK, "*.py"))):
        h.update(open(f, "rb").read())
    return h.hexdigest()


def purger() -> None:
    shutil.rmtree(os.path.join(PACK, "__pycache__"), ignore_errors=True)


def main() -> None:
    shutil.rmtree(SAUV, ignore_errors=True)
    shutil.copytree(PACK, SAUV)
    avant = empreinte()
    print("empreinte avant :", avant, flush=True)
    fichiers = sorted(f for f in glob.glob(os.path.join(PACK, "hf*.py")) if any(os.path.basename(f).startswith(p) for p in PREFIXES))
    bilan = []
    for i, f in enumerate(fichiers):
        cid = os.path.basename(f)[:-3]
        vrai = f + ".vrai"
        shutil.copy2(f, vrai)
        try:
            open(f, "w").write(STUB)
            purger()
            rapport = "/tmp/subst_hfn_%s.json" % cid
            env = dict(os.environ, CAS_PREFIX="hfs")
            subprocess.run([sys.executable, os.path.join(RACINE, "tools", "test_capacites.py"), GAME_DIR, str(BASES[i % len(BASES)]), rapport, cid + " "],
                           capture_output=True, timeout=3600, env=env, cwd=RACINE)
            try:
                r = json.load(open(rapport))
                morts = sum(1 for c in r["cas"] if not c["ok"] and "processus mort" in (c.get("message") or ""))
                rouges = sum(1 for c in r["cas"] if not c["ok"]) - morts
                total = r["total"]
            except Exception:
                rouges, total, morts = -1, -1, 0
        finally:
            shutil.move(vrai, f)
            purger()
        if total == 0:
            v = "AUCUN CAS"
        elif morts:
            v = "%d/%d processus MORT(S) : non probant" % (morts, total)
        elif rouges == total:
            v = "rouges %d/%d" % (rouges, total)
        else:
            v = "rouges %d/%d (un cas reste vert sans module : contre-cas d'ABSENCE d'effet ?)" % (rouges, total)
        bilan.append((cid, total, rouges, v))
        print("SUBST", cid, ":", v, flush=True)
    apres = empreinte()
    print("empreinte apres :", apres, "IDENTIQUE" if apres == avant else "DIFFERENTE : RESTAURER DEPUIS " + SAUV)
    print("BILAN :", sum(1 for _, t, r, _ in bilan if t > 0 and r > 0), "/", len(bilan), "cartes avec au moins un cas rouge sans leur module")


main()
