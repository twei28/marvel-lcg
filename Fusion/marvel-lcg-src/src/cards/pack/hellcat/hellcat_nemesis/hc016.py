from . import *
# * Daimon Hellstrom — SBIRE nemesis. DEMON. CTR 3 / ATQ 1, 4 PV, boost 2.
# Stalwart. Villainous. (bases automatiques, desc)
# Daimon Hellstrom cannot be in the same play area as Blackheart.
# When Revealed: If Blackheart is in your play area, Daimon Hellstrom engages
#   with the next player in turn order. If he cannot, this card gains surge.
# Voir hc015 et `RevelationDUnDemon`.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenThisRevealed(
            None,
            lambda effect, message: RevelationDUnDemon(effect, message, BLACKHEART),
        ),
    ]
