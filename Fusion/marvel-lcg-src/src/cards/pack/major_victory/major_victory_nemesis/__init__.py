from cards.pack import *
# Helpers partages du set « Major Victory Nemesis ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
NOM_KORVAC = "Michael Korvac"
NOM_FUTURE = "Korvac's Future"


def FutureEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Korvac's Future, si elle est EN JEU (elle commence mise de cote : le set nemesis n'entre pas en jeu avant Korvac)."""
    for face in Worlds.FindCardsOnField(effect, card_type=Scheme2):
        if face.IsName(NOM_FUTURE):
            return face
    return None
