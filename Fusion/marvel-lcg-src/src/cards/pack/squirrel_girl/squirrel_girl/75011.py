from . import *

# * Central Park
# Action: Exhaust Central Park → if you control fewer than 3 SQUIRREL allies,
#   call 1 Squirrel.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        if len(EcureuilsControles(effect, joueur)) >= 3:
            return
        AppelerEcureuil(joueur, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        (AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, appeler)
            .SetCostFunc(CostFunc.Exhaust("This"))),
    ]
