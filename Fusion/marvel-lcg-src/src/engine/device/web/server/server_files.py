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

    @staticmethod
    def TypeImage(octets: bytes) -> str:
        """Le type reel d'une image, lu dans sa SIGNATURE, jamais dans son nom.

        ⚠ TOUTES LES IMAGES ETAIENT ANNONCEES `image/jpeg`, quelle qu'elles
        soient (16/09/2026). Les navigateurs devinent et affichent quand meme,
        mais pas toujours : un PNG annonce en JPEG a fait echouer un controle
        qui verifie que l'image du narval est bien DECODEE, et non seulement
        recue. Le meme raisonnement que `_ecrire_capture` cote site : on ne
        fait confiance ni au nom, ni a l'etiquette, seulement aux octets.
        """
        if octets[1:4] == b"PNG":
            return "image/png"
        if octets[:4] == b"RIFF" and octets[8:12] == b"WEBP":
            return "image/webp"
        if octets[:3] == b"GIF":
            return "image/gif"
        if octets[:5] == b"<?xml" or octets[:4] == b"<svg":
            return "image/svg+xml"
        # JPEG, et le repli : c'est le format de l'immense majorite des scans.
        return "image/jpeg"

    def handle_sets_image(self, request: web.Request) -> web.StreamResponse:
        file_path = request.path

        image_bytes = Cache.LoadImage(file_path)

        return web.Response(body=image_bytes, content_type=self.TypeImage(image_bytes), headers=self.HeaderCache)

    def handle_hd_request(self, request: web.Request) -> web.StreamResponse:
        # La scene de l'assistant : le scan haute definition, ou le scan
        # habituel a defaut. Le telechargement eventuel a lieu ici, une fois.
        file_path = request.path.split("/")[-1]
        image_bytes = Cache.LoadImageHD(file_path)
        self.device_manager.AddSize("Image", len(image_bytes))
        return web.Response(body=image_bytes, content_type=self.TypeImage(image_bytes), headers=self.HeaderCache)

    def handle_vignette_request(self, request: web.Request) -> web.StreamResponse:
        # Meme forme que handle_image_request : seul le DERNIER segment compte,
        # et Cache.LoadVignette retombe sur le scan complet si besoin.
        file_path = request.path.split("/")[-1]
        image_bytes = Cache.LoadVignette(file_path)
        self.device_manager.AddSize("Image", len(image_bytes))
        return web.Response(body=image_bytes, content_type=self.TypeImage(image_bytes), headers=self.HeaderCache)

    def handle_image_request(self, request: web.Request) -> web.StreamResponse:
        # file_path = request.match_info['path']
        file_path = request.path
        file_path = file_path.split("/")[-1]

        image_bytes = Cache.LoadImage(file_path)
        image_size = len(image_bytes)

        self.device_manager.AddSize("Image", image_size)

        return web.Response(body=image_bytes, content_type=self.TypeImage(image_bytes), headers=self.HeaderCache)

    @override
    def __init__(self) -> None:
        super().__init__()

        self.AddDefaultGet()

        self.AddAwaitGetSecurity('/', self.handle_marvel)
        self.AddAwaitGetSecurity(r'/p={player:\d+}', self.handle_players_404)
        self.AddAwaitGetSecurity('/watch', self.handle_marvel)

        self.AddNonAwaitGetSecurity(r'/sets/{path:.+}', self.handle_sets_image)
        # ⚠ AVANT la route fourre-tout : sinon /vignette/<nom> y tomberait et
        # servirait le scan complet, comme n'importe quel chemin.
        self.AddNonAwaitGetSecurity(r'/vignette/{path:.+}', self.handle_vignette_request)
        self.AddNonAwaitGetSecurity(r'/hd/{path:.+}', self.handle_hd_request)
        self.AddNonAwaitGetSecurity(r'/{path:.+}', self.handle_image_request)

