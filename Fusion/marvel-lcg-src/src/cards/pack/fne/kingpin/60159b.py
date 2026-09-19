from . import *

# * Kingpin (A2) — SCH 2 / ATK 2 / 25[per_hero], CRIMINAL MARTIAL ARTIST. Steady : base desc.
# [star] Forced Interrupt: When Kingpin activates against you, if you are not
#   engaged with a minion, give Kingpin 1 additional boost card for this activation.
# Voir CapacitesDeKingpin2.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin2(overkill=False)]
