from . import *

# Angel of Death : ATTACHEMENT (TITLE.), boost 3. Set « Sentry Nemesis ».
# Attach to The Void. If you cannot, place 2 balance counters on Duality Aspect, then this card gains surge. The Void gains guard and patrol.
# Forced Interrupt: At the end of the round (after the first player token is passed), the Sentry player discards cards from the top of their deck until they discard a SPLIT card. Resolve the "Special" ability on that card.
#
# CARTES DE REFERENCE
#  - `ca017` (Death Spiral) : `AttachToFaceWhenPutIntoPlay(CardFinder(card_type=Minion, name=..), if_cannot_gain_surge=True)` ; ici `if_cannot_operation` pose en plus les 2 compteurs.
#  - « gains guard and patrol » : `GiveKeywordToAttached(.., guard=1, patrol=1)` ; fin de round : `WhenRoundEnd(ForcedInterrupt, None, op)` (`bw016`) ; Special : `carte.ResolveSpecialAbility(joueur, effect)`.
#
# TEXTE CONTRE CODE
#  « If you CANNOT (attach) » : Void absent -> 2 compteurs sur Duality Aspect PUIS surge. « AT THE END OF THE ROUND (after the first player token is passed) » : code sur la fin de round ; le moteur n'a pas de fenetre distincte
#  « apres le jeton » (note). « discards cards FROM THE TOP of their deck UNTIL they discard a SPLIT card » : on defausse une a une ; deck epuise sans SPLIT -> rien a resoudre. Chiffres : boost 3.


def GetAbilities() -> Sequence['Ability']:

    def deux_compteurs(effect: 'Effect', joueur: 'Player') -> None:
        Unused(joueur)
        PoserEquilibre(effect, 2)

    def fin_de_round(effect: 'Effect', message: 'Message.WhenRoundEnd') -> None:
        Unused(message)
        joueur = JoueurSentry(effect)
        if joueur is None:
            return
        while len(joueur.player_deck.Get()) > 0:
            carte = joueur.DiscardDeckTopCard(effect)
            if carte is not None and carte.HasTrait("SPLIT"):
                carte.ResolveSpecialAbility(joueur, effect)
                return

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(card_type=Minion, name=NOM_VOID),
            if_cannot_gain_surge=True,
            if_cannot_operation=deux_compteurs,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_VOID),
            guard=1,
            patrol=1,
        ),
        AbilityFactory.WhenRoundEnd(AbilityType.ForcedInterrupt, None, fin_de_round),
    ]
