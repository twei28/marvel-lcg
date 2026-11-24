from . import *

# M-Pox Sickness — OBLIGATION, boost 2. A donner au joueur Roberto Da Costa.
# Increase the resource cost of the first card you play each round by 1.
# Alter-Ego Action: Remove 3 solar counters from your identity -> remove M-Pox Sickness from the game.
#
# CARTES DE REFERENCE
#  - `27132` Friends and Family : obligation PERSISTANTE a `IncreaseResourceCostToPlay(type, +1, "You", conditions=[..])`.
#  - `51031` : `CardFace` comme « which_card » = n'importe quelle carte.
#  - `21026` Loss of Control : `PlayerActionToRemoveThisFromGame(AbilityType.AlterEgoAction).SetCostFunc(..)`.
#
# TEXTE CONTRE CODE
#  ⚠ « the FIRST card you play each ROUND » : `stat.this_round_played_cards` vide (remis a zero a chaque round).
#  ⚠ « remove from the GAME » (pas « discard ») : `PlayerActionToRemoveThisFromGame`.
#  ⚠ Cout : 3 compteurs RETIRES de l'identite (stock < 3 : la capacite n'est pas jouable).


def GetAbilities() -> Sequence['Ability']:

    def premiere_carte_du_round(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        Unused(effect)
        return len(message.GetToPlayer().stat.this_round_played_cards) == 0

    return [
        AbilityFactory.IncreaseResourceCostToPlay(
            CardFace,
            +1,
            "You",
            conditions=[premiere_carte_du_round],
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Counter("YourIdentity", 3, COMPTEUR)),
    ]
