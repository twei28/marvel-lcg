from . import *


def GetAbilities() -> Sequence['Ability']:

    def family_home(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()
        Faces.ReadyAll([player.GetIdentity()], effect)

    return [
        *AbilityFactory.GiveKeywordToAttached("You", recover=1),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            family_home,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetName("Family Home"),
    ]
