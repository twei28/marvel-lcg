from . import *

# Merc Squad

def GetAbilities() -> Sequence['Ability']:

    def merc_squad(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.DealDamage(effect.targets, 1, effect)
        this.RemoveThreatFromSchemes("MainScheme", 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            merc_squad
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'tactic'))
        .SetTarget(Enemy),
    ]
