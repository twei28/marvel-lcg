from . import *

# Protection Training — AMELIORATION 1 [mental], aspect Protection (TMNT Reskins, Inkwire). TRAINING.
# Attach to a [[NINJA]] or [[MUTANIMAL]] ally. Max 1 [[Training]] upgrade per ally.
# Attached ally gets a +3 hit points.
#
# MODIFIEE de `32013` Protective Training (« Attach to an X-MEN ally ») : script propre.
#
# CARTE DE REFERENCE : `32013` : `CanPlayThisUpgradeCard(CardFinder2("X-MEN", Ally))` +
# `GiveKeywordToAttached(Ally, health=3)`. « Max 1 TRAINING upgrade per ally » est porte par le moteur
# (`ability.py`, `filter_training_upgrade_per_ally`, lu sur le trait TRAINING de la carte).
#
# TEXTE CONTRE CODE
#  ⚠ « NINJA OR MUTANIMAL » : l'un ou l'autre trait : `CardFinder(traits=[...])` (« # OR » dans finder.py).
#  ⚠ « ally » : un allie (pas une identite) : `card_type=Ally`.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally, traits=["NINJA", "MUTANIMAL"])
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            health=3,
        )
    ]
