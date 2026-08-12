from . import *

# Fantasti-Flare — custom « DesignHacker »
# Uses (4 flare counters).
# Action: Exhaust Fantasti-Flare and remove one flare counter from it ->
# choose a player. Reduce the cost of the next ally that player plays this
# phase by 1.

def GetAbilities() -> Sequence['Ability']:

    def fantasti_flare(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        for target in effect.targets:
            player = target.GetControlByPlayer()
            if player is None:
                continue
            Worlds.UpdateNextCardPlayCost(
                player,
                -1,
                effect,
                finder=CardFinder(card_type=Ally),
                in_this="Phase",
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            fantasti_flare
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'flare'))
        .SetTarget("Players"),
    ]
