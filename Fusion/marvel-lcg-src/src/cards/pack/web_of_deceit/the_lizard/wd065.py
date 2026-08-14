from . import *

# Regenerative Research

def GetAbilities() -> Sequence['Ability']:

    def regeneration(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        # « Forced Interrupt: When the villain phase begins, heal 1 damage from
        # each enemy. »
        this = effect.this.CastTo(EncounterSideScheme)
        ennemis = Worlds.GetOnFieldEnemies(effect)
        if ennemis:
            this.HealthUnits(ennemis, 1, effect)

    return [
        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedInterrupt,
            regeneration
        ),
    ]
