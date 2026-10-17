from . import *

# * Commando (Raph) — ALLIE 2 [energy], ATK 1 (1), THW 1 (1), PV 2. NINJA. SOLDIER. TURTLE.
# Response: After Commando enters play, discard an event from your hand → stun an enemy.
#
# CARTES DE REFERENCE
#  - `01083` * Mockingbird : « After Mockingbird enters play, stun an enemy » = `AfterCardEnterPlay(Response,
#    "This", ...)` + `.SetTarget(Enemy, canbe_stunned=True)`.
#  - `60191` / `18027` : « discard an event from your hand » en COUT = `CostFunc.Discard("YourHandCards",
#    card_type=Event)`.
# TEXTE CONTRE CODE
#  ⚠ fleche → : la defausse est le COUT (sans evenement en main, pas de Reponse).
#  ⚠ « an event » : n'importe quel evenement, sans trait.
#  ⚠ « enters play » (pas « you play ») : toute entree en jeu.


def GetAbilities() -> Sequence['Ability']:

    def commando(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            commando,
        ).SetCostFunc(CostFunc.Discard("YourHandCards", card_type=Event))
        .SetTarget(Enemy, canbe_stunned=True),
    ]
