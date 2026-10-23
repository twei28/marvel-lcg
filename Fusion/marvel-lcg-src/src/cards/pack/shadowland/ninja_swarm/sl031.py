from . import *

# Fukiya Ninja — SBIRE. HAND. NINJA. ATQ 1* / MNG 1 / PV 2, Boost 1. Teamwork (NINJA).
# [star] This minion's attacks gain ranged.
# When Defeated : The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
#
# Cartes de reference : aos/50107b (`UnitAttackGainKeyword("This", ranged=True)`, permanent), toafk/anachronauts/11045 + wave_nemesis/62030 (When Defeated), mots-cles/ranged.md.
# ⚠ Mots-pieges : « this minion's attacks gain ranged » = effet PERMANENT sur les attaques de CE sbire (le texte [star] annonce l'ATQ 1*), jamais sur celles des autres (`ranged` ignore
#  Retaliate) ; la cle `Ranged` n'existe pas dans `desc`. Pour le When Defeated, voir sl030. Teamwork est lu dans `desc`.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.UnitAttackGainKeyword("This", ranged=True),
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", DefausserDeuxEtReveler),
    ]
