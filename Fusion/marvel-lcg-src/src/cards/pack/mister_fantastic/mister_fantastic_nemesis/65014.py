from . import *

# * Wizard — custom « DesignHacker » (sbire némésis de Mister Fantastic)
# Each hero gets -1 THW.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(card_type=Hero),
            thwart=-1,
        ),
    ]
