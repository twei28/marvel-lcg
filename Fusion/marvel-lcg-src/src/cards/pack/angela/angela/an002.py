from . import *

# * Sera — allie signature. HEVEN. Cout 3 / PV 2 / THW 1 / ATK 2*
# Angela gets +1 hand size.
#
# Carte de reference : 06007 * Asgard (pack rainy), qui porte exactement
# « You get +1 hand size » et le rend par
# `GiveKeywordToInPlayWhenApplyThis(Identity, control_by="You", hand_size=1)`.
#
# 05023 Endurance (`GiveKeywordToAttached`) ne conviendrait PAS : Sera est un
# ALLIE, elle ne s'attache a rien. Et `GiveKeywordToUnits` n'existe pas dans
# le moteur, malgre ce que son nom laisserait esperer.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            hand_size=1,
        ),
    ]
