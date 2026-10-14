from . import *

# hs205 * Lizard

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", piercing=True)]
