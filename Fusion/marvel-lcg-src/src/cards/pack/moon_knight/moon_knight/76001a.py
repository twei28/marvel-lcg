from . import *

# * Moon Knight (face héros) — custom « DesignHacker »
# A Good Offense — Reduce the cost of Aggression (red) cards you play by 1.
# La réduction couvre aussi Deck and Cover, imprimée « both a Moon Knight card
# and an Aggression card » (le moteur n'a qu'une classe par carte).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(card_class="Aggression"),
            1,
            "You",
        ).SetName("A Good Offense"),
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(name="Deck and Cover"),
            1,
            "You",
        ).SetName("A Good Offense"),
    ]
