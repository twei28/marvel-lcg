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
        #   'sonne'        (05/10/2026) un ennemi Sonne s'active : la carte Sonne
        #                  remplace l'activation AVANT l'annonce, donc ni
        #                  `attaque` ni `annule` n'existent. game/card/face/
        #                  attribute/can_attack.py, JournaliserActivationEmpechee,
        #                  appele par Enemy.DoActivate. Champs : temps ('attaque'
        #                  | 'manigance'), type ('mechant' | 'sbire'), auteur,
        #                  auteur_id, cible, cible_id, statut_retire, annule_par,
        #                  annule_par_id, fait_id, et rang_sbire/total_sbires
        #                  pour un sbire.
        #   'paquet_vide'  (13/10/2026) le paquet rencontre s'est vide PENDANT la
        #                  phase : defausse remelangee, +1 jeton d'acceleration.
        #                  game/player/scenario.py, process_after_shuffle.
        #                  Champs : phase, cible, cible_id (la manigance
        #                  principale), jetons (ses jetons d'acceleration apres).
        #
        # Les activations (points 2) sont inscrites QUELLE QUE SOIT la phase :
        # une carte revelee peut faire frapper le vilain, et le client range le
        # fait grace a son champ `phase`. Les trois autres genres n'ont de sens
        # qu'a leur etape et sont filtres a l'inscription.
        #
        # DEUX TEMPS PAR ACTIVATION. Une activation ennemie inscrit d'abord une
        # INTENTION (`etat: 'annonce'`), a la declaration, puis sa RESOLUTION
        # (`etat: 'resolu'`), qui REMPLACE la premiere : meme `activation_id`,
        # meme place dans la liste. Sans ce premier temps, il n'existait a
        # aucun moment un etat « le mechant va attaquer » que le plateau puisse
        # montrer, et la fenetre ou le joueur peut defendre ou interrompre
        # passait sans qu'il la voie venir.
        #
        # Une activation qui n'a finalement pas lieu (un « ... instead » qui la
        # remplace, une cible qui disparait) se clot par un fait
        # `etat: 'annule'`, sous le meme identifiant : une intention sans suite
        # laisserait le cartouche sur « va attaquer » jusqu'a la fin de la phase.
        self.faits_mechant: List[Dict[str, Any]] = []
        self._faits_mechant_round: int = -1
        # Le compteur des activations du round. Il numerote, il ne compte pas :
        # sa seule fonction est de lier l'intention a sa resolution. Reparti de
        # zero a chaque round, comme le journal lui-meme.
        self._activation_suivante: int = 0
        # Le sbire en train de s'activer (`{'id', 'rang', 'total'}`), pose par
        # Enemies.DoActivateAgainstYouInternal le temps de son activation et
        # remis a None ensuite. `RecordFaitMechant` en recopie `rang_sbire` et
        # `total_sbires` sur chaque fait dont l'`auteur_id` est ce sbire : le
        # cartouche affiche « 1 / 2 » des la premiere annonce (05/10/2026).
        self.sbire_en_cours: 'Dict[str, int]|None' = None

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
        self._DemarrerLeRound(round_id)
        # 13/10/2026 : une activation qui s'annonce repart d'un registre de
        # reductions vide ; celles d'avant (une traitrise, une autre attaque)
        # ne lui appartiennent pas.
        if fait.get('etat') == 'annonce':
            self._reductions_en_cours = {}
        complet = {**fait, 'round_id': round_id}
        en_cours = self.sbire_en_cours
        if en_cours is not None and 'auteur_id' in fait \
                and fait['auteur_id'] == en_cours['id'] and 'rang_sbire' not in fait:
            complet['rang_sbire'] = en_cours['rang']
            complet['total_sbires'] = en_cours['total']

        # REMPLACEMENT plutot qu'ajout quand le fait porte un identifiant
        # d'activation deja vu : c'est la resolution qui prend la place de son
        # intention. A LA MEME PLACE, et cela compte — le plateau lit les faits
        # dans l'ordre de la liste, et une activation qui sauterait en fin de
        # journal ferait reculer le joueur d'une etape a chaque coup resolu.
        activation_id = complet.get('activation_id')
        if activation_id is not None:
            for rang, ancien in enumerate(self.faits_mechant):
                if ancien.get('activation_id') == activation_id:
                    self.faits_mechant[rang] = complet
                    return
        # Meme regle pour `fait_id`, l'identifiant des faits qui ne sont pas
        # des activations : la revelation d'une carte rencontre est inscrite
        # AVANT son effet (pour survivre a une defaite), puis reinscrite avec
        # ce que l'effet a change (`effets`), a la meme place.
        fait_id = complet.get('fait_id')
        if fait_id is not None:
            for rang, ancien in enumerate(self.faits_mechant):
                if ancien.get('fait_id') == fait_id:
                    self.faits_mechant[rang] = complet
                    return

        self.faits_mechant.append(complet)
        # Garde-fou : une partie pathologique ne doit pas faire enfler le
        # descripteur envoye a chaque rendu.
        if len(self.faits_mechant) > 200:
            del self.faits_mechant[:-200]

    def _DemarrerLeRound(self, round_id: int) -> None:
        """Vide le journal au premier fait d'un round different du dernier vu.

        On ne purge pas a la FIN d'un round : le bilan s'affiche apres la
        phase et lirait alors un journal vide. On attend donc le premier fait
        du round suivant.
        """
        if round_id != self._faits_mechant_round:
            self._faits_mechant_round = round_id
            self.faits_mechant = []
            self._activation_suivante = 0
            self._reductions_en_cours = {}

    @staticmethod
    def NoterReduction(world: 'Any', cible_id: int, by_effect: 'Any', valeur: int) -> None:
        """Une reduction de degats sur `cible_id`, et la carte qui l'a causee
        (13/10/2026, encadres 1 et 4 : « 4 degats barre -> 2, Bouclier -2 »).
        Pendant la phase du mechant seulement ; le fait d'attaque la reprend
        (`PrendreReductions`) quand il est inscrit."""
        try:
            if valeur <= 0 or not world.phase.IsVillainPhase():
                return
            source = getattr(by_effect, 'this', None)
            nom = getattr(source, 'name', None)
            if not nom:
                return
            reductions = getattr(world.stat, '_reductions_en_cours', None)
            if reductions is None:
                reductions = {}
                setattr(world.stat, '_reductions_en_cours', reductions)
            # `source_id` (19/10/2026) : l'identifiant d'objet de la carte, pour que le plateau l'affiche sous SON nom
            # francais (« Barriere Energetique »), comme sur la table, au lieu du nom anglais du moteur.
            reductions.setdefault(cible_id, []).append(
                {'source': nom, 'valeur': int(valeur),
                 'source_id': getattr(getattr(source, 'card', None), 'object_id', None) or getattr(source, 'object_id', None)})
        except Exception:
            pass

    @staticmethod
    def ChampReductions(world: 'Any', cible_id: int) -> 'Dict[str, Any]':
        """Le champ `reductions` d'un fait, ou rien s'il n'y en a pas."""
        reductions = WorldStat.PrendreReductions(world, cible_id)
        return {'reductions': reductions} if reductions else {}

    @staticmethod
    def PrendreReductions(world: 'Any', cible_id: int) -> 'List[Dict[str, Any]]':
        """Les reductions notees sur `cible_id`, retirees du registre."""
        try:
            reductions = getattr(world.stat, '_reductions_en_cours', None) or {}
            return reductions.pop(cible_id, [])
        except Exception:
            return []

    @staticmethod
    def PhotoAvantStade(world: 'Any') -> 'Dict[str, Any]|None':
        """La table AVANT un changement de stade (13/10/2026), hors phase : rien."""
        try:
            if not world.phase.IsVillainPhase():
                return None
            from game.player.action.player_action import PlayerAction
            return PlayerAction._PhotoDeLaTable(world)
        except Exception:
            return None

    @staticmethod
    def _EffetsDuStade(world: 'Any', photo_avant: 'Dict[str, Any]|None', apres: 'Any') -> 'Dict[str, Any]':
        if photo_avant is None:
            return {}
        try:
            from game.player.action.player_action import PlayerAction
            # La menace de depart de la NOUVELLE carte n'est pas un effet : l'ecran
            # du stade la montre deja (et une face A retournee garde son objet).
            nouvelle = apres.card.object_id
            effets = [e for e in PlayerAction._EffetsDeLaRevelation(photo_avant, world)
                      if not (e.get('genre') == 'menace' and e.get('cible_id') == nouvelle)]
            return {'effets': effets} if effets else {}
        except Exception:
            return {}

    @staticmethod
    def RecordStade(world: 'Any', quoi: str, avant: 'Any', apres: 'Any',
                    stats_avant: 'Dict[str, int]|None' = None,
                    photo_avant: 'Dict[str, Any]|None' = None) -> None:
        """CHANGEMENT DE STADE en pleine phase du mechant (04/10/2026) : la
        manigance principale ou le mechant passe au stade suivant. Le cartouche
        en fait une etape a part, la nouvelle carte en grand. Hors phase du
        mechant, rien : le cartouche ne raconte que cette phase. Sous garde,
        comme tout ce journal d'affichage."""
        try:
            if not world.phase.IsVillainPhase() or world.is_game_over or apres is None:
                return
            world.stat.RecordFaitMechant(world.round_id, {
                'genre': 'stade',
                'quoi': quoi,
                'phase': world.GetPhaseText(),
                'avant': avant.name if avant is not None else '',
                'carte': apres.name,
                'carte_id': apres.card.object_id,
                # « PV 14 → 15, ATQ 2 → 3 » (cartouche, 04/10/2026). La carte
                # d'avant a deja quitte la table quand ce fait part : ses
                # valeurs relues ICI sont fausses (mesure sur Ultron, PV max 22
                # au lieu de 17, l'objet est repris par la nouvelle carte).
                # L'appelant les lit donc AVANT l'avancee et les passe dans
                # `stats_avant` ; sans elles, le fait se tait plutot que mentir.
                **({'avant_id': avant.card.object_id} if avant is not None else {}),
                **({'stats_avant': stats_avant} if avant is not None and stats_avant else {}),
                'stats_apres': WorldStat.StatsDuStade(apres, courantes=True),
                # 13/10/2026 (encadre 2) : ce que les « Une fois revele » du
                # nouveau stade ont fait sur la table (faces A et B ensemble :
                # elles se resolvent dans le meme appel). Meme photo que les
                # cartes rencontre revelees.
                **WorldStat._EffetsDuStade(world, photo_avant, apres),
            })
        except Exception:
            pass

    @staticmethod
    def StatsDuStade(face: 'Any', courantes: bool) -> 'Dict[str, int]':
        """Les valeurs qu'un changement de stade fait varier, celles que la
        carte porte seulement (un mechant n'a pas de seuil, une manigance pas
        d'ATQ). `courantes` ajoute la menace posee, lue sur la carte en jeu."""
        noms = {'pv_max': 'max_health', 'atq': 'attack', 'man': 'scheme', 'seuil': 'target_threat'}
        if courantes:
            noms['menace'] = 'threat'
        stats: 'Dict[str, int]' = {}
        try:
            for cle, attribut in noms.items():
                valeur = getattr(face, attribut, None)
                if isinstance(valeur, int) and not isinstance(valeur, bool):
                    stats[cle] = valeur
        except Exception:
            pass
        return stats

    def NouvelleActivation(self, round_id: int) -> int:
        """Le numero de la prochaine activation ennemie de ce round.

        Un COMPTEUR, et non une identite de carte : le meme vilain s'active
        plusieurs fois dans un round (une carte de rencontre peut le faire
        frapper une seconde fois), et deux activations qui partageraient un
        identifiant se remplaceraient l'une l'autre dans le journal — le joueur
        n'en verrait qu'une.
        """
        self._DemarrerLeRound(round_id)
        self._activation_suivante += 1
        return self._activation_suivante

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

