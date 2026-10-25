# Cas test_capacites du scenario THE VAULT, 3e fichier : LES HUIT VILAINS (vt001-vt016), stades I et II. Memes conventions et aides que
# `the_vault.py` ; prefixe de nom « [vt] ».
#
# Pour chaque vilain : (1) la Reponse forcee « After you attack X with a card you control, choose to either A or place 1 threat on the main
# scheme » dans ses DEUX branches (`choisir_option` force la branche menace ; sans lui le pilote prend la 1re option, A) ; (2) au stade II,
# le « When Revealed » (revelation vraie : `Puzzle.RevealNextVillain(True)`).
# L'attaquant est Spider-Man en forme HEROS (ATK 2 ; le vilain a 7 ou 8 PV par joueur : il ne tombe pas) ; Mentallo est attaque par Jessica Jones
# (01059, allie ATK 2, sans capacite d'entree) pour que l'identite soit encore prete quand « exhaust your identity » doit la fatiguer.
import importlib.util as _imp
import os as _os

_spec = _imp.spec_from_file_location("cas_vt_aides", _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "the_vault.py"))
_h = _imp.module_from_spec(_spec)
_spec.loader.exec_module(_h)
_c, mechants_en_jeu, sous_le_vault = _h._c, _h.mechants_en_jeu, _h.sous_le_vault
HEROS = _h.HEROS
MENACE = "Place_1_threat_on_the_main_scheme"
COMPLOT = "vt017b"
H = "01001a"          # Spider-Man, forme heros
DECK6 = "Puzzle.CreatePlayerDeck('01089', '01089', '01089', '01089', '01089', '01089')"
ALLIE = "Puzzle.PutIntoPlay('01059', under_control=True)"
SIDE = "01107"        # une manigance annexe quelconque (Mad Thinker) ; on lui pose 2 menaces


def _fr(num, nom, libelle, *, a, b, allie=False, mise=(), coups=1):
    """Les deux cas de la Reponse forcee d'un vilain (stade `num`) : branche A et branche menace.
    `a` / `b` : attendus de la branche A / de la branche menace (la menace du complot s'ajoute a `b`)."""
    cid = f"vt{num:03d}"
    stade = "I" if num % 2 else "II"
    base = [HEROS] + ([ALLIE] if allie else []) + list(mise)
    sous = sous_le_vault("vt005" if num not in (5, 6) else "vt003")
    un = "Puzzle.Attack('01059')" if allie else f"Puzzle.Attack('{H}')"
    attaque = [un] if coups == 1 else ([un, f"Puzzle.Ready('{H}')"] * coups)[:-1]   # le heros s'epuise en attaquant : on le redresse entre deux coups
    return [
        _c(f"{cid} {nom} ({stade}) : apres une attaque, branche A ({libelle})",
           f"« After you attack {nom} with a card you control, choose to either {libelle} or place 1 threat on the main scheme » : branche A",
           base + mechants_en_jeu(cid) + sous, attaque, dict(a), cibles=[cid] * coups, main_exclusive=["01090"]),
        _c(f"{cid} {nom} ({stade}) : apres une attaque, branche menace (1 menace sur le complot principal, rien de la branche A)",
           "meme Reponse forcee, branche « place 1 threat on the main scheme »",
           base + mechants_en_jeu(cid) + sous, attaque, {"menace": [[COMPLOT, coups]], **b}, cibles=[cid] * coups, choisir_option=MENACE,
           main_exclusive=["01090"]),
    ]


def _wr(num, nom, texte, *, attendu, mise=(), extra=()):
    cid = f"vt{num:03d}"
    return _c(f"{cid} {nom} (II) When Revealed : {texte}",
              f"« When Revealed: {texte} »",
              [HEROS] + list(mise) + sous_le_vault("vt005" if num not in (5, 6) else "vt003") + [f"Puzzle.BuildVillainDeck('{cid}')"],
              ["Puzzle.RevealNextVillain(True)"] + list(extra), dict(attendu), main_exclusive=["01090"])


CAS = []
for _n in (1, 2):
    CAS += _fr(_n, "Batroc", "discard the top 3 cards of the encounter deck",
               a={"defausse_rencontre": ["01105"] * 3}, b={"defausse_rencontre": []})
for _n in (3, 4):
    CAS += _fr(_n, "Mentallo", "exhaust your identity",
               a={"exhausted": [H]}, b={"pret": [H]}, allie=True)
for _n in (5, 6):
    CAS += _fr(_n, "Grey Gargoyle", "stun the attacker",
               a={"statuts": [[H, "Stunned"]]}, b={"statuts_absents": [[H, "Stunned"]]})
for _n in (7, 8):
    CAS += _fr(_n, "Hydro-Man", "deal 1 damage to each character you control",
               a={"degats_identite": 1}, b={"degats_identite": 0})
for _n in (9, 10):
    CAS += _fr(_n, "Mad Thinker", "place 1 threat on each side scheme",
               a={"menace": [[SIDE, 3], [COMPLOT, 0]]}, b={"menace": [[COMPLOT, 1], [SIDE, 2]]},
               mise=[f"Puzzle.PutIntoPlay('{SIDE}')", f"Puzzle.SetThreat('{SIDE}', 2)"])
for _n in (11, 12):
    CAS += _fr(_n, "Nekra", "give Nekra 1 facedown boost card",
               a={"boosts_sur": [[f"vt{_n:03d}", 1]]}, b={"boosts_sur": [[f"vt{_n:03d}", 0]]})
for _n in (13, 14):
    CAS += _fr(_n, "Vapor", "confuse the attacker",
               a={"statuts": [[H, "Confused"]]}, b={"statuts_absents": [[H, "Confused"]]})
CAS += _fr(15, "Venom", "heal 1 damage from him", a={"degats": [["vt015", 1]]}, b={"degats": [["vt015", 2]]})
# Venom II est TENACE (Toughness) : sa carte Tenace absorbe la 1re attaque ; on attaque donc DEUX fois (la 2e inflige 2 degats, moins 1 soigne ; la menace compte 2).
CAS += _fr(16, "Venom", "heal 1 damage from him", a={"degats": [["vt016", 1]]}, b={"degats": [["vt016", 2]]}, coups=2)

# ---------------------------------------------------------------- When Revealed (stades II)
CAS += [
    _wr(2, "Batroc", "each player discards the top 5 cards of their deck", attendu={"taille_deck_joueur": 1},
        mise=["Puzzle.EmptyPlayerDeck()", DECK6]),
    _wr(4, "Mentallo", "each player exhausts a character they control", attendu={"exhausted": [H]}),
    _wr(6, "Grey Gargoyle", "each player stuns a character they control", attendu={"statuts": [[H, "Stunned"]]}),
    _wr(8, "Hydro-Man", "deal 1 damage to each friendly character", attendu={"degats_identite": 1}, mise=[ALLIE]),
    _wr(10, "Mad Thinker", "1 threat on the main scheme for each enemy in play (le vilain + 2 sbires = 3)", attendu={"menace": [[COMPLOT, 3]]},
        mise=["Puzzle.PutIntoPlay('01101')", "Puzzle.PutIntoPlay('01102')"]),
    _wr(12, "Nekra", "give each villain 1 facedown boost card (Nekra II et un autre vilain deja en jeu)",
        attendu={"boosts_sur": [["vt012", 1], ["vt001", 1]]}, mise=mechants_en_jeu("vt001")),
    _wr(14, "Vapor", "each player confuses a character they control", attendu={"statuts": [[H, "Confused"]]}),
]
