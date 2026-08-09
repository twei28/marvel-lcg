from . import *
def GetAbilities() -> Sequence['Ability']:
    def echos_katana(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        value = GetPrintedCostValue(message.played_face)
        if (value <= 0):
            return
        this.DealDamage(effect.targets, value, effect, property=AttackProperty(piercing=True))
    def check_printed_cost(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> bool:
        return (GetPrintedCostValue(message.played_face) > 0)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterPlayerPlayedCard(AbilityType.HeroResponse, 'You', CardFinder(card_type=Event), echos_katana, conditions=[check_printed_cost]).SetCostFunc(CostFunc.Exhaust('This')).SetLabel('attack').SetTarget(Enemy)]
