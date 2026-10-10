from typing import TypeAlias
from core import *
# from engine.lib import Json
from game.card.face import *

KEY_NAME: TypeAlias = Literal['damage_dealt', 'damage_taken', 'thwarted_threat', 'entered_play']

# Les compteurs de la PARTIE, par joueur (ecran de fin, onglet Stats, 10/10/2026).
# Recrees a chaque `GameSetup` : un Undo rejoue la partie depuis le debut et les
# reconstruit a l'identique, sans rien compter deux fois.
CLES_SIEGE: Tuple[str, ...] = (
    'degats_mechant',       # degats infliges au(x) mechant(s)
    'degats_sbires',        # degats infliges aux sbires
    'menace_principale',    # menace retiree de la manigance principale
    'menace_annexes',       # menace retiree des manigances annexes
    'degats_subis',         # degats pris par le heros et les allies du joueur
    'degats_evites',        # attaques ennemies : valeur d'attaque - degats subis
    'attaques_defendues',   # attaques ennemies prises par un defenseur du joueur
    'cartes_jouees',        # cartes jouees (AfterPlayerPlayedCard)
    'ressources_depensees', # ressources produites pour payer (WhenCardBeSpendAsResource)
)

class SessionStatistics:

    def __init__(self) -> None:
        self.dic: Dict[int, Dict[KEY_NAME, int]] = {}
        self.DEFAULT_STATS = dict.fromkeys(get_args(KEY_NAME), 0)
        # index du joueur (const_players) -> compteur -> valeur
        self.sieges: Dict[int, Dict[str, int]] = {}
        # index du joueur -> card_id -> {'nom', 'piochee', 'jouee'}
        self.cartes: Dict[int, Dict[str, Dict[str, Any]]] = {}
        # Duree de la partie en secondes, figee au premier calcul apres la fin.
        self.temps_fin: 'int|None' = None

    def Add(self, face: 'CardFace', value: int, name: KEY_NAME):
        if not PlayerCard.IsType(face):
            return
        id = face.card.object_id
        stats = self.dic.setdefault(id, self.DEFAULT_STATS.copy())
        stats[name] += value

    @staticmethod
    def _Siege(player: 'Player|None') -> 'int|None':
        if player is None:
            return None
        try:
            return player.world.const_players.index(player)
        except Exception:
            return None

    def AddSiege(self, player: 'Player|None', name: str, value: int) -> None:
        siege = self._Siege(player)
        if siege is None or value <= 0:
            return
        compteurs = self.sieges.setdefault(siege, dict.fromkeys(CLES_SIEGE, 0))
        compteurs[name] = compteurs.get(name, 0) + value

    def AddCarte(self, player: 'Player|None', face: 'CardFace', name: Literal['piochee', 'jouee']) -> None:
        siege = self._Siege(player)
        if siege is None:
            return
        card_id = face.paper.card_id
        cartes = self.cartes.setdefault(siege, {})
        entree = cartes.setdefault(card_id, {'nom': face.paper.name, 'piochee': 0, 'jouee': 0})
        entree[name] += 1

    # def Get(self) -> str:
    #     return Json.Dumps(self.dic)
