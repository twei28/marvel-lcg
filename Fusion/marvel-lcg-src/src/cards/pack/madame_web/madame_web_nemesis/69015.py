from . import *

# Power Absorption — custom « Kajislav », traitrise nemesis
# When Revealed: Discard an ally you control. If no ally was discarded this way,
#   flip to alter-ego form and exhaust your identity.

def GetAbilities() -> Sequence['Ability']:

    def absorption(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()

        defausses = player.AskDiscardFaces(player.GetControlAllies(), (1, 1), effect)
        if defausses:
            return

        identity = player.GetIdentity()
        identity.ChangeToForm(AlterEgo, effect)
        Faces.ExhaustAll([player.GetIdentity()], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            absorption
        ),
    ]
