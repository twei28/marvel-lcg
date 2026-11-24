from . import *

# Stakeout — AMELIORATION (PREPARATION), cout 1, [physical].
# Hero Response (attack): After a minion enters play, discard Stakeout → deal 2 damage to that minion and stun it.
#
# CARTES DE REFERENCE
#  - `08010` Widow's Bite : texte identique (`AfterCardEnterPlay(HeroResponse, Minion, ..)` + `SetLabel('attack')` + `Discard("This")` + `SetTarget("Trigger")`).
#
# TEXTE CONTRE CODE
#  « Hero Response » -> sous-type dedie. « (attack) » -> label (alimente Sonne/Desoriente). « discard Stakeout » = COUT. « that minion » -> la cible
#    « Trigger » (le sbire qui vient d'entrer), pas un autre. 2 degats PUIS Sonne.


def GetAbilities() -> Sequence['Ability']:

    def stakeout(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)
        this.DealDamage(effect.targets, 2, effect)
        Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            stakeout,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("Trigger"),
    ]
