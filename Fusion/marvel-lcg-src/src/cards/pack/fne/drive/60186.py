from . import *

# Sports Car (VEHICLE) — +1 ATK (cle desc ATK+).
# Attach to the enemy with the highest ATK without a VEHICLE attachment.
#   Otherwise, this card gains surge.
# Forced Interrupt: When attached character would take any amount of damage,
#   place it here instead. If there is 4 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(4, highest_atk=True)]
