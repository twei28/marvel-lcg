from . import *

# Dam It — custom « DesignHacker » (side scheme némésis de Human Torch)
# When Revealed: Remove all flame counters from enemies in play. Then, place
# 1 additional threat here for each flame counter removed this way.

def GetAbilities() -> Sequence['Ability']:

    def dam_it(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        ennemis = Worlds.GetOnFieldEnemies(effect)
        retires = Faces.RemoveCountersOn(ennemis, "All", 'flame', effect) or 0

        if retires > 0:
            this.PlaceThreatOnSchemes([this], retires, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            dam_it
        ),
    ]
