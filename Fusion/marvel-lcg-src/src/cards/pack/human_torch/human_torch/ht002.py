from . import *

# * The Thing — custom « DesignHacker »
# Toughness (desc).
# Response: After The Thing defends, ready him. (Limit once per phase.)

def GetAbilities() -> Sequence['Ability']:

    def the_thing(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Ally)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.Response,
            "This",
            the_thing
        ).LimitOncePerPhase(),
    ]
