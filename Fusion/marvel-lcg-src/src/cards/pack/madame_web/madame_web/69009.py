from . import *

# Foresight — custom « Kajislav »
# Hero Interrupt: When you reveal an encounter card, exhaust Madame Web ->
#   cancel the effects of that card and discard it.

def GetAbilities() -> Sequence['Ability']:

    def prescience(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.CancelAllEffectsAndDiscardIt(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(
            AbilityType.HeroInterrupt,
            "You",
            None,
            "All",
            prescience,
            from_encounter=True,
        ).SetPlay().SetLabel()
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
