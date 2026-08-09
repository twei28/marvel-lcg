from cards.pack import *
from cards.pack.fne.daredevil import SENSE_DECK_IDS
Unused(SENSE_DECK_IDS)
ENEMY_OR_SCHEME = (CardFinder(card_type=Enemy) | CardFinder(card_type=Scheme2))
def SenseDiscard(this: 'CardFace', by_effect: 'Effect') -> None:
    Faces.DiscardAll([this], by_effect)
