from . import *

# * Scorpia — SBIRE UNIQUE. CRIMINAL. SYNDICATE. SCH 1, ATQ 3★, 6 PV, Boost 2, Guard, Patrol.
# Guard. Patrol.
# ★ Scorpia's attacks gain piercing.
# When Defeated : voir __init__.py.
#
# Cartes de reference : ts201 / gs083 (`UnitAttackGainKeyword("This", piercing=True)`). Guard et Patrol : natifs.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        DefaiteSyndicate(),
    ]
