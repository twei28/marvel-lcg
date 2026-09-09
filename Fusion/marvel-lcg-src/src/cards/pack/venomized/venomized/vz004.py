from . import *

# * Red Goblin (Normie Osborn) — ALLIE, cout 2, PV 2, CTR 1* / ATQ 1*. SYMBIOTE.
# Response: After a minion enters play, exhaust Red Goblin -> deal 1 damage to
#   that enemy.
#
# CARTE DE REFERENCE
#  - `01066` * Hawkeye (Clint Barton) : MEME MONTAGE au declencheur pres du
#    cout. « After a minion enters play » -> `AfterCardEnterPlay(Response,
#    Minion, ...)` + `SetTarget("Trigger")`, qui vise LE sbire qui vient
#    d'entrer et non un ennemi au choix.
#
# TEXTE CONTRE CODE
#  ⚠ « exhaust Red Goblin » est le COUT (avant la fleche) -> `SetCostFunc`.
#    Ecrit dans le corps, un Red Goblin deja incline declencherait quand meme.
#  ⚠ « that enemy » : c'est le SBIRE qui a declenche. `SetTarget("Trigger")`,
#    jamais `SetTarget(Enemy)` — sinon la joueuse choisirait sa cible, ce que
#    la carte ne dit pas.
def GetAbilities() -> Sequence['Ability']:

    def red_goblin(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)

        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            red_goblin
        ).SetTarget("Trigger")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
