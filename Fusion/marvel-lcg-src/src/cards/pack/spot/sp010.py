from . import *

# * Chameleon

def GetAbilities() -> Sequence['Ability']:
    # « Chameleon gets +1 SCH for every 2 threat on him. »
    return [GagneParMenacePosee(2, scheme=1)]
