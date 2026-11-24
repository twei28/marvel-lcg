from . import *
# Batsuit — AMELIORATION cout 2 [physical]. ARMOR. ITEM. TECH. « You get +3 hit points. Batman gets +1 DEF. »
# Reference : 01036 Mark V Armor (`GiveKeywordToAttached("You", health=)`), 01028 (`CardFinder(name=...)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached("You", health=3),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Batman"), defense=1),
    ]
