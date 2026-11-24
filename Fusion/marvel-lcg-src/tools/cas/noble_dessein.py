# Cas test_capacites de 62019 « Righteous Purpose » (FR « Noble Dessein »), signale en partie reelle le 01/11/2026 : « le bonus n'est donne
# qu'au premier allie a qui il reste un point de vie et pas aux deux autres ». Filtre : `[nd]`.
# Le cas existant `ul022` pose la carte APRES le degat : l'entree en jeu de la carte recalcule tout, le defaut n'y apparait pas. Ici la carte est
# deja en jeu et les allies TOMBENT ensuite a 1 PV (ce qui arrive en partie).
SC = "rhino"
HEROS = "Puzzle.ChangeForm('01001b')"


def M(card):
    return f"Puzzle.PutIntoPlay('{card}', under_control=True)"


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[nd] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man", "mise_en_place": list(mise),
           "declencher": list(declencher), "verifier": "etat_attendu", "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("62019 Righteous Purpose en jeu, TROIS allies tombent ensuite a 1 PV : chacun gagne +2 CTR et +2 ATQ",
       "la capacite doit etre recalculee quand les PV changent, pour CHAQUE allie (Hulk 5 PV -> 1, Spider-Man 3 PV -> 1, Deadpool 3 PV -> 1)",
       [HEROS, M("01050"), M("13019"), M("40024"), M("62019")],
       ["Puzzle.Damage('01050', 4)", "Puzzle.Damage('13019', 2)", "Puzzle.Damage('40024', 2)"],
       {"attributs_carte": [["01050", "attack", 2], ["01050", "thwart", 2], ["13019", "attack", 2], ["13019", "thwart", 2],
                            ["40024", "attack", 2], ["40024", "thwart", 2]]}),
    _c("62019 Righteous Purpose : un allie a 2 PV restants ne gagne rien (temoin), celui a 1 PV gagne +2/+2",
       "« exactly 1 hit point remaining » : Hulk (5 PV, 3 degats : 2 restants) n'a rien, Deadpool (3 PV, 2 degats : 1 restant) a +2/+2",
       [HEROS, M("01050"), M("40024"), M("62019")],
       ["Puzzle.Damage('01050', 3)", "Puzzle.Damage('40024', 2)"],
       {"attributs_carte": [["01050", "attack", 0], ["01050", "thwart", 0], ["40024", "attack", 2], ["40024", "thwart", 2]]}),
    _c("62019 Righteous Purpose : un allie soigne au-dela de 1 PV perd le bonus",
       "Deadpool tombe a 1 PV (+2/+2) puis recupere 1 PV (2 restants) : le bonus disparait",
       [HEROS, M("40024"), M("62019")],
       ["Puzzle.Damage('40024', 2)", "Puzzle.Heal('40024', 1)"],
       {"attributs_carte": [["40024", "attack", 0], ["40024", "thwart", 0]]}),
]
