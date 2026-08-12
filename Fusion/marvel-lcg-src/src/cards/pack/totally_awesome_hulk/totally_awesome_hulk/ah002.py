from . import *

# * Hercules — custom « DesignHacker »
# Response: After Hercules defeats a minion, ready him.


def GetAbilities() -> Sequence['Ability']:

    def hercules(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)

        Faces.ReadyAll([this], effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Minion,
            hercules,
        ),
    ]
