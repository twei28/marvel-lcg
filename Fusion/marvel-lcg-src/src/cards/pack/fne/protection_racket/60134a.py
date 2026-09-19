from . import *

# Protection Racket 1A (face commune aux cinq complots) : voir CapacitesDe1A.

from cards.pack.fne.campaign import CapacitesDeCampagne


def _premier_complot(effect: 'Effect', message: 'Message2') -> bool:
    """Un complot principal PAR JOUEUR : seul le premier en jeu porte les
    capacites de campagne (voir CapacitesDeCampagne, `garde`)."""
    # ⚠ Par la CARTE, pas par la face : a la mise en place de campagne le
    # complot est deja retourne cote 1B, `effect.this` est la face 1A.
    complots = ComplotsRacket(effect)
    return bool(complots) and complots[0].card is effect.this.card


def GetAbilities() -> Sequence['Ability']:
    return [
        *CapacitesDe1A(),
        # Mode campagne (livret p. 9 et p. 13) : inerte hors campagne.
        *CapacitesDeCampagne("protection_racket", garde=_premier_complot),
    ]
