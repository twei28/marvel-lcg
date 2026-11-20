from . import *

# * Electro — SBIRE UNIQUE. CRIMINAL. SYNDICATE. SCH 1, ATQ 1, 5 PV, Boost 3, Villainous 1.
# Villainous. Electro's attacks deal indirect damage.
# When Defeated : voir __init__.py.
#
# Cartes de reference : sk162 (`UnitAttackGainKeyword("This", ...)`), sm/sinister_six (indirect_damage=True : sk166,
# sk224b). Villainous : natif (`desc`).
# ⚠ « deal INDIRECT damage » : le joueur attaque repartit les degats sur ses personnages ; pas de defenseur utile.

def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", indirect_damage=True),
        DefaiteSyndicate(),
    ]
