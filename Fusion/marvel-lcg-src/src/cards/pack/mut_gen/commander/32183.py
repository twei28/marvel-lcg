from . import *
def GetAbilities() -> Sequence['Ability']:
    def group_assault(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        for ally in player.allies.Get():
            ally.CastTo(Unit2).TemporaryGain(effect, None, Message.WhenPhaseEnd, attack_consequential_damage=-9)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, group_assault)]
