from . import *

# Splinter Dojo Training — AMELIORATION Leadership (TMNT Reskins, Inkwire), cout 1, [physical]. TRAINING.
# Attach to a [[NINJA]] or [[MUTANIMAL]] ally. Max 1 [[TRAINING]] upgrade per ally.
# Attached ally gets +1 THW, +1 ATK, and +1 hit point.
#
# MODIFIEE (reskin de `33015` Danger Room Training) : « an [[X-MEN]] ally » -> « a [[NINJA]] or
# [[MUTANIMAL]] ally » ; ressource [mental] -> [physical] (poing rouge, compare a `ul012` Inspired =
# `01074` RES R). Script propre copie de 33015.
#  « Max 1 TRAINING upgrade per ally » : regle generique du moteur (`ability.py`, « 32013 »).
#
# TEXTE CONTRE CODE
#  ⚠ « NINJA OR MUTANIMAL » : l'un des deux traits suffit.
#  ⚠ « MUTANIMAL » (singulier) : Old Hob (`ul019`) imprime « MUTANIMALS » (pluriel) et n'est donc PAS
#    accepte tant que la question Q-UL-4 n'est pas tranchee (fichier des questions ul).
#  ⚠ « an ally » : n'importe quel allie en jeu (le texte ne dit pas « you control »).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder2("NINJA", Ally) | CardFinder2("MUTANIMAL", Ally)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            thwart=1,
            attack=1,
            health=1,
        ),
    ]
