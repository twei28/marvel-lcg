from . import *

# * Kingpin (A1) — SCH 2 / ATK [star] / 25[per_hero], CRIMINAL. Stalwart : base desc.
# Kingpin cannot be dealt damage or have upgrades attached.
# [star] Forced Interrupt: When Kingpin would attack you, he schemes instead.
# Voir CapacitesDeKingpin1.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeKingpin1()]
