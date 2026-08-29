from . import *
def GetAbilities() -> Sequence['Ability']:
    def suggestion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this)
        player = effect.GetInitiator()
        faces = [f for f in player.hand_cards.Get() if HasResourceIcon.IsType(f) and getattr(f.printed_resource, 'r', False)]
        def play_card(targets: Sequence['CardFace']):
            player.PlayCardsLikeInTurn(list(targets), effect)
        def add_threat(_targets: Sequence['CardFace']):
            main_scheme = Worlds.FindMainScheme(effect)
            if main_scheme:
                main_scheme.PlaceThreatInternal(2, effect)
        if faces:
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility('Play a card with a printed physical resource icon', play_card).SetTarget(faces, range=(1, 1)),
                AbilityFactory.ForChoiceAbility('Add 2 threat to the main scheme', add_threat),
            )
        else:
            add_threat([])
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.ForcedAction, suggestion)
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'pheromone')),
    ]
