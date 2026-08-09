from . import *
def GetAbilities() -> Sequence['Ability']:
    def stand_alone(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        Faces.ReadyAll([player.GetIdentity()], effect)
    def check_no_allies(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        player = effect.this.GetControlByPlayer()
        if (message.GetAgainstPlayer() != player):
            return False
        return (player.allies.FindCard(card_type=Ally) == None)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Enemy, stand_alone, conditions=[check_no_allies]).SetCostFunc(CostFunc.Exhaust('This'))]
