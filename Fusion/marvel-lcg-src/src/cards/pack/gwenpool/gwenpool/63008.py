from . import *

# * Comicbook Panels — custom « ekAugust »
# Hero Resource: Exhaust Comicbook Panels -> generate a [wild] resource
# and ____.
# Hero Action: Exhaust Comicbook Panels and Unbelievable Gwenpool ->
# ____ and ____.
# Bulle : « Look at the top card of any deck. »

def GetAbilities() -> Sequence['Ability']:

    def et_un_blanc(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        ResolveBlank(effect)

    def deux_blancs(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        ResolveBlank(effect, 2)

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            ex_operation=et_un_blanc,
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            deux_blancs
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Exhaust(
            name="Unbelievable Gwenpool",
            card_type=Upgrade,
            from_where=["YouControlCards"])),
    ]
