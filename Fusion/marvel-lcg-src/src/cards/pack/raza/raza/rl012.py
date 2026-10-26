from . import *
def GetAbilities() -> Sequence['Ability']:
    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Upgrade),
            control_by="You",
            treat_as_blank=True,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            retirer,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
