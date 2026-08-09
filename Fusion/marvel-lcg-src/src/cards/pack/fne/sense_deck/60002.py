from . import *
def GetAbilities() -> Sequence['Ability']:
    def defeat_enemy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        SenseDiscard(this, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)
    def defeat_scheme(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        SenseDiscard(this, effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)
    def check_enemy_you(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        killer = message.killer
        return bool(killer) and (killer.GetControlByPlayer() == this.GetControlByPlayer())
    def check_scheme_you(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        return (message.GetDefeatingPlayer() == this.GetControlByPlayer())
    return [AbilityFactory.CanPlayThisUpgradeCard(ENEMY_OR_SCHEME),
            AbilityFactory.WhenUnitBeDefeated(AbilityType.Interrupt, None, defeat_enemy, conditions=[check_enemy_you]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Interrupt, None, defeat_scheme, has_defeating_player=True, conditions=[check_scheme_you])]
