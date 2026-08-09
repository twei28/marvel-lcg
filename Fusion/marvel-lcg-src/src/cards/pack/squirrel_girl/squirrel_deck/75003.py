from . import *

# Monkey Joe
# Response: After Monkey Joe defeats a minion, call 1 Squirrel.

def GetAbilities() -> Sequence['Ability']:

    def appeler(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Ally)
        joueur = this.GetControlByPlayer()
        if joueur is not None:
            AppelerEcureuil(joueur, effect)

    return [
        *Ecureuil(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Minion,
            appeler,
            conditions=[PasDeDiscorde],
        ),
    ]
