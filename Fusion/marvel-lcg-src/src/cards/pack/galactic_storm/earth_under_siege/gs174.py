from . import *

# Andromeda — SBIRE (ensemble Attuma), unique. ATLANTIS. ELITE. SCH 1, ATK 2, PV 5.
# [star] While another ATLANTIS card is in play, Andromeda gains retaliate 2.
#
# Cartes de reference :
#  - « While another ATLANTIS card is in play, gains retaliate 2 » : `AbilityFactory.ThisGainKeyword`
#    avec `retaliate=2`, meme condition que gs170/gs171 Attuma (`UneAutreCarteAtlantisEstEnJeu`,
#    earth_under_siege/__init__.py).
#
# ⚠ Mots-pieges : « ANOTHER Atlantis card » exclut Andromeda elle-meme.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.ThisGainKeyword(
            UneAutreCarteAtlantisEstEnJeu, retaliate=2,
            change_on_event=OnEvent.CardInPlay(CardFinder(trait="ATLANTIS")),
        ),
    ]
