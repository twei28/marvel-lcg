from . import *

# * Misty Knight

def GetAbilities() -> Sequence['Ability']:

    def misty_knight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()

        def chercher_bounty(targets: Sequence['CardFace']) -> None:
            face = Search.PlayerCard(effect, initiator,
                                     include_player_deck=True,
                                     include_discard_pile=True,
                                     may=True,
                                     name="Bounty")
            if face:
                initiator.GainCard(face, effect)

        def reduire_le_cout(targets: Sequence['CardFace']) -> None:
            # « la PROCHAINE amelioration Bounty jouee ce tour » : la reduction
            # vise une AUTRE carte que celle-ci, d'ou ReduceCostToPlayFaceWhen
            # et non ReduceCostToPlayThis.
            initiator.effect.RegisterTemp(
                AbilityFactory.ReduceCostToPlayFaceWhen(
                    CardFinder(name="Bounty"),
                    1,
                    "You",
                ),
                unregister_after_exec=True,
                until_turn_end=True,
            )

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Search your deck and discard pile for a copy of Bounty",
                chercher_bounty
            ).SetHasNoTargetEffect(),
            AbilityFactory.ForChoiceAbility(
                "Reduce the cost of the next Bounty you play this turn by 1",
                reduire_le_cout
            ).SetHasNoTargetEffect(),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            misty_knight
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
