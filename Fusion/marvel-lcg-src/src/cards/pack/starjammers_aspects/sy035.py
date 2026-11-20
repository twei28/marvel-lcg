from . import *
# * Lilandra: Lilandra Neramani (Leadership, allie 3 [mental], THW 2*, ATK 1*, PV 3). PSIONIC. SHI'AR. STARJAMMER.
# Action: Exhaust Lilandra and deal 1 damage to her → choose another ally. Until the end of the phase the chosen ally does not take
# consequential damage.
#
# Cartes de reference : dt066 Misty Knight (`WhenInYourPlayTurn(Action, op).SetCostFunc(Exhaust("This")).SetCostFunc(CostFunc.DealDamage(1,
# "This"))`) ; `AbilityFactory.WhenAllyWouldTakeConsequentialDamage` (friend.py:427) + `message.ReduceDamage(n, effect)` ; `RegisterTemp(..,
# unregister_after_exec=False, until_phase_end=True)` (effect.py:211) pour « until the end of the phase ».
# « does not take consequential damage » : tous les degats consecutifs de l'allie choisi, attaque comme contre, jusqu'a la fin de la phase.
def GetAbilities() -> Sequence['Ability']:
    def lilandra(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        choisi = effect.targets[0]
        def le_choisi(eff: 'Effect', msg: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
            return msg.trigger is choisi
        def aucun_degat(eff: 'Effect', msg: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
            if msg.will_take_damage > 0:
                msg.ReduceDamage(msg.will_take_damage, eff)
        this.effect.RegisterTemp(
            Ability(
                AbilityType.Temp0,
                Message.WhenAllyWouldTakeConsequentialDamage,
                [le_choisi],
                aucun_degat,
            ),
            unregister_after_exec=False,
            until_phase_end=True,
        )
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            lilandra,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealDamage(1, "This"))
        .SetTarget(Ally, check_fn=lambda effect, face: face is not effect.this),
    ]
