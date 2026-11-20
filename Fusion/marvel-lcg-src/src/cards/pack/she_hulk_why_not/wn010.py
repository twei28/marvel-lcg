from . import *

# Gamma Power (Team-Up Hulk / She-Hulk, Basic, Max 1 per deck)
# Action: Place a total of 2 stun status cards on up to 2 enemies. Remove
# Gamma Power from the game.
# Deux ennemis choisis : une carte Sonne chacun. Un seul : les deux cartes vont
# sur lui (le moteur n'en garde qu'une sauf Steady, regle du jeu).


def GetAbilities() -> Sequence['Ability']:

    def gamma_power(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        ennemis = list(effect.targets2)
        if len(ennemis) == 1:
            ennemis = ennemis * 2
        for ennemi in ennemis:
            Faces.GiveStatus([ennemi], "Stunned", effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            gamma_power
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Enemy, range=(1, 2)),
    ]
