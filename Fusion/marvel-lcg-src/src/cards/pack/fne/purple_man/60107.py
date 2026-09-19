from . import *

# "Serve." (obligation, Uses 3 command) — Forced Action: ... -> place 2
# threat on the main scheme.

def GetAbilities() -> Sequence['Ability']:

    def servir(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        this.PlaceThreatOnSchemes("MainScheme", 2, effect)

    return [
        *ObligationCommandee("Serve.", servir),
    ]
