from . import *

# * Cadre K — SOUTIEN de campagne (Justice / Campaign, n° 278). Cout 2. SKRULL.
# Action: Exhaust Cadre K -> remove 1 threat from a scheme.
#
# Cartes de reference :
#  - **`20029`** Crew Quarters : « Action: Exhaust ... -> » d'un soutien = `WhenInYourPlayTurn(Action, op)
#    .SetCostFunc(CostFunc.Exhaust("This")).SetTarget(...)`.
#  - **`jubilee/47021`** Multitalented : « remove threat from a scheme » = `this.RemoveThreatFromSchemes(cibles,
#    n, effect)` avec `SetTarget(Scheme2)` (toute manigance, principale comprise).
#
# ⚠ Mots-pieges : « A scheme » = n'importe quelle manigance (principale ou annexe, de joueur ou de rencontre) ;
# « remove 1 threat » ; l'Action n'est PAS un contre (pas de libelle `thwart` : ni Sonne/Desoriente, ni
# consequence) ; la Crise bloque le retrait sur le complot principal (comportement natif).


def GetAbilities() -> Sequence['Ability']:

    def cadre_k(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            cadre_k,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),
    ]
