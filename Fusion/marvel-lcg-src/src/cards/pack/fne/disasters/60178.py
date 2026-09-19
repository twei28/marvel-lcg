from . import *

# Sinking Ferry (DISASTER) — Uses (2 civilian counters).
# Hero Action: Spend [energy][energy] resources or exhaust a hero or ally you
#   control -> remove 1 civilian counter (2 instead if you exhausted an AERIAL
#   character).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("YY", "[energy][energy]", lambda f: f.HasTrait("AERIAL"))]
