from . import *

# * Excelsior — amelioration signature (15/16). KREE. SKRULL. WEAPON.
# Cout 3 [energy].
# Restricted. (Max 2 restricted cards per player.)
# While Excelsior is ready, Hulkling's basic attacks gain piercing.
# Resource: Exhaust Excelsior → generate a [energy] resource.
#
# Cartes de reference :
#  - **`41002b`** Psi-Katana : « Restricted. Psylocke ... her basic attacks
#    gain piercing. Hero Resource: Exhaust Psi-Katana → generate a [physical]
#    resource » — meme carte a la condition « ready » pres :
#    `UnitAttackGainKeyword(CardFinder(name=...), is_basic_attack=True,
#    piercing=True)`.
#  - `ab007` / `ma005` : `CanGenerateResources(Resource, Resources("Y"))
#    .SetCostFunc(CostFunc.Exhaust("This"))` (RECETTES §4).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Restricted » : base automatique lue dans desc.Restricted.
#  - « **While Excelsior is ready** » : condition relue A CHAQUE attaque ; en
#    l'inclinant pour payer, Hulkling perd le percant. C'est tout le dilemme
#    de la carte.
#  - « **Hulkling's** basic attacks » : la face heros, basic seulement.
#  - « **Resource** » (pas Hero Resource) : utilisable dans les deux formes.
#    Decision du 15/10/2026 : l'utiliser ne « depense » PAS une carte KREE /
#    SKRULL au sens de sk002a/b (seules les cartes defaussees de la main).
#  - UNE SEULE CanGenerateResources par carte (assert, RECETTES §4).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.UnitAttackGainKeyword(
            CardFinder(name="Hulkling", card_type=Hero),
            is_basic_attack=True,
            piercing=True,
            conditions=[lambda effect, message: effect.this.IsReady()],
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("Y"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
