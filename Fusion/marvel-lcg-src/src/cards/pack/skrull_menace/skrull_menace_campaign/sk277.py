from . import *

# * Antalya — SOUTIEN de campagne (Protection / Campaign, n° 277). Cout 2. PERSONA. SKRULL.
# Action: Exhaust Antalya -> heal 1 damage from a friendly character.
#
# Cartes de reference :
#  - **`20029`** Crew Quarters (support, « Action: Exhaust ... -> heal 1 damage from ... ») :
#    `WhenInYourPlayTurn(Action, op).SetCostFunc(CostFunc.Exhaust("This")).SetTarget(...)` + `this.HealthUnits`.
#  - **`ra001b`** : la cible « friendly character » = `SetTarget(Friend, canbe_heal=True)`.
#
# ⚠ Mots-pieges : « Action » (pas « Hero Action » : jouable sous les DEUX formes) ; « a FRIENDLY character »
# (heros, alter egos et allies de TOUS les joueurs) ; « heal 1 » (un seul) ; « Exhaust Antalya » est un COUT :
# inclinee, l'action n'est plus offerte.


def GetAbilities() -> Sequence['Ability']:

    def antalya(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.HealthUnits(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            antalya,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Friend, canbe_heal=True),
    ]
