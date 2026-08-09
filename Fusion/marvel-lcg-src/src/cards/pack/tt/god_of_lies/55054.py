from . import *
def GetAbilities() -> Sequence['Ability']:
    def mounting_resistance(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        message.RemoveAdditionalThreat(4, effect)
    def check_friendly(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> bool:
        thwarter = message.trigger
        return (Hero.IsType(thwarter) or Ally.IsType(thwarter))
    return [AbilityFactory.WhenUnitWouldThwart(AbilityType.Interrupt, who_make_thwart=None, operation=mounting_resistance, conditions=[check_friendly]).SetTarget('Trigger').SetCostFunc(CostFunc.Counter('This', 1, 'synergy'))]
