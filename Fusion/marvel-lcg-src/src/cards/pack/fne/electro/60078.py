from . import *

# * Electro (60078) : voir CapacitesDElectro (charges par manigance = 2, 3[per_hero] charges a la revelation, alea : base).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDElectro(2, '3*'),
    ]
