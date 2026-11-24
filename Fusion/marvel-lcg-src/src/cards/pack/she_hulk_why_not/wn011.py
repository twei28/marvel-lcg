from . import *

# A Spider on the Wall (Team-Up She-Hulk / Spider-Man, Basic, Max 1 per deck)
# Action: Ready She-Hulk and draw 3 cards. Remove A Spider on the Wall from
# the game. « She-Hulk » est l'un des deux personnages du Team-Up (identite ou
# alliee) : on le retrouve parmi les cibles TeamUp par son nom.


def GetAbilities() -> Sequence['Ability']:

    def a_spider_on_the_wall(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        she_hulk = [perso for perso in effect.targets if perso.IsName("She-Hulk")]
        Faces.ReadyAll(she_hulk, effect)
        effect.GetInitiator().DrawUp(3, effect)
        Faces.RemoveAllFromGame([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            a_spider_on_the_wall
        ).SetPlay().SetLabel()
        .SetTarget("TeamUp"),
    ]
