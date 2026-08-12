from . import *

# * Khonshu — custom « DesignHacker »
# Action: Exhaust Khonshu → change your form to Moon Knight.
# Response: After you change form, exhaust Khonshu → draw a card.


def GetAbilities() -> Sequence['Ability']:

    def vers_moon_knight(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        ChangerVersFaceNommee(initiator, effect, "Moon Knight")

    def apres_changement(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        controleur = effect.this.GetControlByPlayer()
        if controleur is not None:
            controleur.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            vers_moon_knight,
            conditions=[
                lambda effect, message:
                    TrouverFaceIdentite(effect.GetInitiator(), "Moon Knight") is not None,
            ],
        ).SetName("Khonshu")
        .SetCostFunc(CostFunc.Exhaust("This")),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.Response,
            "You",
            apres_changement,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
