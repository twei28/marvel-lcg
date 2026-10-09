from . import *

# hs096 A Feast for Vultures
# When Revealed : +1 menace ici par personnage (tous, ennemis compris) ayant moins de la moitie de ses PV max.

def GetAbilities() -> Sequence['Ability']:

    def festin(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        n = sum(1 for c in Worlds.GetOnFieldCharacters(effect) if MoinsDeLaMoitie(c))
        if n > 0:
            effect.this.PlaceThreatOnSchemes([effect.this], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, festin),
    ]
