from . import *

# Selective Breeding — COMPLOT ANNEXE (Supreme Intelligence). Menace 6 (fixe), icone d'AMPLIFICATION,
# 3 icones de boost.
# When Revealed: Shuffle each KREE minion from the encounter discard pile into the encounter deck.
#
# Cartes de reference : **`falcon/53033`** Adder-tisement (meme phrase, trait SERPENT SOCIETY) :
# `Worlds.GetEncounterDiscardPileCards(effect, CardFinder2(<trait>, Minion))` + `Faces.ShuffleAllTo(...,
# "EncounterDeck", effect)`. Amplify : base AUTOMATIQUE (`desc.Amplify`).
#
# ⚠ Mots-pieges : « EACH KREE MINION » (sbires KREE seulement, pas les traitrises) ; « from the encounter
# DISCARD PILE » (pas la pile de victoire) ; « INTO the encounter deck » (melange) ; aucun : rien.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        sbires = Worlds.GetEncounterDiscardPileCards(effect, CardFinder(card_type=Minion, trait="KREE"))
        if sbires:
            Faces.ShuffleAllTo(sbires, "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
