from . import *


def GetAbilities() -> Sequence['Ability']:

    def spectral_shift(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        player = effect.GetInitiator()
        identity = player.GetIdentity()
        if IsInvisibleForm(identity):
            ChangeToPsionicForm(player, effect)
            player.DrawUp(1, effect)
        else:
            ChangeToInvisibleForm(player, effect)
            player.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            spectral_shift,
        ).SetPlay()
        .SetName("Spectral Shift"),
    ]
