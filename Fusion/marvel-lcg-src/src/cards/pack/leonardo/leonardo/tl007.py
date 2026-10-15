from . import *

# * Leo's Greenhouse — SOUTIEN signature, x1. LOCATION. NYC. SKYLINE.
# Cout 1, [mental].
# Alter-Ego Action: Exhaust Leo's Greenhouse and discard 1 card from your hand
#   -> draw 2 cards and heal 2 damage from your identity.
#
# Cartes de reference :
#  - `ls007` Sif's Chambers : `AlterEgoAction` + `CostFunc.Exhaust("This")`,
#    `this.HealthUnits([identite], n, effect)` sur `joueur.GetIdentity()` ;
#  - `ra026` / `45080` : `CostFunc.Discard("YourHandCards", ...)` en cout ;
#  - `player.DrawUp(n, effect)`.
#
# Mots-pieges :
#  - « Exhaust Leo's Greenhouse AND discard 1 card -> » : DEUX parties de cout,
#    aucune oubliee (`SetCostFunc` chaines, elles s'ajoutent) ;
#  - « draw 2 cards AND heal 2 damage » : les deux effets, dans cet ordre ;
#  - « your IDENTITY » : l'identite du joueur (ici l'alter-ego, puisque
#    Alter-Ego Action) ;
#  - le NOM contient une apostrophe (« Leo's Greenhouse »).


def GetAbilities() -> Sequence['Ability']:

    def greenhouse(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        joueur.DrawUp(2, effect)
        identite = joueur.GetIdentity()
        if identite is not None:
            this.HealthUnits([identite], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            greenhouse,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
