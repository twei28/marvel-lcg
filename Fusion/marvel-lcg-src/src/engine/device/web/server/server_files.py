from core import *

from engine.file import Cache
from engine.device.web import *

from aiohttp import web
from engine.device.web.server.server_base import GameServerBase

CATEGORY_NAME = "WEB"

class GameServerFiles(GameServerBase):

    async def handle_marvel(self, request: web.Request) -> web.StreamResponse:
        if request.query_string == '':
            # CORRECTIF : la racine ouvre directement l'assistant de préparation
            # (notre wizard) au lieu de l'ancien menu `main.html`, qui n'était
            # qu'une liste de boutons et imposait un clic de plus.
            # Les pages qu'il listait restent joignables par URL :
            # /scene /replay /deck /cards /puzzle /credits.
            return self.ReadFile('./public/prepare.html')
        else:
            return self.ReadFile('./public/marvel.html')

    async def handle_players_404(self, request: web.Request) -> web.StreamResponse:
        player = request.match_info.get('player')
        return web.Response(text=f"Please visiting /?p={player}", status=404)

    def handle_sets_image(self, request: web.Request) -> web.StreamResponse:
        file_path = request.path

        image_bytes = Cache.LoadImage(file_path)

        return web.Response(body=image_bytes, content_type='image/jpeg', headers=self.HeaderCache)

    def handle_image_request(self, request: web.Request) -> web.StreamResponse:
        # file_path = request.match_info['path']
        file_path = request.path
        file_path = file_path.split("/")[-1]

        image_bytes = Cache.LoadImage(file_path)
        image_size = len(image_bytes)

        self.device_manager.AddSize("Image", image_size)

        return web.Response(body=image_bytes, content_type='image/jpeg', headers=self.HeaderCache)

    @override
    def __init__(self) -> None:
        super().__init__()

        self.AddDefaultGet()

        self.AddAwaitGetSecurity('/', self.handle_marvel)
        self.AddAwaitGetSecurity(r'/p={player:\d+}', self.handle_players_404)
        self.AddAwaitGetSecurity('/watch', self.handle_marvel)

        self.AddNonAwaitGetSecurity(r'/sets/{path:.+}', self.handle_sets_image)
        self.AddNonAwaitGetSecurity(r'/{path:.+}', self.handle_image_request)

