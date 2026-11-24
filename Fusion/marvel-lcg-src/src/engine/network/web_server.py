from typing import TypeAlias
from core import *
from aiohttp import web
from build import Build
from engine.config import ConfigVariables
from engine.task import TaskManager
# from engine.job import JobManager
from engine.lib import MimeType, Json, Ver
from engine.log import Log
from engine.file import FileManager
import hashlib
import html
import re

CATEGORY_NAME = "WEB"

SOUND_FOLDERS   = ConfigVariables.Folders('sound_folders', ["./assets/sounds/"])
IMAGE_FOLDERS   = ConfigVariables.Folders('image_folders')
TEXTURE_FOLDER  = ConfigVariables.Folder('texture_folder')
CACHE_MAX_AGE   = ConfigVariables.Int('cache_max_age', 31536000)

# Taille maximale de la ligne de requete HTTP (l'URL). Voir le commentaire dans
# `__init__` : 128 Kio laissent passer une table a quatre joueurs avec les plus
# gros decks du depot, et gardent une marge. Le CORPS des requetes, lui, reste
# plafonne a 8 Mio par `client_max_size`.
MAX_LIGNE_REQUETE = 128 * 1024
"""
one hour:   3600
one day:    86400
one week:   604800
one year:   31536000
"""

PASSWORD            = ConfigVariables.Str('password', "")
DETECTED_VERSION    = ConfigVariables.Bool('detected_version', True)

@web.middleware
async def _cadre_discord(request: "web.Request", handler):
    """Adapte les reponses servies a l'activite Discord (hote `discord.<domaine>`),
    et a elle seule. Voir docs/reference/DISCORD.md.
    """
    discord = request.host.split(':')[0].startswith('discord.')
    try:
        reponse = await handler(request)
    except web.HTTPRedirection as redirection:
        if not discord:
            raise
        reponse = redirection
    # ⚠ DANS DISCORD, JAMAIS DE VRAIE REDIRECTION. Le proxy de Discord suit
    # lui-meme les 3xx et rend la page finale en 200 : les `Set-Cookie` de la
    # redirection sont perdus (`claim_seat` perdait ainsi les cles de siege).
    # On rend une page 200 qui porte les cookies et enchaine d'elle-meme.
    if discord and isinstance(reponse, web.HTTPRedirection) and reponse.location:
        vers = html.escape(str(reponse.location), quote=True)
        page = web.Response(
            text=f'<!doctype html><meta charset="utf-8">'
                 f'<meta http-equiv="refresh" content="0;url={vers}">',
            content_type='text/html')
        for cookie in reponse.headers.getall('Set-Cookie', []):
            page.headers.add('Set-Cookie', cookie)
        for morsel in reponse.cookies.values():
            page.headers.add('Set-Cookie', morsel.OutputString())
        return page
    return reponse


