from . import *
def GetAbilities() -> Sequence['Ability']:
    def system_shock(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, system_shock).SetCost(Cost('B')).CanWorkOnlyInHand()]
