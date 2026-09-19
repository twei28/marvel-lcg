from . import *

# Jackknifed Tanker Truck (side scheme 2, crisis) — [star] Hinder 1[per_hero] : base.
# The villain cannot be dealt damage.  (UnitCannotTakeDamage(Villain), fabrique
# corrigee le 30/08/2026, rend une liste.)

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.UnitCannotTakeDamage(Villain),
    ]
