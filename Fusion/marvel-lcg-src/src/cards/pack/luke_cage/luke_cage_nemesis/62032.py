from . import *
def GetAbilities() -> Sequence['Ability']:
    def stun_you(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        # L'initiateur de l'effet est Asp elle-meme (un ennemi), pas un joueur :
        # `GetInitiator` leve une assertion. Le « you » de la carte est le joueur
        # contre qui Asp vient de comploter, que le message porte deja.
        player = message.GetAgainstPlayer()
        if player:
            Faces.GiveStatus([player.GetIdentity()], "Stunned", effect)
    def boost_ability(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        # « You are stunned » : le joueur vise est celui contre qui l'ennemi
        # s'active, que le message porte deja.
        player = message.GetToPlayer()
        if player:
            Faces.GiveStatus([player.GetIdentity()], "Stunned", effect)
    return [
        AbilityFactory.AfterUnitSchemeAgainst(AbilityType.ForcedResponse, "This", "You", stun_you),
        AbilityFactory.WhenBoostCardTurnedFaceUp(AbilityType.Boost, None, boost_ability),
    ]
