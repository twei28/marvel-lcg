from core import *
from game.card.face import *

class PlayerStat:

    def __init__(self) -> None:
        self.this_turn_played_cards: List['CardFace'] = []
        self.this_round_played_cards: List['CardFace'] = []
        self.this_phase_played_cards: List['CardFace'] = []
        self.this_phase_revealed_cards: List['CardFace'] = []
        # CORRECTIF (26/10/2026, pack custom corsair, cr007 Parry / cr008 Riposte / cr009 Remise) : « the last card you
        # played » ne se limite pas au round (Riposte se joue en phase du vilain, Remise au tour suivant). Liste de toute
        # la PARTIE, jamais remise a zero en cours de partie (seulement a la mise en place).
        self.game_played_cards: List['CardFace'] = []
        self.kill_counter: List['Unit2'] = []
        # CORRECTIF (pack custom angela, 31/08/2026) : `kill_counter` est remis
        # a zero a chaque PHASE (OnBeginPhase). Les cartes d'Angela comptent
        # « each minion you defeated this ROUND » (an004 Murderous Glare,
        # an007 Asgard's Assassin), ce qui inclut les sbires vaincus pendant la
        # phase du vilain. On tient donc un second compteur, vide seulement au
        # changement de round.
        self.round_kill_counter: List['Unit2'] = []
        # CORRECTIF (25/10/2026, pack custom roz, jakxin) : « each "Special" ability resolved this
        # turn » (rz002 Thor Jane Foster) et « if you resolved a "Special" ability this turn »
        # (rz003 Thor Odinson). Une entree par capacite Special REELLEMENT resolue pour ce joueur ; vide a chaque
        # tour. Alimente par `EffectInvoker._ResolveSelfInternal` (effect_invoke.py), une fois le cout paye.
        self.this_turn_resolved_specials: List['CardFace'] = []
        # CORRECTIF (26/10/2026, pack custom smasher, sz001b Battle Ready) : « (Limit once per TURN.) ». Une limite par TOUR ne se
        # confond pas avec « par round » des qu'un joueur joue un tour de plus (rm007) : une entree par capacite deja utilisee ce tour,
        # videe a chaque tour. Alimentee par la carte elle-meme (`RecordLimitedAbility`).
        self.this_turn_limited_abilities: List['CardFace'] = []

    def RecordResolvedSpecial(self, face: 'CardFace'):
        self.this_turn_resolved_specials.append(face)

    def RecordLimitedAbility(self, face: 'CardFace'):
        self.this_turn_limited_abilities.append(face)

    def HasUsedLimitedAbilityThisTurn(self, face: 'CardFace') -> bool:
        return face in self.this_turn_limited_abilities

    def ResetPlayedRevealedCards(self):
        self.game_played_cards.clear()
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
        self.game_played_cards.append(face)
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
        self.this_turn_resolved_specials.clear()
        self.this_turn_limited_abilities.clear()

    def OnEndTurn(self) -> None:
        self.this_turn_played_cards.clear()
        self.this_turn_resolved_specials.clear()
        self.this_turn_limited_abilities.clear()

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

