from . import *

# Manifest Will — TRAITRISE. 1 icone de boost.
#
# When Revealed: Shuffle all minions in the encounter discard pile into the
#   encounter deck. Discard cards from the top of the encounter deck until a
#   minion is discarded. Reveal that card.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Jumelle exacte de nv005, au type pres (sbires ici, attachements la-bas).
# - Remelange depuis la defausse de rencontre : gb016 (Brutal Cunning), meme
#   `Faces.ShuffleAllTo(..., 'EncounterDeck', effect)`.
# - « Discard from the top until ... Reveal that card » : 04113b et gb016,
#   `Worlds.DiscardEncounterCardsUntil` puis `Reveal`.
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « ALL minions in the encounter DISCARD PILE » -> tous, d'un coup, et depuis
#   la defausse seulement.
# Ordre : le remelange D'ABORD, la fouille ENSUITE — c'est ce qui garantit
#   qu'un sbire est trouvable meme si le deck n'en contenait plus.
# « REVEAL that card » -> le sbire entre en jeu, il n'est pas seulement
#   defausse.


def GetAbilities() -> Sequence['Ability']:

    def volonte_manifeste(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        defausse = Worlds.GetEncounterDiscardPile(effect)
        sbires = CardFinder(card_type=Minion).Checks(defausse.Get(True))
        if sbires:
            Faces.ShuffleAllTo(sbires, 'EncounterDeck', effect)

        trouve = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if trouve is not None and joueur:
            trouve.Reveal(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, volonte_manifeste),
    ]
