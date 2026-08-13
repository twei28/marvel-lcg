from . import *

# Resistance Training

def GetAbilities() -> Sequence['Ability']:

    def resistance_training(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            resistance_training
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'training'))
        .SetTarget(
            finder=CardFinder(card_type=Event, card_class="Determination"),
            from_where=["YourDiscardPile"],
            range=(1, 1)
        ),
    ]
