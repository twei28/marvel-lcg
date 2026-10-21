# Cas test_capacites du set PUNISHMENT (scenario 3 « One Last Kill », pack MC×DC 2026), PU-4. Prefixe `[pun]`.
SC = "one_last_kill_jigsaw"
SCE = "one_last_kill_jigsaw_expert"
HEROS = "Puzzle.ChangeForm('01001b')"
SANS_DEFENSE = {"passer_sur_option": "Defense"}


def _u(nom, pourquoi, mise, declencher, attendu, **cle):
    deck = cle.pop("deck", None)
    cas = {"nom": "[pun] " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", SC), "heros": "spider_man",
           "mise_en_place": [*(["Puzzle.EmptyEncounterDeck()", "Puzzle.CreateEncounterDeck(%s)" % ", ".join(repr(x) for x in deck)] if deck else []), HEROS, *mise],
           "declencher": declencher, "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu,
           "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    _u("SONDE mise en place : Punisher I, Jigsaw, Target Lock, In the Crosshairs, M1911s",
       "x", [], [], {"en_jeu": ["pu086a", "pu056a", "pu091a", "pu092", "pu088b", "pu090b", "pu095"]}),
]
