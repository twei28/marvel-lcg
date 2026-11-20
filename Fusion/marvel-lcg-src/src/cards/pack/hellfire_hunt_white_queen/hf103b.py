from . import *

# White Queen, forme B (DIAMOND), stade 3 (mode expert) : identique a la forme B du stade 2.


def GetAbilities() -> Sequence['Ability']:
    return [ReponseForceeFormeB(), InterruptionForceeFormeB()]
