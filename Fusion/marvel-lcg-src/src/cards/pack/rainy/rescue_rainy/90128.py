from . import *

# Burning Building

def GetAbilities() -> Sequence['Ability']:

    def incendie(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Environment)

        def action(player: 'Player') -> None:
            this.DealIndirectDamage(player.GetIdentity(), 1, effect)

        Players.ForEachPlayer(effect, action)

    return [
        AbilityFactory.WhenVillainPhaseBegin(
            AbilityType.ForcedResponse,
            incendie
        ),
        # « Exhaust your hero and spend a [physical] resource -> discard this ».
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCostFunc(CostFunc.Exhaust("YourHero"))
        .SetCostFunc(CostFunc.Spend(Cost("R"))),
    ]
