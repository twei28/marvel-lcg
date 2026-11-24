from . import *

# Cryptic Threatening Message (manigance annexe de campagne). Victory 1.
# Treat the printed text box of each LOCATION support as if it were blank (except for TRAITS). The "Action" ability of Xavier's
# Institute environment cannot be triggered.
# When Defeated: The player who defeated this scheme searches the Charles Xavier ally from the set-aside area and put it into play.
#
# Cartes de reference : `AbilityFactory.WhenCardTreatAsIfBlank` (card.py/resources) ; `PlayersCannotTriggerAbility(which_player, which_ability,
# on_which_card=...)` (player.py).
# ⚠ « printed text box of each LOCATION support blank » : les soutiens de trait LOCATION perdent leur texte mais gardent leurs traits.
def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.PlayersCannotTriggerAbility(
            "AnyPlayer",
            AbilityType.Action,
            on_which_card=CardFinder(name="Xavier's Institute"),
        ),
        AbilitePotentialAlly("Charles Xavier"),
    ]
