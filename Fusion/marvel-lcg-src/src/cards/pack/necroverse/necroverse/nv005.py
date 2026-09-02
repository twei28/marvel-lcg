from . import *

# The Ingenuity of Hatred — TRAITRISE. 1 icone de boost.
#
# When Revealed: Shuffle all attachments in the encounter discard pile into the
#   encounter deck. Discard cards from the top of the encounter deck until a
#   minion is discarded. Reveal that card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Jumelle exacte de nv004, au type pres : elle rappelle les ATTACHEMENTS
#   la ou nv004 rappelle les sbires. Meme squelette, meme ordre.
# - Remelange depuis la defausse de rencontre : gb016 (Brutal Cunning), meme
#   `Faces.ShuffleAllTo(..., 'EncounterDeck', effect)`.
# - « Discard from the top until ... Reveal that card » : 04113b et gb016,
#   `Worlds.DiscardEncounterCardsUntil` puis `Reveal`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « ALL attachments in the encounter DISCARD PILE » -> tous, d'un coup, et depuis
#   la defausse seulement.
# Ordre : le remelange D'ABORD, la fouille ENSUITE — c'est ce qui garantit
#   qu'un attachement est trouvable meme si le deck n'en contenait plus.
# « REVEAL that card » -> l'attachement s'attache et resout son texte, il n'est
#   pas seulement defausse.


def GetAbilities() -> Sequence['Ability']:

    def ingeniosite_de_la_haine(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        defausse = Worlds.GetEncounterDiscardPile(effect)
        attachements = CardFinder(card_type=Attachment).Checks(defausse.Get(True))
        if attachements:
            Faces.ShuffleAllTo(attachements, 'EncounterDeck', effect)

        trouve = Worlds.DiscardEncounterCardsUntil(effect, card_type=Attachment)
        if trouve is not None and joueur:
            trouve.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, ingeniosite_de_la_haine),
    ]
