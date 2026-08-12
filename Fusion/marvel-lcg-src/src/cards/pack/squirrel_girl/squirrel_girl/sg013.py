from . import *

# Call the Squirrels
# Action: Call 2 Squirrels. Squirrels called this way enter play ready.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            AppelerEcureuils(joueur, effect, 2, pret=True)

    return [
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, appeler)
            .SetPlay()),
    ]
