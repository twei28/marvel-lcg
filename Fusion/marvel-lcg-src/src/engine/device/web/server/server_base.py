from core import *
from engine.network import WebServer
from aiohttp import web
from engine.device.manager.web.manager import WebDeviceManager
from engine.controller import *
from engine.config import ConfigVariables

# Ajout local : PROTECTION DES SIEGES en multijoueur distant.
# `seat_passwords` (launch.online.json) donne un mot de passe par joueur
# (liste de 4 chaines ; chaine vide = siege libre). Vide ou absent = aucun
# controle, comportement d'origine (JOUER-SOLO et hot-seat local intacts).
# Un client prouve son siege via le cookie seat_token_<n> pose par /claim_seat.
SEAT_PASSWORDS = ConfigVariables.ListStr('seat_passwords', [])
# Adresse de l'administration du SITE qui a lance cette partie. Vide par
# defaut : un moteur lance a la main n'a pas de site devant lui, et le bouton
# n'apparait alors nulle part. L'orchestrateur ne renseigne cette cle que pour
# la partie de l'administrateur.
SITE_ADMIN_URL = ConfigVariables.Str('site_admin_url', '')
# Adresse LOCALE du site qui a lance cette partie, et jeton pour parler en son
# nom. Vides par defaut : un moteur lance a la main n'a pas de site derriere
# lui, et le panneau des joueurs ne s'affiche alors nulle part.
# ⚠ Le jeton ne doit JAMAIS partir vers le navigateur : c'est le moteur qui
# appelle le site, pas le client.
SITE_INTERNE = ConfigVariables.Str('site_interne', '')
SITE_JETON = ConfigVariables.Str('site_jeton', '')

