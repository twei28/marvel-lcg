from . import *
def GetAbilities() -> Sequence['Ability']:
    def place_limb(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceCountersInternal(1, 'limb', effect, maximum=8)
    def discard_for_damage(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        n = this.GetCounters('limb')
        this.DealDamage(effect.targets, n, effect)
    return [
        AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, "You", None, place_limb),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, discard_for_damage)
        .SetPlay().SetCostFunc(CostFunc.Discard("This")).SetTarget(Enemy, range=(1, 1)),
    ]
