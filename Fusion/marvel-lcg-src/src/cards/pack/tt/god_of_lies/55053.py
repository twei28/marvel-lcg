from . import *
def GetAbilities() -> Sequence['Ability']:
    def feigned_retreat(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DealAdditionalDamage(-4, effect)
    def check_identity_target(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return Enemy.IsType(message.trigger)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, Enemy, feigned_retreat, conditions=[check_identity_target]).SetTarget('Trigger').SetCostFunc(CostFunc.Counter('This', 1, 'synergy'))]
