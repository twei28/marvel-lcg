from . import *

# The Other Guy

def GetAbilities() -> Sequence['Ability']:

    def cote_alter_ego(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    def cote_hero(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)

        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.AlterEgoResponse,
            "You",
            cote_alter_ego
        ).SetLabel('thwart')
        .SetTarget(Scheme2)
        .LimitOncePerPhase(),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            cote_hero
        ).SetLabel('attack')
        .SetTarget(Enemy)
        .LimitOncePerPhase(),
    ]
