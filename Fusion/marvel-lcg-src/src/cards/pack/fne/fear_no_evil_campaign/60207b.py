from . import *

# Protection Racket (FAILED) — Setup: Each player chooses and discards 1 card
#   from their hand (in expert mode, 2 cards instead).

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        n = 2 if Worlds.IsExpert(effect) else 1
        Players.ForEachPlayer(effect, lambda player: DefausserDeLaMain(effect, player, n))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
