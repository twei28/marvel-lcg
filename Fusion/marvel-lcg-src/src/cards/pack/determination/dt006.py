from . import *

# Human Shield

def GetAbilities() -> Sequence['Ability']:

    def check_friendly(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        initiator = effect.GetInitiator()
        unit = message.trigger
        return unit.GetControlByPlayer() == initiator

    def human_shield(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        num = initiator.DeclareNumber(0, 3)
        message.PreventDamage(num, effect)

        # « si VOUS avez encaisse des degats de cette attaque » : le protege
        # peut etre un allie, auquel cas l'identite n'a rien pris et le heros
        # ne se redresse pas.
        if message.trigger == identity and message.will_take_damage > 0:
            Faces.ReadyAll([initiator.GetHero()], effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            None,
            human_shield,
            is_from_attack=True,
            conditions=[check_friendly],
        ).SetPlay().SetLabel('defense'),
    ]
