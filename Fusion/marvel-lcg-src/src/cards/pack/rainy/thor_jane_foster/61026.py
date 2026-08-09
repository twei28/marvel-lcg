from . import *

# Chemotherapy — custom "Rainy" (obligation de Jane Foster)
# Give to the Jane Foster player. Flip to alter-ego form. Choose:
# - Exhaust Jane Foster and Medical Clinic -> remove Chemotherapy from the game.
# - Choose to either discard 2 cards or take 2 damage. Discard this obligation.

def GetAbilities() -> Sequence['Ability']:

    def chemotherapy(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def penalty_then_discard(targets: Sequence['CardFace']) -> None:
            def take_2_damage(t: Sequence['CardFace']) -> None:
                this.DealDamage([player.GetIdentity()], 2, effect)

            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 2 cards",
                    lambda t: None
                ).SetCostFunc(CostFunc.Discard(
                    "YourHandCards",
                    range=(2, 2))),
                AbilityFactory.ForChoiceAbility(
                    "Take 2 damage",
                    take_2_damage
                )
            )
            Faces.DiscardAll([this], effect)

        clinic = [x for x in Worlds.FindCardsOnField(effect, name="Medical Clinic", card_type=Support)
                  if x.GetControlBy() == player]

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Jane Foster and Medical Clinic → remove Chemotherapy from the game",
                lambda t: Faces.RemoveAllFromGame([this], effect),
                condition=(player.IsAlterEgo() and len(clinic) > 0),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Exhaust(
                name="Medical Clinic",
                card_type=Support,
                from_where=["YouControlCards"])),
            AbilityFactory.ForChoiceAbility(
                "Discard 2 cards or take 2 damage. Discard this obligation",
                penalty_then_discard
            )
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            chemotherapy
        )
    ]
