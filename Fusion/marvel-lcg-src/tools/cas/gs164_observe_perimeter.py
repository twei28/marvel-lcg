# Cas test_capacites de gs164 Observe the Perimeter (Earth Under Siege, lot GS-7). Filtre `[eus] gs164`.

MEC_SOCLE = [
    "Puzzle.RemoveVillain('01094')",
    "Puzzle.SetVillainRule('Leftmost', 'PlayerChooses')",
    "Puzzle.BuildVillainDeck('gs166','gs170')",
]


def _c(nom, pourquoi, mise, declencher, attendu, **cle):
    cas = {"nom": "[eus] gs164 " + nom, "pourquoi": pourquoi, "scenario": cle.pop("scenario", "rhino"),
           "heros": cle.pop("heros", "spider_man"), "mise_en_place": mise, "declencher": declencher,
           "verifier": cle.pop("verifier", "etat_attendu"), "attendu": attendu}
    cas.update(cle)
    return cas


CAS = [
    _c("You cannot attack : une attaque de base est refusee tant que l'obligation est en jeu",
       "« You cannot attack » : PlayersCannotAttackWhile(\"You\", Enemy)",
       MEC_SOCLE + ["Puzzle.RevealNextVillain()", "Puzzle.Reveal('gs164')", "Puzzle.ChangeForm('01001b')"],
       ["Puzzle.Attack('01001a')"],
       {"degats": [["gs166", 0]]}),
    _c("Alter-Ego Action : exile identite -> regarde le dessus du deck de mechants et se defausse",
       "« Exhaust your identity -> look at the top card of the villain deck and discard this card » : "
       "PlayerActionToDiscardThis(AlterEgoAction, ex_operation=regarder), cout Exhaust(YourIdentity)",
       MEC_SOCLE + ["Puzzle.RevealNextVillain()", "Puzzle.Reveal('gs164')"],
       ["Puzzle.Action('gs164')"],
       {"hors_jeu": ["gs164"], "exhausted": ["01001b"]}),
]
