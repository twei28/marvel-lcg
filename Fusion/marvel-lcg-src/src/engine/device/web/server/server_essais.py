"""Les ESSAIS par compte : ce qui est livré mais réservé à quelques tables.

AJOUT du 10/10/2026 : « Nouvelle phase du méchant (essai) », cochée par
l'administrateur dans /admin pour un compte (le site écrit
`essai_phase_mechant` dans la configuration de sa table). Un moteur lancé à la
main n'a pas la clé : l'ancien panneau reste.

⚠ LECTURE OUVERTE, ET C'EST SANS DANGER : le drapeau ne choisit qu'un
affichage. Toute la table le voit, invités compris, puisque c'est la table du
compte qui fait l'essai.
"""
from core import *
from aiohttp import web
from engine.config import ConfigVariables
from engine.device.web.server.server_base import GameServerBase

ESSAI_PHASE_MECHANT = ConfigVariables.Bool('essai_phase_mechant', False)


class GameServerEssais(GameServerBase):

    async def get_essais(self, request: web.Request) -> web.Response:
        return web.json_response({'phase_mechant': bool(ESSAI_PHASE_MECHANT.value)})

    @override
    def __init__(self) -> None:
        super().__init__()
        self.AddAwaitGetSecurity('/get_essais', self.get_essais)
