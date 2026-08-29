from . import *
def GetAbilities() -> Sequence['Ability']:
    def calling_in_favors(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        player = effect.GetInitiator()
        faces = Search.SearchForCards(effect, player, include_player_deck=True, card_type=Ally)
        def action(targets: Sequence['CardFace']):
            player.PlayCardsLikeInTurn(list(targets), effect, update_resources_cost=-2)
            player.player_deck.Shuffle(effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Choose an ally to play, reducing its cost by 2', action).SetTarget(faces, range=(0, 1)))
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, calling_in_favors)
        .SetPlay()
        .SetCostFunc(CostFunc.Counter(CardFinder(name='Alias Investigations'), 2, 'evidence'))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
