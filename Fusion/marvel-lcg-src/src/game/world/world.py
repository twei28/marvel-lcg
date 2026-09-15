from typing import Final, TypeAlias
from core import *

from game.card.face import *
from game.ability import *
from game.player import *
from game.deck import *
from game.scene import *
from game.message import *
from engine.job import JobManager
from engine.controller import *
from game.world.game_area import *
from engine.lib import Json
from game.world.game_over import GameOverReason
from game.world.competitive import Competitive

from game.world.world_action import WorldAction
from game.world.world_find import WorldFind
from game.world.phase import Phase, PhaseName

from game.world.variable import Variable
from game.world.world_rule import WorldRule
from game.world.world_stat import WorldStat
from game.world.world_render import WorldRender
from game.world.cheat.cheat_cmd import CheatCommand

GAME_OVER: TypeAlias = Literal[True, False]

class World(WorldAction, WorldFind):

    def __init__(self, scene: 'Scene', controllers: List['Controller']) -> None:
        from game.deck import Deck2, DeckType
        from game.card.face.base import SchemeSide2
        from game.card.face.card_type import Environment
        from game.card.face.card_type import MainScheme
        from game.event.manager import EventManager
        from game.buff.manager import BuffManager
        # from game.message.on_event.manager import OnEventManager
        from game.object.manager import ObjectManager
        from game.operate.worlds import Worlds
        from game.world.limit_monitor import PlayerSideSchemeLimit

        self.object_manager = ObjectManager()
        self.rule = WorldRule()
        self.render = WorldRender(self)

        self.scenario = Scenario("Scenario", self)
        scenario = self.GetScenario()

        self.game_areas: List['GameArea'] = [GameArea(self)]

        self.players: List['Player'] = []
        # Add separate game area
        # Cards and components in one game area cannot affect another game area
        # Players cannot attack or defend enmies in other game areas
        # Players cannot target any game elements in the other game areas

        self.const_seat_order_players: List['Player'] = []
        self.current_player: 'Player|None' = None
        self.asking_player: List['Player'] = []

        self.phase = Phase()
        self.stat = WorldStat()
        self.store = Variable()

        self.area_removed       = Deck2(scenario, DeckType.RemovedArea, CardFace)
        self.area_insert        = Deck2(scenario, DeckType.RemovedArea, Insert)
        self.area_status_cards  = Deck2(scenario, DeckType.RemovedArea, CardFace)
        self.aside_deck         = Deck2(scenario, DeckType.AsideDeck, CardFace)
        self.aside_modular      = Deck2(scenario, DeckType.AsideDeck, CardFace)
        self.area_boosting      = Deck2(scenario, DeckType.BoostingArea, CardFace)
        self.area_environment   = Deck2(scenario, DeckType.EnvironmentArea, Environment)
        self.area_evidence      = Deck2(scenario, DeckType.EvidenceArea, Evidence)
        self.area_rule          = Deck2(scenario, DeckType.RuleArea, CardFace)
        self.area_processing    = Deck2(scenario, DeckType.ProcessingArea, CardFace)
        self.area_revealing     = Deck2(scenario, DeckType.RevealingArea, CardFace)

        self.victory_display    = Deck2(scenario, DeckType.VictoryDisplay, CardFace)

        self.area_schemes_main  = Deck2(scenario, DeckType.MainSchemesArea, MainScheme)
        self.area_schemes_side  = Deck2(scenario, DeckType.SideSchemesArea, SchemeSide2)
        self.main_schemes_deck  = Deck2(scenario, DeckType.MainSchemesDeck, MainScheme)

        self.round_id = 0
        self.phase_id = 0
        self.event_manager = EventManager(self)
        self.buff_manager = BuffManager(self)
        # self.on_event_manager = OnEventManager(self)
        self.scene = scene

        self.game_over = GameOverReason(self)
        # Fin de partie a deux camps. Inerte hors mode competitif : rien ne
        # l'interroge, et aucune condition ne s'y enregistre.
        self.competitive = Competitive(self)
        # Mode competitif : les cartes joueur du leader de chaque camp, mises
        # de cote a l'etape 3 de la mise en place (mc56 p.14). Vide ailleurs.
        self.team_set_aside: Dict[int, 'Deck'] = {}

        player_num = len(scene.players)

        for i in (0, 1, 2, 3)[:player_num]:
            player = Player(scene.players[i].name, controllers[i], i, self)
            self.players.append(player)
            self.const_seat_order_players.append(player)

        self.started_player_num: Final = player_num

        self.additional_decks: List[Deck] = []
        self.additional_discard_piles: List[Deck] = []

        self.scenario_decks: Dict[Worlds.ASIDE_DECK_NAME, SetAsideDeck] = {}
        for name in Types.LiteralToList(Worlds.ASIDE_DECK_NAME):
            self.scenario_decks[name] = SetAsideDeck()

        self.limit_player_side_scheme = PlayerSideSchemeLimit(self)
        self.controller_manager = controllers[0].manager
        self.cheat = CheatCommand(self)

        from game.operate.campaign_logs import CampaignLog
        for name in scene.campaign.campaign_log:
            value = scene.campaign.campaign_log[name]
            CampaignLog.SetStr(name, value, self)

        self.insert: Insert

    ################################################################################
    #
    def LoadFromJson(self, file_name: str, controllers: List['Controller']) -> None:
        from game.render.descriptor.world import WorldDescriptor
        from game.card.factory import CardFactory

        world_descriptor = Json.LoadAs(file_name, WorldDescriptor)
        self.players = []
        for i in (0, 1, 2, 3)[:world_descriptor.players]:
            player = Player(world_descriptor.players[i].area_hero[0].name, controllers[i], i, self)
            self.players.append(player)
            self.const_seat_order_players.append(player)
            player.setup.SelectIdentity(player.name,
                [world_descriptor.players[i].area_hero[0].card_id] + world_descriptor.players[i].area_hero[0].down_card_ids,
                [], [], [], [])

            for card in world_descriptor.players[i].player_deck:
                CardFactory.GenerateCard(card.card_id, self.players[0].player_deck, self)

            for card in world_descriptor.players[i].hand_cards:
                CardFactory.GenerateCard(card.card_id, self.players[0].hand_cards, self)

            pass

        for card in world_descriptor.villain_deck:
            CardFactory.GenerateCard(card.card_id, self.scenario.villain_deck, self)

    ################################################################################
    #
    def GetScenario(self) -> 'Scenario':
        return self.scenario

    def GetFirstGameArea(self) -> 'GameArea':
        return self.game_areas[0]

    def CreateGameArea(self) -> 'GameArea':
        self.game_areas.append(GameArea(self))
        return self.game_areas[-1]

    ################################################################################
    # Camps (mode competitif, livret mc56 p.14-17)
    #
    # Un camp EST une zone de jeu : l'equipe 0 joue dans `game_areas[0]`,
    # l'equipe 1 dans `game_areas[1]`. Rien d'autre n'est a retenir, le moteur
    # filtrant deja par zone les complots, les manigances, les sbires et le
    # deck rencontre. Hors mode competitif il n'existe qu'une zone, et toutes
    # ces fonctions rendent 0 / tous les joueurs / la premiere zone.
    def GetTeamOfPlayer(self, player: 'Player') -> int:
        # Le camp est pose une fois pour toutes par `SetupTeamGameAreas`. On ne
        # le relit PAS depuis la zone de l'identite : un joueur elimine perd sa
        # table, et le decompte des camps a besoin de lui jusqu'au bout
        # (mc56 p.17, « defeats all their opponents' identities »).
        return player.team

    def GetTeamPlayers(self, team: int) -> List['Player']:
        return [x for x in self.const_players if self.GetTeamOfPlayer(x) == team]

    def GetTeamGameArea(self, team: int) -> 'GameArea':
        while len(self.game_areas) <= team:
            self.CreateGameArea()
        return self.game_areas[team]

    def GetPhasePlayers(self, team: 'int|None') -> List['Player']:
        """Les joueurs concernes par une phase.

        `None` veut dire « tout le monde » : c'est le cas hors mode competitif,
        ou une phase appartient a la partie entiere. En competitif, chaque camp
        joue SA phase heros puis SA phase vilain (mc56 p.16), et une phase ne
        concerne donc que les joueurs d'un camp.
        """
        if team is None:
            return self.const_players
        return self.GetTeamPlayers(team)

    def PassFirstPlayerToken(self, team: int, by_effect: 'Effect') -> None:
        """Fait tourner le jeton de premier joueur A L'INTERIEUR d'un camp.

        « In a 2v2 game, each team has its own first player token that passes
        at the end of their villain phase » (mc56 p.16). L'ordre des joueurs
        vit dans une seule liste, `self.players`, dont `players[0]` est le
        premier joueur : on ne tourne donc que les places tenues par ce camp,
        et l'autre camp garde exactement les siennes.
        """
        from game.message import Message
        from game.effect.rule import GameRule

        places = [i for i, x in enumerate(self.players) if self.GetTeamOfPlayer(x) == team]
        if len(places) > 1:
            tournes = Types.Rotate([self.players[i] for i in places], 1)
            for place, player in zip(places, tournes):
                self.players[place] = player

        for player in self.GetTeamPlayers(team):
            identity = player.GetIdentity()
            identity.SetActive(GameRule(identity))
            break

        message = Message.AfterPlayersOrderChange(self, by_effect)
        message.Send()

    def GetTeamOfGameArea(self, game_area: 'GameArea') -> int:
        if game_area in self.game_areas:
            return self.game_areas.index(game_area)
        return 0

    def GetOtherTeam(self, team: int) -> int:
        """Le camp d'en face. Le livret n'en connait que deux (mc56 p.14)."""
        return 1 - team if team in (0, 1) else 0

    def CompetitiveEncounterSets(self, names: List[str]) -> List[str]:
        """« Replace the standard set with the standard PvP set when playing
        in competitive mode » (mc56 p.4). Le meme fichier de scenario sert aux
        deux modes : le remplacement se fait donc au lancement, pas dans les
        donnees, sinon une partie cooperative recevrait le set PvP.
        """
        if not self.rule.mode_competitive:
            return names
        return ["standard_pvp" if x == "standard" else x for x in names]

    def SetupTeamGameAreas(self) -> None:
        """Assied chaque joueur a la table de son camp.

        Le camp vient du descripteur (`HeroDescriptor.team`). Un joueur du
        camp 0 ne bouge pas : il est deja dans la premiere zone.
        """
        for i, player in enumerate(self.const_seat_order_players):
            if i >= len(self.scene.players):
                continue
            team = self.scene.players[i].team
            player.team = max(0, team)
            if team <= 0:
                continue
            self.GetTeamGameArea(team).AddPlayer(player)

    def GetTeamSetAside(self, team: int) -> 'Deck':
        """Les cartes joueur du leader d'un camp, mises de cote (mc56 p.14).

        Une zone par camp, et pas une par joueur : les 4 cartes appartiennent a
        l'equipe, qui se les partage a deux en 2v2 (p.16)."""
        from game.deck import Deck2, DeckType
        from game.card.face.card_face import CardFace

        if team not in self.team_set_aside:
            self.team_set_aside[team] = Deck2(self.GetScenario(), DeckType.AsideDeck, CardFace)
        return self.team_set_aside[team]

    def SetupTeamLeaderCards(self) -> None:
        """Etape 3 de la mise en place competitive (mc56 p.14).

        « Each team finds their chosen leader's basic player cards and sets
        them aside. » Le leader d'un camp est celui pose sur la table d'EN
        FACE, puisque les equipes echangent leurs scenarios (p.14, etape 4) :
        le camp 0 a apporte `campaign_2`, le camp 1 a apporte `campaign`.
        """
        from game.card.factory import CardFactory

        apportes = {0: self.scene.campaign_2, 1: self.scene.campaign}
        for team, campaign in apportes.items():
            if not campaign or not campaign.villain:
                continue
            cartes = Competitive.CartesDuLeader(campaign.villain[0])
            if not cartes:
                continue
            deck = self.GetTeamSetAside(team)
            CardFactory.GenerateCards(cartes, deck, self)
            Message.TextRender(
                f"\n--- Cartes du leader mises de cote pour {Competitive.NOMS[team]} : "
                f"{len(cartes)} ---", self)

    def SetupSecondTable(self, game_start_effect: 'Effect') -> 'Deck|None':
        """Monte la table du second camp : son complot, son leader, son deck.

        Chaque equipe apporte SON scenario et affronte celui de l'autre
        (mc56 p.14, etape 4). La seconde table vit dans sa propre zone de jeu.

        Rend son deck rencontre, pour que l'etape 11 de la mise en place y
        cherche aussi les cartes qui portent le mot-cle Setup.
        """
        from game.card.factory import CardFactory
        from game.message import Message
        from game.effect.rule import GameRule
        from game.operate.faces import Faces
        from game.card.face.base import Villain

        campaign = self.scene.campaign_2
        assert campaign.villain, "mode competitif : le second camp n'apporte pas de leader"
        assert campaign.schemes, "mode competitif : le second camp n'apporte pas de complot principal"

        game_area = self.GetTeamGameArea(1)
        players = self.GetTeamPlayers(1)
        assert players, "mode competitif : le second camp n'a aucun joueur"
        first_player = players[0]
        scenario = self.GetScenario()

        # Son complot principal.
        scheme_cards = CardFactory.GenerateCards(campaign.schemes, self.main_schemes_deck, self)
        assert scheme_cards
        for card in scheme_cards:
            game_area.AddCard(card)
        scheme_cards[0].face.PutIntoPlay(first_player, GameRule(scheme_cards[0].face),
                                         target_game_area=game_area)

        # Son leader. Les cartes naissent dans la premiere zone (factory.py) :
        # on les deplace avant qu'elles servent a quoi que ce soit.
        villain_cards = CardFactory.GenerateCards(campaign.villain, scenario.villain_deck, self)
        assert villain_cards
        for card in villain_cards:
            game_area.AddCard(card)

        # Son deck rencontre. Le message de mise en place est renvoye pour
        # CETTE table : une carte qui change la preparation (sets de rencontre,
        # cartes mises de cote) doit pouvoir le faire pour la sienne.
        message = Message.WhenGameBeginSetup(campaign, self)
        message.Send()

        deck, _ = scenario.CreateEncounterDeck()
        scenario.extra_encounter_decks.append(deck)

        if not message.skip_create_encounter_deck:
            encounters: List[str] = campaign.encounters[:]
            for encounter_set in self.CompetitiveEncounterSets(message.encounter_set_names):
                encounters += CardFactory.LoadEncounterSet(encounter_set)
            CardFactory.GenerateCards(encounters, deck, self)
            Message.WhenDeckCreated_Text(deck)

            # Les obligations d'un joueur vont dans le deck qu'il AFFRONTE,
            # c'est-a-dire celui de sa propre table.
            if not message.no_use_obligation:
                for player in players:
                    Faces.MoveAllToDeck([x.face for x in player.set_aside_obligations],
                                        deck, "Top", game_start_effect)

            for card in deck.GetAll():
                if card.card.GetGameArea() != game_area:
                    game_area.AddCard(card.card)

            deck.Shuffle(game_start_effect)
            message.CreateSetAside()
            message.CreateSetAsideModular()

        # Le leader entre en jeu APRES : `Villain.OnPutIntoPlay` lui attache le
        # deck rencontre du scenario, on lui rend ensuite le sien.
        if not message.skip_put_villain_into_play:
            leader = villain_cards[0].face
            leader.PutIntoPlay(first_player, game_start_effect, target_game_area=game_area)
            villain = leader.CastTo(Villain)
            villain.SetEncounterDeck(deck)

        return deck

    def SelectScenario(self, villains: Sequence[str], schemes: Sequence[str]) -> None:
        from game.card.factory import CardFactory
        from game.effect.rule import GameRule

        main_schemes = CardFactory.GenerateCards(schemes, self.main_schemes_deck, self)
        main_scheme = main_schemes[0].face

        main_scheme.PutIntoPlay(self.GetFirstPlayer(), GameRule(main_scheme))

        self.GetScenario().SelectVillain(villains)

    def Initialize(self) -> None:
        from game.card.factory import CardFactory
        from game.message import Message
        from game.effect.rule import GameRule
        from game.operate.worlds import Worlds
        from game.operate.faces import Faces

        # We register these ability bind card main scheme
        self.event_manager.RegisterPlayRule()

        initialize_message = Message.WhenGameInitialize(self)
        initialize_message.Send()

        Message.TextRender("\n--- Select Hero and Villain ---", self)
        # [x] 1. Select Identities
        # [x] 2. Set Hit Points
        # [x] 3. Select First Player
        # [x] 4. Set Aside Obligation
        # [x] 5. Set Aside Nemesis Sets
        # [x] 6. Shuffle Player Decks
        for player in self.const_players:
            i = self.const_players.index(player)
            scene_player = self.scene.players[i]
            player.setup.SelectIdentity(scene_player.name, scene_player.hero, scene_player.hero_deck, scene_player.obligations, scene_player.nemesis_set, scene_player.player_deck)

        if self.is_game_over:
            return

        identity = self.const_players[0].GetIdentity()
        identity.SetActive(GameRule(identity))


        # [x] 7. Collect Tokens and Status Cards
        # [x] 8. Select Scenario
        campaign = self.scene.campaign

        # Mode competitif : chaque camp a sa table. On l'ouvre AVANT de monter
        # les scenarios, pour que les cartes du second camp naissent, se
        # deplacent et se revelent dans la bonne zone.
        if self.rule.mode_competitive:
            self.SetupTeamGameAreas()
            # « Each team has its own first player token » (mc56 p.16) : le
            # jeton pose plus haut est celui du camp 0, il en faut un second
            # pour le camp 1. `SetActive` ne retire le jeton qu'aux joueurs du
            # meme camp, les deux coexistent donc.
            for team in (0, 1):
                for player in self.GetTeamPlayers(team):
                    team_identity = player.GetIdentity()
                    team_identity.SetActive(GameRule(team_identity))
                    break

        if self.rule.mode_skirmish:
            villain = [identity.GetControlByPlayer().AskChoosePaper(campaign.villain)]
        else:
            villain = campaign.villain
        self.SelectScenario(villain, campaign.schemes)

        if self.is_game_over:
            return

        game_start_effect = GameRule(Worlds.GetAllMainSchemes(self)[0])

        Message.TextRender("\n--- Set Up ---", self)
        message = Message.WhenGameBeginSetup(campaign, self)
        message.Send()

        # [x] 9. Set the Villain’s Hit Points
        scenario = self.GetScenario()
        if not message.skip_put_villain_into_play:
            if scenario.villain_deck.GetSize():
                villain = scenario.villain_deck.Get()[0]
                player = self.GetFirstPlayer()
                villain.PutIntoPlay(player, game_start_effect)

        if self.is_game_over:
            return

        # [x] 10. Create and Shuffe Encounter Deck
        if not message.skip_create_encounter_deck:
            encounters: List[str] = campaign.encounters[:]
            from game.card.factory import CardFactory
            for encounter_set in self.CompetitiveEncounterSets(message.encounter_set_names):
                encounters += CardFactory.LoadEncounterSet(encounter_set)

            CardFactory.GenerateCards(encounters, scenario.encounter_deck, self)
            Message.WhenDeckCreated_Text(scenario.encounter_deck)

            if not message.no_use_obligation:
                # Un joueur affronte le deck rencontre de SA table. En partie
                # ordinaire il n'y en a qu'une ; en competitif, les obligations
                # du second camp partent dans son deck a lui, monte plus bas.
                obligation_players = self.GetTeamPlayers(0) if self.rule.mode_competitive else self.const_players
                for player in obligation_players:
                    Faces.MoveAllToDeck([x.face for x in player.set_aside_obligations], scenario.encounter_deck, "Top", game_start_effect)

            if self.rule.crisis_of_infinite_deadpools:
                used_pool_aspect = False
                for player in self.const_players:
                    if player.player_deck.FindCardSize(CardFinder(card_class="'Pool")):
                        used_pool_aspect = True
                        break
                if used_pool_aspect:
                    dreadpool = CardFactory.LoadEncounterSet("dreadpool")
                    CardFactory.GenerateCards(dreadpool, self.aside_deck, self)
                    Message.WhenDeckCreated_Text(self.aside_deck)

                    face = self.aside_deck.FindCard(name="44037")
                    if face:
                        Faces.MoveAllTo([face], scenario.encounter_deck, game_start_effect)

            scenario.encounter_deck.Shuffle(game_start_effect)

            message.CreateSetAside()
            message.CreateSetAsideModular()

        if self.is_game_over:
            return

        # Mode competitif : la table du second camp, avec son complot
        # principal, son leader et son propre deck rencontre.
        second_encounter_deck: 'Deck|None' = None
        if self.rule.mode_competitive:
            second_encounter_deck = self.SetupSecondTable(game_start_effect)
            # Etape 3 : les 4 cartes joueur du leader de chaque camp. Elles
            # arrivent apres les deux tables, parce qu'elles se lisent depuis
            # le scenario APPORTE par chaque camp, celui d'en face.
            self.SetupTeamLeaderCards()

        if self.is_game_over:
            return

        # Move nemesis sets
        for player in self.const_players:
            faces = [card.face for card in player.set_aside_obligations if card.face in player.set_aside_nemesis_sets.Get()]
            Faces.RemoveAllFromGame(faces, game_start_effect)

        if self.is_game_over:
            return

        # For 21165a
        for scheme in Worlds.GetAllMainSchemes(self):
            scheme.Setup(True)

        # [x] 11. Put Setup Cards Into Play
        # A card with the setup keyword begins the game in play.
        decks = [x.player_deck for x in self.const_players] + \
                [x.set_aside_nemesis_sets for x in self.const_players] + \
                [self.GetScenario().encounter_deck] + \
                ([second_encounter_deck] if second_encounter_deck else []) + \
                self.additional_decks
        faces = [x for y in decks for x in y.GetAll() if HasSetup.IsType(x) and x.printed_setup > 0]
        for face in faces:
            face.ProcessSetup(game_start_effect)

        if self.is_game_over:
            return

        # [x] 12. Resolve Scenario Setup and When Revealed abilities
        self.phase.SetState(Phase.State.ScenarioSetup)
        for scheme in Worlds.GetAllMainSchemes(self):
            scheme.Setup(False)
            scheme.Advance(None, game_start_effect) # Has already reveal here

        for villain in Worlds.GetAllVillains(self):
            villain.Setup(False)
            villain.Reveal(None, game_start_effect)

        # Evidence
        faces = [x for y in decks for x in y.GetAll() if Evidence.IsType(x)]
        for face in faces:
            face.Setup(False)

        if self.is_game_over:
            return

        # [x] 13. Campaign Setup
        campaign_message = Message.WhenCampaignSetup(self)
        campaign_message.Send()

        # [x] 14. Draw Cards
        Message.TextRender("\n--- Draw Cards ---", self)
        if not self.rule.disable_setup_draw_cards:
            for player in self.const_players:
                player.DrawUp("Max", game_start_effect)

        # [x] 15. Resolve Mulligans
        self.phase.SetState(Phase.State.ResolveMulligans)
        Message.TextRender("\n--- Resolve Mulligans ---", self)
        if not self.rule.disable_resolve_mulligans:
            def process_player(player: 'Player'):
                player.phase.ResolveMulligans(Message.WhenPlayerResolveMulligans(player))
            JobManager.Simultaneous(process_player, self.const_players)

        if self.rule.additional_resolve_mulligans:
            def process_player(player: 'Player'):
                player.phase.ResolveMulligans(Message.WhenPlayerResolveMulligans(player))
            JobManager.Simultaneous(process_player, self.const_players)

        # [x] 15 bis. Campaign Setup, la part qui attend la fin des mulligans
        # Les encarts des scenarios 2 a 5 d'Agents of S.H.I.E.L.D. le disent
        # mot pour mot : « After resolving mulligans, resolve the "Setup"
        # ability of each evidence card the players have earned ». C'est le
        # seul endroit ou une carte peut chercher dans le deck et l'ajouter a
        # une main deja piochee et deja mulliganee.
        campaign_message = Message.WhenCampaignSetupAfterMulligans(self)
        campaign_message.Send()

        if self.is_game_over:
            return

        # [x] 16. Resolve Character Setup Abilities
        Message.TextRender("\n--- Resolve Character Setup Abilities ---", self)
        for player in self.const_players:
            player.GetIdentity().Setup(False)

        if self.is_game_over:
            return

        if self.rule.ex_start_hand_size:
            for player in self.const_players:
                player.DrawUp(self.rule.ex_start_hand_size, game_start_effect)

        self.phase.SetState(Phase.State.InitFinished)

        begin_message = Message.WhenGameWouldBegin(self)
        begin_message.Send()
        return

    ################################################################################
    # Phase
    def PlayerPhase(self, team: 'int|None'=None) -> None:

        def turn_begin():
            self.stat.OnTurnBegin()
        def turn_end():
            self.stat.OnTurnEnd()

        self.phase.SetState(Phase.State.PlayerTurn)

        def get_player_phase_order():
            players = self.GetPhasePlayers(team)[:]
            for player in players:
                if player.flag.Get("YOU_TAKE_THE_FIRST_TURN_DURING_THE_PLAYER_PHASE"):
                    players.remove(player)
                    players.insert(0, player)
            return players

        for player in get_player_phase_order():
            self.current_player = player
            turn_begin()
            player.phase.BeginTurn()
            player.phase.PlayerTurn()
            if self.is_game_over:
                return
            player.phase.EndTurn()
            turn_end()

        self.phase.SetState(Phase.State.PlayerTurnEnd)

    def PlayersEndPhase(self, team: 'int|None'=None) -> None:
        def process_player(player: 'Player'):
            player.phase.EndPhase()
        JobManager.Simultaneous(process_player, self.GetPhasePlayers(team))

    def VillainPhase(self, team: 'int|None'=None) -> None:
        from game.message import Message
        from game.effect.rule import GameRule
        from game.operate.worlds import Worlds

        phase_players = self.GetPhasePlayers(team)

        for player in phase_players:
            player.stat.this_phase_revealed_cards = []

        def process_villain_phase_step(step: int, callback: Callable[[], None], phase: 'Phase.State') -> None:
            self.phase.SetState(phase)

            step_message = Message.WhenVillainPhaseStepStart(step, self)
            step_message.Send()

            callback()

            if self.is_game_over:
                return

            after_step_message = Message.AfterResolveVillainPhaseStep(step, step_message)
            after_step_message.Send()
            return

        def place_threat() -> None:
            self.current_player = None
            start_message = Message.WhenMainSchemePhaseStart(self)
            start_message.Send()
            # Seul le complot de la table qui joue avance : l'autre table
            # avancera le sien pendant SA phase vilain.
            schemes = Worlds.GetAllMainSchemes(self) if team is None \
                else Worlds.GetMainSchemes(self.GetTeamGameArea(team))
            for scheme in schemes:
                scheme.Phase()
            end_message = Message.WhenMainSchemePhaseEnd(self)
            end_message.Send()

        def enemy_activation() -> None:
            for player in phase_players:
                self.current_player = player
                effect = GameRule(player.GetIdentity())
                Worlds.Enemies.VillainAndEngagedMinionsActivateAgainstYou(effect, player)
            return

        def deal_encounter_cards() -> None:
            Message.TextRender("\n--- Encounter Cards Phase ---", self)
            num = 1 + self.rule.mode_heroic

            hazards: Dict[GameArea, List[HasHazard]] = {}
            for player in phase_players:
                game_area = player.GetGameArea()

                if game_area not in hazards:
                    hazards[game_area] = Worlds.GetHazardFaces(game_area)

                self.current_player = player
                player.DealEncounterCards(num, GameRule(player.GetIdentity()))

            for game_area in hazards:
                while hazards[game_area]:
                    for player in game_area.FindAllPlayers():
                        for face in hazards[game_area][:]:
                            player.DealEncounterCards(1, GameRule(face))
                            hazards[game_area].remove(face)
                            break
                        if self.is_game_over:
                            return
            return

        def reveal_encounter_cards() -> None:
            while any(player.dealt_encounter_cards.GetSize() != 0 for player in phase_players):
                for player in phase_players:
                    self.current_player = player
                    player.RevealEncounterCards()
                    if self.is_game_over:
                        return
            return

        # STEP ONE  - PLACE THREAT
        # STEP TWO  - VILLAIN AND MINION ACTIVATIONS
        # STEP THREE - DEAL ENCOUNTER CARDS
        # STEP FOUR - REVEAL ENCOUNTER CARDS
        steps_data: Final = {
            1: (place_threat,           Phase.State.PlaceThreat),
            2: (enemy_activation,       Phase.State.EnemyActivation),
            3: (deal_encounter_cards,   Phase.State.DealEncounterCards),
            4: (reveal_encounter_cards, Phase.State.RevealsEncounterCards),
        }
        for step_number, (action, state) in steps_data.items():
            process_villain_phase_step(step_number, action, state)
            if self.is_game_over:
                return
        return

    def OnGameLoop(self) -> None:
        from game.message import Message
        from game.effect.rule import GameRule

        def game_round() -> None:

            def start_round() -> None:
                self.phase.SetState(Phase.State.StartRound)
                self.current_player = None
                self.round_id += 1
                start_message = Message.WhenRoundStart(self.round_id, self)
                start_message.Send()

                for player in self.const_players:
                    player.phase.BeginRound()

                self.controller_manager.OnBeginRound()

            def end_round() -> None:
                self.phase.SetState(Phase.State.EndRound)
                self.current_player = None
                round_message = Message.WhenRoundEnd(self)
                round_message.Send()
                self.stat.OnRoundEnd()
                self.buff_manager.OnRoundEnd()

                for player in self.const_players:
                    player.phase.EndRound()

                # Pass the first player token clocwise to the next player.

                end_round_effect = GameRule(self.const_players[0].GetIdentity())
                # En competitif le jeton a deja tourne, camp par camp, a la fin
                # de chaque phase vilain (mc56 p.16) : le faire tourner une
                # seconde fois ici le ferait changer de camp.
                if not self.rule.mode_competitive:
                    self.players = Types.Rotate(self.players, 1)
                    self.UpdatePlayersOrder(end_round_effect)
                self.ProcessTemporary(end_round_effect)

                end_message = Message.AfterRoundEnd(round_message)
                end_message.Send()

            def phase_begin(phase_type: PhaseName) -> None:
                self.phase_id += 1

                phase_message = Message.WhenPhaseBegin(phase_type, self)
                phase_message.Send()

                for player in self.const_players:
                    player.phase.BeginPhase()

                self.controller_manager.OnBeginPhase()

                begin_message = Message.AfterPhaseBegin(phase_message)
                begin_message.Send()

            def phase_end(phase_type: PhaseName) -> None:
                from game.message import Message

                self.phase.SetState(Phase.State.EndPhase)
                self.current_player = None

                phase_message = Message.WhenPhaseEnd(self.phase_id, phase_type, self)
                phase_message.Send()

                self.stat.OnPhaseEnd()

                end_message = Message.AfterPhaseEnd(self.phase_id, phase_type, phase_message)
                end_message.Send()

            start_round()
            if self.is_game_over:
                return

            # L'ordre du round. Hors mode competitif, une seule phase heros et
            # une seule phase vilain pour toute la table : `None` veut dire
            # « tous les joueurs », et la suite est mot pour mot celle d'avant.
            #
            # En competitif, le round est ENFILE (mc56 p.16) : phase heros du
            # camp 0, phase heros du camp 1, PUIS phase vilain du camp 0, puis
            # phase vilain du camp 1. Le camp 0 (registration) joue en premier.
            teams: List['int|None'] = [None]
            if self.rule.mode_competitive:
                teams = [0, 1]

            for team in teams:
                phase_begin("Player")
                if self.is_game_over:
                    return
                self.PlayerPhase(team)
                if self.is_game_over:
                    return
                self.PlayersEndPhase(team)
                if self.is_game_over:
                    return
                phase_end("Player")
                if self.is_game_over:
                    return
                self.competitive.AFinDePhase(team)
                if self.is_game_over:
                    return

            for team in teams:
                phase_begin("Villain")
                if self.is_game_over:
                    return
                self.VillainPhase(team)
                if self.is_game_over:
                    return
                phase_end("Villain")
                if self.is_game_over:
                    return
                # « each team has its own first player token that passes at the
                # end of their villain phase » (mc56 p.16).
                if team is not None:
                    self.PassFirstPlayerToken(team, GameRule(self.const_players[0].GetIdentity()))
                self.competitive.AFinDePhase(team)
                if self.is_game_over:
                    return

            end_round()


        while not self.is_game_over:
            game_round()

    def OnGameOver(self, reason: 'GameOverReason'):
        from game.message import Message
        assert reason.reason != None
        Message.GameOver_Text(reason.players_won, reason.reason, reason.by_effect, self)

    ################################################################################
    #
    def SetGameOver(self, player_won: bool, by_effect: 'Effect'):
        return self.game_over.SetPlayersWon(player_won, by_effect)

    @property
    def is_game_over(self) -> bool:
        return self.game_over.is_game_over

    @property
    def is_game_started(self) -> bool:
        return self.phase.IsGameStarted()

    @property
    def is_initializing(self) -> bool:
        return self.phase.IsGameInitializing()

    ################################################################################
    # Advance

    # Le nom TECHNIQUE de l'option de confirmation de la face A. Il ne
    # s'affiche jamais tel quel : le plateau le reconnait et pose son propre
    # libelle traduit. Sans espace, parce que le moteur remplace les espaces
    # par des underscores dans les noms d'options publies.
    CONFIRM_MAIN_SCHEME_OPTION = "Reveal_Main_Scheme"

    def ConfirmMainSchemeReveal(self, scheme: 'MainScheme') -> None:
        """Le premier joueur retourne la manigance, comme sur une vraie table.

        ⚠ `forced=False`, ET C'EST TOUT LE SUJET. Mesure du 15/09/2026 : avec
        `forced=True` (le defaut de `AskChooseOneText`), une question a une
        seule option ne quitte JAMAIS le moteur —
        `PlayerAction.ChoiceAndSpellEffect` pose `need_choose = False` et
        choisit a la place du joueur. Le client n'a rien vu passer : 0 appel a
        `DoGetInput`. Avec `forced=False`, il est bien interroge.

        ⚠ Le premier joueur SEUL (decision du 15/09/2026) : c'est lui qui tient
        le jeton et qui retourne la carte. Personne d'autre n'est retenu.
        """
        from game.ability.factory import AbilityFactory
        from game.effect.rule import GameRule

        if not self.rule.confirm_main_scheme:
            return
        if self.is_game_over:
            return
        player = self.GetFirstPlayer()
        if player is None or player.is_eliminated:
            return

        ability = AbilityFactory.ForChoiceAbility(
            World.CONFIRM_MAIN_SCHEME_OPTION,
            lambda targets: None,
        )
        player.ChooseAbilities(GameRule(scheme), ability, forced=False)

    # Le nom TECHNIQUE de l'option pour une manigance ANNEXE. Meme role que
    # celui de la principale : le plateau le reconnait et pose son propre
    # libelle traduit.
    CONFIRM_SIDE_SCHEME_OPTION = "Reveal_Side_Scheme"

    def ConfirmSideSchemeReveal(self, scheme: 'CardFace') -> None:
        """Le premier joueur prend connaissance d'une manigance annexe qui arrive.

        Demande de l'utilisateur, 15/09/2026 : « s'il y a une sidescheme qui
        commence en partie je veux qu'on la voie aussi comme la principale, idem
        quand une sidescheme arrive en jeu apres ».

        ⚠ SEULEMENT CE QUE LE SCENARIO IMPOSE. Une manigance-joueur
        (`PlayerSideScheme`) est jouee depuis la main : le joueur vient de la
        lire et de la choisir, un panneau ne lui apprendrait rien et lui
        couterait un clic. Decision du 15/09/2026.

        ⚠ APRES l'entree en jeu, et non avant : le panneau MONTRE la carte, elle
        doit donc etre sur la table quand la question part.

        ⚠ `forced=False` pour la meme raison que la principale : une question a
        une seule option avec `forced=True` n'atteint jamais le client, le
        moteur y repond a la place du joueur (mesure du 15/09/2026).
        """
        from game.ability.factory import AbilityFactory
        from game.effect.rule import GameRule
        from game.card.face.card_type.scheme_side import EncounterSideScheme

        if not self.rule.confirm_side_scheme:
            return
        if self.is_game_over:
            return
        if not EncounterSideScheme.IsType(scheme):
            return
        player = self.GetFirstPlayer()
        if player is None or player.is_eliminated:
            return

        ability = AbilityFactory.ForChoiceAbility(
            World.CONFIRM_SIDE_SCHEME_OPTION,
            lambda targets: None,
        )
        player.ChooseAbilities(GameRule(scheme), ability, forced=False)

    def AdvanceMainScheme(self, prev_scheme: 'MainScheme', to_face: Literal["2A", "3A"]|CardFace|None, by_effect: 'Effect'):
        from game.message import Message
        from game.effect.rule import GameRule
        from game.operate.faces import Faces

        assert prev_scheme.card.back_faces, f"{prev_scheme.card=}"
        message = Message.WhenMainSchemeWouldAdvance(prev_scheme, by_effect)
        message.Send()
        if message.is_be_instead:
            return
        if prev_scheme.card.printed_faces[0] == prev_scheme:
            card = prev_scheme.card
            # Le temps d'arret sur la face A. Cette branche est la SEULE qui
            # retourne une face A, mise en place et changements d'etape
            # confondus : trace du 15/09/2026, 01097a a la mise en place et
            # 01117a a l'etape 2 y passent tous les deux.
            self.ConfirmMainSchemeReveal(prev_scheme)
            card.Flip(GameRule(card.face))
            # Reveal is call when `Filp`
            # card.face.Reveal(None, GameRule(card.face))
        elif self.main_schemes_deck.GetSize() > 0:
            if to_face == None:
                scheme = self.main_schemes_deck.Get()[0]
            elif to_face == "2A":
                scheme = self.main_schemes_deck.FindCard(CardFinder(stage=2), card_type=MainScheme)
                assert scheme != None
            elif to_face == "3A":
                scheme = self.main_schemes_deck.FindCard(CardFinder(stage=3), card_type=MainScheme)
                assert scheme != None
            else:
                scheme = to_face
                assert MainScheme.IsType(scheme)
            acceleration_token = prev_scheme.acceleration_token
            # Fix "32127b"
            if not prev_scheme.card.area.flags.is_victory_display:
                Faces.RemoveAllFromGame([prev_scheme], GameRule(prev_scheme))
            scheme.PlaceAccelerationToken(acceleration_token, GameRule(scheme))
            scheme.Reveal(None, by_effect)
        elif self.CountMainSchemesOfSameArea(prev_scheme) == 1:
            # En competitif, le complot accompli est celui d'UNE table : son
            # camp perd, la partie continue jusqu'a ce que les deux camps aient
            # joue autant de phases (mc56 p.17).
            if not self.RecordCompetitiveDefeat(prev_scheme, "complot principal accompli", by_effect):
                self.game_over.SetGameOverByRule("The Final Stage of the Main Scheme was Completed")
        after_message = Message.AfterMainSchemeAdvanced(message)
        after_message.Send()

    def CheckIsAllPlayersEliminated(self):
        if self.rule.mode_competitive:
            # « Whichever team's leader defeats all their opponents' identities
            # first wins » (mc56 p.17) : c'est le camp d'en face qui marque, et
            # chaque camp se compte a part. `const_seat_order_players` ne bouge
            # pas, contrairement a `const_players` d'ou un joueur elimine sort.
            fini = False
            for team in (0, 1):
                joueurs = [x for x in self.const_seat_order_players
                           if self.GetTeamOfPlayer(x) == team]
                if not joueurs:
                    continue
                if all(x.is_eliminated or x.GetIdentity().IsDefeated() for x in joueurs):
                    self.competitive.EnregistrerDefaite(
                        team, "tous les heros du camp sont vaincus", None)
                    fini = True
            return fini
        for player in self.const_players:
            if not player.GetIdentity().IsDefeated() and not player.is_eliminated:
                return False
        self.game_over.SetGameOverByRule("All players were eliminated")
        return True

    ################################################################################
    # Mode competitif : les conditions de fin sont enregistrees, pas appliquees
    def CountMainSchemesOfSameArea(self, scheme: 'MainScheme') -> int:
        """Combien de complots principaux vivent dans la zone de ce complot.

        Hors mode competitif il n'y a qu'une zone, et le compte est celui
        d'avant : la taille de `area_schemes_main`."""
        if not self.rule.mode_competitive:
            return self.area_schemes_main.GetSize()
        game_area = scheme.card.GetGameArea()
        return len([x for x in self.area_schemes_main.Get()
                    if x.card.GetGameArea() == game_area])

    def RecordCompetitiveDefeat(self, face: 'CardFace', raison: str, by_effect: 'Effect|None') -> bool:
        """Le camp de la table ou vit cette carte vient de perdre.

        Rend False hors mode competitif : l'appelant termine alors la partie
        comme avant."""
        if not self.rule.mode_competitive:
            return False
        team = self.GetTeamOfGameArea(face.card.GetGameArea())
        return self.competitive.EnregistrerDefaite(team, raison, by_effect)

    ################################################################################
    #
    def GetPhaseText(self) -> str:
        if self.phase.state == Phase.State.PlayerTurn:
            assert self.current_player != None
            return f"Player {self.const_seat_order_players.index(self.current_player)+1} Turn"
        else:
            return self.phase.state

