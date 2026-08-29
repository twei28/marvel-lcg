from . import *
def GetAbilities() -> Sequence['Ability']:
    def internal_injury(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Obligation)
        player = this.GetGaveToPlayer()
        identity = player.GetIdentity() if player else None
        if identity:
            this.DealDamage([identity], DamageProperty(damage=3, ignore_tough=True), effect)
    def after_recover(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Obligation)
        Faces.RemoveAllFromGame([this], effect)
    return [
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Player", internal_injury),
        AbilityFactory.AfterUnitRecovery(AbilityType.AlterEgoResponse, "You", after_recover),
    ]
