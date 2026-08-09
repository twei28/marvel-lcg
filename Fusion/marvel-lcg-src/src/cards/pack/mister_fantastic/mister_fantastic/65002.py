from . import *

# * Invisible Woman — custom « DesignHacker »
# Response: After Invisible Woman enters play, ready your identity.

def GetAbilities() -> Sequence['Ability']:

    def invisible_woman(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetIdentity()], effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            invisible_woman,
        ),
    ]
