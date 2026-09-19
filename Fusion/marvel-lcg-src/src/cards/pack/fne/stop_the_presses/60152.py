from . import *

# Daily Bugle (environment)
# Alter-Ego Action: Exhaust a DAILY BUGLE support you control -> place 1
#   stamina counter on that support. (Any player can do this.)
# CostFunc.Exhaust(finder) puis `return_exhausted_cards` pour viser CE soutien.

def GetAbilities() -> Sequence['Ability']:
    inclinaison = CostFunc.Exhaust(CardFinder(trait="DAILY BUGLE", card_type=Support))

    def recharge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        for face in inclinaison.return_exhausted_cards:
            Faces.PlaceCountersOn([face], 1, 'stamina', effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, recharge)
            .SetName("Exhaust a Daily Bugle support you control: place 1 stamina counter on it")
            .SetCostFunc(inclinaison),
    ]
