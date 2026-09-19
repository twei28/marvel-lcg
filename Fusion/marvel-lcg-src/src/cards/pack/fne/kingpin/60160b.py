from . import *

# * Kingpin (B2, expert) — SCH 3 / ATK 3 / 28[per_hero]. Steady : base desc.
# [star] Forced Interrupt: ... give Kingpin 1 additional boost card for this
#   activation and this activation gains overkill if it is an attack.
# Voir CapacitesDeKingpin2(overkill=True).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin2(overkill=True)]
