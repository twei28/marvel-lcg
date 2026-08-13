from . import *

# Masochism

def GetAbilities() -> Sequence['Ability']:

    def check_more_than_3(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        return message.took_damage > 3

    def masochism(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        effect.GetInitiator().DrawUp(message.took_damage - 3, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.HeroResponse,
            "You",
            masochism,
            conditions=[check_more_than_3],
        ).SetPlay(),
    ]
