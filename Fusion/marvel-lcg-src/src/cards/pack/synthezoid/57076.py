from . import *
def GetAbilities() -> Sequence['Ability']:
    def phased_out(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        leader = Worlds.GetEnemyLeader(effect)
        if not leader:
            return
        attachments = [x for x in leader.GetAttachedAttachments() if ('Hero Response' in (x.paper.text or '')) or ('Hero Interrupt' in (x.paper.text or ''))]
        if attachments:
            def action(targets: Sequence['CardFace']):
                Faces.DiscardAll(list(targets), effect)
            initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard an attachment', action).SetTarget(attachments, range=(1, 1), not_move=True))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, phased_out).SetPlay().SetLabel()]
