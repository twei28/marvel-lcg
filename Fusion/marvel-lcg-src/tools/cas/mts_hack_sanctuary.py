# Cas test_capacites : 21184a Hack Sanctuary's Computer (campagne Mad Titan's Shadow, rapport #105). Prefixe `[mts]`.
# Montage : scenario `thanos`, Spider-Man (01001) en HEROS, deck rencontre vide.
SC = "thanos"


def _m(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[mts] " + nom, "pourquoi": pourquoi, "scenario": SC, "heros": "spider_man",
           "mise_en_place": ["Puzzle.EmptyEncounterDeck()", "Puzzle.ChangeForm('01001b')", *mise],
           "declencher": declencher, "verifier": "etat_attendu", "attendu": attendu, "main_exclusive": cle.pop("main_exclusive", ["01088"])}
    cas.update(cle)
    return cas


CAS = [
    _m("21184a vaincue : se retourne en Defensive Protocols (21184b) et reste en jeu",
       "« When Defeated : each player searches ... Flip this card over »",
       ["Puzzle.CreatePlayerDeck('01090')", "Puzzle.PutIntoPlay('21184a,21184b')", "Puzzle.SetThreat('21184a', 1)"], ["Puzzle.Thwart('01001a')"],
       {"en_jeu": ["21184b"], "hors_jeu": ["21184a"], "en_main": ["01090"]}, cibles=["21184a", "01090"], accepter_choix=True),
]
