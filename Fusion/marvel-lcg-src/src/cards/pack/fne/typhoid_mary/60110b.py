from . import *

# * Bloody Mary (A) — SCH 1 / ATK 2 / 10[per_hero]. Voir CapacitesDeMary.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeMary("10*")]
