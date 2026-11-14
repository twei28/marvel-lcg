from . import *

# Psionic Mindlock : AMELIORATION (PSIONIC. PREPARATION.), cout 1, [mental]. Hero Class.
# Hero Response (attack): After a minion enters play, discard Psionic Mindlock → deal 2 damage to that minion and confuse it.
#
# CARTES DE REFERENCE
#  - `bf013` Stakeout (pack Buffy) / `08010` Widow's Bite : texte identique au statut pres (`AfterCardEnterPlay(HeroResponse, Minion, ..)` + `SetLabel('attack')`
#    + `Discard("This")` + `SetTarget("Trigger")`).
#
# TEXTE CONTRE CODE
#  « Hero Response » -> sous-type dedie. « (attack) » -> label. « discard Psionic Mindlock » = COUT. « that minion » -> la cible « Trigger » (le sbire qui vient d'entrer), pas un autre.
#  2 degats PUIS Desoriente (« Confused »). Chiffres : cout 1, 2 degats.


def GetAbilities() -> Sequence['Ability']:

    def psionic_mindlock(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        this.DealDamage(effect.targets, 2, effect)
        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.HeroResponse,
            Minion,
            psionic_mindlock,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("Trigger"),
    ]
