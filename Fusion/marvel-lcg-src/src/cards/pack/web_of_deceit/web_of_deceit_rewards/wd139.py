from . import *

# Backflip

def GetAbilities() -> Sequence['Ability']:

    def esquive(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        # « Hero Interrupt (defense): When your hero would take any amount of
        # damage from an enemy attack, prevent all of that damage. »
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "YourHero",
            esquive,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
