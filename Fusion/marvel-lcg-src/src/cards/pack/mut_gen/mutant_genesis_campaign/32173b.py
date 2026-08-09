from . import *
def GetAbilities() -> Sequence['Ability']:
    def rescue_captives(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Environment)
        initiator = effect.GetInitiator()
        faces = list(this.GetPlacedCardArea().Get())
        if not faces:
            return
        def action(targets: Sequence['CardFace']):
            for face in targets:
                face.CastTo(Ally).PutIntoPlay(initiator, effect, under_control=True)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Put a facedown ally into play under your control', action).SetTarget(faces, range=(1, 1), not_move=True))
    def check_sentinel(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> bool:
        return message.trigger.HasTrait('SENTINEL')
    return [AbilityFactory.AfterUnitBeDefeated(AbilityType.Response, Minion, rescue_captives, conditions=[check_sentinel]).SetTarget('Trigger').SetCost(Cost('1')).AnyPlayerCanDoThis()]
