from . import *

# Overwhelming Force — TRAITRISE (Apex Standard). Boost ★ + 2.
# When Revealed: Discard the highest cost upgrade or support you control. If no card was discarded this way, this card gains surge.
# [star] Boost: Give the villain 1 additional boost card for this activation.
#
# Cartes de reference : 07034 Pile It On (`DiscardControlCards(upgrade=True, support=True, highest_cost=True)`) ; surge gagne :
#   `ThisCardGainSurge` (01187) ; « 1 additional boost card for this activation » : `message.GiveBoostCardForThisActivation(Villain, 1)` (16116).
#
# ⚠ Mots-pieges : « the HIGHEST cost » (egalite : le joueur choisit, natif) ; « upgrade OR support YOU control » ; rien a defausser -> surge.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = JoueurDuMessage(message, effect)
        defaussee = joueur.DiscardControlCards(effect, upgrade=True, support=True, highest_cost=True)
        if defaussee is None:
            ThisCardGainSurge(effect, message)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GiveBoostCardForThisActivation(Villain, 1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
