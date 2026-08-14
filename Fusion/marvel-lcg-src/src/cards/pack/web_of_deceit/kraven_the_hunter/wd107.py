from . import *

# Prey for Mercy

def GetAbilities() -> Sequence['Ability']:

    return [
        # « Threat cannot be removed from this scheme while Kraven the Hunter is
        # in play. » Tant que le chasseur tient la table, la proie ne s'echappe
        # pas : il faut l'abattre AVANT de defaire sa manigance.
        AbilityFactory.ThreatCannotBeRemovedFromWhile(
            "This",
            while_face_is_in_play=CardFinder(name="Kraven the Hunter", card_type=Minion),
        ),
    ]
