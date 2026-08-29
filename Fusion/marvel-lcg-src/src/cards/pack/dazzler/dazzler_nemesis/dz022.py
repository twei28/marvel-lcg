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
        # donc `AssertionError: self.initiator=Rhino`, avalee par le moteur —
        # la Setlist n'etait jamais defaussee et le surge jamais gagne. On lit
        # le joueur vise sur le message, comme le fait dz023.
        joueur = message.GetToPlayer()
        if joueur is None:
            return

        setlist = Setlist(effect, joueur)
        partis = Faces.DiscardAll(setlist, effect) if setlist else []
        # Les marques `sound` partent avec les cartes, sinon une chanson
        # ramenee par Encore reviendrait « deja repetee ».
        OublierLaSetlist(effect, setlist)

        if not partis:
            ThisCardGainSurge(effect, message)

    return [
        AbilityFactory.WhenThisRevealed(None, voler_le_son),
    ]
