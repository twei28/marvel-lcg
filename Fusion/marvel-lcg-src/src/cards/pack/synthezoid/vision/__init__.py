from cards.pack import *
def FindMassForm(effect: 'Effect') -> 'Attachment|None':
    for name in ('Dense', 'Intangible'):
        face = Worlds.FindCardOnField(effect, name=name, card_type=Attachment)
        if face:
            return face
    return None
def FlipMassForm(effect: 'Effect', to_name: 'str|None' = None) -> None:
    face = FindMassForm(effect)
    if not face:
        return
    if to_name and (face.paper.name == to_name):
        return
    face.card.Flip(effect)
