from . import *

# Captain America's Shield — AMELIORATION, cout 1, [wild]. ITEM. Restricted.
# Major Victory gets +1 DEF and gains retaliate 1.
#
# CARTE DE REFERENCE : `03009` * Captain America's Shield (officiel) : meme texte, meme fabrique
# (`GiveKeywordToAttached(CardFinder(name=..), defense=1, retaliate=1)`), seul le nom du porteur change.
#
# TEXTE CONTRE CODE
#  « Restricted » -> lu par le moteur dans `desc` (`Restricted: "1"`), aucun module.
#  « Major Victory gets +1 DEF and gains retaliate 1 » -> porteur nomme « Major Victory » (la face HEROS ; l'alter-ego
#    Vance Astro n'a ni DEF ni retaliate imprimes). Chiffres : +1 DEF, retaliate 1.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Major Victory"),
            defense=1,
            retaliate=1,
        ),
    ]
