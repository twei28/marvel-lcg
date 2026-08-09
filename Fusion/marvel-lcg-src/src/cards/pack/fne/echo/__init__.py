from cards.pack import *
ASPECT_OR_BASIC_CLASSES = ('Aggression', 'Justice', 'Leadership', 'Protection', 'Basic', "'Pool")
def IsAspectOrBasicEvent(face: 'CardFace') -> bool:
    if not Event.IsType(face):
        return False
    return face.IsClass(*ASPECT_OR_BASIC_CLASSES)
def GetPrintedCostValue(face: 'CardFace') -> int:
    value = face.paper.desc.get('Cost', '')
    value = str(value).replace('*', '')
    try:
        cost = int(value)
    except ValueError:
        return 0
    return max(cost, 0)
