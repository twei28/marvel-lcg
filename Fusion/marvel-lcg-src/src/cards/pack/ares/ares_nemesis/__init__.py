from cards.pack import *

# ===========================================================================
# Set nemesis « Ares Nemesis » (Athena et sa cuirasse).
#
# ⚠ L'OBLIGATION `ar010` Ire of Athena N'EST PAS ICI : son bandeau imprime dit
# « ARES », pas « ... NEMESIS ». Son `set_name` est celui du set HEROS, son
# module vit donc dans `ares/ares/`. Piege bt019 / nt012 / yd013 / dr010 /
# bk017 / tt020 / br012 / tg011 / sn011 / bc012 / sf010 — douzieme fois.
#
# ⚠⚠ LES NOMS S'ECRIVENT SANS L'ETOILE D'UNICITE (`name.lstrip("* ")`,
# cards/paper.py). Aucune carte de ce set ne cherche par le nom de toute
# facon : « * Ares » est aussi `59036` (Hercules Nemesis).
# ===========================================================================

TRAIT_TACTIC: 'CardFace.TRAITS' = "TACTIC"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas."""
    return getattr(face, "bind_face", None) if face is not None else None


def JoueurALOrigine(effect: 'Effect', message: Any) -> 'Player|None':
    """Le joueur a l'origine d'un effet de degats, pour renvoyer les degats
    a son identite quand la source n'est pas un personnage (ar013).

    ⚠ `by_effect.GetInitiator()` leve un assert si l'initiateur n'est pas un
    joueur : on lit `initiator` avec un `getattr`, puis le controleur de la
    carte source, sans jamais appeler l'accesseur qui saute.
    """
    par_effet = getattr(message, "by_effect", None)
    initiateur = getattr(par_effet, "initiator", None)
    if EstJoueur(initiateur):
        return initiateur
    source = getattr(message, "source", None)
    if source is not None:
        controleur = source.GetControlByOrOwner()
        if EstJoueur(controleur):
            return controleur
    Unused(effect)
    return None
