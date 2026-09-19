from cards.pack import *
from cards.pack.fne import PeutCouvrirLeCout, RetournerLAttachement


def CompteursDeVitesse(effect: 'Effect') -> int:
    """« speed counters on the main scheme »."""
    scheme = Worlds.FindMainScheme(effect)
    return scheme.GetCounters('speed') if scheme is not None else 0


def TrouverOutFrontOuAlongside(effect: 'Effect') -> 'Attachment|None':
    face = Worlds.FindCardOnField(effect, name="Out Front", card_type=Attachment)
    if face is None:
        face = Worlds.FindCardOnField(effect, name="Alongside", card_type=Attachment)
    return face


def PourChaqueCompteurDeVitesse(effect: 'Effect', joueur: 'Player', branches: Callable[[], Sequence['Ability']]) -> None:
    """Burning Rubber / Pedestrians : « For each speed counter on the main
    scheme, choose: ... » -> un choix par compteur (60083 Chain Lightning)."""
    for _ in range(CompteursDeVitesse(effect)):
        joueur.ChooseAbilities(effect, *branches())
