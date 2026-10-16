#!/usr/bin/env python3
"""Compare le moteur NORMAL (Python 3.10) et celui du NAVIGATEUR (Pyodide, Python 3.12) sur les memes parties.

    python3 navigateur/essais/equivalence.py [N=24] [graine=2026]

Meme heros, meme scenario, meme graine, meme pilote deterministe : une partie qui differe (questions posees,
round atteint, issue, PV du vilain) trahit une difference de comportement du moteur sous WebAssembly.
Pre-requis : `python3 navigateur/construire.py` (cree dist/moteur.zip).
"""
import json, os, random, shutil, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
ICI = os.path.dirname(os.path.abspath(__file__)); NAV = os.path.dirname(ICI); RACINE = os.path.dirname(NAV)
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src"); NATIF = os.path.join(NAV, ".cache", "natif")
# Le Python 3.10 du moteur natif : variable NARWHAL_PY310, sinon l'environnement du
# lanceur Linux (.venv-linux), sinon l'ancien chemin WSL.
PY310 = os.environ.get("NARWHAL_PY310") or next(
    (p for p in (os.path.join(RACINE, ".venv-linux", "bin", "python"),
                 os.path.expanduser("~/marvel-work/python/bin/python3.10")) if os.path.exists(p)),
    os.path.expanduser("~/marvel-work/python/bin/python3.10"))
N = int(sys.argv[1]) if len(sys.argv) > 1 else 24
GRAINE = int(sys.argv[2]) if len(sys.argv) > 2 else 2026

def preparer_natif():
    shutil.rmtree(NATIF, ignore_errors=True); os.makedirs(NATIF)
    ign = shutil.ignore_patterns("__pycache__", "*.bak*", "marvelcdb")
    for d in ("cards", "core", "engine", "game", "editor"):
        shutil.copytree(os.path.join(MOTEUR, "src", d), os.path.join(NATIF, d), ignore=ign)
    for f in ("build.py", "game_entry.py", "main.py"):
        shutil.copy(os.path.join(MOTEUR, "src", f), NATIF)
    for d in ("data", "deck", "puzzle"):
        shutil.copytree(os.path.join(MOTEUR, d), os.path.join(NATIF, d), ignore=ign)
    # EXACTEMENT la configuration du paquet navigateur (statistiques et hauts faits compris) : l'ecart de
    # configuration change le nombre d'effets de regle, donc les identifiants d'objets, donc certaines parties.
    sys.path.insert(0, NAV)
    import construire
    json.dump(construire.config_navigateur(), open(os.path.join(NATIF, "launch.json"), "w"), indent=1)
    for d in ("persist/replays", "persist/campagnes", "persist/deck/custom", "deck/custom"):
        os.makedirs(os.path.join(NATIF, d), exist_ok=True)

def combos():
    heros = sorted(f[:-5] for f in os.listdir(os.path.join(MOTEUR, "deck", "starter")) if f.endswith(".json"))
    vilains = sorted(f[:-5] for f in os.listdir(os.path.join(MOTEUR, "data", "scenarios")) if f.endswith(".json"))
    r = random.Random(GRAINE)
    hs = r.sample(heros, min(N, len(heros))); out = []
    for i, h in enumerate(hs):
        out.append((h, r.choice(vilains), r.randint(1, 9999)))
    return out

def lancer(cmd, env, cwd, delai=420):
    t = time.time()
    try:
        p = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True, timeout=delai)
        sortie = p.stdout + p.stderr
    except subprocess.TimeoutExpired:
        return {"erreur": "delai depasse"}
    for l in sortie.splitlines():
        if l.startswith("RESULTAT "):
            return json.loads(l[9:])
    return {"erreur": "pas de resultat: " + sortie[-200:].replace("\n", " | ")}

