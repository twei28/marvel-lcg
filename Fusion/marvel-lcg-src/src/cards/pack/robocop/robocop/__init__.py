from cards.pack import *
# Helpers partages du set « RoboCop ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur
# (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
NOM_AUTO_9 = "Auto-9"
NOM_ALEX_MURPHY = "Alex Murphy"
TRAIT_WEAPON = "WEAPON"
ICONES_MANIGANCE = ("acceleration_icon", "amplify", "crisis", "hazard")


def PorteUneIcone(face: 'CardFace') -> bool:
    """« has an [acceleration], [amplify], [crisis] or [hazard] icon » : au moins une des quatre icones de manigance."""
    return any((getattr(face, nom, 0) or 0) > 0 for nom in ICONES_MANIGANCE)


def ArmeDuJoueur(face: 'CardFace', joueur: 'Player') -> bool:
    """« a WEAPON upgrade you control »."""
    return Upgrade.IsType(face) and face.HasTrait(TRAIT_WEAPON) and face.GetControlByPlayer() == joueur
