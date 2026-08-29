from . import *

# The Forager
# Interrupt: When you spend The Forager to pay for a Squirrel Girl card, look
#   at the top 2 cards of your deck. You may discard 1 of those cards. Return
#   the remaining cards to the top of your deck in any order.
#
# 28/08/2026 : la ressource des ecureuils paie desormais n'importe quelle
# carte, mais cet effet-ci reste reserve aux cartes du set (garde pose dans
# `ReponseALaDepense`).
#
# Meme montage que The Gatherer (sg007) : la depense etant portee par
# l'identite, l'effet se lit sur le depart du jeu de cet ecureuil.
#
# ECART DE TEXTE ASSUME (28/08/2026) : la carte est libellee « Interrupt /
# When », le moteur declenche sur AfterCardLeavePlay (« Response / After ») —
# il n'existe aucun crochet « quand tu depenserais un ecureuil », la depense
# n'etant pas une notion moteur. Sans consequence observable ici : l'effet ne
# reference pas l'ecureuil lui-meme, il se resout une fois, au moment de la
# depense, dans les deux lectures.

def GetAbilities() -> Sequence['Ability']:

    def fouiller(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        deux = joueur.LookAtDeck(joueur.player_deck, 2, effect)
        if not deux:
            return

        # Les cartes d'un deck ne se designent pas par un selecteur de cible
        # (voir le correctif de Tippy-Toe sg002), mais par MayChooseFace.
        choisi = joueur.MayChooseFace(list(deux), effect, not_move=True)
        if choisi is not None:
            Faces.DiscardAll([choisi], effect)

    return [
        *Ecureuil(),
        ReponseALaDepense(fouiller),
    ]
