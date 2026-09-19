from . import *

# Power of Suggestion (side scheme 2) — [star] Hinder 3[per_hero] et alea : bases desc.
# Each minion gains the INFLUENCED trait.

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Minion),
            trait="INFLUENCED",
        ),
    ]
