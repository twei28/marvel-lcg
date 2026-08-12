from . import *

# Kinetic Stomp — custom « DesignHacker »
# Hero Interrupt: When you make a basic attack, you get +6 ATK for that attack.
#   If this attack deals 10 or more damage, ready your hero.


def GetAbilities() -> Sequence['Ability']:

    def kinetic_stomp(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Event)

        message.GainATKForThisAttack(6, effect)

        def ready_hero(effect2: 'Effect', message2: 'Message.AfterFaceDealDamage') -> None:
            Faces.ReadyAll([effect2.GetInitiator().GetIdentity()], effect2)

        this.effect.RegisterTemp(
            AbilityFactory.AfterFaceDealDamage(
                AbilityType.Temp0,
                "You",
                Enemy,
                ready_hero,
                is_from_attack=True,
                dealt_more_than_damage=10,
            ),
            unregister_after_exec=True,
            until_event_end=message,
        )

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            "You",
            kinetic_stomp,
            is_basic_attack=True,
        ).SetPlay(),
    ]
