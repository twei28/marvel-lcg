from . import *
def GetAbilities() -> Sequence['Ability']:
    def unpreventable(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Hero)
        this.DealDamage([this], DamageProperty(damage=1, ignore_tough=True), effect)
    return [
        AbilityFactory.ThisCanHaveAdditionalTough("Any"),
        AbilityFactory.UnitAttackGainKeyword(None, "This", lost_piercing=True),
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.ForcedResponse, "This", "Tough", unpreventable),
    ]
