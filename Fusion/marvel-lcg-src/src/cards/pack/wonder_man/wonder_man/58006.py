from . import *
def GetAbilities() -> Sequence['Ability']:
    class SiphonState:
        damage = 0
    def pay_damage(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        SiphonState.damage = 0
        player = effect.GetInitiator()
        if not player:
            return False
        if not player.IsInHeroForm():
            return True
        identity = player.GetIdentity()
        max_damage = min(3, identity.health)
        damage = player.DeclareNumber(0, max_damage)
        if (damage > 0):
            identity.CastTo(Unit2).TakeDamage(effect.this, damage, effect)
            SiphonState.damage = damage
        return True
    def energy_siphon_res(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)
        return Resources('Y' * (1 + SiphonState.damage))
    def energy_siphon_check(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> 'Resources':
        this = effect.this.CastTo(Resource)
        Unused(this)
        player = message.GetToPlayer()
        if player and player.IsInHeroForm():
            return Resources('YYYY')
        return Resources('Y')
    return [AbilityFactory.DoDiscardThisToGenerateResources(AbilityType.Interrupt, res_fn=energy_siphon_res).SetCostFunc(CostFunc.Custom(None, pay_damage)),
            AbilityFactory.CheckThisCanDropPay(energy_siphon_check)]
