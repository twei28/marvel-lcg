from . import *

# Mountain of Muscle (CONDITION) — boost 2.
# If Kingpin has the MARTIAL ARTIST trait, attach to Kingpin. Otherwise, this
#   card gains surge.
# Kingpin gains retaliate 1.
# Forced Interrupt: When Kingpin would take any amount of damage, place it
#   here instead. Then, if there is 8 or more damage here, discard this card.
# Modeles : CapacitesDUnVehicule (drive, seuil + if_cannot_gain_surge), 03009
# (GiveKeywordToAttached retaliate).

def GetAbilities() -> Sequence['Ability']:

    def encaisse(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Attachment)
        total = message.will_take_damage
        if total <= 0:
            return
        message.PreventDamage("All", effect)
        Faces.PlaceCountersOn([this], total, 'damage', effect)
        if this.GetCounters('damage') >= 8:
            Faces.DiscardAll([this], effect)

    def le_porteur(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Attachment)
        return message.trigger is this.GetBindFace()

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Kingpin", card_type=Villain, trait=TRAIT_ARTS_MARTIAUX),
            if_cannot_gain_surge=True,
        ),
        *AbilityFactory.GiveKeywordToAttached("Character", retaliate=1),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, Villain, encaisse, conditions=[le_porteur]),
    ]
