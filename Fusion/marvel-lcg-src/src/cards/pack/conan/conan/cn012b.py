from . import *

# * The Cimmerian — verso KING. Permanent.
# Hero Interrupt: When you use one of King Conan's basic powers, remove X Crom
#   counters from here and exhaust The Cimmerian -> King Conan gets +X to that
#   power for this use.
#
# CARTES DE REFERENCE
#  - rs002 Conan (pack red_sonja) : `WhenUnitUseBasicPower(..., op)` et
#    `message.GainValue(X, effect)` sur le pouvoir en cours.
#  - X choisi par le joueur : `CostFunc.Counter("This", (1, N), 'crom')`
#    (DeclareNumber), relu par `return_remove_counter`.
#
# TEXTE CONTRE CODE
#  « King Conan's basic powers » : seulement la face heros cn001d (ATK, THW, DEF).
#  « remove X ... and exhaust » : deux couts, les deux payes.


def GetAbilities() -> Sequence['Ability']:

    def bonus(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        x = effect.cost_func.Get(CostFunc.Counter).return_remove_counter
        if x > 0:
            message.GainValue(x, effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            "YourIdentity",
            bonus,
            conditions=[lambda effect, message: message.trigger.paper.card_id == ID_ROI],
        ).SetCostFunc(CostFunc.Counter("This", (1, 99), 'crom'))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
