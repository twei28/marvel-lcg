from . import *

# Psionic Tracking — custom « Nugget »
# Alter-Ego Action: Choose a player. Search that player's deck for any card
#   and discard it.


def GetAbilities() -> Sequence['Ability']:

    def pister(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is None:
                continue
            face = Search.PlayerCard(
                effect,
                joueur,
                include_player_deck=True,
                not_move=True,
            )
            if face:
                Faces.DiscardAll([face], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            pister,
        ).SetPlay()
        .SetTarget("Players"),
    ]
