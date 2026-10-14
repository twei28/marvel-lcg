from . import *

# hs134 Quicksand
# A_FAIRE_CLAUDE: Resolve the printed attachment condition and removal trigger. Verify DEF+ is accepted in desc and not automatically applied twice; prefer the engine-native attachment stats when supported.
# Printed: <b>When Revealed</b>: Choose to either exhaust your identity or attach this card to your identity. If you exhausted your identity, discard this card.
# Printed: <b>Interrupt</b>: When you play an event card, cancel its effects and discard that event → discard Quicksand.

def GetAbilities() -> Sequence['Ability']:
    return [*AbilityFactory.GiveKeywordToAttached(
        "You", attack=-1, thwart=-1, defense=-1)]
