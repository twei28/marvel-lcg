from cards.pack import *

# Helpers partages du set « Ch'od » (Phenexian et Mysteltainn, prefixe `co`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

NOM_CRREEE = "Cr'reee"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur l'avale). Modele : `batgirl/batgirl/__init__.py`."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    try:
        return effect.GetInitiator()
    except Exception:
        return None


def IdentiteDe(effect: 'Effect') -> 'CardFace|None':
    joueur = JoueurDeCetteCarte(effect)
    return joueur.GetIdentity() if joueur is not None else None


def Types(face: 'CardFace|None') -> set:
    """Types de ressource IMPRIMES sur une carte (R, B, Y, G). Hors paiement, un wild n'est QUE « wild » : il compte comme
    le type « G », jamais comme R, B ou Y (RR « Wild Resource », 26/10/2026) ; une carte sans icone rend l'ensemble vide."""
    res = getattr(face, "printed_resource", None) if face is not None else None
    if res is None:
        return set()
    return {c for c in ("R", "B", "Y", "G") if res.GetColor(c, convert_green_res=False) > 0}


def PlusUneTailleDeMain(effect: 'Effect', identite: 'CardFace|None') -> None:
    """« Ch'od gets +1 hand size until the end of the phase » (les cartes qui l'impriment se jouent en phase joueur)."""
    if identite is not None:
        identite.GainUntilPhaseEnd(effect, hand_size=1, end_phase="Player")
