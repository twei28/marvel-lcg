from . import *

# hs004a Rats and More Rats
# A_FAIRE_CLAUDE: Standalone setup must search/move existing cards, then advance to 1B with native main-scheme lifecycle. Never create duplicate scenario environment/support copies.
# Printed: <b>Contents</b>: Vermin (I) and Vermin (II). <i>(Vermin (II) and Vermin (III) instead for expert mode.)</i> Vermin and Standard encounter sets. One modular encounter set <i>(recommended: Feral Instincts)</i>.
# Printed: <b>Setup</b>: Put the Even More Rats environment into play. Put a Regular Rats minion into play engaged with each player. Shuffle the encounter deck. Advance to stage 1B.

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    # A_FAIRE_CLAUDE: implement printed standalone setup before campaign setup.
    return [*CampaignSetup(1)]
