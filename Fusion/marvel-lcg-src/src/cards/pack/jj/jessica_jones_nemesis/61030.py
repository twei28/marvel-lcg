from . import *
def GetAbilities() -> Sequence['Ability']:
    def alter_ego_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        player = effect.GetInitiator()
        allies = player.GetControlCardsByType(ally=True)
        def remove_ally(targets: Sequence['CardFace']):
            Faces.RemoveAllFromGame(list(targets), effect)
            Faces.RemoveAllFromGame([this], effect)
        def confuse(_targets: Sequence['CardFace']):
            Faces.GiveStatus([player.GetIdentity()], "Confused", effect)
            Faces.DiscardAll([this], effect)
        options = [AbilityFactory.ForChoiceAbility('Confuse your identity → discard this card', confuse)]
        if allies:
            options = [AbilityFactory.ForChoiceAbility('Remove an ally you control from the game → remove this card from the game', remove_ally).SetTarget(allies, range=(1, 1))] + options
        player.ChooseAbilities(effect, *options)
    return [
        AbilityFactory.AdditionalCostToChangeForm("You", CostFunc.Discard(from_where=["YourHandCards"], range=(1, 1))),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, alter_ego_action),
    ]
