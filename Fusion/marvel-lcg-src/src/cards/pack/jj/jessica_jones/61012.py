from . import *
def GetAbilities() -> Sequence['Ability']:
    def ticked_off(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        # « After the villain activates against a player » : attaque OU
        # manigance, contre n'importe quel joueur. « If you are in alter-ego
        # form » vise le porteur ; les sbires vises sont ceux de « that player ».
        player = message.to_player
        if player is None:
            return
        moi = this.GetControlByPlayer()
        if moi is not None and moi.IsAlterEgo():
            moi.GetIdentity().ChangeToForm(Hero, effect)
        villain = Worlds.FindVillain(effect)
        targets: List['CardFace'] = []
        if villain:
            targets.append(villain)
        for minion in Worlds.FindCardsOnField(effect, card_type=Minion):
            if minion.CastTo(Minion).GetEngagedPlayer() == player:
                targets.append(minion)
        this.AttackDamage(targets, 5, effect)
        Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, Villain, ticked_off),
    ]
