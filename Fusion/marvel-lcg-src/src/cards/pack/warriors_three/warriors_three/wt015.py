from . import *


def GetAbilities() -> Sequence['Ability']:
    def leap(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        changer_de_heros(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, leap).SetPlay().SetLabel(),
    ]
