from cards.pack import *

# ⚠ Les helpers partages d'un set vivent dans le `__init__.py` DU SET, pas
# dans celui du pack (lecon hk005 : un helper defini ailleurs leve un
# NameError avale par le moteur).

# Les quatre classes SHINOBI (« both a Jennika card and a X card »), portees par
# `desc.Class` (ex. « Hero;Taijutsu »). Voir l'en-tete du pack.
CLASSES_SHINOBI = ["Bushido", "Ninjutsu", "Kuji-Kiri", "Taijutsu"]


# TODO-QUESTION Q2 (.planning/tmnt/jennika-questions.md) : seules les cartes portant une classe Shinobi
# imprimee comptent comme Shinobi (lecture retenue) ; ou toutes les cartes de Jennika ?
def CarteShinobi() -> 'CardFinder':
    """Le filtre « un Shinobi card » : une carte portant l'une des quatre classes."""
    return CardFinder(card_classes=CLASSES_SHINOBI)  # type: ignore


def Cloak(effect: 'Effect', face: 'CardFace|None') -> None:
    """« Cloak X » = poser la carte d'etat Cloaked sur X (fiches cloak.md / cloaked.md,
    decision utilisateur du 15/10/2026). Meme corps que `Cloak` du pack leonardo,
    recopie ici : un helper vit dans le `__init__` de SON set."""
    if face is None:
        return
    Faces.GiveStatus([face], "Cloaked", effect)
