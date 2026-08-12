from . import *

# Toughen Up — custom « DesignHacker »
# Response: After you take any amount of damage, give your identity a tough
# status card.

def GetAbilities() -> Sequence['Ability']:

    def toughen_up(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.GiveStatus([initiator.GetIdentity()], "Tough", effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            "You",
            toughen_up,
        ).SetPlay(),
    ]
