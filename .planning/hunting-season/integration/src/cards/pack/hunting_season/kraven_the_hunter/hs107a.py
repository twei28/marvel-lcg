from . import *

# hs107a Acquiring Targets
# A_FAIRE_CLAUDE: Standalone setup must search/move existing cards, then advance to 1B with native main-scheme lifecycle. Never create duplicate scenario environment/support copies.
# Printed: <b>Contents</b>: Kraven The Hunter (I) and Kraven The Hunter (II). <i>(Kraven The Hunter (II) and Kraven The Hunter (III) instead for expert mode.)</i> Kraven The Hunter and Standard encounter sets. One modular encounter set <i>(recommended: Savage Six)</i>.
# Printed: <b>Setup</b>: Shuffle all of the [[TRAP]] cards into a separate [[TRAP]] deck. Advance to stage 1B.

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    # A_FAIRE_CLAUDE: implement printed standalone setup before campaign setup.
    return [*CampaignSetup(5)]
