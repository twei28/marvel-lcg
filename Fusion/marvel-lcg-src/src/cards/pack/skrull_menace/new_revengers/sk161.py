from . import *

# O.M.N.I.T.R.O.N.I.C.U.S. — ENVIRONNEMENT (New Revengers). COMPUTER. REVENGER. 1 boost.
# Each REVENGER minion gains villainous.
# Hero Action: If there is no REVENGER enemy in play, spend [energy][energy] resources → discard this card.
#
# Cartes de reference :
#  - « each X minion gains villainous » : **`spiderham 30037`** Solus (`GiveKeywordToInPlayWhenApplyThis(
#    CardFinder2("INHERITOR", Minion), villainous=1)`) et `ah015` For The Queen!.
#  - Defausse a cout + condition : `PlayerActionToDiscardThis(HeroAction, conditions=[...])` (attachment.py:8,
#    modele 01100 pour `SetCost`) ; cout `[energy][energy]` = `YY` (eclairs, verifie contre sk044).
#
# ⚠ Mots-pieges : « REVENGER MINION » (sbires seulement : le mechant qui gagne le trait par The Revenge Time
# n'est PAS villainous par cette carte) ; « If there is NO REVENGER ENEMY in play » (ennemi, pas sbire : le
# mechant devenu Revenger compte) ; l'environnement porte lui-meme le trait REVENGER mais n'est pas un
# ennemi ; « Hero Action » : forme heros seulement.


def GetAbilities() -> Sequence['Ability']:

    def aucun_revenger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        return not EnnemisRevenger(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2(TRAIT_REVENGER, Minion), villainous=1),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction, conditions=[aucun_revenger]).SetCost(Cost("YY")),
    ]
