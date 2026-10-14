from . import *

# hs083a Aerial Mayhem
# A_FAIRE_CLAUDE: Standalone setup must search/move existing cards, then advance to 1B with native main-scheme lifecycle. Never create duplicate scenario environment/support copies.
# Printed: <b>Contents</b>: Vulture (I) and Vulture (II). <i>(Vulture (II) and Vulture (III) instead for expert mode.)</i> Vulture and Standard encounter sets. One modular encounter set <i>(recommended: Red Vulture)</i>.
# Printed: <b>Setup</b>: Search the encounter deck and discard pile for the S.H.I.E.L.D. Wing Suits environment and put it into play. Advance to stage 1B.

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    # A_FAIRE_CLAUDE: implement printed standalone setup before campaign setup.
    return [*CampaignSetup(4)]
