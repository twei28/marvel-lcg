from . import *
def GetAbilities() -> Sequence['Ability']:
    def find_ava(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer() if hasattr(message, 'GetToPlayer') else Worlds.GetFirstPlayer(effect)
        RevealAllVersusAll(effect, player)
    def after_activate(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        PlaceThreatOnAllVersusAll(effect, this, 2)
    def after_attack(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Minion)
        PlaceThreatOnAllVersusAll(effect, this, 2)
    return [AbilityFactory.WhenThisRevealed(None, find_ava),
            AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, 'This', find_ava),
            AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, 'This', after_activate),
            AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, 'This', after_attack)]
