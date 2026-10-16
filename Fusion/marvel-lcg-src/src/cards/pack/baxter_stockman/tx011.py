from . import *

# Mad Lab — MANIGANCE ANNEXE (Baxter's Lab 21/22, x2). 2[per_hero] menaces, 1 boost.
# Forced Interrupt: When the villain phase begins, the first player must resolve the "Special" ability
#   on Baxter's Laboratory.
#
# Cartes de reference : `tx001` (meme declencheur, tous les joueurs) ; `Worlds.GetFirstPlayer`.
#
# Mots-pieges : « the FIRST player » (un seul joueur, pas tous : a la difference de Baxter) ; « MUST » :
# obligatoire, interruption forcee.


def GetAbilities() -> Sequence['Ability']:

    def premier_joueur(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        ResoudreLeSpecial(effect, Worlds.GetFirstPlayer(effect))

    return [AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, premier_joueur)]
