from . import *

# * Spider-Man Noir

def GetAbilities() -> Sequence['Ability']:

    def sortie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        # « Response: After Spider-Man Noir leaves play, heal 4 damage from your
        # identity. »
        this = effect.this.CastTo(Ally)
        joueur = effect.GetInitiator()
        this.HealthUnits([joueur.GetIdentity()], 4, effect)

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            sortie
        ),
    ]
