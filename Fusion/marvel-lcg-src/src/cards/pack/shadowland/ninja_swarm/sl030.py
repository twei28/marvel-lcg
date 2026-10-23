from . import *

# Bo Staff Ninja — SBIRE. HAND. NINJA. ATQ 1 / MNG 1 / PV 2, Boost 2. Teamwork (NINJA). Toughness.
# When Defeated : The defeating player discards the top 2 cards of the encounter deck and reveals the first minion with the teamwork keyword discarded this way.
#
# Cartes de reference : toafk/anachronauts/11045 (`WhenDefeated`), wave_nemesis/62030 (defausser jusqu'a trouver, puis `Reveal(joueur)`), docs/reference/mots-cles/teamwork.md.
# ⚠ Toughness (statut Tough a l'entree en jeu) est natif.
#  Mots-pieges : « the defeating player » = qui a vaincu le sbire (a defaut, le joueur engage) ; « top 2 » = DEUX cartes defaussees quoi qu'il arrive, un seul sbire revele :
#  le PREMIER (dans l'ordre de defausse) qui porte Teamwork ; les deux cartes defaussees restent defaussees. Teamwork, Guard, Patrol, Toughness sont lus dans `desc`.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", DefausserDeuxEtReveler),
    ]
