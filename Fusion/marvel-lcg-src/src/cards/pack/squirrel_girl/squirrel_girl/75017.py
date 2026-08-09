from . import *

# Nuts!
# Response: After you spend this card to pay for a Squirrel Girl card,
#   call 1 Squirrel.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.WhenCardBeSpendAsResource') -> None:
        joueur = effect.GetInitiator()
        if joueur is not None:
            AppelerEcureuil(joueur, effect)

    return [
        AbilityFactory.WhenYouSpendThisCardToPlay(
            AbilityType.Response,
            appeler,
            FinderCarteSquirrelGirl(),
        ),
    ]
