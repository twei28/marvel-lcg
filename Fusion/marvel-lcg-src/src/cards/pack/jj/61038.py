from . import *
def GetAbilities() -> Sequence['Ability']:
    def echo(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        hero = effect.GetInitiator().GetHero()
        if hero:
            message.PreventDamage(hero.defense, effect)
    def check_from_enemy_attack(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return message.would_atk_message is not None
    return [
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.NonKeyword, "This", echo, conditions=[check_from_enemy_attack]),
    ]
