from core import *
from aiohttp import web
from engine.device.web.server.server_base import GameServerBase

from engine.lib import Json
from engine.config import ConfigVariables
# from engine.log import Log
from game.puzzle.puzzle_data import PuzzleData
from game.game_run.game_new import NewGameDescriptor

# Kingsfall multi-tables : le nom de cette table et le fichier d'etat commun des assemblees (poses par `tools/config_serveur.py`).
TABLE_NOM = ConfigVariables.Str('table_nom', 'local')
ASSEMBLEES_FICHIER = ConfigVariables.Str('assemblees_fichier', '')


class GameServerNewGame(GameServerBase):

    async def new_debug(self, request: web.Request) -> web.Response:
        self.game.Restart()
        return web.json_response({'result': "New game created"})

    async def new_game(self, request: web.Request) -> web.Response:
        data = request.rel_url.query.get('data', "")
        new_game = Json.LoadsAs(data, NewGameDescriptor)
        # La table n'est plus « en attente d'une partie ordinaire » : la partie
        # qui demarre dit elle-meme ce qu'elle est (regle `mode_campaign`).
        self.table_ordinaire = False
        # Le salon multijoueur a rempli son office : on le vide pour que la
        # partie suivante ne reparte pas avec les choix de la precedente.
        # GameServer herite de GameServerGet et de GameServerNewGame :
        # `self.choix_sieges` est le meme attribut des deux cotes.
        self.choix_sieges = {}
        self.equipe_hote = None
        # La roue de « Partie au hasard » aussi : la partie est lancee.
        self.roue = None
        # Qui fait avancer la phase du mechant en multi (lot 6) se choisit pour
        # CETTE partie : une nouvelle partie le redemande a l'hote (finition du
        # 12/10/2026 ; l'ancien choix survivait a /new).
        self.avance_phase = ''
        # Le carnet arrive du CLIENT, donc ampute de ce qu'il n'a pas le droit
        # de voir. Le serveur y remet ici la part secrete de la campagne — pour
        # Agents of S.H.I.E.L.D., la combinaison de la taupe. Le moteur recoit
        # un carnet complet, le navigateur n'en a jamais eu qu'une moitie.
        # Seulement pour une partie de CAMPAGNE (regle `mode_campaign`) : une
        # campagne dont un scenario est reste « en cours » ne doit pas deposer
        # son secret dans une partie ordinaire (07/10/2026).
        try:
            from engine.device.web.server.server_campagne import secret_pour_le_moteur
            secret = secret_pour_le_moteur() if 'mode_campaign' in (new_game.rules or []) else {}
            if secret:
                new_game.campaign_log = {**(new_game.campaign_log or {}), **secret}
        except Exception:
            pass
        # KINGSFALL MULTI-TABLES (22/10/2026). Le client demande `assemblee_creer` (cette table ouvre l'assemblee et en est l'organisatrice) ou
        # `assemblee_rejoindre_<CODE>` ; le serveur s'inscrit dans le stockage COMMUN AVANT de lancer la partie et remplace la demande par la regle
        # `assemblee_<CODE>_<TABLE>` que le monde lit. Un refus (code inconnu, assemblee pleine) arrete le lancement avec son message.
        try:
            self._inscrire_dans_une_assemblee(new_game)
        except Exception as erreur:
            from game.operate.assemblee import ErreurAssemblee
            if isinstance(erreur, ErreurAssemblee):
                return web.json_response({'error': str(erreur)}, status=400)
            raise
        self.game.NewGame(new_game)
        return web.json_response({'result': "New game created"})

    def _inscrire_dans_une_assemblee(self, new_game: 'NewGameDescriptor') -> None:
        from game.operate.assemblee import Assemblee
        rules = list(new_game.rules or [])
        demande = next((r for r in rules if r == 'assemblee_creer' or r.startswith('assemblee_rejoindre_')), None)
        if demande is None:
            return
        table = TABLE_NOM.value or 'local'
        fichier = ASSEMBLEES_FICHIER.value
        if fichier:
            import os
            os.environ['MCLCG_ASSEMBLEES'] = os.path.abspath(fichier)
        noms = []
        for heros in new_game.hero_json or []:
            try:
                import json
                noms.append(str(json.loads(heros).get('name') or '').strip())
            except Exception:
                noms.append('')
        joueurs = max(1, len(new_game.hero_json or []))
        libelle = ', '.join(n for n in noms if n)
        if demande == 'assemblee_creer':
            code = Assemblee.Creer(table, joueurs, libelle)
        else:
            code = demande[len('assemblee_rejoindre_'):].strip().upper()
            Assemblee.Rejoindre(code, table, joueurs, libelle)
        rules = [r for r in rules if r != demande] + [f'assemblee_{code}_{table}']
        new_game.rules = rules

    async def load_replay(self, request: web.Request) -> web.Response:
        self.table_ordinaire = False
        self.game.LoadReplay(request.rel_url.query_string)
        return web.json_response({'result': "New game created"})

    async def load_replay_data(self, request: web.Request) -> web.Response:
        from game.scene.scene import Scene

        data = await request.json()
        replay_data = data.get('data', None)

        try:
            step = int(request.rel_url.query_string)
        except:
            step = None

        if replay_data is None:
            return web.json_response({'error': 'No data provided'}, status=400)

        # Process the replay_data as needed
        # Log.Print("Received replay data:", replay_data)

        scene = Json.LoadsAs(replay_data, Scene)
        self.table_ordinaire = False
        if step == 0:
            state = 'Replay'
        else:
            state = 'Load'
        self.game.session.LoadScene(scene, step, state)

        return web.json_response({'result': "New game created"})

    async def save_replay_data(self, request: web.Request) -> web.Response:
        data = Json.SaveString(self.game.scene, ignore_check_sum=False)
        compressed_data = Json.DumpGZip(data)
        self.device_manager.AddSize("Save", len(compressed_data))
        return web.Response(body=compressed_data, content_type='application/json', headers={'Content-Encoding': 'gzip'})

    def play_puzzle(self, puzzle: 'PuzzleData'):
        from game.scene.scene import Scene
        from game.puzzle.puzzle_scene import BuildPuzzleScene

        puzzle_data = BuildPuzzleScene(puzzle)

        scene = Json.LoadsAs(Json.Dumps(puzzle_data), Scene)
        scene.UpdateVersion()

        self.game.session.LoadScene(scene, None, 'Replay')
        self.controller_manager.skip.SetSkipTo(0)

    async def load_puzzle(self, request: web.Request) -> web.Response:
        puzzle = Json.LoadAs(request.rel_url.query_string, PuzzleData, check_sum="Warn")
        self.play_puzzle(puzzle)
        return web.json_response({'result': "New game created"})

    async def new_puzzle_replay(self, request: web.Request) -> web.Response:
        from game.scene.scene import Scene

        scene = Json.LoadsAs(request.rel_url.query_string, Scene)
        scene.UpdateVersion()

        self.game.session.LoadScene(scene, None, 'Replay')
        self.controller_manager.skip.SetSkipTo(0)
        return web.json_response({'result': "New game created"})

    async def new_puzzle(self, request: web.Request) -> web.Response:
        puzzle = Json.LoadsAs(request.rel_url.query_string, PuzzleData)
        self.play_puzzle(puzzle)
        return web.json_response({'result': "New game created"})

    async def new_game_online(self, request: web.Request) -> web.Response:
        ip = request.query.get('ip')
        port = int(request.query.get('port', 2345))
        assert ip
        text = self.device_manager.AddOnlineSite(ip, port)
        return web.Response(text=text)

    async def new_game_lan(self, request: web.Request) -> web.Response:
        port = int(request.query.get('port', 2345))
        text = self.device_manager.AddLocalNetworkSite(port)
        return web.Response(text=text)

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/new', self.new_game)
        self.AddAwaitGetSecurity('/new_debug', self.new_debug)
        self.AddAwaitGetSecurity('/load_replay', self.load_replay)
        self.AddPostSecurity('/load_replay_data', self.load_replay_data)
        self.AddAwaitGetSecurity('/save_replay_data', self.save_replay_data)
        self.AddAwaitGetSecurity('/load_puzzle', self.load_puzzle)
        self.AddAwaitGetSecurity('/new_puzzle_replay', self.new_puzzle_replay)
        self.AddAwaitGetSecurity('/new_puzzle', self.new_puzzle)
        self.AddAwaitGetSecurity('/new_game_online', self.new_game_online)
        self.AddAwaitGetSecurity('/new_game_lan', self.new_game_lan)

