from . import *

# * Siri's Dress — amelioration. ARMOR. ASGARD. Cout 2.
# You get +4 hit points.
# Angela gains the AERIAL trait.
#
# Cartes de reference : 05023 Endurance pour « You get +N hit points »
# (`GiveKeywordToAttached("You", health=N)`), et ra007 Mjolnir (pack rainy)
# pour l'octroi d'un TRAIT par la meme fabrique.
#
# Les deux effets visent la meme cible (« You » = l'identite porteuse), un
# seul appel suffit donc.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=4,
            trait="AERIAL",
        ),
    ]
