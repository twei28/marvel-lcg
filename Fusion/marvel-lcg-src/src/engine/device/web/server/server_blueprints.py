# Recovered automatically from Python 3.10 bytecode.
# Comments and original formatting were not present in the compiled file.

from core import *
from engine.device.web.server.server_base import GameServerBase
CATEGORY_NAME = 'BLUEPRINT'
class GameServerBlueprints(GameServerBase):
    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddHtmlSecurity('/blueprints', './public/blueprints/index.html')
