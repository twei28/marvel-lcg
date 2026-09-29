from . import *

# * Synth-Suit

def GetAbilities() -> Sequence['Ability']:

    def synth_suit(effect: 'Effect', message: 'Message.WhenEffectWouldResolve') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)


    return [
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Black Widow"),
            defense=1,
        ),
        # Errata RRG 1.8 (MC4DB, 29/09/2026) : « after you RESOLVE the ability »
        # (et non « trigger »), meme fabrique que Widowmaker 08001a.
        AbilityFactory.AfterPlayerResolveAbility(
            AbilityType.HeroResponse,
            "You",
            CardFinder2("PREPARATION"),
            synth_suit,
            control_by_you=True
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(name="Black Widow", canbe_ready=True),
    ]

