from cards.pack import *


def Cloak(effect: 'Effect', face: 'CardFace|None') -> None:
    """« Cloak <carte> » : pose une carte d'etat Cloaked sur la carte visee.

    Mot-cle maison du pack TMNT : « Cloak X » = X recoit une carte d'etat
    Cloaked (+2 au prochain pouvoir de base / a la prochaine activation, OU -2
    aux prochains degats, un seul effet, puis la carte part). Fiches :
    docs/reference/mots-cles/cloak.md et cloaked.md. Les trois appels du pack
    (tl015 x2, tl016) passent par ici ; `face` vaut None quand la cible n'existe
    plus (vilain absent) : rien a poser.
    """
    if face is None:
        return
    Faces.GiveStatus([face], "Cloaked", effect)
