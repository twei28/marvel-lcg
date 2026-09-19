from . import *

# Public Support (HIGH)
# Interrupt: When an enemy would be given a facedown boost card, remove
#   1[per_hero] support counters from here instead.
# Forced Response: After a minion is defeated, place 1 support counter here.
#
# Fenetre moteur ajoutee le 18/09/2026 pour cette carte :
# Message.WhenEnemyWouldBeGivenBoostCards, envoye par
# CanBoost.GiveFacedownBoostCardsInternal AVANT la pioche, pour TOUTES les
# sources (activation, James Wesley, Bag of Tricks). Fabrique
# AbilityFactory.WhenEnemyWouldBeGivenBoostCards (activate.py) ; l'operation
# retire UNE carte du compte (message.SetNum(num - 1)) et les compteurs.

def GetAbilities() -> Sequence['Ability']:

    def remplacable(effect: 'Effect', message: 'Message.WhenEnemyWouldBeGivenBoostCards') -> bool:
        return message.num > 0 and \
            effect.this.GetCounters('support') >= Worlds.GetPlayerNumIcon(effect)

    def remplacer(effect: 'Effect', message: 'Message.WhenEnemyWouldBeGivenBoostCards') -> None:
        message.SetNum(message.num - 1)
        Faces.RemoveCountersOn([effect.this], Worlds.GetPlayerNumIcon(effect), 'support', effect)

    return [
        AbilityFactory.WhenEnemyWouldBeGivenBoostCards(AbilityType.Interrupt, Enemy, remplacer, conditions=[remplacable]),
        ReponseForceeSoutien(),
    ]
