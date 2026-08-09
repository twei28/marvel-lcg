from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword('This', piercing=True, ranged=True)]
