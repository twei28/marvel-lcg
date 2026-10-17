from . import *

# * Road Rage (Raph) — ALLIE 3 [mental], aspect Protection (TMNT Aspects, Inkwire). NINJA. TURTLE. VIGILANTE.
# THW 1 (1), ATK 2 (1), PV 3.
# Road Rage enters play with 3 fuel counters on him.
# Response: After a minion enters play, remove 1 fuel counter from Road Rage -> deal 2 damage to that minion.
#
# MODIFIEE de `01066` Hawkeye (4 compteurs « arrow ») : 3 compteurs « fuel ». Script propre.
#
# CARTE DE REFERENCE : `01066` Hawkeye : `ThisEnterPlayWithCounters(N, nom)` + `AfterCardEnterPlay(Response,
# Minion, ...)` + `SetTarget("Trigger")` + `CostFunc.Counter("This", 1, nom)`.
#
# TEXTE CONTRE CODE
#  ⚠ « 3 FUEL counters » (pas 4 arrow) ; « remove 1 » = cout ; « that minion » = celui qui vient d'entrer
#    (`"Trigger"`), 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def road_rage(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            road_rage
        ).SetTarget("Trigger")
        .SetCostFunc(CostFunc.Counter("This", 1, 'fuel')),
        AbilityFactory.ThisEnterPlayWithCounters(3, 'fuel'),
    ]
