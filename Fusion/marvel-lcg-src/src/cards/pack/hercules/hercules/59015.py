from . import *
def GetAbilities() -> Sequence['Ability']:
    def hercs_helm(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.DealAdditionalDamage(-1, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Villain, hercs_helm).SetLabel('defense').SetCostFunc(CostFunc.Exhaust('This'))]
