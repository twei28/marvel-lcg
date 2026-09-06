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

        # --- Journal de la phase du mechant (ajout local, lu par ui-app) ------
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
        #
        # QUATRE GENRES DE FAITS, un par evenement, et un seul site d'appel
        # chacun (la liste vaut contrat avec le client) :
        #
        #   'menace'       point 1 — game/card/face/card_type/scheme_main.py,
        #                  MainScheme.Phase()
        #   'attaque'      point 2 — game/card/face/attribute/can_attack.py,
        #   'manigance'             JournaliserActivation / JournaliserManigance
        #   'distribution' point 3 — game/player/action/player_action.py,
        #                  PlayerAction.DealEncounterCard
        #   'revelation'   point 4 — game/player/action/player_action.py,
        #                  PlayerAction.RevealEncounterCards
        #
        # Les activations (points 2) sont inscrites QUELLE QUE SOIT la phase :
        # une carte revelee peut faire frapper le vilain, et le client range le
        # fait grace a son champ `phase`. Les trois autres genres n'ont de sens
        # qu'a leur etape et sont filtres a l'inscription.
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
        """Inscrit un fait de la phase du mechant au journal du round en cours.

        Les genres et leurs sites d'appel sont listes plus haut, a la
        declaration de `faits_mechant`.

        Le changement de round vide le journal : on ne le purge pas a la fin
        d'un round, parce que le bilan s'affiche APRES la phase et lirait alors
        un journal vide. On attend donc le premier fait du round suivant.

        Le fait recoit ICI son `round_id` : sans lui, ui-app (etapesDeroule)
        ne peut pas distinguer un fait du round en cours d'un fait perime, et
        le cartouche de la phase du mechant rouvrait au round suivant en
        plein tour du joueur, sur une manigance deja vaincue. On copie le
        dict plutot que de le muter : l'appelant (can_attack.py) le construit
        pour cet appel, mais rien ne garantit qu'il ne le reutilise pas.
        """
        if round_id != self._faits_mechant_round:
            self._faits_mechant_round = round_id
            self.faits_mechant = []
        self.faits_mechant.append({**fait, 'round_id': round_id})
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

