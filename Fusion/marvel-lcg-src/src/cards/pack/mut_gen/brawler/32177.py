from . import *
def GetAbilities() -> Sequence['Ability']:
    def swagger(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        message.would_message.GainDEFForThisAttack(3, effect)
        Faces.ReadyAll([identity], effect)
        Faces.RemoveAllFromGame([this], effect)
    def check_defense(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        return (message.power == 'DEF')
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitUseBasicPower(AbilityType.HeroInterrupt, 'YourHero', swagger, conditions=[check_defense])]
