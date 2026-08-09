from . import *

# * Hulk

def GetAbilities() -> Sequence['Ability']:

    def anger(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Hero)

        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            anger
        ).SetName("Anger")
        .SetTarget(Enemy),
    ]
