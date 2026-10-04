from . import *

# Savage Sword — evenement, cout 4* [wild]. ATTACK. THWART.
# [star] Discount 1 (KING).
# Hero Action (attack/thwart): Exhaust your hero -> deal damage to an enemy or
#   remove threat from a scheme equal to the total of your hero's THW, ATK and
#   DEF values.
#
# CARTES DE REFERENCE
#  - « Exhaust your hero -> » : `SetCostFunc(CostFunc.Exhaust("YourIdentity"))`
#    (recette §3, 60122-60125).
#  - choix degats/menace : `ChoisirDegatsOuMenace` (modele 44043).
#
# TEXTE CONTRE CODE
#  « the total of your hero's THW, ATK and DEF values » : valeurs COURANTES,
#    lues a la resolution (apres l'inclinaison, qui ne les change pas).


def GetAbilities() -> Sequence['Ability']:

    def savage_sword(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        joueur = JoueurDe(effect)
        if joueur is None:
            return
        heros = joueur.GetIdentity()
        total = 0
        if isinstance(heros, CanThwart):
            total += heros.thwart
        if isinstance(heros, CanAttack):
            total += heros.attack
        if isinstance(heros, CanDefense):
            total += heros.defense
        ChoisirDegatsOuMenace(joueur, this, effect, total, total)

    return [
        DiscountAbility(1, ["KING"]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            savage_sword,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
