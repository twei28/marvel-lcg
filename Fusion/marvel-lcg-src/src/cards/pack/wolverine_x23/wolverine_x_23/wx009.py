from . import *

# Adamantium Lacing
# You get +2 hit points.
# Wolverine gains retaliate 1 and her basic attacks gain piercing.
#
# Copie d'Adamantium Lacing (43009). Les deux references a « Wolverine » sont
# bornees au controleur.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_HEROS, check_effect_fn=EstTonHeros),
            retaliate=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name=NOM_HEROS, check_effect_fn=EstTonHeros),
            piercing=True
        ),
    ]
