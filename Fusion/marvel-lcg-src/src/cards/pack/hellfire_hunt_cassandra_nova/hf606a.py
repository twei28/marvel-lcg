from . import *

# Mutant Extermination (3A). « When Revealed : Deal each player 1 facedown encounter card for each character they control. »
# Cartes de reference : `Player.DealEncounterCards(n, effect)` (hf118, sk), `player.allies.Get()` (allies controles).
# ⚠ « each character they control » : l'identite (1) + chaque allie ; les sbires et le vilain ne sont pas controles par le joueur.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for joueur in Worlds.GetPlayers(effect):
            joueur.DealEncounterCards(PersonnagesControles(joueur), effect)

    return [AbilityFactory.WhenThisRevealed(None, revelee)]
