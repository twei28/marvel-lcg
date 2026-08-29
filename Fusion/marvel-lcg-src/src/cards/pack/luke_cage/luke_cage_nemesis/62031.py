from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_tough(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        target = message.target
        target.DiscardTough(effect, rule="All")
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Cottonmouth') | CardFinder(card_type=Villain)),
        AbilityFactory.WhenUnitWouldAttackUnit(AbilityType.ForcedInterrupt, "AttachedCharacter", None, discard_tough),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCostFunc(CostFunc.Spend(Cost('BB'))),
    ]
