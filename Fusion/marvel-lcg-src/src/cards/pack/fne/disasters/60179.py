from . import *

# Towering Inferno (DISASTER) — Uses (2 civilian counters).
# Hero Action: Spend [physical][physical] resources or exhaust a hero or ally
#   you control -> remove 1 civilian counter (2 instead if you exhausted a
#   character that has a tough status card).
# ⚠ « has a tough status card » lu AU MOMENT du cout : incliner ne retire pas
# la robustesse, la lecture apres inclinaison est donc fidele.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDeCatastrophe("RR", "[physical][physical]", lambda f: f.IsTough())]
