from . import *

# Execution — custom « DesignHacker » (traîtrise némésis de Mister Fantastic)
# When Revealed: Discard each Projection attachment in play. For each
# attachment discarded this way, each player must choose to either discard 2
# cards from their hand or take 2 indirect damage. If no Projection
# attachments were discarded this way, shuffle Execution back into the
# encounter deck and this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def execution(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        projections = Worlds.FindCardsOnField(
            effect,
            name="Projection",
            card_type=Attachment,
        )

        if not projections:
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)
            ThisCardGainSurge(effect)
            return

        nombre = len(projections)
        Faces.DiscardAll(projections, effect)

        for _ in range(nombre):
            for player in list(effect.world.players):
                if player.is_eliminated:
                    continue

                def degats(targets: Sequence['CardFace'], player=player) -> None:
                    player.GetIdentity().TakeIndirectDamage(this, 2, effect)

                player.ChooseAbilities(
                    effect,
                    AbilityFactory.ForChoiceAbility(
                        "Discard 2 cards from your hand",
                        lambda targets: None
                    ).SetCostFunc(CostFunc.Discard(
                        "YourHandCards",
                        range=(2, 2))),
                    AbilityFactory.ForChoiceAbility(
                        "Take 2 indirect damage",
                        degats
                    ),
                )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            execution
        ),
    ]
