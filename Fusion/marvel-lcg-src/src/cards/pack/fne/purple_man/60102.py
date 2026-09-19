from . import *

# Judge (CIVILIAN, INFLUENCED) — Vulnerable : base.
# When Defeated: Place 3 threat on the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceThreatOnSchemes("MainScheme", 3, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
