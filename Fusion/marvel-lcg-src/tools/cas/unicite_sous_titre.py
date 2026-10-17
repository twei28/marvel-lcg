# Cas test_capacites de l'UNICITE PAR SOUS-TITRE (decision de l'utilisateur, 17/10/2026).
# Filtre : `[unique-st]` (ou `[unique`). Doc : docs/reference/RECETTES-MOTEUR.md, section « Unicite par sous-titre ».
#
# Regle (Rules Reference v1.8, alignee sur le deck-builder `public/js/deckbuilder/regles.js`, `correspondent`) :
# deux cartes uniques d'un joueur (identite comprise) NE COEXISTENT PAS quand
#   - elles ont le meme titre et ni sous-titre ni titre d'alter ego d'aucun cote ; ou
#   - le sous-titre (ou le titre d'alter ego) de l'une egale le titre, le sous-titre ou le titre d'alter ego de l'autre.
# Avant le correctif le moteur ne jugeait que « meme titre ET meme sous-titre » : Ronin (Mikey) pouvait etre joue
# avec Michelangelo (alter ego Mikey), et Heavy Metal (Jenny) avec Nightwatcher (Jenny).
#
# LA TABLE DES CAS est dans `tools/tests-lanceur/unicite-sous-titre-cas.json`, lue AUSSI par le test du
# deck-builder (`tools/tests-lanceur/unicite-sous-titre.test.mjs`) : moteur et deck-builder repondent au meme
# tableau (un cas « parite: false » est un ecart voulu, explique dans le JSON).
#
# Montage : le heros est mis en forme heros, la carte a jouer est en main, avec 4 ressources ; `jouable` = `CanPlayBy`.
# Un TEMOIN par cas montre que c'est bien la carte en jeu qui bloque (sans elle la meme carte est jouable).
import json
import os

SC = "rhino"
MAIN4 = ["01088", "01089", "01090", "01088"]

FORMES = {
    "spider_man": "Puzzle.ChangeForm('01001b')",
    "michelangelo": "Puzzle.ChangeToFace('tm001b', 'tm001a')",
    "leonardo": "Puzzle.ChangeToFace('tl001b', 'tl001a')",
    "raphael": "Puzzle.ChangeToFace('tr001b', 'tr001a')",
    "donatello": "Puzzle.ChangeToFace('td001b', 'td001a')",
    "jennika": "Puzzle.ChangeToFace('tj001b', 'tj001a')",
    "nick_fury": "Puzzle.ChangeToFace('50034b', '50034a')",
}

_TABLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tests-lanceur", "unicite-sous-titre-cas.json")
with open(_TABLE, encoding="utf-8") as _f:
    _DONNEES = json.load(_f)


def _cas(c):
    en_jeu = c.get("en_jeu", [])
    mise = [FORMES[c["heros"]]] + [f"Puzzle.PutIntoPlay('{x}', under_control=True)" for x in en_jeu] \
        + [f"Puzzle.Gain('{c['a_jouer']}')"]
    return {"nom": "[unique-st] " + c["nom"], "pourquoi": c["pourquoi"], "scenario": SC, "heros": c["heros"],
            "mise_en_place": mise, "main": list(MAIN4), "declencher": [],
            "verifier": "max_par_joueur_jouable",
            "attendu": {"carte": c["a_jouer"], "jouable": not c["conflit"], "en_jeu": 0}}


CAS = [_cas(c) for c in _DONNEES["cas"]]
