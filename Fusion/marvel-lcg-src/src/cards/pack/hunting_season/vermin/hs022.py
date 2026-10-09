from . import *

# hs022 A Mischief of Rats
# When Revealed: Discard X cards from the encounter deck, X = double the villain's stage
# number. For each RAT minion discarded this way, choose to either place 2 threat on the
# main scheme or put that minion into play engaged with you.

def GetAbilities() -> Sequence['Ability']:

    def mischief(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        vilain = Worlds.FindCardOnField(effect, card_type=Villain)
        if joueur is None or vilain is None:
            return
        defaussees = Worlds.DiscardEncounterCards(vilain.printed_stage * 2, effect)
        for rat in [f for f in defaussees if EstRat(f)]:
            def menace(cibles, rat=rat):
                complot = Worlds.FindMainScheme(effect)
                if complot is not None:
                    Faces.PlaceTokensOn([complot], 2, 'threat', effect)

            def engager(cibles, rat=rat):
                rat.PutIntoPlay(joueur, effect)

            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Place 2 threat on the main scheme", menace),
                AbilityFactory.ForChoiceAbility("Put that minion into play engaged with you", engager),
            )

    return [
        AbilityFactory.WhenThisRevealed(None, mischief),
    ]
