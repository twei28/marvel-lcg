from cards.pack import *


def Cloak(effect: 'Effect', face: 'CardFace|None') -> None:
    """« Cloak X » = poser la carte d'etat Cloaked sur X (fiches
    docs/reference/mots-cles/cloak.md et cloaked.md, decision utilisateur du
    15/10/2026). `face` vaut None quand la cible n'existe plus : rien a poser.
    Meme corps que `Cloak` de leonardo_nemesis : un helper vit dans le
    `__init__` de SON set."""
    if face is None:
        return
    Faces.GiveStatus([face], "Cloaked", effect)
