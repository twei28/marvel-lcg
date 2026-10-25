from . import *

# Cruel Intentions — TRAITRISE (Apex Standard). Boost ★ + 1. Incite 1.
# Incite 1.
# When Revealed: Deal each player 1 facedown encounter card. Give the villain 1 facedown boost card.
# [star] Boost: Deal yourself 1 facedown encounter card.
#
# Cartes de reference : Incite natif (`desc`) ; `DealEncounterCards(1)` ; « Give the villain 1 facedown boost card » :
#   `Faces.GiveFacedownBoostCards([mechant], 1)` (27150).
#
# ⚠ Mots-pieges : « EACH player » ; « the villain » = le mechant actif ; en boost, « yourself » = le joueur attaque / vise.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        for joueur in Worlds.GetPlayers(effect):
            joueur.DealEncounterCards(1, effect)
        mechant = Worlds.FindVillain(effect)
        if mechant is not None:
            Faces.GiveFacedownBoostCards([mechant], 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        JoueurDuMessage(message, effect).DealEncounterCards(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
