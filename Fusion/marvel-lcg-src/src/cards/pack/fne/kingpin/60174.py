from . import *

# Organized Crime (side scheme) — 3[per_hero], boost 2.
# Each minion gets +2 hit points.
# Modele : 60097 Purple Man (GiveKeywordToInPlayWhenApplyThis, liste), health=2.

def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Minion), health=2),
    ]
