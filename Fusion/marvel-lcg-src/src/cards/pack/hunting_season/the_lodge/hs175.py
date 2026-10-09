from . import *

# hs175 Steadfast (Experience Cost 3)
# Hero Interrupt : quand tu reveles une carte rencontre, depense une ressource [physical]
# -> annule ses effets « When Revealed ».

def GetAbilities() -> Sequence['Ability']:

    def annuler(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        message.CancelWhenRevealedEffect(effect)

    return [
        AbilityFactory.WhenPlayerRevealCard(AbilityType.HeroInterrupt, "You", None, "WhenRevealed", annuler)
        .SetPlay().SetCostFunc(CostFunc.Spend(Cost("R"))),
    ]
