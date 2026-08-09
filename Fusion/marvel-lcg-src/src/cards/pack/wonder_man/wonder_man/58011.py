from . import *
def GetAbilities() -> Sequence['Ability']:
    def what_are_you(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity()
        message.SetBeInstead(effect)
        if player.IsInHeroForm():
            identity.ChangeToForm(AlterEgo, effect)
        identity.CastTo(CanHealth).SetHealth(4, effect)
        ip = FindIonicPhysiology(effect, player)
        if ip:
            while (len(ip.GetPlacedCardArea().Get()) < 3):
                before = len(ip.GetPlacedCardArea().Get())
                TuckEnergyEventFromDiscard(effect, player)
                if (len(ip.GetPlacedCardArea().Get()) == before):
                    break
        Faces.RemoveAllFromGame([this], effect)
    def check_wonder_man(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        this = effect.this
        if not Hero.IsType(message.trigger):
            return False
        return (message.trigger == this.GetControlByPlayer().GetIdentity())
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Identity, what_are_you, conditions=[check_wonder_man])]
