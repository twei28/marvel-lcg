from . import *

# * Four Seasons' Room — LOCATION
# Alter-Ego Action: Exhaust Four Seasons' Room -> draw 1 card (2 instead if
#   you give a facedown boost card to the villain).
#
# Choix binaire du joueur entre "piocher 1" et "donner une carte boost face
# cachee au vilain -> piocher 2" : modele core/02035.py (Intimidation),
# `player.ChooseAbilities` + `Faces.GiveFacedownBoostCards(targets, 1,
# effect)` (game/operate/faces.py:447) pour la carte boost.


def GetAbilities() -> Sequence['Ability']:

    def four_seasons_room(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        def draw_one(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            initiator.DrawUp(1, effect)

        def give_boost_and_draw_two(targets: Sequence['CardFace']) -> None:
            Faces.GiveFacedownBoostCards(targets, 1, effect)
            initiator.DrawUp(2, effect)

        initiator.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Draw 1 card",
                draw_one,
            ),
            AbilityFactory.ForChoiceAbility(
                "Give the villain 1 facedown boost card -> draw 2 cards",
                give_boost_and_draw_two,
            ).SetTarget(Villain),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            four_seasons_room,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetName("Four Seasons' Room"),
    ]
