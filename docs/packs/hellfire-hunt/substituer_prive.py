#!/usr/bin/env python3
"""(Generalisation du 01/11/2026 de `hellfire-hunt-torn/substituer_prive.py` a TOUT pack hf : le nom du pack est le 1er argument.)
Preuve par substitution d'un pack hf SUR UNE COPIE PRIVEE du pack (jamais sur les sources partagees).

Pourquoi : `tools/substituer_pack.py` remplace le module par un stub DANS `src/cards/pack/...` pendant le test. Plusieurs agents partagent ce dossier (le scenario
Cassandra Nova joue les cartes Immensity hf35x) : un stub pose un instant fausserait leurs cas. Ici le jeu tourne sur `<racine>/.hft-prive/cards`, un arbre de liens
vers `src/cards` SAUF `pack/hellfire_hunt_torn`, copie reelle ; les stubs ne touchent que cette copie.

Usage (depuis Fusion/marvel-lcg-src) :
    ../../.venv-linux/bin/python ../../docs/packs/hellfire-hunt/substituer_prive.py <pack> <port_base> <sortie.json> [card_id ...]
    (<pack> = hellfire_hunt | hellfire_hunt_white_queen | hellfire_hunt_black_king | ... ; copie du harnais `.game-src-hff`)
Sans card_id : tous les modules du pack. Un cas dont le NOM contient « <card_id> » (suivi d'une espace) est rejoue ; verdict « rouges N/N » = carte prouvee.
"""
import glob
import json
import os
import shutil
import subprocess
import sys

RACINE = os.getcwd()
PACK = sys.argv.pop(1)
PRIVE = os.path.join(RACINE, ".hff-prive")
GAME = os.path.join(RACINE, ".game-src-hffx")
STUB = 'from . import *\n\ndef GetAbilities() -> Sequence["Ability"]:\n    return []\n'


def preparer():
    shutil.rmtree(PRIVE, ignore_errors=True)
    os.makedirs(os.path.join(PRIVE, "cards", "pack"))
    src = os.path.join(RACINE, "src", "cards")
    for nom in os.listdir(src):
        if nom in ("pack", "__pycache__"):
            continue
        os.symlink(os.path.join(src, nom), os.path.join(PRIVE, "cards", nom))
    for nom in os.listdir(os.path.join(src, "pack")):
        cible = os.path.join(PRIVE, "cards", "pack", nom)
        if nom == PACK:
            shutil.copytree(os.path.join(src, "pack", nom), cible, ignore=shutil.ignore_patterns("__pycache__"))
        elif nom != "__pycache__":
            os.symlink(os.path.join(src, "pack", nom), cible)
    shutil.rmtree(GAME, ignore_errors=True)
    for d in glob.glob(GAME + "-par*"):       # les dossiers paralleles d'une passe precedente gardent leur ancien launch.json
        shutil.rmtree(d, ignore_errors=True)
    shutil.copytree(os.path.join(RACINE, ".game-src-hff"), GAME, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    os.remove(os.path.join(GAME, "cards"))
    os.symlink(os.path.join(PRIVE, "cards"), os.path.join(GAME, "cards"))
    lj = os.path.join(GAME, "launch.json")
    texte = open(lj).read().replace(".game-src-hff/", ".game-src-hffx/")
    open(lj, "w").write(texte)


def purger(dossier):
    for c in glob.glob(os.path.join(dossier, "**", "__pycache__"), recursive=True):
        shutil.rmtree(c, ignore_errors=True)


def main():
    port = int(sys.argv[1])
    sortie = sys.argv[2]
    ids = sys.argv[3:]
    preparer()
    pack = os.path.join(PRIVE, "cards", "pack", PACK)
    modules = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(pack, "hf*.py")))
    if ids:
        modules = [m for m in modules if m in ids]
    harnais = os.path.join(RACINE, "tools", "test_capacites.py")
    env = dict(os.environ, CAS_PREFIX="hffx", PARALLELES="3")
    bilan = {}
    for card_id in modules:
        f = os.path.join(pack, card_id + ".py")
        vrai = open(f).read()
        try:
            open(f, "w").write(STUB)
            purger(pack)
            rapport = f"/tmp/subst_hff_{card_id}.json"
            if os.path.exists(rapport):
                os.remove(rapport)
            # hf503a : ses deux cas de CARNET SORTANT ecrivent le meme fichier (`campaign_log_last_file`) : jamais en parallele.
            env_carte = dict(env, PARALLELES="1" if card_id == "hf503a" else env["PARALLELES"])
            subprocess.run([sys.executable, harnais, GAME, str(port), rapport, f"{os.environ.get('HFF_TAG', '[hf]')} {card_id} "], env=env_carte, capture_output=True, timeout=3000)
            try:
                r = json.load(open(rapport))
                total = r["total"]
                morts = sum(1 for c in r["cas"] if not c["ok"] and "processus mort" in (c.get("message") or ""))
                rouges = sum(1 for c in r["cas"] if not c["ok"]) - morts
                restent = [c["nom"][:90] for c in r["cas"] if c["ok"]]
            except Exception:
                total, rouges, morts, restent = -1, -1, 0, []
        finally:
            open(f, "w").write(vrai)
            purger(pack)
        bilan[card_id] = {"total": total, "rouges": rouges, "morts": morts, "restent_verts": restent}
        print(f"SUBST {card_id} : rouges {rouges}/{total}" + (f" ({morts} morts)" if morts else "") + (f"  VERTS SANS MODULE : {restent}" if restent else ""), flush=True)
    json.dump(bilan, open(sortie, "w"), indent=1, ensure_ascii=False)
    if not os.environ.get("HFF_GARDER"):
        shutil.rmtree(PRIVE, ignore_errors=True)
        for d in [GAME] + glob.glob(GAME + "-par*"):
            shutil.rmtree(d, ignore_errors=True)


main()
