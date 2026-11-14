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
        # Rapport 132 (14/11/2026) : la question etait posee meme heros PRET, alors que « ready your hero » ne
        # sert a rien. On ne propose la carte que si l'identite est epuisee.
        if not player.GetIdentity().IsExhaust():
            return False
        return (player.allies.FindCard(card_type=Ally) == None)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitAttackYou(AbilityType.HeroInterrupt, Enemy, stand_alone, conditions=[check_no_allies]).SetCostFunc(CostFunc.Exhaust('This'))]
