from . import *

# hs041 Coiled Up
# A_FAIRE_CLAUDE: Resolve the printed attachment condition and removal trigger. Verify DEF+ is accepted in desc and not automatically applied twice; prefer the engine-native attachment stats when supported.
# Printed: Move 5 damage from Scorpion’s Tail to Scorpion. If Scorpion’s Tail is attached to Scorpion, attach Coiled Up to your identity. If you cannot, this card gains surge.
# Printed: <b>Forced Interrupt</b>: When Scorpion’s Tail is set aside, discard Coiled Up.

def GetAbilities() -> Sequence['Ability']:
    return [*AbilityFactory.GiveKeywordToAttached(
        "You", attack=-1, thwart=-1, defense=-1)]
