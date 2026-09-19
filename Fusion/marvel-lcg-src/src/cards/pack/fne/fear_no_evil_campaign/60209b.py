from . import *

# Stop the Presses! (FAILED) — Setup: Deal each player 1 facedown encounter
#   card (in expert mode, 2 encounter cards instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        n = 2 if Worlds.IsExpert(effect) else 1
        Players.ForEachPlayer(effect, lambda player: player.DealEncounterCards(n, effect))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
