from . import *
def GetAbilities() -> Sequence['Ability']:
    def blaster(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 2 if AbimeDe(effect) else 1, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            blaster,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
