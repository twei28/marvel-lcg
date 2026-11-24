from . import *

# Infernal Temper (mp025, deux exemplaires identiques) — TRAITRISE. Boost 1.
# Capacites : `AbilitesDInfernalTemper` (voir mephisto/__init__.py). Reference : `DoSchemes` / `DoAttackYou` + `GainSCHForThisScheme` / `GainATKForThisAttack`.
# ⚠ Mots-pieges : deux When Revealed distincts selon la forme (alter-ego = manigance, heros = attaque) ; X = pactes EN JEU, tous joueurs, compte au moment
# de la revelation ; « +X SCH / +X ATK » : pour cette seule activation.


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilitesDInfernalTemper(),
    ]
