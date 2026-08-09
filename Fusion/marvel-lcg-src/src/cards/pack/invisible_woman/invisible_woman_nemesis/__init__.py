from cards.pack import *


def RevealDiscardedInvisibleNemesisCards(effect: 'Effect', cards: Sequence['CardFace'], player: 'Player') -> bool:
    revealed = False
    for face in list(cards):
        # CORRECTIF : le scan de « End of the Line » limite la revelation a
        # Microversal Maneuvers et Titanic Terror. Le helper revelait TOUTE
        # carte du set nemesis, donc aussi Psycho-Man et Emotional Masterplan.
        if face.paper.card_id in ("66016", "66017"):
            face.Reveal(player, effect)
            revealed = True
    return revealed
