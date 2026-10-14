from . import *

# hs127 Fierce Cheetah
# A_FAIRE_CLAUDE: Forced Response: extra attack after engaged player-controlled character attacks Kraven; correct engaged-player and controlled-character matching required.
# Printed: Fierce Cheetah’s attacks gain piercing.
# Printed: <b>Forced Response</b>: After a character controlled by the engaged player attacks Kraven The Hunter, Fierce Cheetah attacks that player.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", piercing=True)]
