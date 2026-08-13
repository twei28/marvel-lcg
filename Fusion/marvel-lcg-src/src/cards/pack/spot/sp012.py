from . import *

# * Living Laser

def GetAbilities() -> Sequence['Ability']:
    # « Living Laser gains retaliate 1 for every 2 threat on him
    # (to a maximum of retaliate 4). »
    return [GagneParMenacePosee(2, maximum=4, retaliate=1)]
