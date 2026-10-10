from . import *
def GetAbilities() -> Sequence['Ability']:
    def metal_bracer(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.ReduceDamage(1, effect)
    def pas_imblocable(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> bool:
        # Article FFG « Unbreakable » (11/06/2026) : « the bracers can't reduce
        # the unpreventable damage from Luke's hero ability ».
        return not message.property.unpreventable
    return [
        *AbilityFactory.GiveKeywordToAttached(Hero, retaliate=1),
        # CORRECTIF (10/10/2026, rapport n74) : « When any amount of damage
        # WOULD BE DEALT to Luke Cage ». Accroche a `WhenUnitWouldTakeDamage`
        # (etape « would take »), le Bracelet passait APRES le Tenace : une
        # attaque a 1 coutait un Tenace. Rules Reference, Damage : 1. would be
        # dealt, 2. Tenace, 3. would take.
        AbilityFactory.WhenDamageWouldBeDealtTo(
            AbilityType.HeroInterrupt,
            CardFinder(name="Luke Cage"),
            metal_bracer,
            conditions=[pas_imblocable],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
