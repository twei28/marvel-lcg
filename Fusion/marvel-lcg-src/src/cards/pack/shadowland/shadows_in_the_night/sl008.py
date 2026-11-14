from . import *

# Strategic Positioning — COMPLOT ANNEXE. Menace de depart 3 par joueur, Boost 2.
# While the villain's position is The Streets Below, this scheme gains 1 acceleration icon.
# While the villain's position is Atop the Tenshu, this scheme gains 1 hazard icon.
#
# Cartes de reference : ironheart/ironheart_nemesis/29029 (`ThisGainKeywordWhileFaceIsInPlay(CardFinder(...), hazard=1)`), sl003a/b (une face = une position).
# ⚠ Les deux icones sont EXCLUSIVES (jamais les deux, jamais aucune tant que la carte de position est en jeu) ; la position se lit sur la FACE VISIBLE de sl003
#  (sl003a = The Streets Below, sl003b = Atop the Tenshu), jamais sur sl004 (position du HEROS, memes noms de faces).


def GetAbilities() -> Sequence['Ability']:
    # Le moteur offre `acceleration_icon` seulement dans la variante « face PAS en jeu » et `hazard` dans « face en jeu » : on lit donc la SEULE face sl003b
    # (Atop the Tenshu) : en jeu -> aleas ; pas en jeu (donc sl003a, The Streets Below) -> acceleration. Equivalent, la carte de position etant toujours en jeu.
    return [
        AbilityFactory.ThisGainKeywordWhileFaceIsNotInPlay(CardFinder(card_ids=[POSITION_VILAIN[1]]), acceleration_icon=1),
        AbilityFactory.ThisGainKeywordWhileFaceIsInPlay(CardFinder(card_ids=[POSITION_VILAIN[1]]), hazard=1),
    ]
