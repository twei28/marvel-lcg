from . import *

# * Polaris (Lorna Dane) : allie RECRUITED, cout 2, PV 2, THW 2*, ATK 2*.
# Action: Spend a [energy] resource -> heal 2 damage from Polaris.
#
# Cartes de reference : 04100 Elektra (`SetCost(Cost("R"))`), 01061 / `Faces.Heal` (soin), `WhenInYourPlayTurn(AbilityType.Action, ...)` (22012).
def GetAbilities() -> Sequence['Ability']:
    def polaris(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.HealthUnits([this], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            polaris,
        ).SetCost(Cost("Y")),
    ]
