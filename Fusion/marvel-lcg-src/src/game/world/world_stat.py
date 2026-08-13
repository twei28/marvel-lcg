from core import *

from game.card.card import *
from game.ability import *
from game.player import *
from game.message import *

class WorldStat:
    def __init__(self) -> None:
        self.once_per_round_effects: List['Effect'] = []
        self.once_per_round_player_effects: Dict['Player', List['Effect']] = {}
        self.once_per_phase_player_effects: Dict['Player', List['Effect']] = {}
        self.once_per_phase_effects: List['Effect'] = []
        self.this_turn_made_attack: List[Tuple[CardFace, 'Effect', Sequence['CardFace']]] = []
        self.this_turn_made_thwart: List[Tuple[CardFace, 'Effect', Sequence['CardFace']]] = []
        # self.played_cards_this_turn: List[Tuple['Player', 'CardFace']] = []

        # --- Journal des activations ennemies (ajout local, lu par ui-app) ----
        #
        # Le bilan de la phase du mechant reconstituait ce qui s'etait passe en
        # COMPARANT deux photos du monde : une perte de PV devenait « subit 3
        # degats ». Cette methode voit le resultat mais jamais sa composition —
        # elle ne peut pas dire « 3 d'attaque de base + 2 de boost » — et elle
        # compte plusieurs fois ce que le moteur rend plusieurs fois autour
        # d'une seule resolution.
        #
        # Ici on publie ce que le moteur SAIT, une fois, au moment ou il le
        # calcule. Le journal ne garde que le round en cours : le bilan ne parle
        # jamais d'un autre, et rien n'a a grossir sans fin.
        self.faits_mechant: List[Dict[str, Any]] = []
        self._faits_mechant_round: int = -1

    def OnTurnBegin(self):
        self.this_turn_made_attack = []
        self.this_turn_made_thwart = []
        # self.played_cards_this_turn = []

    def OnTurnEnd(self):
        self.this_turn_made_attack = []
        self.this_turn_made_thwart = []
        # self.played_cards_this_turn = []

    def OnRoundEnd(self):
        self.once_per_round_effects = []
        self.once_per_round_player_effects = {}

    def OnPhaseEnd(self):
        self.once_per_phase_effects = []
        self.once_per_phase_player_effects = {}

    ################################################################################
    #
    def RecordEffectWithPlayer(self, effect: 'Effect', player: 'Player'):
        if player not in self.once_per_round_player_effects:
            self.once_per_round_player_effects[player] = [effect]
        else:
            self.once_per_round_player_effects[player].append(effect)

        if player not in self.once_per_phase_player_effects:
            self.once_per_phase_player_effects[player] = [effect]
        else:
            self.once_per_phase_player_effects[player].append(effect)

    def RecordEffect(self, effect: 'Effect'):
        self.once_per_round_effects.append(effect)
        self.once_per_phase_effects.append(effect)

    def RecordFaitMechant(self, round_id: int, fait: 'Dict[str, Any]') -> None:
        """Inscrit une activation ennemie au journal du round en cours.

        Le changement de round vide le journal : on ne le purge pas a la fin
        d'un round, parce que le bilan s'affiche APRES la phase et lirait alors
        un journal vide. On attend donc le premier fait du round suivant.
        """
        if round_id != self._faits_mechant_round:
            self._faits_mechant_round = round_id
            self.faits_mechant = []
        self.faits_mechant.append(fait)
        # Garde-fou : une partie pathologique ne doit pas faire enfler le
        # descripteur envoye a chaque rendu.
        if len(self.faits_mechant) > 200:
            del self.faits_mechant[:-200]

    def RecordAttack(self, end_message: 'Message.AfterUnitAttackEnd'):
        self.this_turn_made_attack.append((end_message.attacker, end_message.by_effect, end_message.attacked_targets))

    def RecordThwart(self, end_message: 'Message.AfterUnitThwartEnd'):
        self.this_turn_made_thwart.append((end_message.trigger, end_message.by_effect, end_message.schemes))

    def RecordPlayedCard(self, player: 'Player', face: 'CardFace'):
        # self.played_cards_this_turn.append((player, face))
        pass

    ################################################################################
    # return True means can process
    def IsOncePerRound(self, ability: 'Ability|None') -> bool:
        return ability not in [x.ability for x in self.once_per_round_effects]

    def IsOncePerRoundPerPlayer(self, ability: 'Ability|None', player: 'Player') -> bool:
        if player not in self.once_per_round_player_effects:
            return True
        return ability not in [x.ability for x in self.once_per_round_player_effects[player]]

    def IsOncePerPhasePerPlayer(self, ability: 'Ability|None', player: 'Player') -> bool:
        if player not in self.once_per_phase_player_effects:
            return True
        return ability not in [x.ability for x in self.once_per_phase_player_effects[player]]

    def IsOncePerPhase(self, ability: 'Ability|None') -> bool:
        return ability not in [x.ability for x in self.once_per_phase_effects]

