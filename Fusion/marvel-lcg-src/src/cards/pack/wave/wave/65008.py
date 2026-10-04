from . import *

# * Pearl's Lolo — soutien signature, x1 (13/15). PERSONA. Cout 1.
# Alter-Ego Action: Flip a faceup card in your Rising Tide area facedown ->
# heal 3 damage.
#
# Modele du declencheur AlterEgoAction + cout d'inclinaison/retournement :
# aa003 Ebony (`WhenInYourPlayTurn(AlterEgoAction, ...).SetCostFunc(
# CostFunc.Exhaust("This"))`) -- ici le cout est le retournement partage
# `CoutRetournerUneCarteRisingTide` (wave/__init__.py) plutot qu'un
# inclinaison, donc pas de `CostFunc.Exhaust`.
# Modele du soin : av001b Flash Thompson, « heal 2 damage from any character »
# -> `this.HealthUnits(effect.targets, 2, effect)` +
# `.SetTarget(Unit2, canbe_heal=True)`. Aucune restriction de cible n'est
# imprimee sur Pearl's Lolo : meme lecture « any character ».

def GetAbilities() -> Sequence['Ability']:

    def pearls_lolo(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        this.HealthUnits(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            pearls_lolo,
        ).SetCostFunc(CoutRetournerUneCarteRisingTide(
            face_visible=True,
            prompt="Flip to heal 3 damage",
        ))
        .SetTarget(Unit2, canbe_heal=True),
    ]
