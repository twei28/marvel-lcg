from . import *

# Out Front — Permanent (base). Attach to the villain.
# If there is no threat on the main scheme, flip this card.
# [star] Attached villain's attacks gain ranged.
# Forced Interrupt: When the villain would be dealt any amount of damage,
#   remove that amount of threat from the main scheme instead (ignoring
#   crisis icons).
# « no threat on the main scheme » : verifie apres chaque retrait de menace du
# complot principal (AfterSchemeRemoveThreat(MainScheme, last_threat=True) ;
# ⚠ which_scheme est un TYPE, la chaine "MainScheme" leve un AssertionError
# avale dans CheckWhichCard, harnais du 18/09/2026). Le retrait ignore
# la crise : RemoveThreatFromSchemes(ignore_crisis=True). Alongside ->
# Out Front = fin de round (60128b) ; Out Front -> Alongside = ici.

def GetAbilities() -> Sequence['Ability']:

    def plus_de_menace(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        this = effect.this.CastTo(Attachment)
        scheme = message.trigger
        if scheme.threat <= 0 and this.IsInPlay():
            RetournerLAttachement(this, effect)

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        this.RemoveThreatFromSchemes("MainScheme", total, effect, ignore_crisis=True)

    def le_vilain_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.UnitAttackGainKeyword("AttachedEnemy", ranged=True),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, encaisse, conditions=[le_vilain_attache]),
        AbilityFactory.AfterSchemeRemoveThreat(AbilityType.ForcedInterrupt, MainScheme, plus_de_menace, last_threat=True),
    ]
