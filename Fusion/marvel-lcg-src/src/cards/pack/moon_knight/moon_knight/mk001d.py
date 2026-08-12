from . import *

# * Steven Grant (face alter-ego) — custom « DesignHacker »
# CEO — Reduce the cost of Leadership (blue) cards you play by 1.
# Couvre aussi Where'd He Go? (bi-classe Moon Knight / Leadership).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(card_class="Leadership"),
            1,
            "You",
        ).SetName("CEO"),
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(name="Where'd He Go?"),
            1,
            "You",
        ).SetName("CEO"),
    ]
