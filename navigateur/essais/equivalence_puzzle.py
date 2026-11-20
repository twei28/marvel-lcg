#!/usr/bin/env python3
"""Compare le moteur NORMAL (Python 3.10) et celui du NAVIGATEUR (Pyodide, 3.12) sur des PUZZLES de format 2 (E10) :
meme puzzle, meme graine -> la CAPTURE de l'etat monte doit etre identique (cartes en jeu, etats, piles, stades) ainsi
que la validation et les objectifs.

    python3 navigateur/essais/equivalence_puzzle.py

Pre-requis : `python3 navigateur/construire.py --sans-pages` (cree dist/moteur.zip a partir des sources courantes).
"""
import json, os, shutil, subprocess, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
import equivalence as eq

SPIDER, AUTRE = "01001a,01001b", "12001a,12001b,12001c"


def base(joueurs, **extra):
    d = {"version": "0.5.8", "author": "t", "cover": "01094", "comment": "", "seed": 7, "villain": ["01094"],
         "schemes": ["01097a,01097b"], "encounter_deck": ["01110", "01154"], "encounter_discard_pile": [],
         "set_aside": [], "expert": False, "players": joueurs, "puzzle_command": [], "format": 2, "title": "t"}
    d.update(extra)
    return d


def joueur(identite, main=(), deck=(), defausse=()):
    return {"identities": [identite], "hand_cards": list(main), "player_deck": list(deck), "player_discard_pile": list(defausse), "set_aside": []}


PUZZLES = {
    "piles_et_etats": base([joueur("01001b", ["01071"], ["01072", "01073", "01074"], ["01075"])], puzzle_command=[
        "Puzzle.RestoreCard('e1', '01059', 'ally', siege=0, health=2, statuses=[['Stunned', 1]])",
        "Puzzle.RestoreCard('e2', '01006', 'support', siege=0, exhausted=True)",
        "Puzzle.RestoreState('01094', key='e3', health=9)", "Puzzle.RestoreState('01097b', key='e4', threat=4, tokens=[['acceleration_token', 2]])"]),
    "ameliorations_sbire_complot": base([joueur("01001b", [], ["01072"]), joueur("12001b", ["12007"], ["12003"])], villain=["01094", "01095"], puzzle_command=[
        "Puzzle.AdvanceVillain()", "Puzzle.RestoreState('01001b', key='e1', health=6, exhausted=True)",
        "Puzzle.RestoreCard('e2', '01008', 'upgrade', siege=0, host='e1', counters=[['web', 1]])",
        "Puzzle.RestoreCard('e3', '01101', 'minion', siege=1, engaged=True, health=2)",
        "Puzzle.RestoreState('01095', key='e4', statuses=[['Stunned', 1]])",
        "Puzzle.RestoreCard('e5', '01098', 'upgrade', siege=0, host='e4')",
        "Puzzle.RestoreCard('e6', '01107', 'side_scheme', siege=0, threat=3)", "Puzzle.SetFirstPlayer(1)"], first_player=1),
    "objectifs": base([joueur("01001b", ["01071"], ["01072"])],
        objectives=[{"kind": "defeat_villain", "target": "", "text": ""}, {"kind": "free_text", "target": "", "text": "Garde Black Cat"}],
        objectives_mode="all", puzzle_command=["Puzzle.RestoreState('01094', key='e1', health=5)"]),
}


def lancer(cmd, env, cwd):
    p = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True, timeout=420)
    for l in (p.stdout + p.stderr).splitlines():
        if l.startswith("RESULTAT "):
            return json.loads(l[9:])
    return {"erreur": "pas de resultat : " + (p.stdout + p.stderr)[-300:].replace("\n", " | ")}


def main():
    if not os.path.isfile(os.path.join(eq.NAV, "dist", "moteur.zip")):
        sys.exit("dist/moteur.zip absent : lancer navigateur/construire.py --sans-pages")
    eq.preparer_natif()
    echecs = 0
    for nom, puzzle in PUZZLES.items():
        env = {**os.environ, "PUZZLE_JSON": json.dumps(puzzle), "ENG_DIR": eq.NATIF}
        natif = lancer([eq.PY310, os.path.join(ICI, "partie_puzzle.py")], env, eq.NATIF)
        pyodide = lancer([shutil.which("node"), "lanceur_puzzle.mjs", "../dist", "partie_puzzle.py"], env, ICI)
        diffs = {k: (natif.get(k), pyodide.get(k)) for k in sorted(set(natif) | set(pyodide)) if natif.get(k) != pyodide.get(k)}
        etat = "IDENTIQUE" if not diffs and "erreur" not in natif else "DIFFERENT "
        echecs += etat != "IDENTIQUE"
        print(f"{etat} {nom}" + (f"  {json.dumps(diffs, ensure_ascii=False)[:600]}" if diffs else ""), flush=True)
        if "erreur" in natif:
            print("   erreur natif :", natif["erreur"][:300])
    print("TOUT EST IDENTIQUE" if not echecs else f"{echecs} puzzle(s) different(s)")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
