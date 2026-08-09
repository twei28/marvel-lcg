from . import *
def GetAbilities() -> Sequence['Ability']:
    def no_activate(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        message.SetBeInstead(effect)
    def check_not_shatter(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        source = message.source
        if source and ((source.paper.name == 'Fading Figment') or source.HasTrait('AVATAR OF LOKI')):
            return False
        return True
    def all_players_win(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Villain)
        Unused(this)
        Worlds.SetGameOver(True, effect)
    return [AbilityFactory.WhenEnemyWouldActivate(AbilityType.Rule, 'This', no_activate),
            AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, 'This', conditions=[check_not_shatter]),
            AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, 'This', all_players_win)]
