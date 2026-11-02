from . import *

# Operation Hellfire Ascendant (2B). « Hero Action : Exhaust a CAPTIVE ally you control -> remove 2 energy counters from Sebastian Shaw. (Limit once
# per round per player.) If this stage is completed, the players lose the game. »
# Cartes de reference : dz026 / pt004 (`CostFunc.Exhaust("YourAlly")`), 31009-like `LimitOncePerRoundPerPlayer` (FAQ du livret p. 22 : une fois par
# round et PAR JOUEUR, meme si l'on a plusieurs captifs).


def GetAbilities() -> Sequence['Ability']:
    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        shaw = ShawVilain(effect)
        if shaw is not None:
            Faces.RemoveCountersOn([shaw], 2, ENERGIE, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, action)
        .SetCostFunc(CostFunc.Exhaust("YourAlly", trait=CAPTIF))
        .LimitOncePerRoundPerPlayer(),
    ]
