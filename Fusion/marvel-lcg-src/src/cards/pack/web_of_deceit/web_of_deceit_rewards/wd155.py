from . import *

# Bag Head

def GetAbilities() -> Sequence['Ability']:

    def sac_sur_la_tete(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Action: Add Bag Head to the victory display → change to hero form.
        # Draw up to your hand size. »
        this = effect.this.CastTo(Upgrade)
        joueur = effect.GetInitiator()
        Faces.AddToVictoryDisplay([this], effect)
        if joueur.IsAlterEgo():
            joueur.GetIdentity().ChangeToForm(Hero, effect)
        joueur.DrawUp("Max", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            sac_sur_la_tete
        ),
    ]
