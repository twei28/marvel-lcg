from . import *

# * Mister Fantastic (Reed Richards) — ALLIE FANTASTIC FOUR, BASIC. Cout 3, THW 1★, ATK 1★, 4 PV.
# Resource: Exhaust Mister Fantastic and deal 1 damage to him → generate a [mental] resource.
#
# Cartes de reference :
#  - **`sk013`** Excelsior (meme coffret) / **`ab007`** : `CanGenerateResources(Resource,
#    Resources("B")).SetCostFunc(CostFunc.Exhaust("This"))` — UNE seule capacite de
#    ressource par carte (RECETTES §4).
#  - **`22012`** Wraith (Zak-Del) : `.SetCostFunc(CostFunc.Exhaust("This"))
#    .SetCostFunc(CostFunc.DealDamage(1, "This"))` — le meme couple de couts sur un allie.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Exhaust Mister Fantastic AND deal 1 damage to him » : DEUX couts, aucun oublie
#    (PROCESSUS-CARTE, mot-piege « and remove »).
#  - « Resource » (pas Hero Resource) : utilisable dans les deux formes.
#  - [mental] : Resources("B"), icone verifiee sur le scan (carte du meme pack).
#  - THW 1★ / ATK 1★ : degats consecutifs (desc « 1* »).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("B"),
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
