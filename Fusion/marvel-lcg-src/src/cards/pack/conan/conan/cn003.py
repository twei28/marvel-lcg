from . import *

# Crush Your Enemies (x2) — evenement, cout 1* [physical]. ATTACK.
# [star] Discount 1 (KING).
# Hero Action (attack): Deal 3 damage to an enemy (4 damage instead if you are King Conan).
#
# CARTES DE REFERENCE
#  - `DiscountAbility(1, ["KING"])` : 60023 Know Your Enemy (Fear No Evil).
#  - attaque ciblee : rs006 Hyrkanian Fury (`SetPlay().SetLabel('attack').SetTarget(Enemy)`).
#
# TEXTE CONTRE CODE
#  « if you are King Conan » : `EstKingConan` = face heros cn001d en jeu.


def GetAbilities() -> Sequence['Ability']:

    def crush(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 4 if EstKingConan(JoueurDe(effect)) else 3, effect)

    return [
        DiscountAbility(1, ["KING"]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            crush,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
