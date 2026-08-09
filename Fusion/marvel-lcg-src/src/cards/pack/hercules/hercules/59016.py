from . import *
def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, thwart=1, attack=1, defense=1)]
