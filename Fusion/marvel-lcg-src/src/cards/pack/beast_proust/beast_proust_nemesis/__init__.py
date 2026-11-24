from cards.pack import *
# Helpers partages du set « Beast Proust Nemesis » (⚠ un helper du __init__ du PACK leve un NameError avale par le moteur : lecon hk005, tout vit ICI).
NOM_BLACK_BEAST = "Black Beast"


def CoutImprime(face: 'CardFace') -> int:
    """« the printed (resource) cost of this card » : `printed_cost.val` ; 0 pour une carte sans cout imprime."""
    cout = getattr(face, "printed_cost", None)
    return int(cout.val) if cout is not None else 0


def AmeliorationsTech(joueur: 'Player') -> List['CardFace']:
    """« a TECH upgrade you control »."""
    return [f for f in joueur.GetControlUpgrade() if f.HasTrait("TECH")]
