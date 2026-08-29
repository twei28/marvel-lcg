from . import *

# * Iron Lad's Boots
# Iron Lad gains AERIAL.
# Hero Response: After playing an event, exhaust Iron Lad's Boots → return
#   the bottom card of your discard pile to your hand.
#
# Trait accorde sans cible attachee ("You") : modele ag009 Physical Training
# (agent_13/agent_13/ag009.py) et ok012/ok013 Midnight Angel Armor (Okoye),
# `*AbilityFactory.GiveKeywordToAttached("You", trait="AERIAL")`.
# Declencheur generique "apres avoir joue un evenement" :
# `AbilityFactory.AfterPlayerPlayedCard(..., "You", CardFinder(card_type=
# Event), ...)`, signature generale (game/ability/factory/play.py).

def GetAbilities() -> Sequence['Ability']:

    def boots(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ReturnToHand(effect.targets, initiator, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            trait="AERIAL",
        ),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.HeroResponse,
            "You",
            CardFinder(card_type=Event),
            boots,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(from_where=["YourDiscardPileBottommost"]),
    ]
