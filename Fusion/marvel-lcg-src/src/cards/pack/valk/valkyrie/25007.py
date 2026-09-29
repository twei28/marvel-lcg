from . import *

# * Aragorn

def GetAbilities() -> Sequence['Ability']:

    return [
        # This card should say “you” instead of “Valkyrie” to work as intended (like how Thor’s Helmet is worded). Go ahead and treat this card as if it said “you” instead. Switching to Alter-Ego would not change the bonuses the card is granting you.
        *AbilityFactory.GiveKeywordToAttached(
            # name="Valkyrie",
            "You",
            health=4,
        ),
        # Errata RRG 1.5 : « Valkyrie » -> « You » pour le trait aussi (MC4DB,
        # 29/09/2026) : Brunnhilde (alter-ego) gagne AERIAL comme Valkyrie.
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            trait="AERIAL",
        )
    ]