def config_du_run(h, v, s):
    """Une copie de la configuration par partie native : statistiques et sauvegardes ne se partagent pas
    entre les parties lancees en parallele (le paquet navigateur, lui, part d'un systeme de fichiers vierge)."""
    import construire
    ident = f"{h}-{s}"
    texte = json.dumps(construire.config_navigateur()).replace("./persist/", f"./persist/{ident}/")
    shutil.rmtree(os.path.join(NATIF, "persist", ident), ignore_errors=True)     # ETAT VIERGE a chaque partie
    for d in ("replays", "campagnes", "deck/custom"):
        os.makedirs(os.path.join(NATIF, "persist", ident, d), exist_ok=True)
    nom = f"launch-{ident}.json"
    open(os.path.join(NATIF, nom), "w").write(texte)
    return nom

def un(c):
    h, v, s = c
    env = {**os.environ, "HERO": h, "VILLAIN": v, "SEED": str(s), "MAX_ASKS": "700", "ENG_DIR": NATIF, "CONFIG": config_du_run(h, v, s),
           "WSLENV": "HERO:VILLAIN:SEED:MAX_ASKS:" + os.environ.get("WSLENV", "")}
    nat = lancer([PY310, os.path.join(ICI, "partie_headless.py")], env, NATIF)
    pyo = lancer([shutil.which("node"), "lanceur_pyodide.mjs", "../dist", "partie_headless.py"], env, ICI)
    # Le moteur normal est reproductible (etat vierge) ; celui du navigateur a, RAREMENT, une variabilite d'un lancement a
    # l'autre (constatee sur Conan et Invisible Woman, des heros a plusieurs formes : l'ordre des boutons « Change To »
    # change). Une difference n'est donc retenue comme REELLE que si AUCUN des lancements ne retrouve le resultat normal.
    essais = [pyo]
    if any(nat.get(k) != pyo.get(k) for k in CLES):
        for _ in range(4):
            if all(nat.get(k) == essais[-1].get(k) for k in CLES):
                break
            essais.append(lancer([shutil.which("node"), "lanceur_pyodide.mjs", "../dist", "partie_headless.py"], env, ICI))
    egal = next((x for x in essais if all(nat.get(k) == x.get(k) for k in CLES)), None)
    if egal is not None and egal is not pyo:
        pyo = {**egal, "instable": True, "lancements": len(essais)}
    return c, nat, pyo

CLES = ("asks", "round", "won", "reason", "vilain_pv", "cartes", "erreur", "setup")
def main():
    if not os.path.isfile(os.path.join(NAV, "dist", "moteur.zip")):
        sys.exit("dist/moteur.zip absent : lancer navigateur/construire.py")
    preparer_natif()
    cs = combos(); print(f"{len(cs)} parties, 3 en parallele")
    ok = ko = inst = 0; rapport = []
    with ThreadPoolExecutor(3) as ex:
        for c, nat, pyo in ex.map(un, cs):
            diff = {k: (nat.get(k), pyo.get(k)) for k in CLES if nat.get(k) != pyo.get(k)}
            rapport.append({"combo": c, "natif": nat, "pyodide": pyo, "differences": diff})
            if diff: ko += 1
            else:
                ok += 1
                if pyo.get("instable"): inst += 1
            print(("IDENTIQUE " if not diff else "DIFFERENT  ") + ("(INSTABLE: retrouve au lancement " + str(pyo["lancements"]) + ") " if pyo.get("instable") else "") + f"{c[0]:22} contre {c[1]:28} graine {c[2]:5} -> natif {nat.get('asks')}q r{nat.get('round')} | pyodide {pyo.get('asks')}q r{pyo.get('round')}" + (f"  {diff}" if diff else ""), flush=True)
    json.dump(rapport, open(os.path.join(ICI, "resultats-equivalence.json"), "w"), indent=1, ensure_ascii=False)
    print(f"\n{ok} identiques, {ko} differentes sur {len(cs)}" + (f"  (dont {inst} instables : identiques au moteur normal a un lancement sur plusieurs)" if inst else ""))

if __name__ == "__main__":
    main()
