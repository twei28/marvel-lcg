from . import *

# Protection Racket (COMPLETED) — Setup: After resolving mulligans, each player may search
#   their deck and discard pile for a support and add it to their hand. In expert
#   mode, each player who did so discards 1 card from their hand.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenGameWouldBegin') -> None:
        Players.ForEachPlayer(effect, lambda player: ChercherEnMain(effect, player, Support))

    return [AbilityFactory.AfterGameSetup(mise_en_place)]
