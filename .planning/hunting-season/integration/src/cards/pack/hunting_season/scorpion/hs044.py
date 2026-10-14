from . import *

# hs044 * Grizzly
# A_FAIRE_CLAUDE: Boost: this attack gains piercing. Resolve the boost activation using the existing engine API, not the card as attacker.
# Printed: [star] <b>Forced Interrupt</b>: When Grizzly attacks, the attack gains piercing.
# Printed: <hr />
# Printed: [star] <b>Boost</b>: This attack gains piercing.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", piercing=True)]
