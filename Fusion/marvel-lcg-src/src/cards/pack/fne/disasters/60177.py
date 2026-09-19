from . import *

# Mystic Incursion (DISASTER, environment, crisis) — Uses (2 civilian counters).
# Hero Action: Spend [mental][mental] resources or exhaust a hero or ally you
#   control -> remove 1 civilian counter from here (2 counters instead if you
#   exhausted a MYSTIC character).

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("BB", "[mental][mental]", lambda f: f.HasTrait("MYSTIC"))]
