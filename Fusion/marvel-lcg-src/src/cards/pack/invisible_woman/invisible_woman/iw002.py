from . import *


def GetAbilities() -> Sequence['Ability']:

    def mister_fantastic(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Remove 1 threat from each scheme",
                lambda targets: this.RemoveThreatFromSchemes(targets, 1, effect),
            ).SetTarget(Scheme2, range=(1, "All")),
            AbilityFactory.ForChoiceAbility(
                "Add the top card of your discard pile to your hand",
                lambda targets: Faces.MoveAllTo(targets, player.hand_cards, effect),
            ).SetTarget(from_where=["YourDiscardPileTop"], range=(0, 1)),
        )

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            mister_fantastic,
        ).SetName("Brilliant"),
    ]
