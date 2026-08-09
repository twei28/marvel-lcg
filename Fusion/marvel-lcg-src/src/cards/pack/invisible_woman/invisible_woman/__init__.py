from cards.pack import *


def IsInvisibleForm(face: 'CardFace') -> bool:
    return Hero.IsType(face) and face.IsName("Invisible Woman") and face.HasTrait("INVISIBLE")


def IsPsionicForm(face: 'CardFace') -> bool:
    return Hero.IsType(face) and face.IsName("Invisible Woman") and face.HasTrait("PSIONIC")


def ChangeToInvisibleForm(player: 'Player', effect: 'Effect') -> None:
    player.GetIdentity().ChangeToForm(CardFinder2("INVISIBLE", Hero), effect)


def ChangeToPsionicForm(player: 'Player', effect: 'Effect') -> None:
    player.GetIdentity().ChangeToForm(CardFinder2("PSIONIC", Hero), effect)
