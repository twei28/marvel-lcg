from . import *

# Kree Pursuer — SBIRE (Hala Ultimatum). KREE. PURSUER CORPS. SCH 1, ATK 2, PV 6. 2 icones de boost. 2 exemplaires.
# Patrol. Quickstrike.
# When Defeated: If the villain has a tough status card, shuffle Kree Pursuer into the encounter deck.
#
# Cartes de reference :
#  - Patrol, Quickstrike : natifs (desc, fiches mots-cles/patrol.md et quickstrike.md).
#  - « When Defeated: if the villain has a tough status card, shuffle X into the encounter deck » :
#    `WhenUnitBeDefeated(WhenDefeated, "This", ...)` (modele gb022/44038) + `LeVilain`/`Faces.HasStatus`
#    (modele gs147, meme pack) + `Faces.ShuffleAllTo` (modele gs080a Self-Destruct Sequence, meme technique
#    de melange que la recherche encounter deck+defausse).
#
# ⚠ Mots-pieges : « the VILLAIN has a tough status card » (condition sur le mechant, pas sur Kree Pursuer
# lui-meme) ; « shuffle Kree Pursuer » = CETTE carte precise qui vient d'etre vaincue, pas une autre copie.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        villain = LeVilain(effect)
        if villain is not None and Faces.HasStatus([villain], "Tough") > 0:
            Faces.ShuffleAllTo([effect.this], Worlds.GetEncounterDeck(effect), effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
