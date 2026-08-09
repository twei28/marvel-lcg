from . import *

# The Forager
# Response: After you spend The Forager, look at the top 2 cards of your deck.
#   Discard 1 of them, or return them in any order.
#
# Meme montage que The Gatherer (75007) : la depense etant portee par
# l'identite, la reponse se lit sur le depart du jeu de cet ecureuil.

def GetAbilities() -> Sequence['Ability']:

    def fouiller(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        deux = joueur.LookAtDeck(joueur.player_deck, 2, effect)
        if not deux:
            return

        # Les cartes d'un deck ne se designent pas par un selecteur de cible
        # (voir le correctif de Tippy-Toe 75002), mais par MayChooseFace.
        choisi = joueur.MayChooseFace(list(deux), effect, not_move=True)
        if choisi is not None:
            Faces.DiscardAll([choisi], effect)

    return [
        *Ecureuil(),
        ReponseALaDepense(fouiller),
    ]
