from . import *

# * Puma

def GetAbilities() -> Sequence['Ability']:
    # « Puma gets +1 ATK for every 2 threat on him. »
    return [GagneParMenacePosee(2, attack=1)]
