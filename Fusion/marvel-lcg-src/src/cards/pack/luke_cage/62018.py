from . import *
def GetAbilities() -> Sequence['Ability']:
    def defensive_formation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        for target in effect.targets:
            Faces.GiveStatus([target], "Tough", effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, defensive_formation)
        .SetPlay()
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'block'))
        .SetTarget(CardFinder(card_type=Ally, trait='DEFENDER'), range=(1, 1)),
    ]
