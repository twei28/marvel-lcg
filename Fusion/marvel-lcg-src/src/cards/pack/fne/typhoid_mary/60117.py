from . import *

# Assembled Armor (ARMOR) — Attach to the villain. +2 ATK (ATK+).
# Forced Interrupt: When the villain would take any amount of damage, place
#   it here instead. Then, if there is 5 or more damage here (8 or more in
#   expert mode), discard this attachment.
# [star] Boost: If Bloody Mary is activating, you are confused.
# Modele : 60068a (PreventDamage + compteur 'damage').

def GetAbilities() -> Sequence['Ability']:

    def armure(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        seuil = 8 if Worlds.IsExpert(effect) else 5
        if this.GetCounters('damage') >= seuil:
            Faces.DiscardAll([this], effect)

    def le_vilain_attache(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Bloody Mary"):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(Villain),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, armure, conditions=[le_vilain_attache]),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
