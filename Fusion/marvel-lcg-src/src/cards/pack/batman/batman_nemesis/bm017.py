from . import *
# Tails You Lose — TRAITRISE (Boost 2). When Revealed : discard the top 2 cards of the encounter deck. If an odd number of boost icons were discarded
# this way, the first player discards 2 cards at random from their hand. If a deterrence card was discarded this way, this card gains surge.
# Reference : bm016 ; `DiscardRandomHandCards` (player_action.py).
def GetAbilities() -> Sequence['Ability']:
    def tails(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        deck = Worlds.GetEncounterDeck(effect)
        defaussees = list(deck.GetTops(2))
        if defaussees:
            Faces.DiscardAll(defaussees, effect)
        icones = IconesDesCartesDefaussees(effect, defaussees) if defaussees else 0
        if icones % 2 == 1:
            effect.world.GetFirstPlayer().DiscardRandomHandCards(2, effect)
        if any(EstDissuasion(f) for f in defaussees):
            ThisCardGainSurge(effect)
    return [AbilityFactory.WhenThisRevealed(None, tails)]
