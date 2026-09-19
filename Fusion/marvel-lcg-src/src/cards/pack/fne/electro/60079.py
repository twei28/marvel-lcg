from . import *

# * Electric Charge (CONDITION) — Permanent. Attache a Electro.
# [star] Forced Interrupt: When Electro attacks, remove 1 charge counter from
#   here -> give Electro an additional boost card for this attack. This attack
#   gains overkill.  (CostFunc.Counter("This", 1, 'charge') = COUT, la fleche.)
# Hero Action: Spend a [energy] resource or 2 resources of any type -> remove
#   1 charge counter from here. (deux capacites, RECETTES §5 « or ».)

def GetAbilities() -> Sequence['Ability']:

    def decharge(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
        message.GainOverKill(effect)

    def retirer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.RemoveCountersOn([this], 1, 'charge', effect)

    def a_des_charges(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.GetCounters('charge') > 0

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name="Electro")),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            CardFinder(name="Electro"),
            decharge,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retirer, conditions=[a_des_charges])
            .SetName("Spend [energy]: remove 1 charge counter").SetCost(Cost("Y")),
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, retirer, conditions=[a_des_charges])
            .SetName("Spend 2 resources: remove 1 charge counter").SetCost(Cost("2")),
    ]
