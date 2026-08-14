from . import *

# Venom Blast

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action (attack): Deal 5 damage to an enemy. »
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            decharge
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
