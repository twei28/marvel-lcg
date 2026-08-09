from cards.pack import *
SENSE_DECK_IDS = ('60002', '60003', '60004', '60005', '60006')
def SelectSenseTopCard(effect: 'Effect') -> Sequence['CardFace']:
    initiator = effect.GetInitiator()
    face = initiator.additional_deck.GetTop()
    if face:
        return [face]
    return []
def PlaySenseUpgradeFree(player: 'Player', by_effect: 'Effect', *, any_number: bool = False) -> None:
    faces = player.additional_deck.Get()
    if not faces:
        return
    def action(targets: Sequence['CardFace']):
        for face in targets:
            face.CastTo(Upgrade).PutIntoPlay(player, by_effect)
    rng = ((0, len(faces)) if any_number else (1, 1))
    player.ChooseAbilities(by_effect, AbilityFactory.ForChoiceAbility('Choose an upgrade from the Sense deck and play it, ignoring its resource cost', action).SetTarget(faces, range=rng, not_move=True, not_shuffle=True))
