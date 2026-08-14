from . import *

# * Kingpin's Suit

def GetAbilities() -> Sequence['Ability']:

    def encaisser(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        # « Forced Interrupt: When any amount of damage would be dealt to
        # Kingpin, place it here instead. Then, if there is at least 10 damage
        # here, discard Kingpin's Suit. »
        #
        # Le costume n'est pas une unite : il n'a pas de PV. Les degats detournes
        # sont donc des COMPTEURS poses dessus, ce que Fisk Tower sait ensuite
        # retirer un a un.
        this = effect.this.CastTo(Attachment)
        degats = message.will_take_damage
        message.SetBeInstead(effect)
        Faces.PlaceCountersOn([this], degats, 'damage', effect)
        if this.GetCounters('damage') >= 10:
            Faces.DiscardAll([this], effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « [star] Boost: Attach Kingpin's Suit to Kingpin. »
        this = effect.this.CastTo(Attachment)
        villain = Worlds.FindVillain(effect)
        if villain:
            this.PutIntoPlay(message.GetToPlayer(), effect)
            this.AttachTo2(villain, effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            encaisser
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
