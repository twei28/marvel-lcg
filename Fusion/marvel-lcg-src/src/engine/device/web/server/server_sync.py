from core import *
from engine.lib import Json
from engine.log import Log
from engine.device import *
from engine.device.web import *

from aiohttp import web
from engine.device.web.server.server_base import GameServerBase

CATEGORY_NAME = "WEB"

class GameServerSync(GameServerBase):

    def get_render_id(self, request: web.Request) -> int:
        return int(request.rel_url.query.get('r', 0))

    def get_game_id(self, request: web.Request) -> int:
        return int(request.rel_url.query.get('g', 0))

    async def handle_debug_command(self, request: web.Request) -> web.Response:
        # ⚠ LA CONSOLE EST UNE ACTION, ET LA PLUS BRUTALE DE TOUTES.
        #
        # Le bouton « Annuler » du plateau n'envoie pas une reponse au moteur :
        # il appelle `/debug?/undo auto`. Un spectateur qui cliquerait dessus
        # annulerait le coup de quelqu'un d'autre. Le refus de `/post` ne le
        # couvrait pas : ce n'est pas la meme porte. Trouve le 15/09/2026 en
        # regardant l'ecran du spectateur, pas en relisant le code.
        if self.est_spectateur(request):
            return web.Response(status=403, text='Spectator')
        controller = self.get_first_controller(request)
        controller_manager = controller.manager
        debug_cmd = Unquote(request.rel_url.query_string)
        controller_manager.console.SetCommand(debug_cmd, controller.world)

        if controller_manager.console.debug_cmds or \
            controller_manager.console.debug_break or \
            controller_manager.skip.is_skipping or \
            controller_manager.skip.skip_to > 0 or \
            controller_manager.replay.is_updated:
            self.device_manager.ExitWait()

        return web.Response(text=debug_cmd)

    async def handle_client_updated(self, request: web.Request) -> web.Response:
        render_id = self.get_render_id(request)
        player_ids = self.get_player_ids(request)
        game_id = self.get_game_id(request)

        for player_id in player_ids:
            self.device_manager.ClientUpdateRenderId(player_id, render_id, game_id)
        Log.DebugSilent("SYNC", f"[Client] Updated, render id: {render_id}, player_id: {player_ids}")
        return web.Response(status=200)

    async def handle_get_ask(self, request: web.Request) -> web.Response:
        player_ids = self.get_player_ids(request)

        if self.device_manager.asking_players == []:
            return web.json_response({})

        data = None
        for player_id in player_ids:
            if player_id in self.device_manager.asking_players:
                if data == None:
                    data = asdict(self.device_manager.ask_options[player_id])
                else:
                    autre = asdict(self.device_manager.ask_options[player_id])
                    list1 = Json.LoadsAs(data['options_json'], List[Any])
                    list2 = Json.LoadsAs(autre['options_json'], List[Any])
                    combined_list = list1 + list2
                    data['options_json'] = Json.Dumps(combined_list)
                    # ⚠ LES REFUS SE FUSIONNENT AUSSI (10/09/2026). En siege
                    # partage, deux joueurs sont interroges en meme temps :
                    # sans cette ligne, le second perdait ses raisons et ses
                    # cartes injouables restaient muettes, alors que celles du
                    # premier parlaient. Un defaut qui ne se voit qu'a deux.
                    refus1 = Json.LoadsAs(data.get('refus_json') or "[]", List[Any])
                    refus2 = Json.LoadsAs(autre.get('refus_json') or "[]", List[Any])
                    data['refus_json'] = Json.Dumps(refus1 + refus2)
            pass

        if data == None:
            return web.json_response({})

        Log.Debug(CATEGORY_NAME, f"[Client] ask_player_id: {player_ids}")

        # data_size = Json.DumpsSize(data)
        # Game.run.device_manager.GetConfig(WebDeviceConfig).AddSize("Ask", data_size)
        # return web.json_response(data)
        compressed_data = Json.DumpGZip(data)
        self.device_manager.AddSize("Ask", len(compressed_data))
        return web.Response(body=compressed_data, content_type='application/json', headers={'Content-Encoding': 'gzip'})

    async def handle_get_world(self, request: web.Request) -> web.Response:
        player_ids = self.get_player_ids(request)
        controller = self.get_first_controller(request)
        if controller.world:
            data = controller.world.render.descriptor
        else:
            # Bug here, if we return {}, ts code will read null and crash
            from game.render.descriptor.world import WorldDescriptor
            data = WorldDescriptor()

        # Le numero de trame AVANT le masquage : apres, `data` peut etre un
        # dictionnaire, qui n'a pas d'attribut.
        render_id = data.render_id
        data = self.MasquerCeQuOnNaPasLeDroitDeVoir(data, request)
        compressed_data = Json.DumpGZip(data)

        self.device_manager.AddSize("World", len(compressed_data))
        Log.DebugSilent("SYNC", f"[Client] Get world {render_id}, player_id: {player_ids}")

        return web.Response(body=compressed_data, content_type='application/json', headers={'Content-Encoding': 'gzip'})

    def MasquerCeQuOnNaPasLeDroitDeVoir(self, descriptor, request: web.Request):
        """Effacer l'identite des cartes que CE client n'a pas le droit de voir.

        ⚠ POURQUOI, ET C'EST UNE FUITE, PAS UN CONFORT. Mesure du 15/09/2026,
        en partie a deux heros : `/get_world` rend a n'importe quel client la
        MAIN DE TOUS LES JOUEURS, nom des cartes compris, et l'ORDRE COMPLET DU
        DECK RENCONTRE (32 cartes nommees, face cachee). Le plateau, lui,
        cachait deja tout cela a l'ecran (`isVisibleFor`, world.ts) : la regle
        existait cote client, et seulement la. Un `curl` en faisait le tour.

        Demande de l'utilisateur, le meme jour : « ce n'est que moi qui doit
        pouvoir voir les autres ».

        ⚠ LA REGLE EST CELLE DU CLIENT, DEPLACEE ICI, PAS UNE NOUVELLE. Une
        carte se voit si `visible_for_players` croise les sieges de ce client.
        Mesure de controle avant d'ecrire une ligne : dans une partie a deux,
        TOUT ce qui est sur la table (vilain, manigance, personnages en jeu)
        porte `(0, 1)`, les mains portent `(0,)` et `(1,)`, les decks `()`.
        Masquer sur cette regle ne cache donc rien de ce qui est public.

        Ce qu'on efface : le nom, l'identifiant de carte, l'illustration, les
        traits, le type, le cout. Ce qu'on garde : l'identifiant d'OBJET, l'etat
        (engagee ou non), le dos a afficher, la zone. Le client dessine deja un
        dos pour ces cartes-la : rien ne change a l'ecran.

        Qui voit quoi est decide par `sieges_visibles` (server_base), et surtout
        PAS par `allowed_seats` : celle-la ouvre tout siege orphelin pour qu'un
        joueur deconnecte ne bloque pas la partie, ce qui, applique a la vue,
        rendait sa main a tout le monde des qu'il fermait son onglet.
        """
        autorises = self.sieges_visibles(request)
        if autorises is None:
            return descriptor

        from dataclasses import asdict
        brut = asdict(descriptor)

        def masquer(noeud) -> None:
            if isinstance(noeud, dict):
                vus = noeud.get('visible_for_players')
                if isinstance(vus, list) and 'name' in noeud and not (set(vus) & autorises):
                    noeud['name'] = ''
                    noeud['card_id'] = ''
                    noeud['pic_id'] = ''
                    noeud['card_type'] = ''
                    noeud['traits'] = {}
                    noeud['info'] = {}
                    noeud['buffs'] = {}
                    noeud['cost'] = 0
                for valeur in noeud.values():
                    masquer(valeur)
            elif isinstance(noeud, list):
                for valeur in noeud:
                    masquer(valeur)

        masquer(brut)
        return brut

    async def handle_post(self, request: web.Request) -> web.Response:
        post_data = await request.text()
        player_ids = self.get_player_ids(request)
        if not player_ids:
            # Protection des sieges : ce client n'a pas la cle de ce siege.
            return web.Response(status=403, text='This seat is protected')
        post_json = Unquote(post_data)
        assert len(player_ids) == 1
        if post_json:
            for player_id in player_ids:
                if player_id in self.device_manager.asking_players:
                    self.device_manager.WhenInput(post_json, player_id)

        return web.Response(status=200)

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/debug', self.handle_debug_command)

        self.AddAwaitGetSecurity('/client_updated', self.handle_client_updated)
        self.AddAwaitGetSecurity('/get_ask', self.handle_get_ask)
        self.AddAwaitGetSecurity('/get_world', self.handle_get_world)

        self.AddPostSecurity('/post', self.handle_post)

