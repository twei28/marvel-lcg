from . import *

# hs057a Using the Mammal Brain
# A_FAIRE_CLAUDE: Standalone setup must search/move existing cards, then advance to 1B with native main-scheme lifecycle. Never create duplicate scenario environment/support copies.
# Printed: <b>Contents</b>: Curtis Connors (I) and Curtis Connors (II). <i>(Curtis Connors (II) and Curtis Connors (III) instead for expert mode.)</i> The Lizard and Standard encounter sets. One modular encounter set <i>(recommended: Lizard Thralls)</i>.
# Printed: <b>Setup</b>: Put the Reptilian Rage environment into play. The villain starts on the Curtis Connors side. Advance to stage 1B.

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:
    # A_FAIRE_CLAUDE: implement printed standalone setup before campaign setup.
    return [*CampaignSetup(3)]
