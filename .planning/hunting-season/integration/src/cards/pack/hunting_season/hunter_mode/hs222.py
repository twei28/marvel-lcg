from . import *

# hs222 Rabid Rodents
# A_FAIRE_CLAUDE: Forced Response after RAT minion enters play: place 1 threat ON THAT MINION, not on a scheme. Restrict Vermin name match to encounter villain/minion, not campaign ally.
# Printed: Vermin and Vermin Clone get +1 ATK.
# Printed: <b>Forced Response</b>: After a [[RAT]] minion enters play, place 1 threat on that minion.

def GetAbilities() -> Sequence['Ability']:
    return [*AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
        CardFinder(name="Vermin", card_type=Villain), attack=1),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
        CardFinder(name="Vermin Clone", card_type=Minion), attack=1)]
