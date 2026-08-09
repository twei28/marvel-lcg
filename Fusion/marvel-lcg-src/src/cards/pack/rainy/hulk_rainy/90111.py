from . import *

# Intimidating Roar

def GetAbilities() -> Sequence['Ability']:

    def intimidating_roar(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Upgrade)

        # 2 menaces si l'attaque a inflige 3 degats ou plus, 1 sinon.
        # (le champ du message est took_damage, pas damage)
        value = 2 if message.took_damage >= 3 else 1
        this.RemoveThreatFromSchemes(effect.targets, value, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            intimidating_roar,
            is_from_attack=True,
        ).SetLabel('thwart')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
    ]
