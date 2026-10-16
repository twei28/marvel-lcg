from . import *

# Defensive Formation — SOUTIEN Leadership (TMNT Reskins, Inkwire), cout 2, [energy]. TACTIC.
# Uses (3 block counters).
# Action: Exhaust this card and remove 1 block counter from it -> give a [[TURTLE]] ally a tough status card.
#
# MODIFIEE (reskin de `62018` Defensive Formation) : [[DEFENDER]] -> [[TURTLE]]. Script propre copie de
# 62018, seul le trait change. `Uses` vit dans `desc` (fiche uses.md), lu par le moteur.
#
# TEXTE CONTRE CODE
#  ⚠ « Exhaust this card AND remove 1 block counter » : deux couts, les deux payes.
#  ⚠ « a TURTLE ally » : n'importe quel allie TURTLE en jeu (le texte ne dit pas « you control »).
#  ⚠ PAS de `.SetPlay()` (voir le commentaire de 62018 : la carte deviendrait injouable).


def GetAbilities() -> Sequence['Ability']:
    def defensive_formation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        for target in effect.targets:
            Faces.GiveStatus([target], "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, defensive_formation)
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.Counter("This", 1, 'block'))
        .SetTarget(CardFinder(card_type=Ally, trait='TURTLE'), range=(1, 1)),
    ]
