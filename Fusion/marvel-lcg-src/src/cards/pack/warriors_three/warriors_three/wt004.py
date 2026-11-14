from . import *


def GetAbilities() -> Sequence['Ability']:
    # « Inactive hero. Permanent. Setup. » : mis en jeu au Setup (desc.Setup). Il ne sert que tant que Hogun n'est PAS le heros actif.
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("B"),
            conditions=[inactif("Hogun")],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
