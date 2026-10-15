from . import *

# Lazerfist (x2) — AMELIORATION, cout 3 [energie]. SUPERPOWER.
# Lyja gets +1 ATK.
# Hero Resource: Exhaust Lazerfist → generate a [energy] resource.
#
# Cartes de reference :
#  - **`sk002a`** (Hulkling, meme auteur) : `GiveKeywordToAttached(CardFinder(name=...), ...)`
#    pour un bonus qui ne vaut que pour une face NOMMEE ; **`sk013`** Excelsior :
#    `CanGenerateResources(...).SetCostFunc(CostFunc.Exhaust("This"))` (UNE seule
#    capacite de ressource par carte, RECETTES §4).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LYJA gets +1 ATK » : nom propre = la face HEROS seulement ; en alter ego
#    (Laura Green) aucun bonus (RECETTES §3, contre-cas dans l'autre forme).
#  - « HERO Resource » : AbilityType.HeroResource, utilisable en forme heros seulement.
#  - « generate a [energy] resource » : Resources("Y").
#  - Cout 3 [energie] : desc Cost 3 / RES Y (icone verifiee sur le scan).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(CardFinder(name="Lyja"), attack=1),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
