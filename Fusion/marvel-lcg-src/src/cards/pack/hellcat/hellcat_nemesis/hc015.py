from . import *
# * Blackheart — SBIRE nemesis. DEMON. CTR 1 / ATQ 2, 4 PV, boost 2.
# Toughness. Villainous. (bases automatiques, desc)
# Blackheart cannot be in the same play area as Daimon Hellstrom.
# When Revealed: If Daimon Hellstrom is in your play area, Blackheart engages
#   with the next player in turn order. If he cannot, this card gains surge.
#
# Tout est dans `RevelationDUnDemon` (__init__ du set). ⚠ « cannot be in the
# same play area » n'est applique qu'A LA REVELATION : un effet qui
# deplacerait un demon apres coup n'est pas surveille (ecart note).

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenThisRevealed(
            None,
            lambda effect, message: RevelationDUnDemon(effect, message, DAIMON),
        ),
    ]
