from . import *

# * Impossible Object (ART) : confuse a l'attache ; Hero Action [mental] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("B"),
            lambda effect, unite: Faces.GiveStatus([unite], "Confused", effect),
        ),
    ]
