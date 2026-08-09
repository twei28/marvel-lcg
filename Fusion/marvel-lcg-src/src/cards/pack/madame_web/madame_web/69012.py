from . import *

# Neurological Deterioration — custom « Kajislav » (obligation de Madame Web)
# You cannot ready your identity.
# Alter-Ego Action: Spend [energy] [mental] [physical] resources -> remove
#   Neurological Deterioration from the game.

def GetAbilities() -> Sequence['Ability']:

    def deterioration(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)

        Faces.RemoveAllFromGame([this], effect)

    return [
        *AbilityFactory.CardCannotReady(
            Identity,
            control_by="You"
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            deterioration
        ).SetCost(Cost("YBR")),
    ]
