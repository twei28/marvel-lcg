from . import *

# * Doc Jaw's Lab — custom « Nugget »
# Alter-Ego Action: Exhaust Doc Jaw's Lab → ready Tuning Fork.


def GetAbilities() -> Sequence['Ability']:

    def redresser(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        controleur = this.GetControlByPlayer()
        fourchette = Worlds.FindCardOnField(
            effect,
            name="Tuning Fork",
            card_type=Upgrade,
        )
        if fourchette is not None and \
                (controleur is None or fourchette.GetControlByPlayer() == controleur):
            Faces.ReadyAll([fourchette], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            redresser,
        ).SetName("Doc Jaw's Lab")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
