from core import *
from engine.lib import Json
from engine.file import FileManager
from engine.device import *

from aiohttp import web
from engine.device.web.server.server_base import GameServerBase
from engine.config import ConfigVariables

READ_ONLY_FIRST_REPLAY_FOLDER   = ConfigVariables.Bool('read_only_first_replay_folder', True)
CARDS_JSON_FILE         = ConfigVariables.File('cards_json_file')
REPLAY_FOLDERS          = ConfigVariables.Folders('replay_folders')
DECK_FOLDERS            = ConfigVariables.Folders('deck_folders')
STARTER_DECK_FOLDER     = ConfigVariables.Folder('starter_deck_folder')
ENCOUNTER_SETS_FOLDERS  = ConfigVariables.Folders('encounter_sets_folders')
SCENARIOS_FOLDERS       = ConfigVariables.Folders('scenarios_folders')
CUSTOM_SCENARIOS_FOLDER = ConfigVariables.Folder('custom_scenario_folder')
PUZZLE_FOLDER           = ConfigVariables.Folder('puzzle_folder')
PUZZLE_TEST_FOLDER      = ConfigVariables.Folder('puzzle_test_folder')

class GameServerGet(GameServerBase):

    def ListFile(self, *folders: str, ext: str|None=None) -> web.Response:
        return web.json_response(FileManager.ListFiles(*folders, ext=ext))

    async def list_file(self, request: web.Request) -> web.Response:
        return self.ListFile(request.path)

    async def list_scenarios(self, request: web.Request) -> web.Response:
        return self.ListFile(*SCENARIOS_FOLDERS.value, CUSTOM_SCENARIOS_FOLDER.value)

    async def list_encounter_sets(self, request: web.Request) -> web.Response:
        return self.ListFile(*ENCOUNTER_SETS_FOLDERS.value)

    async def list_deck(self, request: web.Request) -> web.Response:
        return self.ListFile(*DECK_FOLDERS.value, ext=".json")

    async def save_deck(self, request: web.Request) -> web.Response:
        # Sauvegarde d'un deck construit dans l'editeur web (deck-builder.html).
        # Ecrit un JSON au meme format que deck/starter/*.json dans le premier
        # dossier de deck_folders : il devient alors visible via /list_deck et
        # chargeable via /get_hero_json (FindJsonPath('Hero') couvre ce dossier).
        import os
        import re
        import json as json_lib
        data = await request.json()
        deck = data.get('deck', None)
        if (type(deck) is not dict) or (not deck.get('hero')):
            return web.json_response({'error': 'Invalid deck'}, status=400)
        raw_name = str(data.get('file_name', '') or deck.get('name', '') or 'deck')
        file_name = re.sub('[^a-zA-Z0-9_-]+', '_', raw_name).strip('_')[:60] or 'deck'
        folder = (DECK_FOLDERS.value[0] if DECK_FOLDERS.value else './deck/custom/')
        os.makedirs(folder, exist_ok=True)
        path = FileManager.JoinPath(folder, f'{file_name}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json_lib.dump(deck, f, ensure_ascii=False, indent=4)
        return web.json_response({'result': 'saved', 'file': path})

    async def sandbox_command(self, request: web.Request) -> web.Response:
        # Mode bac a sable : execute une commande Puzzle.* sur la partie EN COURS.
        # Le moteur sait deja poser une carte en jeu, regler des PV, une menace,
        # un statut... via l'API Puzzle ; on l'expose ici plutot que de reecrire
        # ces mecaniques. Puzzle.Exec n'autorise QUE les appels `Puzzle.<methode>`
        # (il rejette tout le reste a l'analyse syntaxique), donc pas d'execution
        # de code arbitraire.
        from game.puzzle.puzzle import PuzzleHelper

        data = await request.json()
        commands = data.get('commands', None)
        if isinstance(commands, str):
            commands = [commands]
        if not isinstance(commands, list) or not all(isinstance(c, str) for c in commands):
            return web.json_response({'error': 'commands must be a string or a list of strings'},
                                     status=400)

        world = self.game.world
        if world is None:
            return web.json_response({'error': 'no game in progress'}, status=409)

        # Validation syntaxique TOUT DE SUITE, pour repondre une erreur utile au
        # client : Exec refuse tout ce qui n'est pas un appel `Puzzle.<methode>`.
        import ast
        for command in commands:
            try:
                arbre = ast.parse(command)
            except SyntaxError as exc:
                return web.json_response({'error': f'SyntaxError: {exc}'}, status=400)
            for noeud in ast.walk(arbre):
                if not isinstance(noeud, ast.Call):
                    continue
                cible = noeud.func
                if not (isinstance(cible, ast.Attribute)
                        and isinstance(cible.value, ast.Name)
                        and cible.value.id == 'Puzzle'):
                    return web.json_response(
                        {'error': "only 'Puzzle.<method>(...)' calls are allowed"},
                        status=400)

        # L'execution revient au fil du JEU : on ne fait que deposer.
        jeu = self.game
        manager = self.device_manager
        manager.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
        manager.QueueSandboxCommands(commands)

        return web.json_response({'result': 'queued', 'count': len(commands)})

    async def list_starter_deck(self, request: web.Request) -> web.Response:
        return self.ListFile(STARTER_DECK_FOLDER.value)

    async def list_replay_files(self, request: web.Request) -> web.Response:
        if READ_ONLY_FIRST_REPLAY_FOLDER.value:
            return self.ListFile(REPLAY_FOLDERS.value[0])
        else:
            return self.ListFile(*REPLAY_FOLDERS.value)

    async def list_puzzle_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_FOLDER.value)

    async def list_puzzle_test_files(self, request: web.Request) -> web.Response:
        return self.ListFile(PUZZLE_TEST_FOLDER.value)

    def ReadReplayFile(self, file_path: str) -> web.Response:
        from game.scene.scene import Scene
        replay, checksum = Json.LoadAsInternal(file_path, Scene)
        return web.json_response({
            "version": replay.version,
            "is_puzzle": replay.is_puzzle,
            "time": replay.time,
            "cover": replay.cover,
            "path": replay.path,
            "comment": replay.comment,
            "villain": replay.campaign.villain[0] if replay.campaign.villain else replay.campaign.schemes[0],
            "players": [x.hero[0] for x in replay.players],
            "seed": replay.seed,
            "checksum": checksum == "Ok",
            "author": "",
            "step": len(replay.inputs),
        })

    def ReadPuzzleFile(self, file_path: str) -> web.Response:
        from engine.device.web.server.server_new_game import PuzzleData
        puzzle, checksum = Json.LoadAsInternal(file_path, PuzzleData)
        return web.json_response({
            "version": puzzle.version,
            "is_puzzle": True,
            "time": "",
            "cover": puzzle.cover,
            "path": file_path,
            "comment": puzzle.comment,
            "villain": puzzle.villain[0],
            "players": [puzzle.players[0].identities[0]],
            "seed": puzzle.seed,
            "checksum": checksum == "Ok",
            "author": puzzle.author,
            "step": 0,
        })

    async def read_file(self, request: web.Request) -> web.Response:
        file = request.rel_url.query_string
        return self.ReadJsonFile(file)

    async def get_encounter_set_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("EncounterSet", path)
        return self.ReadJsonFile(file)

    async def get_scenario_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Campaign", path)
        return self.ReadJsonFile(file)

    async def get_hero_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Hero", path)
        return self.ReadJsonFile(file)

    async def get_sets_json(self, request: web.Request) -> web.Response:
        file = FileManager.FindJsonPath("SetInfo", "sets_info.json")
        return self.ReadJsonFile(file)

    async def get_statistics_json(self, request: web.Request) -> web.Response:
        # Ajout local : statistiques globales (statistics.json) pour l'ecran de
        # stats du wizard.
        from game.statistics.game_statistics import GAME_STATISTICS_FILE
        import os
        if not os.path.exists(GAME_STATISTICS_FILE.value):
            return web.json_response({})
        return self.ReadJsonFile(GAME_STATISTICS_FILE.value)

    async def get_aspect_decks(self, request: web.Request) -> web.Response:
        # Packages d'aspect prefaits (« Reckless Aggression »...) et deck
        # conseille par heros. Ces 30 cartes ne forment pas un deck a elles
        # seules : l'assistant les assemble avec les cartes signature du heros.
        import os
        chemin = './data/decks_aspect.json'
        if not os.path.exists(chemin):
            return web.json_response({'packages': {}, 'recommandations': {}})
        return self.ReadJsonFile(chemin)

    async def get_achievements(self, request: web.Request) -> web.Response:
        # Etat complet des hauts faits : definitions, progression, dates.
        import json as json_lib
        import os
        from engine import Engine
        from game import achievements
        from engine.config import ConfigVariables

        history_file = ConfigVariables.File('games_history_file', 'games_history.json').value
        try:
            journal = json_lib.load(open(history_file, encoding='utf-8'))
            if not isinstance(journal, list):
                journal = []
        except Exception:
            journal = []

        stats = Engine.statistics.content
        return web.json_response(achievements.etat_complet(stats, journal))

    async def get_games_history(self, request: web.Request) -> web.Response:
        # Ajout local : journal des parties terminees (voir game/rule/statistics.py).
        from engine.config import ConfigVariables
        import os
        history_file = ConfigVariables.File('games_history_file', 'games_history.json').value
        if not os.path.exists(history_file):
            return web.json_response([])
        return self.ReadJsonFile(history_file)

    async def get_sets_custom_scenario(self, request: web.Request) -> web.Response:
        files = FileManager.ListFiles(CUSTOM_SCENARIOS_FOLDER.value, ".json")
        return web.json_response(files)

    async def get_cards_json(self, request: web.Request) -> web.Response:
        # Le frontend a besoin des cartes personnalisees (Stan Lee...) au meme
        # titre que les officielles : sans elles il n'a ni nom, ni PV, ni image
        # pour ces cartes. On fusionne donc les fichiers custom par-dessus la
        # base, comme le fait CardsDB.Initialize.
        from cards.database import CardsDB
        if not CardsDB.cards_custom_files:
            return self.ReadJsonFile(CARDS_JSON_FILE.value)

        fusion: Dict[str, List] = {}

        def ajouter(chemin: str) -> None:
            data, _ = Json.LoadInternal(chemin)
            if not isinstance(data, dict):
                return
            for pack, cartes in data.items():
                if isinstance(cartes, list):
                    fusion.setdefault(pack, []).extend(cartes)

        ajouter(CARDS_JSON_FILE.value)
        for chemin in CardsDB.cards_custom_files:
            ajouter(chemin)
        return web.json_response(fusion)

    async def get_translate_json(self, request: web.Request) -> web.Response:
        from engine.lib import TransText
        return self.ReadJsonFile(TransText.translate_file)

    async def get_card_json(self, request: web.Request) -> web.Response:
        from cards.database import CardsDB
        name = request.rel_url.query_string
        paper = CardsDB.FindCardPaper(name)
        return web.json_response(paper)

    async def get_completion_rate(self, request: web.Request) -> web.Response:
        return web.Response(text=str(self.game.statistics.completion_rate))

    async def get_statistics(self, request: web.Request) -> web.Response:
        return web.json_response(self.game.statistics.content.data)

    async def get_session_statistics(self, request: web.Request) -> web.Response:
        return web.json_response(self.game.session.statistics.dic)

    async def get_play_scene_name(self, request: web.Request) -> web.Response:
        controller = self.get_first_controller(request)
        if controller.world:
            text = controller.world.scene.name
        else:
            text = ""
        return web.Response(text=text)

    async def get_max_timeout(self, request: web.Request) -> web.Response:
        return web.Response(text=str(self.device_manager.timer.max_timeout))

    async def get_puzzle_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Puzzle", path)
        assert file
        return self.ReadPuzzleFile(file)

    async def get_replay_json(self, request: web.Request) -> web.Response:
        path = request.rel_url.query_string
        file = FileManager.FindJsonPath("Replay", path)
        assert file
        return self.ReadReplayFile(file)

    async def marvelcdb_card(self, request: web.Request) -> web.Response:
        # Proxy OPTIONNEL vers fr.marvelcdb.com (textes officiels FR dans
        # l'apercu). Appele seulement si l'option reseau du client est active.
        # Cache memoire, timeout court : le jeu reste 100 % jouable hors ligne.
        import re
        import aiohttp
        code = request.rel_url.query_string.strip()
        if not re.fullmatch(r"\d{5}[a-z]?", code):
            return web.json_response({'error': 'bad code'}, status=400)
        if not hasattr(self, 'marvelcdb_cache'):
            self.marvelcdb_cache = {}
        if code in self.marvelcdb_cache:
            data = self.marvelcdb_cache[code]
            if data is None:
                return web.json_response({'error': 'not found'}, status=404)
            return web.json_response(data)
        try:
            timeout = aiohttp.ClientTimeout(total=6)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(f"https://fr.marvelcdb.com/api/public/card/{code}.json") as reponse:
                    if reponse.status != 200:
                        self.marvelcdb_cache[code] = None
                        return web.json_response({'error': 'not found'}, status=404)
                    brut = await reponse.json(content_type=None)
        except Exception:
            return web.json_response({'error': 'offline'}, status=502)
        data = {k: brut.get(k) for k in ('name', 'text', 'flavor', 'traits') if brut.get(k)}
        self.marvelcdb_cache[code] = data
        return web.json_response(data)

    async def set_cursor(self, request: web.Request) -> web.Response:
        # Curseurs partages en multijoueur : chaque client envoie la position
        # de sa souris normalisee (0..1) par rapport a la scene du plateau.
        # Purement cosmetique, stocke en memoire, perime en 5 s.
        import time
        data = await request.json()
        try:
            p = int(data['p'])
            x = float(data['x'])
            y = float(data['y'])
        except Exception:
            return web.json_response({'error': 'p, x, y required'}, status=400)
        if not hasattr(self, 'cursors'):
            self.cursors = {}
        self.cursors[p] = {'x': x, 'y': y, 't': time.time()}
        return web.json_response({'result': 'ok'})

    async def get_cursors(self, request: web.Request) -> web.Response:
        import time
        cursors = getattr(self, 'cursors', {})
        now = time.time()
        frais = {p: {'x': c['x'], 'y': c['y']} for p, c in cursors.items() if now - c['t'] < 5.0}
        return web.json_response(frais)

    # --- Salon multijoueur : un choix de heros/deck par siege ---------------
    # Meme forme que set_cursor/get_cursors ci-dessus, a deux differences pres :
    # aucune peremption (un choix vaut jusqu'au lancement) et une verification
    # du siege en ECRITURE. Sans elle, un spectateur muni du mot de passe
    # d'entree pourrait changer le heros d'un joueur.
    #
    # On ne stocke PAS le deck complet, seulement de quoi le retrouver :
    # l'hote le recharge par /get_hero_json et /list_deck, deja en place. Cela
    # evite de faire transiter 40 cartes et supprime tout risque de decalage
    # entre ce que l'invite a vu et ce que l'hote enverra au moteur.
    async def set_choix_siege(self, request: web.Request) -> web.Response:
        data = await request.json()
        try:
            p = int(data['p'])
        except Exception:
            return web.json_response({'error': 'p required'}, status=400)

        autorises = self.allowed_seats(request)
        if autorises is not None and p not in autorises:
            return web.json_response({'error': 'not your seat'}, status=403)

        hero_card_id = str(data.get('hero_card_id', ''))
        deck_id = str(data.get('deck_id', ''))
        if not hero_card_id or not deck_id:
            return web.json_response(
                {'error': 'hero_card_id and deck_id required'}, status=400)

        if not hasattr(self, 'choix_sieges'):
            self.choix_sieges = {}
        self.choix_sieges[p] = {
            'hero_card_id': hero_card_id,
            'deck_id': deck_id,
            'deck_source': str(data.get('deck_source', '')),
        }
        return web.json_response({'result': 'ok'})

    async def get_choix_sieges(self, request: web.Request) -> web.Response:
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        passwords = SEAT_PASSWORDS.value
        choix = getattr(self, 'choix_sieges', {})
        return web.json_response({
            'multi': bool(passwords) and any(passwords),
            'sieges': {str(p): c for p, c in choix.items()},
        })

    async def set_language(self, request: web.Request) -> web.Response:
        # Bascule FR/EN de la narration a chaud (bouton langue du client) :
        # recharge la table TransText ('fr') ou la vide ('en'). N'affecte que
        # les messages generes apres l'appel.
        from engine.lib import TransText
        lang = request.rel_url.query_string.strip().lower()
        if lang not in ('fr', 'en'):
            return web.json_response({'error': "lang must be 'fr' or 'en'"}, status=400)
        if lang == 'en':
            TransText.translations = {}
        else:
            file = TransText.translate_file or './data/translate_fr.json'
            try:
                TransText.translations = Json.Load(file)
                TransText.translate_file = file
            except Exception:
                return web.json_response({'error': f'cannot load {file}'}, status=500)
        return web.json_response({'result': 'ok', 'language': lang})

    async def get_language(self, request: web.Request) -> web.Response:
        from engine.lib import TransText
        return web.json_response({'language': 'fr' if TransText.translations else 'en'})

    async def get_gamers(self, request: web.Request) -> web.Response:
        if self.controller_manager.game.state.is_running:
            num = str(self.controller_manager.total_players)
        else:
            num = "0"
        return web.Response(text=num)

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/list_file', self.list_file)
        self.AddAwaitGetSecurity('/list_scenarios', self.list_scenarios)
        self.AddAwaitGetSecurity('/list_encounter_sets', self.list_encounter_sets)
        self.AddAwaitGetSecurity('/list_deck', self.list_deck)
        self.AddPostSecurity('/save_deck', self.save_deck)
        self.AddPostSecurity('/sandbox_command', self.sandbox_command)
        self.AddAwaitGetSecurity('/list_starter_deck', self.list_starter_deck)
        self.AddAwaitGetSecurity('/list_replay_files', self.list_replay_files)
        self.AddAwaitGetSecurity('/list_puzzle_files', self.list_puzzle_files)
        self.AddAwaitGetSecurity('/list_puzzle_test_files', self.list_puzzle_test_files)
        
        self.AddAwaitGetSecurity('/read_file', self.read_file)
        self.AddAwaitGetSecurity('/get_encounter_set_json', self.get_encounter_set_json)
        self.AddAwaitGetSecurity('/get_scenario_json', self.get_scenario_json)
        self.AddAwaitGetSecurity('/get_hero_json', self.get_hero_json)
        self.AddAwaitGetSecurity('/get_sets_json', self.get_sets_json)
        self.AddAwaitGetSecurity('/get_sets_custom_scenario', self.get_sets_custom_scenario)
        self.AddAwaitGetSecurity('/get_statistics_json', self.get_statistics_json)
        self.AddAwaitGetSecurity('/get_games_history', self.get_games_history)
        self.AddAwaitGetSecurity('/get_achievements', self.get_achievements)
        self.AddAwaitGetSecurity('/get_aspect_decks', self.get_aspect_decks)
        self.AddAwaitGetSecurity('/get_cards_json', self.get_cards_json)
        self.AddAwaitGetSecurity('/get_translate_json', self.get_translate_json)
        self.AddAwaitGetSecurity('/get_card_json', self.get_card_json)
        self.AddAwaitGetSecurity('/get_completion_rate', self.get_completion_rate)
        self.AddAwaitGetSecurity('/get_statistics', self.get_statistics)
        self.AddAwaitGetSecurity('/get_session_statistics', self.get_session_statistics)
        self.AddAwaitGetSecurity('/get_play_scene_name', self.get_play_scene_name)
        self.AddAwaitGetSecurity('/get_max_timeout', self.get_max_timeout)
        self.AddAwaitGetSecurity('/get_puzzle_json', self.get_puzzle_json)
        self.AddAwaitGetSecurity('/get_replay_json', self.get_replay_json)

        self.AddAwaitGetSecurity('/marvelcdb_card', self.marvelcdb_card)
        self.AddPostSecurity('/set_cursor', self.set_cursor)
        self.AddAwaitGetSecurity('/get_cursors', self.get_cursors)
        self.AddPostSecurity('/set_choix_siege', self.set_choix_siege)
        self.AddAwaitGetSecurity('/get_choix_sieges', self.get_choix_sieges)
        self.AddAwaitGetSecurity('/set_language', self.set_language)
        self.AddAwaitGetSecurity('/get_language', self.get_language)
        self.AddAwaitGetSecurity('/get_gamers', self.get_gamers)

