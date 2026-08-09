from . import *

# Canine Urges — custom « Nugget » (obligation de Lockjaw)
# Give to the Lockjaw player. You may flip to alter-ego form. Choose:
# - Exhaust Lockjaw and Tuning Fork -> remove Canine Urges from the game.
# - Discard all TELEPORT events in your hand. If no events were discarded this
#   way, this card gains surge. Discard this obligation.


def GetAbilities() -> Sequence['Ability']:

    def canine_urges(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        fourchette = [
            x for x in Worlds.FindCardsOnField(effect, name="Tuning Fork", card_type=Upgrade)
            if x.GetControlByPlayer() == player
        ]

        def defausser_les_teleports(targets: Sequence['CardFace']) -> None:
            evenements = [
                x for x in player.hand_cards.GetAll()
                if Event.IsType(x) and x.HasTrait("TELEPORT")
            ]
            if evenements:
                Faces.DiscardAll(evenements, effect)
            else:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Lockjaw and Tuning Fork → remove Canine Urges from the game",
                lambda t: Faces.RemoveAllFromGame([this], effect),
                condition=(player.IsAlterEgo() and len(fourchette) > 0),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Exhaust(
                name="Tuning Fork",
                card_type=Upgrade,
                from_where=["YouControlCards"])),
            AbilityFactory.ForChoiceAbility(
                "Discard all TELEPORT events in your hand. Discard this obligation",
                defausser_les_teleports,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            canine_urges
        )
    ]
