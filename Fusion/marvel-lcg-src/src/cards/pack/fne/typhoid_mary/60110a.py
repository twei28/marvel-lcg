from . import *

# * Typhoid Mary (A) — SCH 2 / ATK 1 / 10[per_hero]. Voir CapacitesDeMary.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeMary("10*")]
