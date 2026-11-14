from . import *

# Stealing Sound
# TREACHERY.
# When Revealed: Discard all SONG events from Dazzler's Setlist. If no cards
#   were discarded this way, this card gains surge.
#
# La Setlist appartient au joueur qui subit la trahison : on la lit depuis
# l'effet, qui porte deja le bon joueur.
#
# « If NO cards were discarded THIS WAY » : le surge se decide sur le nombre
# reellement parti, pas sur l'existence d'une Live Concert. Un joueur qui a
# Live Concert en jeu mais la Setlist vide prend quand meme le surge.


def GetAbilities() -> Sequence['Ability']:

    def voler_le_son(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        # La trahison est revelee DEPUIS LE DECK RENCONTRE : l'initiateur de
        # l'effet est le VILAIN, pas un joueur. `Setlist(effect)` seule levait
        # donc `AssertionError: self.initiator=Rhino`, avalee par le moteur.
        #
        # « DAZZLER's Setlist » : la Setlist est NOMMEE. Revelee par un autre
        # joueur, la carte vise quand meme celle de Dazzler. Jusqu'au 20/10/2026
        # le module lisait le joueur qui revele (`message.GetToPlayer()`), ce
        # qui ne marchait que parce que `Concert` ignorait son filtre de joueur
        # (corrige le meme jour, backlog 12).
        joueur = JoueurDeDazzler(effect)
        setlist = Setlist(effect, joueur) if joueur is not None else []
        partis = Faces.DiscardAll(setlist, effect) if setlist else []
        # Les marques `sound` partent avec les cartes, sinon une chanson
        # ramenee par Encore reviendrait « deja repetee ».
        OublierLaSetlist(effect, setlist)

        if not partis:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(None, voler_le_son),
    ]
