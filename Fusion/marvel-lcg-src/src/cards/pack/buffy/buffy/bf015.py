from . import *

# * Kendra — ALLIE (SLAYER), cout 0, [physical]. THW 1*, ATQ 1*, PV 3. Unique. Victory 0.
# Kendra enters play with 3 stake counters on her.
# Response: After a minion enters play, remove 1 stake counter from Kendra → deal 2 damage to that minion.
#
# CARTES DE REFERENCE
#  - `01066` Hawkeye : `ThisEnterPlayWithCounters(N, 'nom')` + `AfterCardEnterPlay(Response, Minion, op).SetTarget("Trigger").SetCostFunc(CostFunc.Counter("This", 1, 'nom'))`.
#  - `Victory 0` : lu dans `desc` (fiche `mots-cles/victory.md`).
#
# TEXTE CONTRE CODE
#  « 3 stake counters » -> 3 jetons « stake ». « remove 1 » = COUT (sans jeton, la Reponse n'est pas proposee). « that minion » -> « Trigger ».
#  Pas de limite imprimee : une Reponse par sbire entre en jeu tant qu'il reste des jetons.


def GetAbilities() -> Sequence['Ability']:

    def kendra(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this, message)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            Minion,
            kendra,
        ).SetTarget("Trigger")
        .SetCostFunc(CostFunc.Counter("This", 1, 'stake')),
        AbilityFactory.ThisEnterPlayWithCounters(3, 'stake'),
    ]
