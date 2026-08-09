from . import *
def GetAbilities() -> Sequence['Ability']:
    def domineering_force(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DealAdditionalDamage(4, effect)
    def check_friendly(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attacker = message.trigger
        return (Hero.IsType(attacker) or Ally.IsType(attacker))
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, None, domineering_force, conditions=[check_friendly]).SetTarget('Trigger').SetCostFunc(CostFunc.Counter('This', 1, 'synergy'))]
