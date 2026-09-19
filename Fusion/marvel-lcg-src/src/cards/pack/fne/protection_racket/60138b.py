from . import *

# A Slice of the Pizza Dough 1B — 10, +1 : bases desc.
# Forced Response: After a character in this play area defeats another
#   character or a side scheme (in any play area), heal 1 damage from the
#   defeating character and place 1 threat here.

def GetAbilities() -> Sequence['Ability']:

    def recompense(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(MainScheme)
        tueur = getattr(message, "killer", None) or getattr(message, "trigger", None)
        if tueur is not None and tueur.IsInPlay():
            tueur.HealHealth(1, effect)
        this.PlaceThreatOnSchemes([this], 1, effect)

    def tueur_de_cette_aire(effect: 'Effect', message: 'Message') -> bool:
        tueur = getattr(message, "killer", None) or getattr(message, "trigger", None)
        return tueur is not None and Unit2.IsType(tueur) and DansCetteAire(tueur, effect.this)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(AbilityType.ForcedResponse, None, None, recompense, conditions=[tueur_de_cette_aire]),
        AbilityFactory.AfterUnitDefeatedScheme(AbilityType.ForcedResponse, None, EncounterSideScheme, recompense, conditions=[tueur_de_cette_aire]),
        *CapacitesCommunes1B(),
    ]
