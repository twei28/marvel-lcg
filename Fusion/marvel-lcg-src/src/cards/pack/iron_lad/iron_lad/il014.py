from . import *

# * Iron Lad's Helmet
# Hero Response: After Iron Lad uses a basic power, exhaust Iron Lad's
#   Helmet → return the bottom card of your discard pile to your hand.
#
# Modele du declencheur : ok001a The Art of War (okoye/okoye/ok001a.py),
# `AbilityFactory.AfterUnitUseBasicPower(..., "You", powers=["ATK", "THW"])`.

def GetAbilities() -> Sequence['Ability']:

    def helmet(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ReturnToHand(effect.targets, initiator, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.HeroResponse,
            "You",
            helmet,
            powers=["ATK", "THW"],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(from_where=["YourDiscardPileBottommost"]),
    ]
