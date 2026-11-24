from . import *

# * Mr. Pointy — AMELIORATION (WEAPON), cout 1, [wild]. Unique. Restricted.
# Buffy gains retaliate 1 and her basic attacks gain piercing.
#
# CARTES DE REFERENCE
#  - `43009` Adamantium Lacing : `GiveKeywordToAttached(CardFinder(name=..), retaliate=1)` + `UnitAttackGainKeyword(CardFinder(name=..), piercing=True)`.
#  - `04012` Black Knight : `UnitAttackGainKeyword(.., is_basic_attack=True, piercing=True)` pour « basic attack(s) gain piercing ».
#  - `Restricted` : lu dans `desc` (fiche `mots-cles/restricted.md`), aucun module.
#
# TEXTE CONTRE CODE
#  « Buffy » -> nom propre : la face HEROS (alter-ego = Buffy Summers). « basic attacks » -> `is_basic_attack=True` : les attaques d'evenements n'ont PAS piercing.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name=NOM_BUFFY),
            retaliate=1,
        ),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name=NOM_BUFFY),
            is_basic_attack=True,
            piercing=True,
        ),
    ]
