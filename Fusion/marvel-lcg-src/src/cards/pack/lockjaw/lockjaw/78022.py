from . import *

# * Lockheed — custom « Nugget » (carte d'aspect PROTECTION)
# Companion. [star] Lockheed's attacks gain ranged.


def GetAbilities() -> Sequence['Ability']:

    def a_distance(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainRanged(effect)

    return [
        *Companion(),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            a_distance,
        ),
    ]
