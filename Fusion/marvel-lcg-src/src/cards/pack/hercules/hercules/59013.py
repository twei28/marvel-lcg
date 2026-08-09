from . import *
def GetAbilities() -> Sequence['Ability']:
    def gauntlets(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        value = CountGifts(effect, player)
        if (value <= 0):
            return
        for ability in AbilityFactory.GiveKeywordToAttached(CardFinder(name='Hercules', card_type=Hero), retaliate=value):
            this.effect.RegisterTemp(ability, unregister_after_exec=False, until_event_end=message)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Enemy, gauntlets).SetCostFunc(CostFunc.Exhaust('This'))]
