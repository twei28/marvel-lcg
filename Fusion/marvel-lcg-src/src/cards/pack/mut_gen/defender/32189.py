from . import *
def GetAbilities() -> Sequence['Ability']:
    def determined_defense(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        attacker = message.trigger.CastTo(HasAttack)
        value = attacker.attack
        message.SetBeInstead(effect)
        if (value > 0):
            this.RemoveThreatFromSchemes('MainScheme', value, effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Enemy, determined_defense).SetLabel('defense', 'thwart').SetTarget('Trigger').SetCost(Cost('2'))]
