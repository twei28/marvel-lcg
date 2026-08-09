from . import *

# Spark — custom « DesignHacker »
# Hero Resource: Exhaust Spark -> generate an [energy] resource for a FIRE
# card.
# Hero Action: Exhaust Spark -> place a flame counter on an enemy.

def GetAbilities() -> Sequence['Ability']:

    def spark(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.PlaceCountersOn(effect.targets, 1, 'flame', effect)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("Y"),
            CardFinder(trait="FIRE"),
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            spark
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
