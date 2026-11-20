from . import *

# * Captain Marvel (MONICA RAMBEAU) — ALLIE de campagne (Identity-Specific / Campaign, n° 228). Cout 3.
# THW 2 / ATK 2, 3 PV. AERIAL.
# Honorary.
# Resource: Discard Captain Marvel -> generate [energy][energy] resources.
#
# Cartes de reference :
#  - **`core/iron_man/01033`** Pepper Potts et **`falcon/falcon/53006`** Falcon's Flock :
#    `AbilityFactory.CanGenerateResources(AbilityType.Resource, ...)`, la fabrique native des allies
#    « Resource: ... -> generate ... resources ».
#  - cout « Discard Captain Marvel » : `CostFunc.Discard("This")` (meme cout que de nombreuses allies
#    « Resource », ex. `01033`).


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("YY"),
        ).SetCostFunc(CostFunc.Discard("This")),
    ]
