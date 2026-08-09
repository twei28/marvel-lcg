from . import *
def GetAbilities() -> Sequence['Ability']:
    def prince_of_power(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity()
        identity.HealHealth(message.excess_damage, effect)
    def check_excess(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> bool:
        return (message.excess_damage > 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.HeroResponse, 'YourHero', Enemy, prince_of_power, conditions=[check_excess]).SetCostFunc(CostFunc.Exhaust('This'))]
