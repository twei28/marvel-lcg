from . import *

# Aerial Advantage

def GetAbilities() -> Sequence['Ability']:

    def bouclier(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        # « Forced Interrupt: When any amount of damage would be dealt to
        # Vulture, discard Aerial Advantage instead. Place 1 pigeon counter on
        # the main scheme. »
        this = effect.this.CastTo(Attachment)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)
        PigeonsSurLeComplot(effect, 1)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Villain
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "AttachedVillain",
            bouclier
        ),
    ]
