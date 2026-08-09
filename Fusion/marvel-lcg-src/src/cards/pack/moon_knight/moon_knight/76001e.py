from . import *

# * Jake Lockley (face alter-ego) — custom « DesignHacker »
# Just 'Cause — Reduce the cost of Justice (yellow) cards you play by 1.
# Couvre aussi Fight or Foil (bi-classe Moon Knight / Justice).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(card_class="Justice"),
            1,
            "You",
        ).SetName("Just 'Cause"),
        AbilityFactory.ReduceCostToPlayFaceWhen(
            CardFinder(name="Fight or Foil"),
            1,
            "You",
        ).SetName("Just 'Cause"),
    ]
