from . import *

# Chosen One — AMELIORATION (TITLE), cout 2, [wild]. Linked (Becoming).
# Hero Action: Exhaust the Chosen One and spend 1 resource of any type → ready Buffy.
#
# CARTES DE REFERENCE
#  - `mv001a` : `.SetCost(Cost("1"))` pour « spend 1 resource of any type ». `CostFunc.Exhaust("This")` pour incliner la carte elle-meme.
#  - `Faces.ReadyAll([face], effect)` (an001a, 31009) pour redresser. `desc.Linked = "Becoming"` (carte absente, nom distinct).
#
# TEXTE CONTRE CODE
#  « Exhaust the Chosen One AND spend 1 resource » -> DEUX couts. « ready Buffy » -> le HEROS (face heros de l'identite), pas la carte.


def GetAbilities() -> Sequence['Ability']:

    def chosen_one(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        hero = effect.GetInitiator().GetHero()
        Faces.ReadyAll([hero], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chosen_one,
        ).SetCost(Cost("1"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
