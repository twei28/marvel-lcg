from . import *
def GetAbilities() -> Sequence['Ability']:
    def overkill_attack(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        def discard():
            if this.IsInPlay():
                Faces.DiscardAll([this], effect)
        RunAt.AfterEventEnd(effect, message, discard)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='She-Hulk', card_type=Leader)),
            AbilityFactory.UnitAttackGainKeyword('AttachedCharacter', overkill=True),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, None, overkill_attack, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)]),
            AbilityFactory.WhenCardBecomeBoost('This', RevealThisCard)]
