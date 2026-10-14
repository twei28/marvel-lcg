from . import *

# hs204 * Vermin
# A_FAIRE_CLAUDE: Implement printed rat-counter replacement/prevention. Rat counters are not Uses; no automatic discard at zero. Confirm minion replacement is unavailable when no counter can be removed.
# Printed: Vermin enters play with 3 rat counters.
# Printed: <b>Forced Interrupt</b>: When Vermin would take any amount of damage, remove a rat counter from him instead.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.ThisEnterPlayWithCounters(3, "rat")]
