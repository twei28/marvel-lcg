from . import *

# Soldier On

def GetAbilities() -> Sequence['Ability']:

    def soldier_on(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        # La condition se lit APRES le cout : les 2 degats font justement passer
        # sous la moitie, et c'est le sens de la carte.
        if identity.health < identity.max_health/2:
            identity.GainUntilPhaseEnd(effect, hand_size=2)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            soldier_on
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(2, "Initiator")),
    ]
