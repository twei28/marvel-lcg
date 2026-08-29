from . import *
def GetAbilities() -> Sequence['Ability']:
    def ticked_off(effect: 'Effect', message: 'Message.AfterUnitSchemeAgainst') -> None:
        this = effect.this.CastTo(Upgrade)
        # « After the villain activates against a player » : l'initiateur de
        # l'effet est le vilain, pas un joueur. Le joueur vise est porte par le
        # message. Le porteur de l'amelioration doit etre CE joueur-la.
        player = message.GetAgainstPlayer()
        if player is None or player != this.GetControlByPlayer():
            return
        if player.IsAlterEgo():
            player.GetIdentity().ChangeToForm(Hero, effect)
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
        AbilityFactory.AfterUnitSchemeAgainst(AbilityType.ForcedResponse, None, "You", ticked_off),
    ]
