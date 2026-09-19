from . import *

# Cold as Ice — +2 SCH (cle desc SCH+).
# Attach to the minion with the highest base hit points and give that minion a
#   tough status card. Otherwise, this card gains surge.
# [star] Forced Response: After attached minion schemes, confuse the first
#   player's identity and discard Cold as Ice.

def GetAbilities() -> Sequence['Ability']:

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Attachment)
        premier = Worlds.GetFirstPlayer(effect)
        Faces.GiveStatus([premier.GetIdentity()], "Confused", effect)
        Faces.DiscardAll([this], effect)

    return [
        AttacheAuSbireLePlusSolide(),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "AttachedEnemy", apres_manigance),
    ]
