from . import *

# hs033a Thirst for Revenge
# A_FAIRE_CLAUDE: Standalone setup must search/move existing cards, then advance to 1B with native main-scheme lifecycle. Never create duplicate scenario environment/support copies.
# Printed: <b>Contents</b>: Scorpion (I) and Scorpion (II). <i>(Scorpion (II) and Scorpion (III) instead for expert mode.)</i> Scorpion and Standard encounter sets. One modular encounter set <i>(recommended: Feral Instincts)</i>.
# Printed: <b>Setup</b>: Put the J. Jonah Jameson support into play under the first player’s control. Put the Scorpion’s Tail upgrade into play, and attach it to Scorpion. Advance to stage 1B.

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    # A_FAIRE_CLAUDE: implement printed standalone setup before campaign setup.
    return [*CampaignSetup(2)]
