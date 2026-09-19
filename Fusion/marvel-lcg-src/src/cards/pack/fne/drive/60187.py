from . import *

# Motorcycle (VEHICLE) — +1 SCH/THW (cles desc SCH+ et THW+).
# Attach to the enemy with the highest SCH without a VEHICLE attachment.
#   Otherwise, this card gains surge.
# Forced Interrupt : ... 3 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(3, highest_sch=True)]
