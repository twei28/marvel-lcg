from . import *

# Nancy Whitehead
# Response: After Nancy Whitehead enters play, call 1 Squirrel.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is not None:
            AppelerEcureuil(joueur, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            appeler,
        ),
    ]
