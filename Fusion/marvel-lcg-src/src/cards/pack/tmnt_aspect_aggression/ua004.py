from . import *

# Attack Training — AMELIORATION 1 [physical], aspect Aggression (TMNT Reskins, Inkwire). TRAINING.
# Attach to a NINJA or MUTANIMAL ally. Max 1 TRAINING upgrade per ally.
# Attached ally gets +1 ATK and +2 hit points.
#
# MODIFIEE de `32043` Attack Training (« Attach to an X-MEN ally ») : un mot de regle differe, donc PAS
# d'`ability_link` (RECETTES-MOTEUR §11 point 7) : script copie de 32043, puis adapte.
#  ⚠ « NINJA OR MUTANIMAL » : `CardFinder(traits=[...])` est un OU (finder.py).
#  ⚠ « Max 1 TRAINING upgrade per ally » : regle native du selecteur d'amelioration
#    (`filter_training_upgrade_per_ally`, ability.py), lue sur le trait TRAINING de la carte, comme 32043.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(traits=["NINJA", "MUTANIMAL"], card_type=Ally)
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Ally,
            attack=1,
            health=2,
        ),
    ]
