from . import *

# Surprise Exam — obligation de Doreen Green
# Give to the Doreen Green player. You may flip to alter-ego form. Choose:
# - Exhaust Doreen Green and discard a card with a printed [mental] resource
#   from your hand -> remove Surprise Exam from the game.
# - Discard 2 SQUIRREL allies you control. If you cannot, discard 1 random card
#   from your hand. Discard this obligation.
#
# Gabarit d'obligation officiel, copie sur Ben's Cure (mf013).
# Equilibrage 28/08/2026 : 1 -> 2 ecureuils (defausser un seul ecureuil ne
# penalisait quasiment pas ce heros, qui en rappelle facilement).

def GetAbilities() -> Sequence['Ability']:

    def surprise_exam(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def penalite(targets: Sequence['CardFace']) -> None:
            ecureuils = EcureuilsControles(effect, player)
            if len(ecureuils) >= 2:
                choisis = player.AskChooseFaces(ecureuils, 2, 2, effect)
                Faces.DiscardAll(list(choisis) if choisis else ecureuils[:2], effect)
            else:
                # « If you cannot » : moins de 2 ecureuils -> la defausse
                # d'ecureuils n'a pas lieu du tout, on paie en carte au hasard.
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
                "Discard 2 SQUIRREL allies you control → discard this obligation",
                penalite
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            surprise_exam
        ),
    ]
