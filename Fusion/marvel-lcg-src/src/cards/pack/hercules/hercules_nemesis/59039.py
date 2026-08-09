from . import *
def GetAbilities() -> Sequence['Ability']:
    def ares_axe(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        took = {'friendly': False}
        def on_damage(units):
            for unit in units:
                if Friend.IsType(unit):
                    took['friendly'] = True
        message.IfUnitTakeDamageFromThisAttack(on_damage, effect)
        def after_attack():
            if not took['friendly']:
                if this.IsInPlay():
                    Faces.DiscardAll([this], effect)
        RunAt.AfterEventEnd(effect, message, after_attack)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Ares', card_type=Minion), otherwise_attach_to=Villain),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, 'AttachedEnemy', ares_axe)]
