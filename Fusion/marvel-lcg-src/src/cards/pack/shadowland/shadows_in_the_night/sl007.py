from . import *

# Sealed Entrances — COMPLOT ANNEXE. Menace de depart 4, Boost 2, Crisis 1. Assault.
# Assault. (Basic thwarts against this scheme use ATK instead of THW.)
# When Defeated : Change the villain's position if it has not changed this phase.
#
# Cartes de reference : punisher_mcdc_2026/jigsaw/pu065 (`WhenSchemeBeDefeated(WhenDefeated, "This")`), fiche mots-cles/assault.md (Assault et Crisis sont natifs).
# ⚠ « 4 » FIXE (pas par joueur) ; le changement de position n'a lieu qu'a la DEFAITE de la manigance, pas a sa revelation.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        ChangerSiPasChange(effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
