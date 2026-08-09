from . import *
def GetAbilities() -> Sequence['Ability']:
    def give_discount(effect: 'Effect') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        identity = player.GetIdentity()
        identity.effect.RegisterTemp(AbilityFactory.CanGenerateResources(AbilityType.Resource, Resources('GG'), is_play_card=True, who_trigger_this_effect='You'), unregister_after_exec=True, until_phase_end=True)
    def defeat_enemy(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        SenseDiscard(this, effect)
        give_discount(effect)
    def defeat_scheme(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        SenseDiscard(this, effect)
        give_discount(effect)
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
