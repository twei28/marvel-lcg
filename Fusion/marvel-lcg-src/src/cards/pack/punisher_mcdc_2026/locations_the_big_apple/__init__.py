from ..commun import *

# Set Locations - The Big Apple (pack MC×DC 2026) : les 9 lieux de la grille 3x3 (cartes Environnement a trait LOCATION).
# Les capacites de lieu posent `conditions=[Ville.AuLieu]` : on n interagit qu avec le lieu qu on occupe (R3).


def JoueurDuPersonnage(face: 'CardFace') -> 'Player|None':
    """Le joueur dont ce personnage fait partie : le controleur d'un heros / allie, le joueur engage d'un sbire ; None pour un vilain.
    Sert a « les personnages DANS ce lieu » (Lower East Side, Hell's Kitchen)."""
    if Minion.IsType(face):
        return face.CastTo(Minion).engaged_player
    if Villain.IsType(face):
        return None
    return face.GetControlByPlayer()
