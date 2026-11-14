from . import *
from cards.pack.fne.kingpin import TrouverPublicSupport

# Down With — ENVIRONNEMENT de campagne (combat 4, p272, face 2B de Kingsfall, verso de pu149a Long Live). Permanent.
# When Revealed : Each group resets the number of support counters on their Public Support to 2[per_hero]+3 counters.
# Pod Action : Choose a group in the pod. Move 1 counter from your Public Support to their Power to the People.   [MULTI-TABLES : `ActionDAssemblee`, set __init__]
#
# Cartes de reference : fne/kingpin/60163a Public Support (`TrouverPublicSupport`, jeton `support`), 60161b / 60162a (`WhenThisRevealed(None, ...)`), pu149a.
# ⚠ Mots-pieges :
#  - « resets ... TO 2[per_hero]+3 » : ramene a EXACTEMENT 2 x joueurs + 3, que Public Support en ait plus OU MOINS (pas seulement un plafond) ;
#  - « each group ... their Public Support » : une table = un groupe, un seul Public Support ;
#  - c'est ce niveau qui fait avancer Kingpin au debut de la prochaine phase du mechant (seuil 2 x joueurs + 2 de Public Support LOW).

def GetAbilities() -> Sequence['Ability']:

    def reinitialiser(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        soutien = TrouverPublicSupport(effect)
        if soutien is None:
            return
        cible = 2 * Worlds.GetPlayerNumIcon(effect) + 3
        actuel = soutien.GetCounters('support')
        if actuel > cible:
            Faces.RemoveCountersOn([soutien], actuel - cible, 'support', effect)
        elif actuel < cible:
            Faces.PlaceCountersOn([soutien], cible - actuel, 'support', effect)

    def synchroniser(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Unused(message)
        SynchroniserLaTable(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, reinitialiser),
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, synchroniser),
        ActionDAssemblee(),
    ]
