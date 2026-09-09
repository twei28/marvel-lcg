from . import *

# The Power of the Bond — RESSOURCE [wild]. Max 2 per deck.
# Double the number of resources this card generates while paying for a
#   Venomized (black) card.
#
# CARTE DE REFERENCE
#  - `01062` The Power of Justice (pack core) : MEME TEXTE, un mot change
#    (« Justice (yellow) » -> « Venomized (black) »). Une seule ligne :
#    `DoubleResourcesThisGenerates(CardFinder(card_class=...))`.
#
# TEXTE CONTRE CODE
#  ⚠ Le sixieme aspect existe DANS `CARD_CLASS` (`card_player.py`) : on peut
#    donc l'ecrire tel quel, sans passer par `check_face_fn`. C'est cette
#    declaration, faite le 09/09/2026, qui rend cette carte tenable en une
#    ligne au lieu d'un predicat maison.
def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.DoubleResourcesThisGenerates(
            CardFinder(card_class=VENOMIZED)
        ),
    ]
