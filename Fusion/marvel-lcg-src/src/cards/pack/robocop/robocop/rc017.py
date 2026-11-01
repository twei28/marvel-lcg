from . import *

# Leg Holster : AMELIORATION (ITEM), cout 0, [physical]. Basic. Max 1 par joueur.
# Play under any player's control. Max 1 per player. You can control 1 additional WEAPON upgrade that has the restricted keyword.
#
# CARTE DE REFERENCE : `20021` Side Holster (officielle) : TEXTE IDENTIQUE, cout et ressource identiques ; le scan porte le sous-titre « Side Holster » (renommee par
#  l'auteur). Meme script (`CanPlayThisUpgradeCard("Players")` + `GiveKeywordToAttached("You", control_additional_restricted=..)`), recopie plutot que lie : la carte est
#  une carte du pack (classe Basic) avec son propre nom.
#
# TEXTE CONTRE CODE
#  « Play under ANY player's control » -> `"Players"`. « Max 1 per player » : `desc.MaxPerUnit`. « 1 ADDITIONAL WEAPON upgrade that has the restricted keyword » -> une arme
#    Restricted de plus (RoboCop en porte deux : Auto-9 et Gunarm). Chiffres : cout 0, +1 arme.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players",
        ),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder2("WEAPON", Upgrade),
        ),
    ]
