from . import *
def GetAbilities() -> Sequence['Ability']:
    def place_threat_on_worlds_collide(effect: 'Effect'):
        this = effect.this
        scheme = Worlds.FindCardOnField(effect, name='Worlds Collide', card_type=MainScheme)
        if scheme:
            this.PlaceThreatOnSchemes([scheme], 1, effect)
    def would_complete(effect: 'Effect', message: 'Message.WhenMainSchemeWouldAdvance') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        this.RemoveThreatFromSchemes([this], 999, effect)
        place_threat_on_worlds_collide(effect)
    def identity_defeated(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)
        message.SetBeInstead(effect)
        identity = message.trigger
        player = identity.GetControlByPlayer()
        if player.IsInHeroForm():
            identity.ChangeToForm(AlterEgo, effect)
        identity.CastTo(CanHealth).SetHealth(1, effect)
        place_threat_on_worlds_collide(effect)
    return [AbilityFactory.WhenMainSchemeWouldAdvance(AbilityType.ForcedInterrupt, 'This', would_complete),
            AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, Identity, identity_defeated)]
