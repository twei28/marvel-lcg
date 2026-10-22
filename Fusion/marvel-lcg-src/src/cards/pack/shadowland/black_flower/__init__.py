from cards.pack.shadowland import *

# ===========================================================================
# Helpers du set BLACK FLOWER (Shadowland, Heart of Shadow) : la CREEPING CORRUPTION.
# Chaque joueur a SA Creeping Corruption (sl072a, qui se retourne en sl072b, trait OVERPOWERING). Les cartes parlent de « votre Creeping Corruption » :
# on la lit toujours par JOUEUR, jamais par nom (une partie a deux heros en met deux en jeu). Le compteur est `corruption` (card_face.py).
# ===========================================================================

CREEPING_CORRUPTION = ["sl072a", "sl072b"]
SEUIL_CORRUPTION = 5


def CreepingCorruptionDe(joueur: 'Player') -> 'CardFace|None':
    """La Creeping Corruption (face visible, a ou b) controlee par ce joueur, ou None s'il n'en a pas en jeu."""
    for face in joueur.GetControlUpgrade():
        if str(face.paper.card_id) in CREEPING_CORRUPTION:
            return face
    return None


def PeutPoserCorruption(joueur: 'Player') -> bool:
    return CreepingCorruptionDe(joueur) is not None


def PoserCorruption(effect: 'Effect', joueur: 'Player', nombre: int=1) -> bool:
    """« Place N corruption counter(s) on your Creeping Corruption ». Rend True si les compteurs ont ete poses (faux sans Creeping Corruption en jeu)."""
    cc = CreepingCorruptionDe(joueur)
    if cc is None:
        return False
    Faces.PlaceCountersOn([cc], nombre, 'corruption', effect)
    return True


def CorruptionOverpowering(joueur: 'Player') -> bool:
    """« If your Creeping Corruption has the OVERPOWERING trait » : lu sur la face COURANTE (le trait n'est imprime que sur sl072b). Faux sans Creeping Corruption."""
    cc = CreepingCorruptionDe(joueur)
    return cc is not None and cc.HasTrait("OVERPOWERING")
