from . import *

# * Wiz-Kid (Takeshi Matsuya) : allie RECRUITED, cout 2, PV 3, THW 1*, ATK 1*.
# Wiz-Kid gets +1 THW for each side scheme in play.
#
# Carte de reference : 01059 Jessica Jones (`AbilityFactory.ThisGainKeywordForEachFaceInPlay(CardFinder(card_type=SchemeSide2), thwart=1)`).
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeywordForEachFaceInPlay(
            CardFinder(card_type=SchemeSide2),
            thwart=1,
        ),
    ]
