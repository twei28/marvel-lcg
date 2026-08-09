from . import *
def GetAbilities() -> Sequence['Ability']:
    def remove_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, remove_this).SetCostFunc(CostFunc.Exhaust('YourIdentity')),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, remove_this).SetCost(Cost('BB'))]
