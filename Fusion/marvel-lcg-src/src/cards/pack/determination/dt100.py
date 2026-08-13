from . import *

# * Archangel

def GetAbilities() -> Sequence['Ability']:

    def archangel(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Faces.ReadyAll([message.trigger], effect)

    return [
        Reckless(),
        AliasReduitLeCout(),
        *AbilityFactory.GiveKeywordToAttached(
            "This",
            retaliate=2,
        ),
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            CardFinder(trait="AERIAL"),
            archangel
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
