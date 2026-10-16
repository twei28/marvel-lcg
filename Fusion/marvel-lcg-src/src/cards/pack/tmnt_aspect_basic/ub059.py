from . import *

# Weapon Harness — AMELIORATION 0 [physical], aspect Basic (MC Custom Content, Inkwire). ITEM.
# Max 1 per player. Play only if your identity has the [[NINJA]] trait.
# You may control 2 additional [[WEAPON]] upgrades that have the restricted keyword.
#
# MODIFIEE de 20021 Side Holster : « Play under any player's control » SUPPRIME (elle se joue chez soi),
# « Play only if your identity has the NINJA trait » AJOUTE, 1 -> 2 armes Restricted supplementaires.
# Script copie de 20021 ; le « 2 » passe par DEUX `GiveKeywordToAttached(control_additional_restricted=...)`
# si la fabrique ne compte pas (voir le cas `[ub] ub059`, qui pose TROIS armes Restricted).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
        ).SetPlay(only_if_your_identity_has_trait="NINJA"),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder2("WEAPON", Upgrade),
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder2("WEAPON", Upgrade),
        ),
    ]
