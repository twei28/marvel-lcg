"""Le serveur de puzzles (E7) : publier, lire, modifier, supprimer, expirer, refuser.

    python3 site/test_puzzles_publies.py
"""

import copy
import json
import os
import sqlite3
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import puzzles_publies as pp  # noqa: E402

echecs = []


def cas(nom, obtenu, attendu):
    if obtenu == attendu:
        print("  ok    %s" % nom)
    else:
        echecs.append(nom)
        print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))


def refuse(nom, serveur, donnees, morceau, statut=400):
    try:
        serveur.publier(donnees, "x")
    except pp.ErreurPuzzle as e:
        cas(nom + " (statut)", e.statut, statut)
        cas(nom + " (raison)", any(morceau in r for r in e.raisons), True)
    else:
        cas(nom, "publié", "refusé")


PUZZLE = {
    "version": "0.5.8", "author": "", "cover": "01094", "comment": "", "seed": 1,
    "villain": ["01094"], "schemes": ["01097a,01097b"], "encounter_deck": ["01110"],
    "encounter_discard_pile": [], "set_aside": [], "expert": False,
    "players": [{"identities": ["01001b"], "hand_cards": ["01071"], "player_deck": ["01072"],
                 "player_discard_pile": [], "set_aside": [], "deck_name": "Spider-Man"}],
    "puzzle_command": ["Puzzle.RestoreCard('e1', '01059', 'ally', siege=0, health=2)", "Puzzle.SetHealth('01094', 9)"],
    "format": 2, "title": "Mon puzzle", "description": "d", "difficulty": 2, "hints": ["h"],
    "objectives": [{"kind": "defeat_villain", "target": "", "text": ""}], "objectives_mode": "all",
    "start_phase": "", "start_step": "", "first_player": 0, "solution_visibility": "after", "has_solution": False,
}

