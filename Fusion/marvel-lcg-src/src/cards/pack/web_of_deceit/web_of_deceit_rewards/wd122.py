from . import *

# Radioactive Spider

def GetAbilities() -> Sequence['Ability']:

    def morsure(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Action: Discard Radioactive Spider → deal 1 damage to your identity.
        # You get +2 hand size until the end of the phase. »
        this = effect.this.CastTo(Support)
        joueur = effect.GetInitiator()
        this.DealDamage([joueur.GetIdentity()], 1, effect)
        joueur.GetIdentity().GainUntilPhaseEnd(effect, hand_size=2)

    return [
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.Action,
            ex_operation=morsure,
        ),
    ]
