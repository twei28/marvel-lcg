from . import *

# * Bedlam

def GetAbilities() -> Sequence['Ability']:

    # « Defeat Bedlam » : le moteur n'a pas de CostFunc de defaite, mais il a
    # Faces.DefeatUnits. Le cout passe donc par un Custom.
    def se_vaincre(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(Ally)
        Faces.DefeatUnits([this], None, effect)
        return True

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("YBR"),
        ).SetCostFunc(CostFunc.Custom(None, se_vaincre)),
    ]
