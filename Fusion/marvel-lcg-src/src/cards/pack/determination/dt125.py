from . import *

# * Night Thrasher

def GetAbilities() -> Sequence['Ability']:

    def night_thrasher(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Ally)
        Faces.ReadyAll([this], effect)

    # APPROXIMATION ECRITE : la carte dit « apres que vous RETOURNEZ une carte
    # que vous controlez ». Le moteur ne publie qu'un retournement vers une face
    # nommee (AfterCardFlipToThisSide), pas un retournement quelconque. On garde
    # le cas de loin le plus courant : le changement de forme de l'identite.
    def check_a_vous(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> bool:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        return player is not None and message.trigger == player.GetIdentity()

    return [
        AbilityFactory.CardsEnterPlayExhausted("This"),
        *AbilityFactory.GiveKeywordToAttached(
            "This",
            retaliate=2,
        ),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            night_thrasher,
            conditions=[check_a_vous],
        ),
    ]
