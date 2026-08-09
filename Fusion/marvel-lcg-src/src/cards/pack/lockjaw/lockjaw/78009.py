from . import *

# Fast Travel — custom « Nugget »
# Action: Choose a player. That player changes form. If you paid for this card
#   using a [wild] resource, you may change your form.


def GetAbilities() -> Sequence['Ability']:

    def voyager(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is not None:
                ChangerDeForme(joueur, effect)

        if PayeAvecOs(effect):
            YouMayChangeForm(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            voyager,
        ).SetPlay()
        .SetTarget("Players"),
    ]
