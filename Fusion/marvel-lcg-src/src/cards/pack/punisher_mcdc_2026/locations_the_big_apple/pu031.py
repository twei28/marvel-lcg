from . import *

# Theater District (2) — LIEU (environnement LOCATION).
# Action: Exhaust a character you control → heal 2 damage from that character. (Limit once per round.)
#
# Cartes de reference : mu004 (Action d'environnement payee par `CostFunc.Exhaust("YouControlUnit")`, personnage epuise lu par
# `effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards`), pu066 (`HealHealth(n, effect)`), `Ville.AuLieu` (brique M1).
# ⚠ « Limit once per round » SANS « per player » : une fois par round AU TOTAL, tous joueurs confondus (FAQ du livret, R10) :
# `LimitOncePerRound` (globale), surtout pas `...PerPlayer`.
# ⚠ « heal 2 damage FROM THAT CHARACTER » : le personnage epuise pour payer, pas l'identite ; « Action » nue : jouable aussi en alter ego.

def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        inclines = effect.cost_func.Get(CostFunc.Exhaust).return_exhausted_cards
        if inclines:
            inclines[0].CastTo(Unit2).HealHealth(2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, soigner, conditions=[Ville.AuLieu])
        .SetCostFunc(CostFunc.Exhaust("YouControlUnit"))
        .LimitOncePerRound(),
    ]
