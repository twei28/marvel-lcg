from core import *
from engine.device.web.server.server_base import GameServerBase

CATEGORY_NAME = "WEB"

class GameServerHTML(GameServerBase):

    @override
    def __init__(self) -> None:
        super().__init__()

        # CORRECTIF : /main servait l'ancien menu ; il ouvre désormais le wizard,
        # pour que les anciens favoris et raccourcis continuent de fonctionner.
        self.AddHtmlSecurity('/main', './public/prepare.html')
        self.AddHtmlSecurity('/deck', './public/deck.html')
        self.AddHtmlSecurity('/cards', './public/cards.html')
        self.AddHtmlSecurity('/scene', './public/scene.html')
        self.AddHtmlSecurity('/replay', './public/replay.html')
        self.AddHtmlSecurity('/puzzle', './public/replay.html')
        self.AddHtmlSecurity('/credits', './public/credits.html')
        self.AddHtmlSecurity('/puzzle_editor', './public/puzzle_editor.html')
        self.AddHtmlSecurity('/puzzle_test', './public/replay.html')
        self.AddHtmlSecurity('/report', './public/report.html')
        # Ajouts locaux (multijoueur / pages hébergées)
        self.AddHtmlSecurity('/blueprints', './public/blueprints/index.html')
        self.AddHtmlSecurity('/peerjs', './public/peerjs.html')
        self.AddHtmlSecurity('/host', './public/host.html')
        # Protection des sieges : chaque joueur reclame le sien avec SON mot de
        # passe (launch.online.json / seat_passwords), via un lien du type
        #   /claim_seat?p=1&key=MOTDEPASSE
        # Bonne cle -> cookie seat_token_<n> (1 an) + redirection vers le
        # plateau de ce siege. Mauvaise cle -> 403.
        self.AddHtmlSecurity('/salon.html', './public/salon.html')
        self.AddAwaitGetSecurity('/claim_seat', self.handle_claim_seat)

    async def handle_claim_seat(self, request):
        from aiohttp import web
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            seat = int(request.query.get('p', ''))
        except ValueError:
            return web.Response(status=400, text='Missing or invalid seat number (p=0..3)')
        key = request.query.get('key', '')
        # L'hote reclame son siege PUIS va creer la partie : &to=prepare.
        # Les invites passent par le SALON choisir heros et deck : &to=salon.
        # Sans `to`, on garde l'ancien comportement (direct au plateau).
        vers = request.query.get('to')
        if vers == 'prepare':
            destination = '/prepare.html'
        elif vers == 'salon':
            destination = f'/salon.html?p={seat}'
        else:
            destination = f'/app/board.html?p={seat}'
        passwords = SEAT_PASSWORDS.value
        if not passwords or not any(passwords):
            # Pas de protection configuree : le lien mene simplement au jeu.
            return web.HTTPFound(destination)
        if seat < 0 or seat >= len(passwords):
            return web.Response(status=400, text='Unknown seat')
        expected = passwords[seat]
        if expected and key != expected:
            return web.Response(status=403, text='Wrong seat password')
        response = web.HTTPFound(destination)
        if expected:
            response.set_cookie(
                f'seat_token_{seat}',
                self.seat_hash(expected),
                max_age=31536000,
                path='/',
                httponly=True,
            )
        return response

