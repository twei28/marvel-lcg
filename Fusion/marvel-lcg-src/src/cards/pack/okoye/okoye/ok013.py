from . import *

# Midnight Angel Armor (2/2)
# Exemplaire physique 2 de 2, contenu identique a ok012 (voir ce fichier pour
# le detail du modele repris).


CIBLE = CardFinder(card_type=Friend, trait="DORA MILAJE")


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(CIBLE),
        *AbilityFactory.GiveKeywordToAttached(
            CIBLE,
            health=2,
            trait="AERIAL",
        ),
    ]
