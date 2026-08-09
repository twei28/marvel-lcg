from cards.pack import *
def FindIonicPhysiology(effect: 'Effect', player: 'Player|None' = None) -> 'Upgrade|None':
    face = Worlds.FindCardOnField(effect, name='Ionic Physiology', card_type=Upgrade)
    if face and player and (face.GetControlByPlayer() != player):
        return None
    return face
def GetTuckedCards(effect: 'Effect', player: 'Player|None' = None) -> List['CardFace']:
    ip = FindIonicPhysiology(effect, player)
    if not ip:
        return []
    return list(ip.GetPlacedCardArea().Get())
def HasPrintedEnergy(face: 'CardFace') -> bool:
    return ('Y' in str(face.paper.desc.get('RES', '')))
def EnergyOverpaid(effect: 'Effect', printed_cost: int, cap: int) -> int:
    paid = effect.GetPaidResources()
    total = paid.val
    energy = paid.GetColor('Y', convert_green_res=False)
    over = max(0, (total - printed_cost))
    return min(cap, min(energy, over))
def TuckEnergyEventFromDiscard(effect: 'Effect', player: 'Player', *, include_resources: bool = False) -> None:
    ip = FindIonicPhysiology(effect, player)
    if not ip:
        return
    if (len(ip.GetPlacedCardArea().Get()) >= 3):
        return
    faces = []
    for face in player.discard_pile.Get():
        if not HasPrintedEnergy(face):
            continue
        if Event.IsType(face) or (include_resources and (face.paper.type == 'Resource')):
            faces.append(face)
    if not faces:
        return
    def action(targets: Sequence['CardFace']):
        for face in targets:
            ip.TuckCardUnderHere(face, effect)
    player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Tuck a card under Ionic Physiology', action).SetTarget(faces, range=(1, 1)))
