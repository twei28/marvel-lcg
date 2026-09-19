from . import *

# * Electro (60077) : voir CapacitesDElectro (charges par manigance = 1).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDElectro(1, None),
    ]
