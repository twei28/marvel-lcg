from . import *
def GetAbilities() -> Sequence['Ability']:
    def cybernetic_eye(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        this.RemoveThreatFromSchemes(effect.targets, 2 if AbimeDe(effect) else 1, effect)
    return [
        AbilityFactory.AfterUnitAttackYou(
            AbilityType.HeroResponse,
            Villain,
            cybernetic_eye,
        ).SetTarget(Scheme2),
    ]
