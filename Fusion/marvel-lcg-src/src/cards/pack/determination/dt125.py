from . import *

# * Night Thrasher

def GetAbilities() -> Sequence['Ability']:

    def night_thrasher(effect: 'Effect', message: 'Message.WhenCardFlip') -> None:
        this = effect.this.CastTo(Ally)
        Faces.ReadyAll([this], effect)

    # « apres que vous retournez une carte que vous controlez » : n'importe
    # quelle carte, pas seulement l'identite. `WhenCardFlip` publie tous les
    # retournements (state.py:88) ; le premier jet se limitait au changement de
    # forme faute d'avoir trouve cette fenetre.
    def check_a_vous(effect: 'Effect', message: 'Message.WhenCardFlip') -> bool:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        return player is not None \
            and message.trigger.GetControlByPlayer() == player

    return [
        AbilityFactory.CardsEnterPlayExhausted("This"),
        AbilityFactory.WhenCardFlip(
            AbilityType.Response,
            None,
            night_thrasher,
            conditions=[check_a_vous],
        ),
    ]
