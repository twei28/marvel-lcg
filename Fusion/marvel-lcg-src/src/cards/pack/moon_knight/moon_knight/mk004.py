from . import *

# * Frenchie — custom « DesignHacker »
# Interrupt: When any amount of threat would be placed on the main scheme,
#   discard Frenchie → prevent all of that threat.


def GetAbilities() -> Sequence['Ability']:

    def frenchie(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        this = effect.this.CastTo(Support)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    def vise_le_complot_principal(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> bool:
        return MainScheme.IsType(message.trigger)

    return [
        Ability(
            AbilityType.Interrupt,
            Message.WhenSchemeWouldPlaceThreat,
            [vise_le_complot_principal],
            frenchie,
        ).SetName("Frenchie"),
    ]
