from cards.pack import *

# ===========================================================================
# Helpers partages du set « Texas Twister Nemesis » (Master Pandemonium).
#
# Le set nemesis ne frappe pas les points de vie : il frappe le TEMPO. Master
# Pandemonium taxe chaque activation (une ressource energie ou l'inclinaison
# de l'identite), Demonic Limbs le rend intouchable, et l'obligation tt020
# interdit de redresser l'identite. Or tout le kit du heros consiste
# precisement a se redresser et a rejouer ses pouvoirs de base.
# ===========================================================================

NOM_PANDEMONIUM = "Master Pandemonium"
NOM_MEMBRES = "Demonic Limbs"


def PandemoniumEnJeu(effect: 'Effect') -> 'CardFace|None':
    """Master Pandemonium sur le terrain, ou None."""
    return Worlds.FindCardOnField(effect, name=NOM_PANDEMONIUM, card_type=Minion)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()`, qui leve
    un assert quand la carte n'est accrochee a rien (leçon du pack yondu, 9
    appels directs corriges apres coup).
    """
    return getattr(face, "bind_face", None) if face is not None else None
