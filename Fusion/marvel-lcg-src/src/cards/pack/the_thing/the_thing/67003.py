from . import *

# * Alicia Masters — custom « DesignHacker »
# Alter-Ego Action: Exhaust Alicia Masters -> draw 2 cards.

def GetAbilities() -> Sequence['Ability']:

    def alicia_masters(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DrawUp(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            alicia_masters
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
