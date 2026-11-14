from . import *

# Hey you! (Team-Up Deadpool / She-Hulk, Basic, Max 1 per deck)
# Action: Stun and confuse an enemy. Remove Hey you! from the game.
# Team-Up : `desc.TeamUp` + `.SetTarget("TeamUp")` (fiche mots-cles/teamup.md) ;
# l'ennemi est le second selecteur (modele 47022 Unlikely Duo). Retrait de la
# partie : modele 16175 Power Unleashed.


def GetAbilities() -> Sequence['Ability']:

    def hey_you(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        # `effect.targets2` ne se lit qu'UNE fois (assert `initialized_targets`) : on le garde.
        ennemis = list(effect.targets2)
        Faces.GiveStatus(ennemis, "Stunned", effect)
        Faces.GiveStatus(ennemis, "Confused", effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            hey_you
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp")
        .SetTarget2(Enemy),
    ]
