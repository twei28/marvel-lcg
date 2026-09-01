from . import *

# * Loki — support signature. ASGARD. PERSONA. Cout 2, [energy].
# Alligator Loki gains the [[MYSTIC]] trait.
# While in hero form, Alligator Loki gets +1 THW.
# Alter-Ego Resource: Exhaust Loki → generate a [wild] resource.
#
# Cartes de reference :
#  - 10008 * Banner's Laboratory : support qui donne un bonus continu a
#    l'identite par `GiveKeywordToInPlayWhenApplyThis(CardFinder(name=...))`
#    et une « Alter-Ego Resource » par `CanGenerateResources(AbilityType
#    .AlterEgoResource, Resources(...)).SetCostFunc(CostFunc.Exhaust("This"))` ;
#  - ma006 Star Flight : `trait=` sur la meme famille de fabriques.
#
# ⚠ « Alligator Loki GAINS the trait » : les DEUX faces portent ce nom
# (al001a et al001b), le trait vaut donc en heros comme en alter-ego. Aucun
# filtre de type.
# ⚠ « WHILE IN HERO FORM, +1 THW » : la, `card_type=Hero` restreint a la face
# heros. L'alter-ego n'a pas de CTR, mais on ne compte pas dessus.
# ⚠ [wild] -> `Resources("G")`, la lettre du joker dans tout le depot.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_HEROS),
            trait="MYSTIC",
        ),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name=NOM_HEROS, card_type=Hero),
            thwart=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.AlterEgoResource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
