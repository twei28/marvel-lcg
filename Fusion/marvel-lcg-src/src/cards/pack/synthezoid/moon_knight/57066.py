from . import *
def GetAbilities() -> Sequence['Ability']:
    def after_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        def discard():
            if this.IsInPlay():
                Faces.DiscardAll([this], effect)
        RunAt.AfterEventEnd(effect, message, discard)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Moon Knight', card_type=Minion), otherwise_attach_to='EnemyLeader'),
            AbilityFactory.UnitAttackGainKeyword('AttachedCharacter', piercing=True, ranged=True),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, None, after_attack, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)])]
