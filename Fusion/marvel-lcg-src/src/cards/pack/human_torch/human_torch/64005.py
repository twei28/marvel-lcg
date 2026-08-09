from . import *

# Internal Combustion — custom « DesignHacker »
# Hero Action: Remove 3 flame counters from an enemy and discard Internal
# Combustion -> draw 3 cards.

def GetAbilities() -> Sequence['Ability']:

    def internal_combustion(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.RemoveCountersOn(effect.targets, 3, 'flame', effect)

        initiator = effect.GetInitiator()
        initiator.DrawUp(3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            internal_combustion
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(CardFinder(card_type=Enemy, has_counter='flame')),
    ]
