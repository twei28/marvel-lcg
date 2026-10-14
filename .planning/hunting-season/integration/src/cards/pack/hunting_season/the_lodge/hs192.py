from . import *

# hs192 Hunterbot
# A_FAIRE_CLAUDE: Restrict +1 ATK to hero form. Forced Interrupt: route damage to Hunterbot instead, then discard at 3 or more accumulated damage. Do not cap routed damage at 3.
# Printed: Experience Cost 3.
# Printed: Max 1 per player.
# Printed: Your hero gets +1 ATK.
# Printed: <b>Forced Interrupt</b>: When you would take any amount of damage, place it here instead. Then, if there is 3 or more damage here, discard Hunterbot.

def GetAbilities() -> Sequence['Ability']:
    return [*AbilityFactory.GiveKeywordToAttached("You", attack=1)]
