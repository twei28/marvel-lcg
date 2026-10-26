from cards.pack import *

# Helpers partages du set « Ch'od Nemesis » (Phenexian et Mysteltainn, prefixe `co`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du pack (NameError avale, lecon hk005).


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


def Types(face: 'CardFace|None') -> set:
    """Types de ressource IMPRIMES (R, B, Y, G). Hors paiement, un wild n'est QUE « wild » : type « G » a part, jamais R, B ou Y
    (RR « Wild Resource », 26/10/2026) ; sans icone : vide."""
    res = getattr(face, "printed_resource", None) if face is not None else None
    if res is None:
        return set()
    return {c for c in ("R", "B", "Y", "G") if res.GetColor(c, convert_green_res=False) > 0}


def NombreDIcones(face: 'CardFace|None') -> int:
    """« the number of printed resources » : le nombre d'ICONES imprimees (une carte YY en compte deux)."""
    res = getattr(face, "printed_resource", None) if face is not None else None
    return int(res.val) if res is not None else 0
