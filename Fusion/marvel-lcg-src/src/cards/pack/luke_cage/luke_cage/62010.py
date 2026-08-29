from . import *
def GetAbilities() -> Sequence['Ability']:
    def metal_bracer(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)
    return [
        *AbilityFactory.GiveKeywordToAttached(Hero, retaliate=1),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.HeroInterrupt, "You", metal_bracer)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
