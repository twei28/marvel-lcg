from . import *

# * Mirage (Danielle Moonstar) : allie RECRUITED, cout 2, PV 3, THW 1*, ATK 2*. [star] ability.
# [star] Mirage's basic attack gains ranged.
#
# Carte de reference : 04002 Hawkeye's Bow (`WhenUnitWouldAttack(..., lambda effect, message: message.GainRanged(effect))`).
# ⚠ « basic attack » : `is_basic_attack=True` ; l'attaquant est MIRAGE ("This"), pas le heros.
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.NonKeyword,
            "This",
            lambda effect, message:
                message.GainRanged(effect),
            is_basic_attack=True,
        ),
    ]
