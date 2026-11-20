from . import *

# * ForgetMeNot (Xabi) : allie RECRUITED, cout 4, PV 4, THW 4***, ATK 4***.
# Forced Response: At the end of the round, if ForgetMeNot is still in play, discard him.
#
# Carte de reference : 01084 Nick Fury (`AbilityFactory.DiscardThisWhenRoundEnd(AbilityType.ForcedResponse)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.DiscardThisWhenRoundEnd(
            AbilityType.ForcedResponse,
        ),
    ]