temps = [1_000_000.0]
with tempfile.TemporaryDirectory() as dossier:
    base = os.path.join(dossier, "p.db")
    s = pp.PuzzlesPublies(base, horloge=lambda: temps[0])

    pub = s.publier(PUZZLE, "  Arnaud<script>  ")
    cas("code au bon format", pub["code"][:3] == "PZ-" and len(pub["code"]) == 7, True)
    cas("la clé est rendue", len(pub["cle"]) >= 20, True)
    lu = s.lire(pub["code"])
    cas("lecture : le puzzle", lu["puzzle"]["title"], "Mon puzzle")
    cas("lecture : pseudo nettoyé", lu["pseudo"], "Arnaudscript")
    cas("lecture : auteur imposé par le serveur", lu["puzzle"]["author"], "Arnaudscript")
    cas("lecture : la clé n'est jamais rendue", pub["cle"] in json.dumps(lu), False)
    cx = sqlite3.connect(base)
    cas("la clé n'est pas stockée en clair", pub["cle"] in "".join(str(x) for x in cx.execute("SELECT * FROM puzzles_publies").fetchall()[0]), False)
    cx.close()
    cas("code saisi en minuscules et espacé", s.lire(pub["code"].lower().replace("-", " "))["code"], pub["code"])
    cas("code inconnu", s.lire("PZ-ZZZZ"), None)

    # --- refus
    v1 = copy.deepcopy(PUZZLE); v1["format"] = 1
    refuse("format 1", s, v1, "format 2")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["import os"]
    refuse("commande sans appel", s, c, "commande 1")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["Puzzle.Win()"]
    refuse("Win n'est pas permise", s, c, "inconnue")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["Puzzle.End('x')"]
    refuse("End n'est pas permise", s, c, "inconnue")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["Puzzle.ValidateObjective(0)"]
    refuse("ValidateObjective n'est pas permise", s, c, "inconnue")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["Puzzle.SetHealth(__import__('os'), 1)"]
    refuse("appel imbriqué", s, c, "commande 1")
    c = copy.deepcopy(PUZZLE); c["players"][0]["hand_cards"] = ["99999z"]
    refuse("carte inconnue", s, c, "carte inconnue")
    c = copy.deepcopy(PUZZLE); c["title"] = "  "
    refuse("titre vide", s, c, "titre")
    c = copy.deepcopy(PUZZLE); c["players"] = [c["players"][0]] * 5
    refuse("5 héros", s, c, "joueurs")
    c = copy.deepcopy(PUZZLE); c["description"] = "x" * 400_000
    refuse("trop gros", s, c, "trop gros", 413)
    refuse("pas un objet", s, ["a"], "objet JSON")
    c = copy.deepcopy(PUZZLE); c["players"][0]["identities"] = []
    refuse("héros sans identité", s, c, "identité")
    c = copy.deepcopy(PUZZLE); c["puzzle_command"] = ["Puzzle.RestoreCard('e1', 'x' * 500, 'ally')"]
    refuse("commande vicieuse", s, c, "commande 1")
    cas("rien n'a été publié par les refus", sqlite3.connect(base).execute("SELECT COUNT(*) FROM puzzles_publies").fetchone()[0], 1)

    # --- clés étrangères : une clé n'ouvre que son puzzle
    autre = s.publier(PUZZLE, "Autre")
    try:
        s.modifier(pub["code"], autre["cle"], PUZZLE)
        cas("mauvaise clé refusée", "modifié", "refusé")
    except pp.ErreurPuzzle as e:
        cas("mauvaise clé refusée", e.statut, 403)
    try:
        s.supprimer(pub["code"], "")
        cas("clé vide refusée", "supprimé", "refusé")
    except pp.ErreurPuzzle as e:
        cas("clé vide refusée", e.statut, 403)
    nouveau = copy.deepcopy(PUZZLE); nouveau["title"] = "Renommé"; nouveau["author"] = "usurpateur"
    s.modifier(pub["code"], pub["cle"], nouveau)
    relu = s.lire(pub["code"])
    cas("modification : titre", relu["puzzle"]["title"], "Renommé")
    cas("modification : l'auteur reste celui de la publication", relu["puzzle"]["author"], "Arnaudscript")
    mauvais = copy.deepcopy(PUZZLE); mauvais["puzzle_command"] = ["Puzzle.Win()"]
    try:
        s.modifier(pub["code"], pub["cle"], mauvais)
        cas("modification invalide refusée", "modifié", "refusé")
    except pp.ErreurPuzzle as e:
        cas("modification invalide refusée", e.statut, 400)
    cas("le puzzle n'a pas été abîmé", s.lire(pub["code"])["puzzle"]["puzzle_command"], PUZZLE["puzzle_command"])

    # --- 28 jours
    jour = 86400
    temps[0] += 27 * jour
    cas("jour 27 : encore là", s.lire(pub["code"]) is not None, True)
    cas("expire_le sans jouer", round(s.lire(pub["code"])["expire_le"] - temps[0]), 1 * jour)
    s.lire(pub["code"], jouer=True)
    cas("jouer remet le compteur à 28 jours", round(s.lire(pub["code"])["expire_le"] - temps[0]), 28 * jour)
    cas("nb_jeux compté", s.lire(pub["code"])["nb_jeux"], 1)
    temps[0] += 27 * jour
    cas("jour 54 : joué au jour 27, encore là", s.lire(pub["code"]) is not None, True)
    cas("jour 54 : l'autre (jamais joué) a expiré", s.lire(autre["code"]), None)
    cas("nettoyage : 1 supprimé", s.nettoyer(), 1)
    temps[0] += 2 * jour
    cas("jour 56 : plus joué depuis 29 jours, parti", s.lire(pub["code"]), None)
    cas("nettoyage : 1 supprimé", s.nettoyer(), 1)

    # --- suppression par le créateur
    p3 = s.publier(PUZZLE, "Z")
    s.supprimer(p3["code"], p3["cle"])
    cas("supprimé par sa clé", s.lire(p3["code"]), None)

    # --- codes uniques
    codes = {s.publier(PUZZLE, "Z")["code"] for _ in range(60)}
    cas("60 codes distincts", len(codes), 60)

sys.exit(1 if echecs else 0)
