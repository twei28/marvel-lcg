from . import *

# The Gang's All Here (3A)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « In player order, each player not engaged with a unique minion
        # searches the encounter deck and discard pile for a unique minion and
        # reveals it. »
        def action(joueur: 'Player') -> None:
            if CardFinder(is_unique=True).Checks(joueur.GetEngagedMinions()):
                return
            Find.FindAndReveal(
                effect,
                joueur,
                finder=CardFinder(card_type=Minion, is_unique=True)
            )

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
