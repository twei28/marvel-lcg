from . import *

# * Founder of the Guardians — AMELIORATION (TITLE), cout 2, [mental]. Unique.
# Each identity gains the GUARDIAN trait.
# Each friendly GUARDIAN character gets +1 hit point.
#
# CARTES DE REFERENCE
#  - `56120` Government Contractor : `GiveKeywordToInPlayWhenApplyThis(Identity, trait=..)` pour « each identity gains the
#    X trait ».
#  - `sk113` : `CardFinder2("TRAIT", Type)` pour cibler « each ... TRAIT ... » avec `GiveKeywordToInPlayWhenApplyThis`.
#
# TEXTE CONTRE CODE
#  « each identity » -> `Identity` (les deux faces, de tous les joueurs). « each friendly GUARDIAN character » -> `Friend`
#    filtre sur le trait (identite ET allies, tous joueurs). Les identites devenant GUARDIAN par la premiere ligne, elles
#    recoivent aussi le +1 PV : c'est le texte (la carte se lit dans l'ordre).  Chiffre : +1 PV.


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            trait=TRAIT_GUARDIAN,
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder2(TRAIT_GUARDIAN, Friend),
            health=1,
        ),
    ]
