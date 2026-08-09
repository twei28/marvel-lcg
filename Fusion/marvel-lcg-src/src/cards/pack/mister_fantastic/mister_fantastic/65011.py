from . import *

# Slippery — custom « DesignHacker »
# Interrupt: When you would take any amount of damage, prevent 2 of that
# damage and draw 2 cards.

def GetAbilities() -> Sequence['Ability']:

    def slippery(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage(2, effect)

        initiator = effect.GetInitiator()
        initiator.DrawUp(2, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            slippery,
        ).SetPlay(),
    ]
