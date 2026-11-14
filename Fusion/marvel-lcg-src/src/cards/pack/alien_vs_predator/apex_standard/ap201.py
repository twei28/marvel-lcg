from . import *

# Advance — TRAITRISE (Apex Standard). Boost 1.
# When Revealed: The villain schemes. Place this threat on the main scheme.
#
# Cartes de reference : 01186 Advance (`FindVillain` + `DoSchemes`) ; la redirection des deux mechants (`ManiganceSurSaManigance`) lit
#   `_ap_vers_le_complot` et s'efface le temps de cette manigance.
#
# ⚠ Mots-pieges :
#  - « Place THIS threat on the MAIN scheme » : malgre « When <mechant> schemes, place that threat on his/her side scheme » ;
#  - « the villain » = le mechant actif (regle du scenario) ; c'est une activation : au stade 1, le compteur passe ensuite.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is None:
            return
        effect.world._ap_vers_le_complot = True
        try:
            mechant.DoSchemes(joueur, effect)
        finally:
            effect.world._ap_vers_le_complot = False

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
