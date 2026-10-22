from . import *
from cards.pack.fne.kingpin import TrouverPublicSupport

# Long Live — ENVIRONNEMENT de campagne (combat 4, p271, face 2A de Kingsfall). Setup. Permanent. Recto de pu149b (Down With).
# Pod Action : Choose a group in the pod. Move 1 counter from your Public Support to their Power to the People.   [MULTI-TABLES : `ActionDAssemblee`, set __init__]
# Forced Interrupt : At the end of the player phase, move each support counter from your Public Support to here. Then, if there are 2[per_hero]+2[per_group]
#   counters here, flip this card.
#
# Cartes de reference : fne/kingpin/60163a Public Support (`TrouverPublicSupport`, jeton `support`, seuil `2 * GetPlayerNumIcon + 2`, `card.Flip`),
# `AbilityFactory.WhenPlayerPhaseEnd(ForcedInterrupt, ...)` (turn_phase.py), `Faces.RemoveCountersOn` / `PlaceCountersOn`.
# ⚠ Mots-pieges :
#  - « EACH support counter » : TOUS les jetons de soutien de Public Support (LOW ou HIGH), pas un seul ;
#  - « 2[per_hero] + 2[per_group] » : 2 par JOUEUR + 2 par GROUPE ; une table = un groupe, donc 2 x joueurs + 2 ;
#  - « Then, if ... flip » : le test se fait APRES le deplacement, sur le total ici (les jetons s'accumulent d'un round a l'autre) ;
#  - le verso (Down With) a le meme ID imprime : « flip » = `card.Flip`, ses jetons restent sur la carte (comme 60163) ;
#  - « Forced Interrupt » a « the end of the player phase » : `WhenPlayerPhaseEnd`.

def GetAbilities() -> Sequence['Ability']:

    def deplacer_les_jetons(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Unused(message)
        pod = Pod(effect)
        soutien = TrouverPublicSupport(effect)
        n = 0
        if soutien is not None:
            n = soutien.GetCounters('support')
            if n > 0:
                Faces.RemoveCountersOn([soutien], n, 'support', effect)
                if pod is None:
                    Faces.PlaceCountersOn([effect.this], n, 'support', effect)
        if pod is not None:
            # ASSEMBLEE : « here » = le total COMMUN (stockage partage) ; le miroir de cette table le montre, et se retourne au seuil de l'assemblee
            # (2 par joueur + 2 par groupe, tous groupes confondus).
            Assemblee.VerserJetons(pod[0], n)
            SynchroniserLaTable(effect)
            return
        if effect.this.GetCounters('support') >= 2 * Worlds.GetPlayerNumIcon(effect) + 2:
            effect.this.card.Flip(effect)

    def synchroniser(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        Unused(message)
        SynchroniserLaTable(effect)

    return [
        AbilityFactory.WhenPlayerPhaseEnd(AbilityType.ForcedInterrupt, deplacer_les_jetons),
        # Assemblee : une autre table a pu faire franchir le seuil ; ce groupe le sait avant SA phase du Mechant (A bas remet ses jetons a 2 par joueur + 3).
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, synchroniser),
        ActionDAssemblee(),
    ]
