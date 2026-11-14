from . import *
# * The Vengeful Wing (sbire ELITE SHI'AR VEHICLE, 6 PV, SCH 2*, ATQ 3*, boost 3).
#
# [star] The Vengeful Wing's attacks deal indirect damage.
#
# Carte de reference : 16137 Starshark (`UnitAttackGainKeyword("This", indirect_damage=True)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            indirect_damage=True,
        ),
    ]
