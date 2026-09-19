from cards.pack import *


def SoutiensDailyBugle(effect: 'Effect', joueur: 'Player|None'=None) -> List['CardFace']:
    """Les soutiens DAILY BUGLE en jeu (sous le controle de `joueur` si donne)."""
    faces = Worlds.FindCardsOnField(effect, trait="DAILY BUGLE", card_type=Support)
    if joueur is not None:
        faces = [f for f in faces if f.GetControlByPlayer() is joueur]
    return list(faces)


def RetirerUneEndurance(face: 'CardFace', effect: 'Effect') -> None:
    Faces.RemoveCountersOn([face], 1, 'stamina', effect)


def CoutDeReporter() -> Sequence['CostFunc.Base']:
    """« Exhaust <nom> and remove 1 stamina counter from him » : deux couts
    (60105 Fight., meme patron)."""
    return [CostFunc.Exhaust("This"), CostFunc.Counter("This", 1, 'stamina')]