class GameServerBase(WebServer):

    def __init__(self) -> None:
        super().__init__()

    def SetManager(self, manager: 'WebDeviceManager'):
        self.device_manager = manager

    def seat_hash(self, seat_password: str) -> str:
        import hashlib
        return hashlib.md5(seat_password.encode()).hexdigest()

    def seats_reprises(self) -> 'Dict[int, str]':
        """Sieges repris par un remplacant : siege -> phase de la prise.

        La reprise DURE jusqu'a la fin du tour ou elle a ete accordee. Sans
        cette memoire, le siege redeviendrait celui de son proprietaire des sa
        reconnexion — donc potentiellement en plein paiement du remplacant, a
        qui on couperait la main au milieu d'un geste.
        """
        if not hasattr(self, '_seats_reprises'):
            self._seats_reprises: Dict[int, str] = {}
        return self._seats_reprises

    def phase_courante(self) -> str:
        try:
            world = self.game.world
            return world.GetPhaseText() if world else ''
        except Exception:
            return ''

    def seat_orphelin(self, seat: int) -> bool:
        """Ce siege n'a plus aucun client connecte."""
        try:
            return not self.device_manager.client_manager.GetClients(seat)
        except Exception:
            return False

    def est_spectateur(self, request: web.Request) -> bool:
        """Ce client REGARDE, il ne joue pas. Cookie pose par `/spectateur`.

        ⚠ C'EST ICI QUE TIENT LA GARANTIE, PAS DANS LE NAVIGATEUR. Desarmer le
        plateau cote client est une politesse : un raccourci clavier, une
        console ouverte ou un simple `curl` en feraient le tour. Le moteur,
        lui, ne laisse pas passer une action sans siege — encore faut-il qu'il
        n'en accorde AUCUN a un spectateur, ce qui n'allait pas de soi :
        `allowed_seats` ouvre tout siege ORPHELIN a n'importe quel client
        authentifie (« reprise d'un siege abandonne », plus bas). Un spectateur
        arrive pendant qu'un joueur s'est deconnecte aurait donc herite de sa
        place. Mesure du 15/09/2026.

        Le cookie ne se falsifie pas utilement : le poser ne fait que RETIRER
        des droits a celui qui le porte.
        """
        return request.cookies.get('spectateur') == '1'

    def sieges_demandes(self, request: web.Request) -> 'List[int]':
        """Les sieges que l'URL demande, SANS aucun filtre de droits.

        Sert a la seule LECTURE : un spectateur doit pouvoir regarder la table
        par les yeux du siege 2 sans jamais obtenir le droit d'y agir.
        """
        p = request.query.get('p', '0')
        if not p:
            return [0]
        try:
            return [int(id) for id in p.split(',')]
        except ValueError:
            return [0]

    def tient_le_siege(self, request: web.Request, seat: int) -> bool:
        """Ce client PROUVE-t-il qu'il tient ce siege, cookie en main ?

        ⚠ NE PAS REMPLACER PAR `allowed_seats` : elle ouvre tout siege
        qu'aucun client ne tient (« reprise d'un siege abandonne », plus bas).
        C'est juste EN COURS de partie, ou un siege muet bloquerait tout le
        monde. C'est faux AVANT : tant que personne ne s'est connecte, les
        quatre sieges sont orphelins, et le premier visiteur venu passerait
        pour l'hote. A n'utiliser que la ou une usurpation coute cher, comme
        la distribution des cles de siege.
        """
        passwords = SEAT_PASSWORDS.value
        if seat < 0 or seat >= len(passwords):
            return False
        attendu = passwords[seat]
        if not attendu:
            return True          # siege volontairement laisse sans protection
        jeton = request.cookies.get(f'seat_token_{seat}')
        return bool(jeton) and jeton == self.seat_hash(attendu)

    def allowed_seats(self, request: web.Request) -> 'Set[int]|None':
        """Sieges que CE client a le droit d'occuper. None = protection coupee."""
        # ⚠ LE SPECTATEUR N'EN A AUCUN, ET C'EST LA PREMIERE CHOSE QU'ON DIT.
        # Avant la protection par mot de passe, avant la reprise des sieges
        # orphelins : un `set()` vide fait echouer `handle_post` (403) quoi
        # qu'il arrive, y compris sur une table sans mot de passe.
        if self.est_spectateur(request):
            return set()
        passwords = SEAT_PASSWORDS.value
        if not passwords or not any(passwords):
            return None
        allowed: Set[int] = set()
        for seat, password in enumerate(passwords):
            if not password:
                allowed.add(seat)
                continue
            token = request.cookies.get(f'seat_token_{seat}')
            if token and token == self.seat_hash(password):
                allowed.add(seat)

        # REPRISE D'UN SIEGE ABANDONNE.
        #
        # Un siege dont plus personne ne tient la place bloquait la partie : le
        # moteur l'interrogeait, personne ne pouvait repondre. On l'ouvre donc a
        # tout client deja authentifie — et on RETIENT la prise, pour qu'elle
        # survive au retour du proprietaire jusqu'a la fin du tour en cours.
        reprises = self.seats_reprises()
        phase = self.phase_courante()
        for seat, phase_de_prise in list(reprises.items()):
            # ⚠⚠ CORRECTIF DU 09/09/2026 — `and self.seat_orphelin(seat)` AJOUTE.
            #
            # Sans lui, une table LOCALE A DEUX HEROS sur un serveur protege ne
            # demarrait jamais : elle restait figee avant « Draw Cards », donc
            # avant le mulligan. Signale en jeu (« il me sort toujours pas la
            # premiere main pour pouvoir mulligan »), et reproduit ici le
            # 09/09/2026 sur une copie locale configuree comme la place 1.
            #
            # La chaine, mesuree par une sonde posee dans `get_player_ids` :
            #   /ws?hot_seat&p=0     -> allowed=[0,1,2,3]  ids=[0,1]
            #   /get_ask?p=0         -> allowed=[2,3]      ids=[]
            # Le plateau annonce le hot-seat sur le SOCKET et sur l'accuse de
            # reception, mais `/get_ask` et `/post` sont per-siege et ne le
            # portent pas (`handle_post` exige d'ailleurs UN seul siege). Un
            # siege sans mot de passe prouve n'etait accorde que tant qu'il
            # etait ORPHELIN ; des que le socket hot-seat le tenait, il cessait
            # de l'etre, la reprise tombait au premier changement de phase, et
            # plus rien ne le rendait. Le moteur posait sa question au siege 1,
            # le client ne la voyait jamais, et la mise en place s'arretait la.
            #
            # La reprise dure donc maintenant tant que le siege est TENU. Le
            # proprietaire, lui, le reprend par son cookie, chemin qui n'a pas
            # bouge : c'est la garde du dessus (`seat_token_<siege>`), pas
            # celle-ci.
            if phase_de_prise != phase and self.seat_orphelin(seat):
                # Le tour a change ET plus personne ne le tient : le siege
                # revient a son proprietaire.
                del reprises[seat]
            else:
                allowed.add(seat)

        for seat in range(len(passwords)):
            if seat not in allowed and self.seat_orphelin(seat):
                reprises[seat] = phase
                allowed.add(seat)

        return allowed

    def get_player_ids(self, request: web.Request) -> List[int]:
        is_hot_seat = 'hot_seat' in request.rel_url.query
        if is_hot_seat:
            manager = self.controller_manager
            player_ids = list(range(manager.total_players))
        else:
            p = request.query.get('p', '0')
            if p == '':
                player_ids = [0]
            else:
                parts = p.split(',')
                player_ids = [int(id) for id in parts] if parts else [0]

        allowed = self.allowed_seats(request)
        if allowed is not None:
            player_ids = [id for id in player_ids if id in allowed]
        return player_ids

    def get_first_controller(self, request: web.Request) -> 'Controller':
        # Un spectateur n'a aucun siege autorise (voir `allowed_seats`) : sans
        # cette ligne il lirait toujours la table par les yeux du siege 0, et
        # « changer de siege » ne montrerait jamais la main du siege 2.
        if self.est_spectateur(request):
            demandes = self.sieges_demandes(request)
            vise = demandes[0] if demandes else 0
            controllers = self.device_manager.controllers
            return controllers[vise if 0 <= vise < len(controllers) else 0]
        player_ids = self.get_player_ids(request)
        # Sieges filtres par la protection : la LECTURE du monde reste permise
        # (plateau public), seule l'ACTION est un privilege du siege.
        player_id = player_ids[0] if player_ids else 0
        controllers = self.device_manager.controllers
        # Siege inexistant (« ?p=1 » en solo, lien de multi recycle...) : on
        # retombe sur le premier plutot que de renvoyer un 500 qui laisse le
        # plateau vide. La lecture est publique, seul l'agir est un privilege.
        if player_id >= len(controllers):
            player_id = 0
        return controllers[player_id]

    @property
    def controller_manager(self):
        controller = self.device_manager.controllers[0]
        return controller.manager

    @property
    def game(self):
        controller = self.device_manager.controllers[0]
        return controller.game
