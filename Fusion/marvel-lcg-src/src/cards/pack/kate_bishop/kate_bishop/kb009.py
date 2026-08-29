from . import *

# Lucky — GOOD BOY
# Alter-Ego Action: Exhaust Lucky -> heal 2 damage from Kate Bishop and place
#   1 arrow counter on Kate's Bow.


def GetAbilities() -> Sequence['Ability']:

    def lucky(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        this.HealthUnits([initiator.GetIdentity()], 2, effect)
        PlacerCompteursFlecheSurArc(effect, 1)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            lucky,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
