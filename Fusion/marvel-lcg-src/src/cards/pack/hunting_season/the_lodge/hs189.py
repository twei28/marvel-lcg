from . import *

# hs189 Hatchet (Experience Cost 2)
# Restricted (donnees). Interrupt : quand tu fais une attaque de base, incline Hatchet -> +1 ATK.

def GetAbilities() -> Sequence['Ability']:

    def frapper(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainATKForThisAttack(1, effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(AbilityType.Interrupt, "You", frapper, is_basic_attack=True)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
