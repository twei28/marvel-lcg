from . import *

# Shuriken Ninja — SBIRE. HAND. NINJA. ATQ 1* / MNG 1 / PV 2, Boost 1. Teamwork (NINJA).
# [star] This minion's attacks gain piercing.
# When Defeated : The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
#
# Cartes de reference : sl031 (meme structure), albert/ab008 (`piercing=True`), mots-cles/piercing.md.
# ⚠ Mots-pieges : « this minion's attacks gain piercing » = PERMANENT, sur ses seules attaques : elles defaussent la carte Tough de leur cible au lieu d'etre absorbees.
#  Teamwork est lu dans `desc`.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", DefausserDeuxEtReveler),
    ]
