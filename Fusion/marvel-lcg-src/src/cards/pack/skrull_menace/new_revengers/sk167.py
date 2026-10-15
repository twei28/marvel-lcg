from . import *

# * White Tiger — SBIRE (New Revengers). REVENGER. PV 3, MNG 2, ATQ 2, 2 boosts. Quickstrike.
# Quickstrike. (After this minion engages your hero, it attacks you.)
# When Defeated: Give the villain 1 facedown boost card.
#
# Cartes de reference :
#  - Quickstrike : natif (`desc.Quickstrike`, fiche mots-cles/quickstrike.md), aucun module pour lui.
#  - « Give the villain 1 facedown boost card » : **`30037`** Solus (`Faces.GiveFacedownBoostCards([unit], 1,
#    effect)`) ; When Defeated : `WhenUnitBeDefeated(WhenDefeated, "This", ...)`.
#
# ⚠ Mots-pieges : « the VILLAIN » (pas le sbire ni un autre ennemi) ; « FACEDOWN boost card » (une carte de
# boost face cachee du deck rencontre, qui servira a sa prochaine activation) ; la carte de boost reste en
# attente : elle n'est pas retournee ici.


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            Faces.GiveFacedownBoostCards([mechant], 1, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
