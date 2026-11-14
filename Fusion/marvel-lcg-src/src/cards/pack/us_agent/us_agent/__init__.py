from cards.pack import *

# Helpers partages du set « U.S. Agent ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un
# NameError avale par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

NOM_BOUCLIER = "U.S. Agent's Shield"
NOM_HEROS = "U.S. Agent"
NOM_ALTER_EGO = "John Walker"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier :
    il leve un assert quand l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None
