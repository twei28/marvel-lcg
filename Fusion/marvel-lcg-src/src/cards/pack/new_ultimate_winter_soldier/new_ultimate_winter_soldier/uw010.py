from . import *

# Adamantium Skeleton — amelioration signature. Cout 2, [physical].
# You get +4 hit points. Winter Soldier gets +1 ATK and his basic attacks gain piercing.
#
# Carte de reference : `35004` Adamantium Skeleton (Wolverine officiel) : TEXTE IDENTIQUE, au nom du heros pres
# (« Wolverine » -> « Winter Soldier »). Meme montage : `GiveKeywordToAttached("You", health=4)`, `UnitAttackGainKeyword(
# ..., is_basic_attack=True, piercing=True)`, `GiveKeywordToAttached(<nom>, attack=1)`.
#
# ⚠ La perforation vise `"You"` (l'identite du proprietaire de la carte) et non `CardFinder(name="Winter Soldier")`, qui designerait aussi le
# Winter Soldier OFFICIEL (54001a) d'un autre joueur ; comme 35004, `+1 ATK` reste lie au nom (la carte est attachee a SON identite).
#
# ⚠ « You get +4 HIT POINTS » vaut pour l'identite (les deux faces) ; « WINTER SOLDIER gets +1 ATK » n'en designe qu'une,
# la face heros (l'alter ego s'appelle Logan) : contre-cas dans l'autre forme (RECETTES-MOTEUR §3).


def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=4,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            "You",
            is_basic_attack=True,
            piercing=True,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Winter Soldier"),
            attack=1,
        ),
    ]
