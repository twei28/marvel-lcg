from . import *

# Hive Incursion — TRAITRISE. Boost ★.
# When Revealed: Discard your hand. Draw up to your hand size.
# [star] Boost: Resolve the "When Revealed" ability on this card.
#
# Cartes de reference : 27093 Fearmonger (`DiscardAllHands` + `DrawUp(hand_size)`) ; Boost qui rejoue le « When Revealed » : 16116.
#
# ⚠ Mots-pieges : « draw UP TO your hand size » : on pioche jusqu'a la taille de main (main videe -> une main pleine) ; en boost, « your » =
#   le joueur attaque / qui subit la manigance.


def Incursion(effect: 'Effect', joueur: 'Player') -> None:
    joueur.DiscardAllHands(effect)
    manque = joueur.GetIdentity().hand_size - joueur.hand_cards.GetSize()
    if manque > 0:
        joueur.DrawUp(manque, effect)


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Incursion(effect, JoueurDuMessage(message, effect))

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Incursion(effect, JoueurDuMessage(message, effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
