from . import *
def GetAbilities() -> Sequence['Ability']:
    def give_himself_tough(effect: 'Effect', message: 'Message.WhenInYourPlayTurn') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage([this], 1, effect)
        Faces.GiveStatus([this], "Tough", effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, give_himself_tough)
        .SetPlay().SetCostFunc(CostFunc.Exhaust("This")),
    ]
