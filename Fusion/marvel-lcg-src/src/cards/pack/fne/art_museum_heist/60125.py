from . import *

# * Stunning Landscape (ART) : stun a l'attache ; Hero Action [energy] ou incliner.

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(
            Cost("Y"),
            lambda effect, unite: Faces.GiveStatus([unite], "Stunned", effect),
        ),
    ]
