from . import *
def GetAbilities() -> Sequence['Ability']:
    def crossfire(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        if target:
            this.DealDamage([target], 1, effect)
    def check_friendly(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        attacker = message.trigger
        return (Hero.IsType(attacker) or Ally.IsType(attacker))
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(non_trait='ELITE', card_type=Minion)),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.Interrupt, None, crossfire, conditions=[check_friendly])]
