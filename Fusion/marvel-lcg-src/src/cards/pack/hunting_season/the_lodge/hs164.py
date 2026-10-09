from . import *

# hs164 * Rocket Raccoon (Experience Cost 4)
# [star] Son attaque de base gagne ranged, piercing et overkill.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", is_basic_attack=True, ranged=True, piercing=True, overkill=True),
    ]
