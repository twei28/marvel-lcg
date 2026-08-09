from . import *

# Hunting Spyders — custom « Kajislav », traitrise nemesis
# When Revealed: Deal 3 damage to an ally you control. If you cannot, deal 3
#   damage to your identity.

def GetAbilities() -> Sequence['Ability']:

    def chasse_aux_spyders(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()

        allie = player.AskChooseFace(player.GetControlAllies(), effect)
        if allie:
            this.DealDamage([allie], 3, effect)
        else:
            this.DealDamage([player.GetIdentity()], 3, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            chasse_aux_spyders
        ),
    ]
