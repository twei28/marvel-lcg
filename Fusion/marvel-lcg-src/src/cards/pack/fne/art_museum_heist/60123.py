from . import *

# * Inspiring Pottery (ART) : le porteur gagne stalwart ; Hero Action [wild] ou incliner.
# Modele du stalwart attache : 16064 Drang's Spear, sur "Character" (le porteur,
# vilain ou heros).

def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDUneOeuvre(Cost("G"), None),
        *AbilityFactory.GiveKeywordToAttached(
            "Character",
            stalwart=1,
        ),
    ]
