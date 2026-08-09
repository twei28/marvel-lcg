from . import *
def GetAbilities() -> Sequence['Ability']:
    def wretch(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Villain)
        faces = Worlds.DiscardEncounterCards(1, effect)
        faces = Filter.ByType(faces, Treachery)
        if faces:
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldAttack(AbilityType.Temp0, 'This', lambda e, m: m.DealAdditionalDamage(1, e)), unregister_after_exec=True, until_turn_end=True)
            this.effect.RegisterTemp(AbilityFactory.WhenUnitWouldScheme(AbilityType.Temp0, 'This', lambda e, m: m.GainSCHForThisScheme(1, e)), unregister_after_exec=True, until_turn_end=True)
    return [AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, 'This', AvatarWouldBeDefeated),
            AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, 'This', wretch)]
