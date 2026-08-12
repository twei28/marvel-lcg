from . import *

# * Zabu — custom « Nugget » (carte d'aspect AGRESSION)
# Companion. [star] Zabu's attacks gain piercing.


def GetAbilities() -> Sequence['Ability']:

    def percant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)

    return [
        *Companion(),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            percant,
        ),
    ]
