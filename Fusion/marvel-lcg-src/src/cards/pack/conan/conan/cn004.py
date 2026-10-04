from . import *

# Reaper's Cleave (x2) — evenement, cout 1* [mental]. THWART.
# [star] Discount 1 (KING).
# Hero Action (thwart): Remove 2 threat from a scheme (3 threat instead if you are King Conan).
#
# CARTES DE REFERENCE
#  - `DiscountAbility(1, ["KING"])` : 60023 Know Your Enemy (Fear No Evil).
#  - contre cible : 60023 (`SetLabel('thwart')`, cible `Scheme2`).


def GetAbilities() -> Sequence['Ability']:

    def cleave(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        this.RemoveThreatFromSchemes(effect.targets, 3 if EstKingConan(JoueurDe(effect)) else 2, effect)

    return [
        DiscountAbility(1, ["KING"]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cleave,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
