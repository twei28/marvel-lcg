from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Taskmaster', card_type=Minion), otherwise_attach_to='EnemyLeader'),
            AbilityFactory.UnitAttackGainKeyword('AttachedCharacter', piercing=True),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCost(Cost('BR'))]
