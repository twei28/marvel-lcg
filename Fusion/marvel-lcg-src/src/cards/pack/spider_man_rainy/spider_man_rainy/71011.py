from . import *

# Web-Shooters — custom « Rainy »
# Your hero gains the AERIAL trait.
# Hero Resource: Exhaust Web-Shooters -> generate a [wild] resource for a WEB
#   card.
# Hero Action: Exhaust Web-Shooters -> web an enemy.

def GetAbilities() -> Sequence['Ability']:

    def toile(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Weber(effect.targets, 1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            trait="AERIAL",
        ),

        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            for_card=CardFinder(traits=["WEB"]),
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            toile
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy),
    ]
