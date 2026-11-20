from . import *


def GetAbilities() -> Sequence['Ability']:
    def rally(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        Faces.ReadyAll(soutiens_persona(effect.GetInitiator()), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, rally).SetPlay().SetLabel(),
    ]
