from . import *
# Kill Order (manigance annexe, boost 3, menace 3 par heros, icone Acceleration).
#
# Each minion gains quickstrike. (After this minion engages your hero, it attacks.)
#
# Cartes de reference : 39047 The Mojo Files (`GiveKeywordToInPlayWhenApplyThis(Minion, quickstrike=1)`), 32079 The Brotherhood.
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Minion,
            quickstrike=1,
        ),
    ]
