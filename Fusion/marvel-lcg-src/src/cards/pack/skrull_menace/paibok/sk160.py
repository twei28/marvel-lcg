from . import *

# Power Demonstration — TRAITRISE x4 (Paibok). 2 boosts.
# When Revealed: Resolve the "Boost" ability on each attachment in play, that belongs to the Paibok
#   encounter set. If no "Boost" ability was resolved this way, this card gains surge.
#   (phrase « If no Boost... surge » ajoutee dans la version Kajislav du 03/11/2026 ; image Drive du
#   17/11/2026.)
#
# Cartes de reference : **`24017`** Double Trouble (`ResolveAbility` d'une capacite nommee de cartes en
# jeu) ; helper `ResoudreLesBoosts` (paibok/__init__.py, rend le nombre de Boost resolus), identique a
# sk159 (alter ego), sk155, sk146 ; surge : `ThisCardGainSurge`, modeles `nt015` et `sk158`.
#
# ⚠ Mots-pieges : « each attachment IN PLAY that belongs to the Paibok SET » (Distracted, Hypnotized,
# Trapped in Ice sur les identites ; Captain Paibok et les POWER SKRULL sur Paibok) ; le Boost se resout
# pour le joueur qui REVELE (« a character you control », « your hand ») ; « If NO Boost ability was
# resolved this way » : aucun attachement du set en jeu (ou aucun qui porte un Boost) -> la carte gagne
# SURGE (avant le 17/11/2026 : « rien », la phrase n'etait pas imprimee).


def GetAbilities() -> Sequence['Ability']:

    def demonstration(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        if ResoudreLesBoosts(effect, message.GetToPlayer()) == 0:
            ThisCardGainSurge(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, demonstration),
    ]
