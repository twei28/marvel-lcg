from . import *

# Get Your Swell On

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        ennemis = Worlds.GetOnFieldEnemies(effect)
        this.HealthUnits(ennemis, 1, effect)
        Faces.GiveStatus(ennemis, "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
