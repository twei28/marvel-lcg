from . import *
def GetAbilities() -> Sequence['Ability']:
    def the_best_offense(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        hero = message.trigger.CastTo(Hero)
        current = (hero.attack if (message.power == 'ATK') else hero.thwart)
        value = (hero.defense - current)
        if value:
            message.GainValue(value, effect)
    def check_attached(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return (effect.this.GetBindFace() == message.trigger)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, defense=1),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.ForcedInterrupt, Hero, the_best_offense, powers=['ATK', 'THW'], conditions=[check_attached])]
