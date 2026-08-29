from . import *

# * Vision AI
# Alter-Ego Action: Exhaust Vision AI → shuffle the top card of your
#   discard pile into your deck. Return the bottom card of your discard
#   pile to your hand.
#
# Modeles : magneto/49002.py (from_where=["YourDiscardPileTopmost"] +
# Faces.ShuffleAllTo) et gam/gamora/18008.py (from_where=
# ["YourDiscardPileBottommost"] + Faces.ReturnToHand), les deux cibles etant
# distinctes (SetTarget / SetTarget2).

def GetAbilities() -> Sequence['Ability']:

    def vision_ai(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)
        Faces.ReturnToHand(effect.targets2, initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            vision_ai
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(from_where=["YourDiscardPileTopmost"])
        .SetTarget2(from_where=["YourDiscardPileBottommost"]),
    ]
