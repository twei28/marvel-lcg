from . import *

# * Replica Shield (ART) : tough a l'attache ; Hero Action [physical] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("R"),
            lambda effect, unite: Faces.GiveStatus([unite], "Tough", effect),
        ),
    ]
