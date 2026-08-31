from core import *
from game.card.face import *

class PlayerStat:

    def __init__(self) -> None:
        self.this_turn_played_cards: List['CardFace'] = []
        self.this_round_played_cards: List['CardFace'] = []
        self.this_phase_played_cards: List['CardFace'] = []
        self.this_phase_revealed_cards: List['CardFace'] = []
        self.kill_counter: List['Unit2'] = []
        # CORRECTIF (pack custom angela, 31/08/2026) : `kill_counter` est remis
        # a zero a chaque PHASE (OnBeginPhase). Les cartes d'Angela comptent
        # « each minion you defeated this ROUND » (an004 Murderous Glare,
        # an007 Asgard's Assassin), ce qui inclut les sbires vaincus pendant la
        # phase du vilain. On tient donc un second compteur, vide seulement au
        # changement de round.
        self.round_kill_counter: List['Unit2'] = []

    def ResetPlayedRevealedCards(self):
        self.this_turn_played_cards.clear()
        self.this_round_played_cards.clear()
        self.this_phase_played_cards.clear()
        self.this_phase_revealed_cards.clear()

    def ResetKillCounter(self):
        self.kill_counter.clear()

    def ResetRoundKillCounter(self):
        self.round_kill_counter.clear()

    def UpdateKillCounter(self, unit: 'Unit2'):
        self.kill_counter.append(unit)
        self.round_kill_counter.append(unit)

    def RecordPlayedFace(self, face: 'CardFace'):
        self.this_turn_played_cards.append(face)
        self.this_round_played_cards.append(face)
        self.this_phase_played_cards.append(face)

    def RecordReveal(self, face: 'CardFace'):
        self.this_phase_revealed_cards.append(face)

    ################################################################################
    #
    # def HasPlayedAllyThisRound(self) -> bool:
    #     from game.card.face.card_type import Ally
    #     for card in self.this_round_played_cards:
    #         if Ally.IsType(card):
    #             return True
    #     return False

    def GetThisRoundPlayedCard(self, index: int) -> 'CardFace|None':
        if index < len(self.this_round_played_cards):
            return self.this_round_played_cards[index]
        return None

    def GetThisPhasePlayedCard(self, index: int) -> 'CardFace|None':
        if index < len(self.this_phase_played_cards):
            return self.this_phase_played_cards[index]
        return None

    def IsFirstCardPlayedThisRound(self) -> bool:
        return self.GetThisRoundPlayedCard(0) == None

    ################################################################################
    #
    def OnBeginTurn(self) -> None:
        self.this_turn_played_cards.clear()

    def OnEndTurn(self) -> None:
        self.this_turn_played_cards.clear()

    def OnBeginPhase(self) -> None:
        self.this_phase_revealed_cards.clear()
        self.this_phase_played_cards.clear()
        self.ResetKillCounter()

    def OnEndPhase(self) -> None:
        self.this_phase_revealed_cards.clear()
        self.this_phase_played_cards.clear()

    def OnBeginRound(self) -> None:
        self.this_round_played_cards.clear()
        self.ResetRoundKillCounter()

    def OnEndRound(self) -> None:
        self.this_round_played_cards.clear()
        self.ResetRoundKillCounter()

