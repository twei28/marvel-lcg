from cards.pack import *

# Helpers partages du set « Predator Alt Nemesis » (Dutch Schaefer, Colonel Dillon, M134 Minigun, Get To The..., Chopper).
#
# ⚠ Les modules du set font `from . import *` : tout ce que les cartes appellent vit ICI (lecon hk005).

ID_CHOPPER = "pd026"
ID_DUTCH = "pd027"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def LeChopper(effect: 'Effect') -> 'CardFace|None':
    """« The Chopper side scheme » en jeu, ou None."""
    for face in Worlds.GetAllSideSchemes(effect):
        if face.paper.card_id == ID_CHOPPER:
            return face
    return None


def PoserDeLaMenaceSurLeChopper(effect: 'Effect', valeur: int) -> None:
    """« Place N threat on the Chopper side scheme » : sans Chopper en jeu, rien."""
    chopper = LeChopper(effect)
    if chopper is not None:
        effect.this.PlaceThreatOnSchemes([chopper], valeur, effect)
