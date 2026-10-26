from . import *


def GetAbilities() -> Sequence['Ability']:
    # « Inactive hero. Permanent. Setup. » : mis en jeu au Setup (desc.Setup). Il ne sert que tant que Fandral n'est PAS le heros actif.
    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
            conditions=[inactif("Fandral")],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
