from . import *

# Ben's Cure — custom « DesignHacker » (obligation de Mister Fantastic)
# Give to the Reed Richards player. You may flip to alter-ego form. Choose:
# - Exhaust Reed Richards and discard a card with a printed [mental] resource
#   -> remove Ben's Cure from the game.
# - Take 1 damage and place 1 threat on the main scheme -> discard this
#   obligation.

def GetAbilities() -> Sequence['Ability']:

    def bens_cure(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def penalite(targets: Sequence['CardFace']) -> None:
            this.DealDamage([player.GetIdentity()], 1, effect)
            this.PlaceThreatOnSchemes("MainScheme", 1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Reed Richards and discard a card with a printed [mental] resource → remove Ben's Cure from the game",
                lambda targets: Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Discard(
                # CORRECTIF 4/8/2026 : le parametre s'appelle `has_printed_res`.
                # Avec `has_res`, CardFinder levait un TypeError et l'obligation
                # plantait a CHAQUE revelation depuis la livraison du pack.
                Select.From(
                    CardFinder(has_printed_res="B"),
                    from_where=["YourHandCards"]
                ))),
            AbilityFactory.ForChoiceAbility(
                "Take 1 damage and place 1 threat on the main scheme → discard this obligation",
                penalite
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            bens_cure
        ),
    ]
