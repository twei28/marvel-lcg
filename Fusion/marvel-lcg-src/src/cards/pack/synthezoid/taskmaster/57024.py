from . import *
def GetAbilities() -> Sequence['Ability']:
    def reduce_damage(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)
    def check_attached(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return (message.trigger == effect.this.bind_face)
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Taskmaster', card_type=Minion), otherwise_attach_to='EnemyLeader'),
            AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, None, reduce_damage, conditions=[check_attached]),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCost(Cost('BR'))]
