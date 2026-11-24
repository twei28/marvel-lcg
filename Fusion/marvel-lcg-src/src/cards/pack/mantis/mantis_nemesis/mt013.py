from . import *

# * Swordsman : SBIRE (COTATI. ELITE.), nemesis de Mantis. SCH 1, ATQ 2*, PV 4, boost 2. Quickstrike.
# [star] Swordsman's attacks gain piercing.
#
# CARTES DE REFERENCE
#  - `bf032` Angelus : `UnitAttackGainKeyword("This", piercing=True)` (« [star] X's attacks gain piercing », capacite etoilee d'un sbire).
#  - `mots-cles/quickstrike.md` : `desc.Quickstrike` est lu NATIVEMENT par le moteur (attaque a l'engagement), AUCUN script pour lui ; `Nemesis: Mantis` lu dans `desc`.
#
# TEXTE CONTRE CODE
#  « Swordsman's attacks » : toutes ses attaques (pas seulement la premiere), perforantes (Robuste defaussee au lieu d'absorber). Chiffres : SCH 1, ATQ 2, PV 4, boost 2.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
    ]
