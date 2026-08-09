from . import *
def GetAbilities() -> Sequence['Ability']:
    def study_the_tape(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        faces = []
        def collect(player: 'Player'):
            for face in player.discard_pile.Get():
                if IsAspectOrBasicEvent(face) or (face.paper.name == 'Photographic Reflexes'):
                    faces.append(face)
        Players.ForEachPlayer(effect, collect)
        if not faces:
            return
        def action(targets: Sequence['CardFace']):
            Faces.AddToHand(list(targets), initiator, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Add that card to your hand', action).SetTarget(faces, range=(1, 1)))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, study_the_tape).SetPlay().SetLabel()]
