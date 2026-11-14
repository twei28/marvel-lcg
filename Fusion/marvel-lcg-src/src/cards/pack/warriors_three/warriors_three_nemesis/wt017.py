from . import *


def GetAbilities() -> Sequence['Ability']:
    def fenris(effect: 'Effect', message: 'Message.WhenUnitWouldScheme') -> None:
        Unused(message)
        compte_a_rebours = en_jeu(effect, "Countdown to Ragnarok", Scheme2)
        if compte_a_rebours is not None:
            effect.this.PlaceThreatOnSchemes([compte_a_rebours], 1, effect)

    return [
        *AbilityFactory.UnitCannotTakeDamage("This"),
        *AbilityFactory.UnitCannotBeDefeatedWhile(AbilityType.NonKeyword, "This"),
        AbilityFactory.WhenUnitWouldScheme(AbilityType.ForcedInterrupt, "This", fenris),
    ]
