from . import *

# One Spyder Down — custom « Kajislav », traitrise nemesis
# When Revealed: Discard an ally you control. If you cannot, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def spyder_down(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()

        if not player.AskDiscardFaces(player.GetControlAllies(), (1, 1), effect):
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            spyder_down
        ),
    ]
