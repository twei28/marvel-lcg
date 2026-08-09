from . import *
def GetAbilities() -> Sequence['Ability']:
    def stealth_training(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        Faces.GiveStatus(effect.targets, 'Stunned', effect)
    def check_you(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        this = effect.this
        return (message.GetDefeatingPlayer() == this.GetControlByPlayer())
    return [AbilityFactory.CanPlayThisUpgradeCard('Players'),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Response, EncounterSideScheme, stealth_training, has_defeating_player=True, conditions=[check_you]).SetCostFunc(CostFunc.Exhaust('This')).SetTarget(Enemy, canbe_stunned=True)]
