from . import *

# Shredder's Wrath (2A) — COMPLOT PRINCIPAL, face A.
# When Revealed: In player order, each player discards 4 cards from the top of
#   the encounter deck and reveals the topmost FOOT CLAN minion in the encounter
#   discard pile.
#
# Cartes de reference : `Players.ForEachPlayer` (11013b, ordre des joueurs),
# `Worlds.DiscardEncounterCards(n, effect)` (15004 / ho014 : « discard N cards
# from the top of the encounter deck ») et `Deck.FindTopmost` (56108 : « the
# topmost X in the encounter discard pile »).
#
# Mots-pieges : « EACH player » discards 4 PUIS revele (par joueur, pas 4 x N
# d'abord) ; « topmost » = le plus recent sur la defausse ; si aucun sbire FOOT
# CLAN, rien ne se passe ; chaque joueur revele a SON propre compte.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        def pour_chaque_joueur(joueur: 'Player') -> None:
            Worlds.DiscardEncounterCards(4, effect)
            RevelerLePlusHautDeLaDefausse(effect, joueur, CardFinder2("FOOT CLAN", Minion))

        Players.ForEachPlayer(effect, pour_chaque_joueur)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
