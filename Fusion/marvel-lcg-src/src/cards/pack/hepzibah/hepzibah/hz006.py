from . import *
# Heavy Machine Gun. Amelioration WEAPON, cout 2, Restricted, Uses (2 ammo counters).
#
# Hero Action: Exhaust Heavy Machine Gun and remove 1 ammo counter from it -> deal 1 damage to each enemy.
#
# Cartes de reference : 01022 Ground Stomp (`SetTarget(Enemy, range="All")`), us007 pour `Uses` + `CostFunc.Counter`.
def GetAbilities() -> Sequence['Ability']:
    def mitrailleuse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        this.DealDamage(effect.targets, 1, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mitrailleuse,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'ammo'))
        .SetTarget(Enemy, range="All"),
    ]
