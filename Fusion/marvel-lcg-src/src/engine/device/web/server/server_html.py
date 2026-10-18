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
        # /deck, /cards, /credits, /puzzle_editor, /scene, /report : pages de l'ancien site, retirees (affichent l'accueil)
        for _p in ('/deck', '/cards', '/credits', '/puzzle_editor', '/scene', '/report'):
            self.AddHtmlSecurity(_p, './public/prepare.html')
        self.AddHtmlSecurity('/replay', './public/replay.html')
        self.AddHtmlSecurity('/puzzle', './public/replay.html')
        self.AddHtmlSecurity('/puzzle_test', './public/replay.html')
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
        # ⚠ `need_auth=False` EST INDISPENSABLE. Cette route est celle qui POSE
        # le cookie de session : la placer derriere le mot de passe qu'elle
        # delivre condamnerait l'hote et ses invites a rester dehors, leur lien
        # a la main. La cle de siege portee par l'URL est le laissez-passer, et
        # elle est verifiee juste en dessous.
        self.AddAwaitGetSecurity('/claim_seat', self.handle_claim_seat, need_auth=False)
        # ⚠ LA PORTE DU SPECTATEUR, ET ELLE NE DONNE AUCUN SIEGE (15/09/2026).
        #
        # Le proprietaire du site veut regarder une partie en cours sans y
        # toucher. `claim_seat` ne convient pas : il pose un `seat_token_<n>`,
        # c'est-a-dire le DROIT D'AGIR a la place de quelqu'un, et il entrerait
        # en concurrence avec le joueur qui occupe deja ce siege.
        #
        # Cette route-ci ne pose QUE le laissez-passer de la table
        # (`session_token`), celui qui ouvre la LECTURE. Le moteur autorise deja
        # `get_world` sans siege (server_base : « seule l'ACTION est un
        # privilege du siege ») : il ne manquait que la porte.
        #
        # `need_auth=False` pour la meme raison que `claim_seat` : c'est elle
        # qui delivre le laissez-passer, la placer derriere lui n'aurait pas de
        # sens. La cle portee par l'URL est verifiee dans le handler.
        self.AddAwaitGetSecurity('/spectateur', self.handle_spectateur, need_auth=False)

    def _marquer_spectateur(self, response, request):
        """Le temoin qui RETIRE les droits.

        ⚠ COOKIE DE SESSION, PAS D'UN AN, contrairement aux cles de siege.
        Un temoin durable serait un piege a retardement : le proprietaire qui
        regarde SA propre table s'interdirait d'y jouer pour un an, sans savoir
        pourquoi. Il meurt donc avec l'onglet — et `claim_seat` l'efface de
        toute facon (qui presente une cle de siege est un joueur, pas un
        spectateur).
        """
        self.PoserCookie(response, request, 'spectateur', '1')

    async def handle_spectateur(self, request):
        """Ouvrir la table en LECTURE, sans prendre de siege.

        ⚠ CE QU'ELLE NE FAIT PAS, ET C'EST L'ESSENTIEL : aucun `seat_token_<n>`
        n'est pose, et elle marque le client d'un cookie `spectateur`.

        Les deux comptent. Ne pas poser de cle de siege ne suffisait PAS :
        `allowed_seats` ouvre tout siege ORPHELIN a n'importe quel client
        authentifie (« reprise d'un siege abandonne »), si bien qu'un spectateur
        arrive pendant qu'un joueur s'est deconnecte aurait herite de sa place.
        Mesure du 15/09/2026. Le cookie `spectateur` ferme cette porte :
        `allowed_seats` rend alors un ensemble VIDE, et `handle_post` repond 403
        quoi qu'on lui envoie.

        Le desarmement du plateau, cote navigateur, n'est qu'une politesse ;
        c'est ICI que la garantie tient.

        La cle attendue est le mot de passe de la table (`password`), le meme
        que celui du cookie `session_token`. Seul le site le connait, et il ne
        fabrique ce lien que pour son administrateur.
        """
        from aiohttp import web
        key = request.query.get('key', '')
        try:
            seat = int(request.query.get('p', '0'))
        except ValueError:
            seat = 0
        if seat < 0 or seat > 3:
            return web.Response(status=400, text='Unknown seat')

        # ⚠ `&multi` N'EST PAS DECORATIF. Sans lui, le plateau tourne en
        # « hot-seat » et s'annonce sur le socket POUR TOUS LES SIEGES : un
        # spectateur ferait alors croire au moteur qu'un joueur absent est
        # connecte. Mesure du 15/09/2026, en partie a deux heros.
        destination = f'/app/board.html?p={seat}&multi&spectateur=1'

        if not getattr(self, 'hash_password', None):
            # Table sans mot de passe (partie locale) : il n'y a pas de porte a
            # ouvrir, et rien a verifier. Le temoin de spectateur, lui, se pose
            # quand meme : c'est lui qui interdit d'agir, et il doit valoir
            # aussi sur une table ouverte.
            reponse = web.HTTPFound(destination)
            self._marquer_spectateur(reponse, request)
            return reponse

        import hashlib
        if hashlib.md5(key.encode()).hexdigest() != self.hash_password:
            return web.Response(status=403, text='Wrong table password')

        response = web.HTTPFound(destination)
        self._marquer_spectateur(response, request)
        self.PoserCookie(response, request, 'session_token', self.hash_password,
                         max_age=31536000)
        return response

    async def handle_claim_seat(self, request):
        from aiohttp import web
        from engine.device.web.server.server_base import SEAT_PASSWORDS
        try:
            seat = int(request.query.get('p', ''))
        except ValueError:
            return web.Response(status=400, text='Missing or invalid seat number (p=0..3)')
        key = request.query.get('key', '')
        # L'hote reclame son siege PUIS va creer la partie : &to=prepare.
        # `prepare-v2` sert au compte d'essai pendant la construction de la V2.
        # Il ne suffit pas de l'ecrire dans l'URL : le cookie n'est pose
        # qu'APRES verification de la cle du siege 0, plus bas.
        # Les invites passent par le SALON choisir heros et deck : &to=salon.
        # Sans `to`, on garde l'ancien comportement (direct au plateau).
        vers = request.query.get('to')
        demande_v2 = vers == 'prepare-v2' and seat == 0
        if vers == 'prepare' or demande_v2:
            destination = '/prepare.html'
        elif vers == 'salon':
            destination = f'/salon.html?p={seat}'
        else:
            destination = f'/app/board.html?p={seat}'
        passwords = SEAT_PASSWORDS.value
        if not passwords or not any(passwords):
            # Pas de protection configuree : le lien mene simplement au jeu.
            # La V2 privee, elle, exige la preuve du siege hote et n'est donc
            # jamais activee sur une table sans cles configurees.
            return web.HTTPFound(destination)
        if seat < 0 or seat >= len(passwords):
            return web.Response(status=400, text='Unknown seat')
        expected = passwords[seat]
        if expected and key != expected:
            return web.Response(status=403, text='Wrong seat password')
        response = web.HTTPFound(destination)
        # Cookie de SESSION et lisible par le frontend : ce n'est pas une
        # autorisation, seulement le selecteur d'interface. Une entree V1
        # l'efface explicitement pour qu'un essai precedent ne survive pas a
        # une nouvelle ouverture de la meme table dans ce navigateur.
        self.PoserCookie(response, request, 'ui_version',
                         'v2' if demande_v2 else '',
                         max_age=None if demande_v2 else 0,
                         httponly=False)
        # ⚠ QUI PRESENTE UNE CLE DE SIEGE VIENT JOUER : on efface le temoin de
        # spectateur s'il en trainait un. Sans cette ligne, regarder sa propre
        # table puis y revenir jouer laissait le moteur refuser toute action,
        # sans rien dire de pourquoi.
        # `del_cookie` ne sait pas viser un cookie `Partitioned` (Discord) :
        # un effacement non partitionne laisserait le temoin en place.
        self.PoserCookie(response, request, 'spectateur', '', max_age=0)
        # `secure` et `samesite` manquaient aux deux cookies poses ici : sur une
        # premiere visite tapee en `http://`, la cle de siege comme le
        # laissez-passer du moteur partaient en clair avant meme que Caddy
        # n'ait redirige. `CookieSecure` deduit le schema de la requete, ce qui
        # laisse l'usage en local (127.0.0.1, sans proxy) intact.
        if expected:
            self.PoserCookie(response, request, f'seat_token_{seat}',
                             self.seat_hash(expected), max_age=31536000)
            # LE LIEN VAUT LE MOT DE PASSE.
            #
            # Le moteur protege l'application entiere par un mot de passe
            # (`password`, cookie `session_token`). Sans la ligne ci-dessous,
            # remettre cette protection en service obligerait l'hote ET chaque
            # invite a taper ce mot de passe apres avoir clique sur leur lien,
            # alors qu'ils viennent precisement de prouver qu'ils sont attendus
            # en presentant une cle de siege valide.
            #
            # On leur ouvre donc la porte au passage. Qui arrive SANS lien reste
            # arrete par la page de mot de passe, ce qui est tout l'objet de la
            # manoeuvre.
            if getattr(self, 'hash_password', None):
                self.PoserCookie(response, request, 'session_token', self.hash_password,
                                 max_age=31536000)
        return response
