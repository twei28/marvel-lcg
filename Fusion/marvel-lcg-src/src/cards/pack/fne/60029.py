from . import *
def GetAbilities() -> Sequence['Ability']:
    def plus_one(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        message.GainValue(1, effect)
    def minus_one(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Support)
        message.GainValue(-1, effect)
        Faces.ReadyAll([this], effect)
    finder = CardFinder2('MARTIAL ARTIST', Friend)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, finder, plus_one).SetTarget('Trigger').SetCostFunc(CostFunc.Exhaust('This')),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.Interrupt, finder, minus_one).SetTarget('Trigger')]
