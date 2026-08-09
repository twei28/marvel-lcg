from . import *
def GetAbilities() -> Sequence['Ability']:
    def kingpin_schemes_instead(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        message.DoSchemeInstead(effect)
    def check_maya_player(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        player = message.GetAgainstPlayer()
        if not Player.IsType(player):
            return False
        identity = player.GetIdentity()
        if (identity.paper.name == 'Maya Lopez'):
            return True
        for face in identity.card.back_faces:
            if (face.paper.name == 'Maya Lopez'):
                return True
        return False
    return [AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, 'This', kingpin_schemes_instead, conditions=[check_maya_player])]
