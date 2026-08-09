from . import *
def GetAbilities() -> Sequence['Ability']:
    def golden_mace(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity()
        value = CountGifts(effect, player)
        if (value > 0):
            identity.CastTo(Unit2).TemporaryGain(effect, message.would_message, attack=value)
        message.would_message.GainOverKill(effect)
    def check_attack(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return (message.power == 'ATK')
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.HeroInterrupt, 'YourHero', golden_mace, conditions=[check_attack]).SetCostFunc(CostFunc.Exhaust('This'))]
