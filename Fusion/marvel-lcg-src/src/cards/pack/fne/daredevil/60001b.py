from . import *
def GetAbilities() -> Sequence['Ability']:
    def flip_top_card(player: 'Player', by_effect: 'Effect'):
        if (player.additional_deck.GetSize() == 0):
            player.additional_deck.ShuffleWithDiscardPile(False, by_effect)
        faces = player.additional_deck.Get()
        if not faces:
            return
        Faces.FlipAllTo(faces[:-1], False, by_effect)
        face = faces[-1]
        face.FlipTo(by_effect, face_up=True)
    def move_to_sense_deck(effect: 'Effect', message: 'Message.WhenCardWouldMoveToArea') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        message.ChangeToArea(player.additional_deck, effect)
        def to_bottom():
            if (this.card.area == player.additional_deck):
                this.card.MoveToBottom(player.additional_deck, effect)
            flip_top_card(player, effect)
        RunAt.AfterEventEnd(effect, message, to_bottom)
    def with_sense_deck(effect: 'Effect', message: 'Message.WhenPlayerSelectHero') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)
        initiator = effect.GetInitiator()
        def register_effect(face: 'CardFace'):
            face.effect.Registers(AbilityFactory.WhenCardWouldMoveToArea(AbilityType.Temp0, 'This', move_to_sense_deck, conditions=[lambda effect, message: message.into_area.flags.is_discards]).NoOutOfPlayLimit())
        for face in initiator.set_aside_deck.Get():
            register_effect(face)
        this.effect.Registers(AbilityFactory.AfterCardsMoved(AbilityType.Temp0,
            initiator.set_aside_deck.Get(),
            lambda effect, message: flip_top_card(initiator, effect),
            by_shuffle=False))
        flip_top_card(initiator, effect)
    return [AbilityFactory.BeginGameWithSetAside([*SENSE_DECK_IDS], with_sense_deck)]
