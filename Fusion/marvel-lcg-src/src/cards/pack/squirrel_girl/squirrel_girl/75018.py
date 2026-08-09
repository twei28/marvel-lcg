from . import *

# Surprise Exam — obligation de Doreen Green
# Give to the Doreen Green player. You may flip to alter-ego form. Choose:
# - Exhaust Doreen Green and discard a card with a printed [mental] resource
#   from your hand -> remove Surprise Exam from the game.
# - Discard 1 SQUIRREL ally you control. If you cannot, discard 1 random card
#   from your hand. Discard this obligation.
#
# Gabarit d'obligation officiel, copie sur Ben's Cure (65013).

def GetAbilities() -> Sequence['Ability']:

    def surprise_exam(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def penalite(targets: Sequence['CardFace']) -> None:
            ecureuils = EcureuilsControles(effect, player)
            if ecureuils:
                choisi = player.AskChooseFace(ecureuils, effect)
                Faces.DiscardAll([choisi] if choisi else ecureuils[:1], effect)
            else:
                player.DiscardRandomHandCards(1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Doreen Green and discard a card with a printed [mental] resource → remove Surprise Exam from the game",
                lambda targets: Faces.RemoveAllFromGame([this], effect),
                condition=player.IsAlterEgo(),
            ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
            .SetCostFunc(CostFunc.Discard(
                Select.From(
                    CardFinder(has_printed_res="B"),
                    from_where=["YourHandCards"]
                ))),
            AbilityFactory.ForChoiceAbility(
                "Discard 1 SQUIRREL ally you control → discard this obligation",
                penalite
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            surprise_exam
        ),
    ]
