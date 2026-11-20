from . import *

# Slayer Strike — EVENEMENT (ATTACK), cout 0, [energy]. x2.
# Hero Action (attack): Discard X cards from your hand → deal 4 damage to X enemies.
#
# CARTES DE REFERENCE
#  - `03006` Shield Toss (Captain America) : meme texte, sans le retour du bouclier. `SetCostFunc(CostFunc.Discard("YourHandCards",
#    range=(0, "All")))` + `SetTarget(Enemy, range=(1, "All"))` + `effect.targets[:X]`, X = cartes reellement defaussees.
#
# TEXTE CONTRE CODE
#  « X enemies » -> X ennemis DISTINCTS, X = nombre de cartes defaussees en cout (pas la taille de la main). Les cibles en trop
#    sont ignorees (tranche `[:X]`). « 4 damage to X enemies » -> 4 degats a CHACUN. « from your hand » -> `YourHandCards`.
#  Chiffres : 4 degats, cout 0.


def GetAbilities() -> Sequence['Ability']:

    def slayer_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        nombre_defausse = len(effect.cost_func.Get(CostFunc.Discard).return_discarded_cards)
        this.DealDamage(effect.targets[:nombre_defausse], 4, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            slayer_strike,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, "All"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(0, "All"))),
    ]