class WebServer:

    HandleAsyncType: TypeAlias = Callable[["web.Request"], Awaitable["web.StreamResponse"]]
    HandleNonAsyncType: TypeAlias = Callable[["web.Request"], "web.StreamResponse"]

    def __init__(self) -> None:
        # aiohttp refuse au-dela de 1 Mio par defaut, et un rapport de bug
        # porte une capture d'ecran plus le journal de la partie. La capture
        # est deja reduite par le navigateur avant l'envoi (panneau-bug.js)
        # et le site a son propre plafond : ce chiffre-ci est la marge, pas
        # une autorisation d'envoyer n'importe quoi.
        self.web_app = web.Application(client_max_size=8 * 1024 * 1024,
                                       middlewares=[_cadre_discord])
        # ⚠ LA LIGNE DE REQUETE, ET C'EST UN BLOCAGE COMPLET QUAND ELLE MANQUE.
        # Le lancement d'une partie passe par `GET /new?data=<descripteur>`,
        # donc par l'URL : le descripteur porte le scenario ENTIER et le deck
        # de chaque joueur. aiohttp refuse au-dela de 8190 octets par defaut
        # (`LineTooLong`, HTTP 400) et le joueur ne voit rien du tout.
        #
        # Mesure du 16/09/2026, un joueur bloque net : le deck de depart le
        # plus gros du depot pese 7861 octets UNE FOIS ENCODE, a lui seul. Un
        # scenario en ajoute jusqu'a 2476, et une table a quatre joueurs
        # approche 34 000 octets. La limite par defaut etait donc franchie par
        # une partie ORDINAIRE a un seul joueur.
        self.runner = web.AppRunner(
            self.web_app,
            max_line_size=MAX_LIGNE_REQUETE,
            max_field_size=MAX_LIGNE_REQUETE,
        )

        if PASSWORD.value:
            self.hash_password = hashlib.md5(PASSWORD.value.encode()).hexdigest()
        else:
            self.hash_password = None

        WebServer.HeaderCache = {'Cache-Control': f'public, max-age={CACHE_MAX_AGE.value}'}

    ################################################################################
    #
    @final
    def LoadHtmlAuthenticate(self):
        return self.ReadFile('./public/authenticate.html')

    @final
    def LoadHtmlCleanCache(self):
        return self.ReadFile('./public/clean_cache.html')

    ################################################################################
    #
    @final
    def AddNonAwaitGetSecurity(self, path: str, handle: HandleNonAsyncType):
        async def new_handle(request: web.Request) -> web.StreamResponse:
            if not self.IsAuthenticate(request):
                return self.LoadHtmlAuthenticate()
            elif not self.IsVersionMatch(request):
                return self.LoadHtmlCleanCache()
            else:
                return await TaskManager.ToThread(handle, request)
        self.web_app.router.add_get(path, new_handle)

    @final
    def AddAwaitGetSecurity(self, path: str, handle: HandleAsyncType, need_auth: bool=True, need_check_version: bool=True):
        async def new_handle(request: web.Request) -> web.StreamResponse:
            if not self.SpectateurPeutLire(path, request):
                return web.Response(status=403, text='Spectator: read-only')
            if need_auth and not self.IsAuthenticate(request):
                return self.LoadHtmlAuthenticate()
            elif need_check_version and not self.IsVersionMatch(request):
                return self.LoadHtmlCleanCache()
            else:
                return await handle(request)
        self.web_app.router.add_get(path, new_handle)

    @final
    def SpectateurPeutLire(self, path: str, request: "web.Request") -> bool:
        """Un spectateur ne passe QUE par les routes de lecture. Refus par defaut.

        ⚠ POURQUOI UN REFUS PAR DEFAUT, ET PAS UNE LISTE D'INTERDITS.
        Le 15/09/2026, en regardant l'ecran du spectateur, j'ai vu le bouton
        « Annuler » : il n'envoie pas une reponse au moteur, il appelle
        `/debug?/undo auto`. Fermer `/post` ne le couvrait pas. Et derriere lui
        il y avait `/new`, `/load_replay`, `/save_replay_data`, `/new_puzzle`...
        Une liste d'interdits aurait laisse passer la prochaine route ajoutee au
        moteur, sans que personne ne s'en apercoive.

        On inverse donc la charge : le spectateur ne voit que ce qui est
        NOMMEMENT autorise. Une route ajoutee demain lui est fermee d'office ;
        si elle doit s'ouvrir, on l'ecrit ici, en connaissance de cause.

        La liste vient d'une MESURE, pas d'une intuition : on a releve tout ce
        que le plateau du spectateur demande au moteur en vraie partie
        (`ui-check/tests/spectateur-moteur.spec.ts`).
        """
        if request.cookies.get('spectateur') != '1':
            return True
        # ⚠ ON JUGE LE CHEMIN DEMANDE, PAS CELUI DECLARE. Une route statique est
        # enregistree sous un motif (`/app/{fichier}`, `/{tail:.*}`) qui ne
        # ressemble pas a l'adresse appelee : compare au motif, `/app/board.html`
        # tombait en 403 et le plateau du spectateur restait blanc. Mesure du
        # 15/09/2026, au curl.
        demande = request.path
        # Les lectures : l'etat du monde, le catalogue, les images, la page.
        for prefixe in ('/get_', '/list_', '/app/', '/public/', '/vignette/',
                        '/scan/', '/assets/', '/img/', '/pics'):
            if demande.startswith(prefixe):
                return True
        return demande in ('/', '/spectateur', '/claim_seat', '/watch')

    @final
    def CookieSecure(self, request: "web.Request") -> bool:
        """Vrai si la requete est arrivee par HTTPS, directement ou par un proxy.

        ⚠ ON NE PEUT PAS METTRE `secure=True` EN DUR. En production le moteur
        est servi sous `pN.<domaine>` par Caddy, qui n'ecoute qu'en HTTPS ; mais
        le meme code tourne en local sur `http://127.0.0.1:2351`, ou l'attribut
        ferait jeter le cookie par le navigateur. On regarde donc ce que la
        requete dit d'elle-meme : Caddy pose `X-Forwarded-Proto`, et un acces
        direct en HTTPS se voit dans le schema de l'URL.

        Falsifier cet en-tete ne rapporte rien : cela ne durcit ou n'abime que
        le cookie de celui qui ment, et pour lui seul.
        """
        entete = request.headers.get('X-Forwarded-Proto', '')
        if entete.split(',')[0].strip().lower() == 'https':
            return True
        return request.url.scheme == 'https'

    @final
    def EstCadreDiscord(self, request: "web.Request") -> bool:
        """Vrai si la table est servie dans l'activite Discord.

        Caddy n'envoie ici `discord.<domaine>` que pour ce cas (voir
        `deploiement/Caddyfile` et `docs/reference/DISCORD.md`).
        """
        return request.host.split(':')[0].startswith('discord.')

    @final
    def PoserCookie(self, response, request: "web.Request", nom: str, valeur: str,
                    max_age: "int | None" = None, httponly: bool = True) -> None:
        """Pose un cookie de la table, `Lax` d'ordinaire, et adapte a Discord.

        ⚠ DANS DISCORD, `Lax` NE MARCHE PAS. La table y tourne dans un iframe
        tiers (`discordsays.com` dans `discord.com`) : le navigateur n'envoie
        jamais un cookie `Lax` dans ce cadre, et le joueur perdait son siege a
        chaque requete. Discord exige `SameSite=None; Partitioned` (doc
        « Networking » des activites, verifie le 29/09/2026).

        ⚠ EN-TETE ECRIT A LA MAIN, PAS `set_cookie(partitioned=True)`. aiohttp
        accepte le parametre, mais `http.cookies` ne connait `Partitioned`
        qu'a partir de Python 3.14 : sur le 3.10 du serveur, `claim_seat`
        tombait en 500 (`CookieError: Invalid attribute 'partitioned'`).
        """
        if self.EstCadreDiscord(request):
            morceaux = [f'{nom}={valeur}', 'Path=/']
            if max_age is not None:
                morceaux.append(f'Max-Age={max_age}')
            if httponly:
                morceaux.append('HttpOnly')
            morceaux += ['Secure', 'SameSite=None', 'Partitioned']
            response.headers.add('Set-Cookie', '; '.join(morceaux))
            return
        options = {'path': '/', 'httponly': httponly,
                   'secure': self.CookieSecure(request), 'samesite': 'Lax'}
        if max_age is not None:
            options['max_age'] = max_age
        response.set_cookie(nom, valeur, **options)

    @final
    def IsAuthenticate(self, request: web.Request) -> bool:
        if not self.hash_password:
            return True
        app_password_cookie = request.cookies.get('session_token')
        if app_password_cookie != self.hash_password:
            return False
        return True

    @final
    def IsVersionMatch(self, request: web.Request) -> bool:
        if not DETECTED_VERSION.value:
            return True
        app_version_cookie = request.cookies.get('app_version')
        if app_version_cookie and app_version_cookie != Ver.ui_version_str:
            return False
        elif not app_version_cookie:
            return False
        return True

    @final
    def AddHtmlSecurity(self, path: str, html: str):
        async def handle(request: web.Request) -> web.StreamResponse:
            if not self.SpectateurPeutLire(path, request):
                return web.Response(status=403, text='Spectator: read-only')
            if not self.IsAuthenticate(request):
                return self.LoadHtmlAuthenticate()
            elif not self.IsVersionMatch(request):
                return self.LoadHtmlCleanCache()
            else:
                return self.ReadFile(html)
        self.web_app.router.add_get(path, handle)

    @final
    def AddPost(self, path: str, handle: HandleAsyncType):
        self.web_app.router.add_post(path, handle)

    @final
    def SpectateurPeutEcrire(self, path: str, request: "web.Request") -> bool:
        """Un spectateur n'ECRIT rien. Refus par defaut, comme en lecture.

        ⚠ LE PENDANT MANQUANT DE `SpectateurPeutLire`, ET IL MANQUAIT DEPUIS
        LE DEBUT. Celle-la n'est appelee que par les routes GET
        (`AddAwaitGetSecurity`, `AddHtmlSecurity`) ; `AddPostSecurity`, lui,
        ne verifiait QUE le mot de passe de la table -- que le spectateur
        possede, sa porte d'entree le lui pose (`handle_spectateur`). Seul
        `/post` se defendait, et par un autre chemin : il applique
        `get_player_ids`, qui ne rend aucun siege a un spectateur. Toutes les
        AUTRES routes POST lui etaient donc ouvertes.

        Ce n'est pas theorique : la pause manuelle (20/09/2026) ajoute
        `/manuel_pause` et `/manuel_passer`. La seconde REPOND A LA PLACE
        d'un joueur assis. C'est mot pour mot le defaut pour lequel
        `SpectateurPeutLire` a ete ecrite le 15/09/2026 (« j'ai vu le bouton
        Annuler sur l'ecran du spectateur »), rejoue sur le verbe POST.

        ⚠ REFUS PAR DEFAUT, PAS UNE LISTE D'INTERDITS -- meme raisonnement
        que `SpectateurPeutLire` : une liste d'interdits laisserait passer la
        prochaine route POST ajoutee au moteur, sans que personne ne s'en
        apercoive. Une ecriture qui doit s'ouvrir au spectateur s'ecrit ICI,
        nommement, en connaissance de cause.

        La liste est VIDE, et c'est une mesure, pas une intuition : le
        plateau du spectateur n'emet aucun POST (il n'ouvre meme pas de
        socket, `ui-check/tests/spectateur-moteur.spec.ts`), et son seul
        envoi possible, le curseur, est deja coupe cote ecran
        (`CoucheCurseurs.tsx` : « le spectateur regarde, il n'emet pas »).
        """
        if request.cookies.get('spectateur') != '1':
            return True
        # Les ECRITURES nommement ouvertes au spectateur. Aucune a ce jour.
        # ⚠ ON JUGE LE CHEMIN DEMANDE, PAS CELUI DECLARE (meme piege que
        # `SpectateurPeutLire` : une route enregistree sous un motif ne
        # ressemble pas a l'adresse appelee).
        return request.path in ()

    @final
    def AddPostSecurity(self, path: str, handle: HandleAsyncType):
        async def new_handle(request: web.Request) -> web.StreamResponse:
            # Avant l'authentification, comme pour les routes de lecture : le
            # spectateur EST authentifie (sa porte lui pose le mot de passe de
            # la table), c'est le siege qui lui manque, pas la cle.
            if not self.SpectateurPeutEcrire(path, request):
                return web.Response(status=403, text='Spectator: read-only')
            if not self.IsAuthenticate(request):
                return web.Response(status=401)
            else:
                return await handle(request)
        self.web_app.router.add_post(path, new_handle)

    @final
    def ReadJsonFile(self, file_path: str|None, *, do_cache: bool=True) -> web.Response:
        if file_path:
            data = Json.Load(file_path)
            compressed_data = Json.DumpGZip(data)
            headers = {'Content-Encoding': 'gzip'}

            if do_cache:
                headers.update(self.HeaderCache)

            return web.Response(body=compressed_data, content_type='application/json', headers=headers)
        else:
            return web.json_response({})

    @final
    def ReadFile(self, file_path: str, find_paths: List[str]=[]) -> web.Response:
        if file_path.startswith("/"):
            file_path = "." + file_path

        def find_path(file_path: str) -> str:
            for path in ["./"] + find_paths:
                check_path = FileManager.JoinPath(path, file_path)
                if FileManager.Exists(check_path):
                    return check_path
            assert False, f"{file_path=}"

        def read_file(path: str, bin: bool):
            try:
                with FileManager.OpenFile(path, read=True, bin=bin) as file:
                    data = file.Read()
                    if not bin:
                        data = data.encode('utf-8')
                return data
            except Exception as exc:
                Log.FailedTrace(CATEGORY_NAME, exc)
                return ""

        try:
            found_path = find_path(file_path)
            data = read_file(found_path, True)
            mime_type = MimeType.GetMimeType(file_path)
            if Build.release:
                header = self.HeaderCache
            else:
                header = {}
            return web.Response(body=data, content_type=mime_type, headers=header)
        except Exception as exc:
            Log.Debug(CATEGORY_NAME, f"{file_path=}")
            Log.FailedTrace(CATEGORY_NAME, exc)
            return web.Response(status=404, headers=self.HeaderCache)

    @final
    def Run(self, ip: str, port: int, name: str="") -> None:
        async def start_server() -> None:
            try:
                await self.runner.setup()
                site = web.TCPSite(self.runner, ip, port)
                await site.start()
                Log.Print(f"{name}:\thttp://{ip}:{port}")
            except Exception as exc:
                Log.Print(f"{name}:\thttp://{ip}:{port} failed")
                Log.FailedTrace(CATEGORY_NAME, exc, no_take_as_error=True)

        self.ip = ip
        self.port = port
        TaskManager.AddTask(start_server, name="WebServer", run_forever=True)

    def Shutdown(self) -> None:
        pass

    ################################################################################
    #
    def AddDefaultGet(self):
        from build import Build

        async def handle_favicon(request: web.Request):
            file_path = './public/favicon.ico'
            return self.ReadFile(file_path)

        async def handle_authenticate(request: web.Request) -> web.Response:
            data = await request.json()
            password_attempt = data.get('password')
            session_token = hashlib.md5(password_attempt.encode()).hexdigest()

            response = web.Response()
            # `httponly` : le cookie reste illisible en JavaScript. `secure` est
            # deduit de la requete (voir `CookieSecure`), `samesite` depend du
            # cadre (voir `PoserCookie`).
            self.PoserCookie(response, request, 'session_token', session_token,
                             max_age=31536000)
            return response

        async def handle_get_version(request: web.Request) -> web.Response:
            # response = web.Response(text=Ver.ui_version_str)
            # Hack, make browser treat it as images and store in cache
            response = web.Response(body=Ver.ui_version_str, content_type='image/jpeg', headers=self.HeaderCache)
            if self.EstCadreDiscord(request):
                self.PoserCookie(response, request, 'app_version', Ver.ui_version_str,
                                 max_age=365 * 24 * 60 * 60, httponly=False)
            else:
                response.set_cookie(
                    'app_version',
                    Ver.ui_version_str,
                    max_age=365 * 24 * 60 * 60, # 1 year
                    path='/',
                    httponly=False
                )
            return response

        # PAGES DE L'ANCIEN SITE (Irefrixs), RETIREES (17/10/2026) : « tout ce qui est de l'ancien
        # site ne doit plus du tout etre visible, meme pas accessible avec une extension ». Elles
        # renvoient a notre accueil, avec ou sans `.html`. Les fichiers restent dans le depot.
        PAGES_RETIREES = {'/credits.html', '/deck.html', '/cards.html', '/main.html',
                          '/puzzle_editor.html', '/credits', '/deck', '/cards', '/puzzle_editor',
                          # Ancien client (18/10/2026) : le plateau est /app/board.html, l'assistant est prepare.html.
                          '/marvel.html', '/scene.html', '/scene', '/report.html', '/report'}

        async def handle_html(request: web.Request):
            if request.path in PAGES_RETIREES:
                raise web.HTTPFound('/')
            return self.ReadFile(request.path, ['./public/', './public/blueprints'])

        # Une feuille de style appelee avec une EMPREINTE DE CONTENU (`?v=` de 8 chiffres hexadecimaux, recalculee a chaque
        # deploiement par ui-app/deployer.sh) ne change jamais sous cette adresse : le navigateur la garde un an, au lieu de la
        # retelecharger toutes les 60 s. Sans cela, apres une minute, l'assistant attendait ses feuilles et montrait l'ancienne
        # page le temps du chargement (retour du 25/10/2026). Les `?v=1`, `?v=9` tenus a la main ne sont PAS concernes : rien
        # ne dit qu'ils changent quand le fichier change.
        async def handle_css(request: web.Request):
            reponse = self.ReadFile(request.path, ['./public/css', './public/'])
            if Build.release and reponse.status == 200 and reponse.content_length and re.fullmatch(r'[0-9a-f]{8}', request.query.get('v', '')):
                reponse.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            return reponse

        async def handle_js(request: web.Request):
            return self.ReadFile(request.path, ['./public/js', './public/'])

        async def handle_ts(request: web.Request):
            if Build.release:
                return web.Response(status=404, headers=self.HeaderCache)
            else:
                return self.ReadFile(request.path, ['./public/js', './public/'])

        async def handle_js_map(request: web.Request):
            if Build.release:
                return web.Response(status=404, headers=self.HeaderCache)
            else:
                return self.ReadFile(request.path, ['./public/js', './public/'])

        def handle_mp3(request: web.Request):
            return self.ReadFile(request.path, SOUND_FOLDERS.value)

        def handle_wav(request: web.Request):
            return self.ReadFile(request.path, SOUND_FOLDERS.value)

        async def handle_font(request: web.Request):
            file_path = request.path
            file_path = file_path.split("/")[-1]
            return self.ReadFile(file_path, ['./public/fonts'])

        async def handle_svg(request: web.Request):
            file_path = request.path
            file_path = file_path.split("/")[-1]
            return self.ReadFile(file_path, [TEXTURE_FOLDER.value])

        async def handle_gif(request: web.Request):
            return self.ReadFile('sparkles.gif', IMAGE_FOLDERS.value + [TEXTURE_FOLDER.value])

        async def handle_image_file(request: web.Request):
            # Fichiers image demandes AVEC extension (ex. les scans de livret de
            # campagne dans /public/stories/...). Les scans de cartes, eux,
            # passent par le resolveur sans extension et ne sont pas concernes.
            return self.ReadFile(request.path)

        self.AddAwaitGetSecurity('/favicon.ico', handle_favicon)

        # L'APPLICATION INSTALLEE DU TELEPHONE (zone 3, 10/10/2026) : manifeste,
        # icones et service worker. SANS session ni controle de version : le
        # navigateur les demande sans cookie quand il installe, et un manifeste
        # remplace par la page « vide ton cache » rendrait le jeu ininstallable.
        # Fichiers statiques et publics, sous public/pwa/ ; le motif n'accepte
        # qu'un nom simple, jamais un chemin.
        async def handle_pwa(request: web.Request):
            return self.ReadFile(request.match_info['fichier'], ['./public/pwa'])

        async def handle_service_worker(request: web.Request):
            # A la RACINE du site : un service worker ne gouverne que les pages
            # sous son propre chemin.
            return self.ReadFile('sw-plateau.js', ['./public/pwa'])

        self.AddAwaitGetSecurity(r'/pwa/{fichier:[a-z0-9-]+\.(?:png|webmanifest)}', handle_pwa,
                                 need_auth=False, need_check_version=False)
        self.AddAwaitGetSecurity('/sw-plateau.js', handle_service_worker,
                                 need_auth=False, need_check_version=False)

        self.AddPost(r'/authenticate', handle_authenticate)
        self.AddAwaitGetSecurity(r'/get_version', handle_get_version, need_auth=False, need_check_version=False)

        self.AddAwaitGetSecurity(r'/{path:.+\.html}', handle_html)
        self.AddAwaitGetSecurity(r'/{path:.+\.css}', handle_css)
        self.AddAwaitGetSecurity(r'/{path:.+\.js}', handle_js)
        self.AddAwaitGetSecurity(r'/{path:.+\.ts}', handle_ts)
        self.AddAwaitGetSecurity(r'/{path:.+\.js.map}', handle_js_map)

        self.AddNonAwaitGetSecurity(r'/{path:.+\.mp3}', handle_mp3)
        self.AddNonAwaitGetSecurity(r'/{path:.+\.wav}', handle_wav)

        self.AddAwaitGetSecurity(r'/{path:.+\.eot}', handle_font)
        self.AddAwaitGetSecurity(r'/{path:.+\.woff}', handle_font)
        # .woff2 : sans cette ligne, l'Inter des pages Epure (public/fonts/Inter-*.woff2) tombait dans la route des
        # images et le navigateur recevait un JPEG a la place de la police (18/10/2026).
        self.AddAwaitGetSecurity(r'/{path:.+\.woff2}', handle_font)
        self.AddAwaitGetSecurity(r'/{path:.+\.ttf}', handle_font)

        self.AddAwaitGetSecurity(r'/{path:.+\.svg}', handle_svg)
        self.AddAwaitGetSecurity(r'/{path:.+\.gif}', handle_gif)

        self.AddAwaitGetSecurity(r'/{path:.+\.jpg}', handle_image_file)
        self.AddAwaitGetSecurity(r'/{path:.+\.jpeg}', handle_image_file)
        self.AddAwaitGetSecurity(r'/{path:.+\.png}', handle_image_file)
        self.AddAwaitGetSecurity(r'/{path:.+\.webp}', handle_image_file)

