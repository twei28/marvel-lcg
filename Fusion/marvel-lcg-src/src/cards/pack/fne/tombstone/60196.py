from . import *

# Hard as Marble — +2 ATK (cle desc ATK+).
# Attach to the minion with the highest base hit points and give that minion a
#   tough status card. Otherwise, this card gains surge.
# [star] Forced Response: After attached minion attacks, stun the attacked
#   character and discard Hard as Marble.
# « the attacked character » = message.attacked_targets (60089 Gatling Gun).

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Attachment)
        cibles = [u for u in message.attacked_targets if u.IsInPlay() and not u.IsDefeated()]
        if cibles:
            Faces.GiveStatus(cibles, "Stunned", effect)
        Faces.DiscardAll([this], effect)

    return [
        AttacheAuSbireLePlusSolide(),
        AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, "AttachedEnemy", apres_attaque),
    ]
