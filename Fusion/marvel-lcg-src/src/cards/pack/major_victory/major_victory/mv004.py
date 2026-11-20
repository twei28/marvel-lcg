from . import *

# Containment Suit — AMELIORATION (ARMOR), cout 1, [energy].
# You get +2 hit points and your identity gains steady.
#
# CARTE DE REFERENCE : `01036` Mark V Armor (`GiveKeywordToAttached("You", health=..)`) ; `steady` est un parametre de la
# meme famille de fabriques (cf. `GiveKeywordToInPlayWhenApplyThis`).
#
# TEXTE CONTRE CODE
#  « You » et « your identity » = la MEME cible (l'identite du joueur, quelle que soit la forme) -> un seul appel.
#  Chiffres : +2 PV, steady 1.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
            steady=1,
        ),
    ]
