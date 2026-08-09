from engine.device.web.server.server_files import GameServerFiles
from engine.device.web.server.server_html import GameServerHTML
from engine.device.web.server.server_get import GameServerGet
from engine.device.web.server.server_new_game import GameServerNewGame
from engine.device.web.server.server_socket import GameServerSocket
from engine.device.web.server.server_sync import GameServerSync
# Ajouts locaux : upload (partage de sauvegardes) et blueprints (pages /host,
# /peerjs et /blueprints du multijoueur). Fichiers absents du dépôt officiel.
from engine.device.web.server.server_upload import GameServerUpload
from engine.device.web.server.server_blueprints import GameServerBlueprints
# Mode campagne : definitions livrees (data/campagnes/) et campagnes en cours
# du joueur (../campagnes/). Fichier absent du depot officiel.
from engine.device.web.server.server_campagne import GameServerCampagne
from engine.device.manager.web.manager import WebDeviceManager

class GameServer(GameServerFiles, GameServerHTML, GameServerGet, GameServerNewGame, GameServerSocket, GameServerSync, GameServerUpload, GameServerBlueprints, GameServerCampagne):

    def __init__(self, manager: 'WebDeviceManager') -> None:
        self.SetManager(manager)
        super().__init__()

