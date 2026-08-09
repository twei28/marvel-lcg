from . import *
def GetAbilities() -> Sequence['Ability']:
    def coup_de_grace(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        message.DealAdditionalDamage(3, effect)
        message.GainOverKill(effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.HeroInterrupt, 'YourHero', coup_de_grace)]
