from . import *
def GetAbilities() -> Sequence['Ability']:
    def target_lock(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        leader = Worlds.FindCardOnField(effect, name='Iron Man', card_type=Leader)
        enemy = Worlds.GetEnemyLeader(effect)
        if leader and enemy and (leader != enemy):
            leader.CastTo(Enemy).BasicAttack([enemy], effect)
        if effect.GetPaidResources().HasColor('B'):
            target = enemy or leader
            if target:
                attachments = [x for x in target.GetAttachedAttachments() if ('Hero Response' in (x.paper.text or '')) or ('Hero Interrupt' in (x.paper.text or ''))]
                if attachments:
                    initiator = effect.GetInitiator()
                    def action(targets: Sequence['CardFace']):
                        Faces.DiscardAll(list(targets), effect)
                    initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard an attachment', action).SetTarget(attachments, range=(1, 1), not_move=True))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, target_lock).SetPlay().SetLabel()]
