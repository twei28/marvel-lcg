from . import *
def GetAbilities() -> Sequence['Ability']:
    def compassion(effect: 'Effect', message: 'Message.AfterUnitRecovery') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        this.HealthUnits(effect.targets, 3, effect)
        initiator.DrawUp(1, effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.AfterUnitRecovery(AbilityType.AlterEgoResponse, 'YourIdentity', compassion).SetTarget('YouControlUnit', canbe_heal=True)]
