from . import *

# Protect The Pack — custom « Nugget » (carte d'aspect PROTECTION)
# Hero Interrupt: When a friendly character would take any amount of damage
#   (including consequential damage), you take that damage instead.


def GetAbilities() -> Sequence['Ability']:

    def encaisser_a_sa_place(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        identite = initiator.GetIdentity()
        if identite is None:
            return

        valeur = message.property.damage
        message.PreventDamage("All", effect)
        if valeur > 0:
            # CORRECTIF (4/8/2026) : la SOURCE des degats est le premier
            # argument. Sans elle, la carte plantait a chaque usage.
            identite.TakeIndirectDamage(this, valeur, effect)

    def pas_l_identite(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        initiator = effect.GetInitiator()
        if initiator is None:
            return False
        return message.trigger != initiator.GetIdentity()

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            Friend,
            encaisser_a_sa_place,
            conditions=[pas_l_identite],
        ).SetPlay(),
    ]
