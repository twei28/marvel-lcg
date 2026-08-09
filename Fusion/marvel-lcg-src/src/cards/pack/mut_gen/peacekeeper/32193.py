from . import *
def GetAbilities() -> Sequence['Ability']:
    def rescue_operation(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        for ally in player.allies.Get():
            ally.CastTo(Unit2).TemporaryGain(effect, None, Message.WhenPhaseEnd, thwart_consequential_damage=-9)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, rescue_operation)]
