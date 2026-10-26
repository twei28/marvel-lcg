from cards.pack import *

# Helpers partages du set « Roz Nemesis » (jakxin, prefixe `rz`).
#
# ⚠ Les modules du set font `from . import *` : tout helper appele par une carte vit ICI, jamais dans le
# `__init__.py` du pack (NameError avale par le moteur, lecon hk005).

NOM_DARIO = "Dario Agger"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit, ou le joueur contre qui la carte rencontre agit."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def ADesSpecial(face: 'CardFace') -> bool:
    """La carte IMPRIME au moins une capacite « Special » (capacites DECLAREES, jamais `face.effect`)."""
    return bool(face.ability.Find(type=AbilityType.Special))
