from . import *

# hs200 * Vermin
# A_FAIRE_CLAUDE: Implement printed rat-counter replacement/prevention. Rat counters are not Uses; no automatic discard at zero. Confirm minion replacement is unavailable when no counter can be removed.
# Printed: Vermin enters play with 3 rat counters.
# Printed: <b>Interrupt</b>: When Vermin attacks, remove a rat counter from him → Vermin does not take consequential damage for this attack.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.ThisEnterPlayWithCounters(3, "rat")]
