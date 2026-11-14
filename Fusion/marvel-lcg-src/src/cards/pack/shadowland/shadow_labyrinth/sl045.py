from . import *

# Sudden Shift — TRAITRISE x2. Boost 2 + ★.
# When Revealed : Shuffle the trap discard pile and the top 3 cards of the encounter deck into the trap deck. Reveal the top card of the trap deck.
# ★ Boost : Shuffle the trap discard pile and the top 2 cards of the encounter deck into the trap deck.
#
# Cartes de reference : `MelangerDansPaquetPiege` / `ReveleDuPaquetPiege` (ce module), hunting_season/trap `RemelangeDefaussePiege` (`ShuffleWithDiscardPile`), sl041 (le deck de rencontre
# alimente le paquet piege).
# ⚠ Mots-pieges : « the trap DISCARD PILE AND the top 3 cards » : les DEUX sont melanges ensemble dans le paquet piege ; « Reveal the top card » : apres le melange, au
#  joueur qui revele ; en Boost : seulement 2 cartes, et RIEN n'est revele.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        MelangerDansPaquetPiege(effect, du_deck_rencontre=3, avec_defausse=True)
        ReveleDuPaquetPiege(effect, message.GetToPlayer())

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        MelangerDansPaquetPiege(effect, du_deck_rencontre=2, avec_defausse=True)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
