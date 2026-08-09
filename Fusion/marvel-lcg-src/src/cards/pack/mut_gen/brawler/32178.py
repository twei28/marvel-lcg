from . import *
def GetAbilities() -> Sequence['Ability']:
    def brazen_defense(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        # « prevent 3 damage from this attack and deal 3 damage to that enemy »
        # Vraie PREVENTION (modele Backflip 01003) au moment des degats, et non
        # plus un -3 sur l'attaque : compatible RR 1.8 (les degats prevenus ne
        # sont pas subis) et avec les effets « cannot be reduced ».
        this = effect.this.CastTo(Upgrade)
        attacker = message.source
        message.PreventDamage(3, effect)
        if attacker:
            this.DealDamage([attacker], 3, effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.HeroInterrupt, 'You', brazen_defense, is_from_attack=True).SetLabel('attack', 'defense').SetCost(Cost('1'))]
