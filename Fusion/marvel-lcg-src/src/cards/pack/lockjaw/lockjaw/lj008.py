from . import *

# Teleport To Safety — custom « Nugget »
# Interrupt: When an identity would take any amount of damage from an attack,
#   change that identity's form → prevent all of that damage.


def GetAbilities() -> Sequence['Ability']:

    def teleporter(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        victime = message.trigger
        joueur = victime.GetControlByPlayer()
        if joueur is not None:
            ChangerDeForme(joueur, effect)
        message.PreventDamage("All", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Identity,
            teleporter,
            is_from_attack=True,
        ).SetPlay(),
    ]
