from . import *

# Reptile Research

def GetAbilities() -> Sequence['Ability']:

    def menace(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        n = NombreReptiles(effect)
        if n > 0:
            effect.this.PlaceThreatOnSchemes([effect.this], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, menace),
    ]
