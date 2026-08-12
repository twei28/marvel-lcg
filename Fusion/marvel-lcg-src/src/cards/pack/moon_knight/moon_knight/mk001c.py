from . import *

# * Mr. Knight (face héros) — custom « DesignHacker »
# The Best Defense — Reduce the cost of Protection (green) cards you play by 1.
# Couvre aussi Gear Up (bi-classe Moon Knight / Protection).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(card_class="Protection"),
            1,
            "You",
        ).SetName("The Best Defense"),
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(name="Gear Up"),
            1,
            "You",
        ).SetName("The Best Defense"),
    ]
