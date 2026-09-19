from . import *

# Utility Van (VEHICLE)
# Attach to the enemy with the fewest remaining hit points without a VEHICLE
#   attachment. Otherwise, this card gains surge.
# Forced Interrupt : ... 6 or more damage here, discard this card.

def GetAbilities() -> Sequence['Ability']:
    return [*CapacitesDUnVehicule(6, fewest_remaining_hp=True)]
