from . import *


def GetAbilities() -> Sequence['Ability']:
    # « Inactive hero. Permanent. Setup. » : mis en jeu au Setup (desc.Setup). Il ne sert que tant que Volstagg n'est PAS le heros actif.
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("R"),
            conditions=[inactif("Volstagg")],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
