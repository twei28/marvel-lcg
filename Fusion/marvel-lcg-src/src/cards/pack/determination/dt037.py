from . import *

# * Star-Lord

def GetAbilities() -> Sequence['Ability']:

    def star_lord(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response,
            "This",
            star_lord
        ).SetTarget(Enemy),
    ]
