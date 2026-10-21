from . import *

################################################################################
# BRIQUE M1/M2 (PU-5, 21/10/2026) : LA VILLE, grille de lieux et territoires.
# Spec : docs/rapports/spec-ville-m1-m2-2026-10-21.md (regles R1-R12 du livret FR « La ville ne dort jamais »).
#
#   - une grille de lieux (lignes x colonnes), chaque case porte une carte (le lieu) ;
#   - chaque LIGNE est le territoire d'un CAPO = une zone de jeu du moteur (`GameArea`) ;
#   - la position d'un joueur est une case ; changer de ligne change de zone (`World.MovePlayerToGameArea`) ;
#   - les manigances et environnements de la ville vivent dans la zone COMMUNE (`World.game_area_commune`).
#
# Sans `Ville.Installer`, RIEN n'existe et aucune partie ordinaire n'est touchee.
class EtatVille:
    def __init__(self) -> None:
        self.cases: Dict[Tuple[int, int], 'CardFace'] = {}
        self.zones: Dict[int, 'GameArea'] = {}          # ligne -> zone de jeu
        self.positions: Dict[int, Tuple[int, int]] = {}  # indice du joueur (`player.player_id`) -> case

Case = Tuple[int, int]


class Ville:

    ############################################################################
    # Installer / lire
    @staticmethod
    def Installer(effect_or_world: 'Effect|World', cases: Dict[Case, 'CardFace'], zones: Dict[int, 'GameArea'],
                  depart: Case) -> None:
        """Pose la grille (case -> carte de lieu), les zones par ligne, et place TOUS les joueurs sur la case de depart
        (R1 : tous a Midtown)."""
        from game.operate.worlds import Worlds
        world = Worlds.CastWorld(effect_or_world)
        etat = EtatVille()
        etat.cases = dict(cases)
        etat.zones = dict(zones)
        world.ville = etat
        from game.message import Message
        for joueur in world.const_players:
            etat.positions[joueur.player_id] = depart
            world.MovePlayerToGameArea(joueur, zones[depart[0]])
            Message.AfterPlayerMovedInCity(joueur).Send()

    @staticmethod
    def Etat(effect_or_world: 'Effect|World') -> 'EtatVille|None':
        from game.operate.worlds import Worlds
        return getattr(Worlds.CastWorld(effect_or_world), 'ville', None)

    @staticmethod
    def Case(effect_or_world: 'Effect|World', joueur: 'Player') -> 'Case|None':
        etat = Ville.Etat(effect_or_world)
        return None if etat is None else etat.positions.get(joueur.player_id)

    @staticmethod
    def Lieu(effect_or_world: 'Effect|World', joueur: 'Player') -> 'CardFace|None':
        """La carte de lieu que le joueur occupe (R3)."""
        etat = Ville.Etat(effect_or_world)
        case = Ville.Case(effect_or_world, joueur)
        return None if etat is None or case is None else etat.cases.get(case)

    @staticmethod
    def CaseDe(effect_or_world: 'Effect|World', lieu: 'CardFace') -> 'Case|None':
        etat = Ville.Etat(effect_or_world)
        if etat is None:
            return None
        for case, carte in etat.cases.items():
            if carte.card is lieu.card:
                return case
        return None

    @staticmethod
    def Joueurs(effect_or_world: 'Effect|World', lieu: 'CardFace') -> List['Player']:
        """Les joueurs presents sur ce lieu."""
        from game.operate.worlds import Worlds
        world = Worlds.CastWorld(effect_or_world)
        case = Ville.CaseDe(world, lieu)
        if case is None:
            return []
        return [j for j in world.const_players if Ville.Case(world, j) == case]

    @staticmethod
    def Inoccupe(effect_or_world: 'Effect|World', lieu: 'CardFace') -> bool:
        """« Lieu inoccupe » = sans aucun joueur present (FAQ du livret)."""
        return Ville.Joueurs(effect_or_world, lieu) == []

    @staticmethod
    def Occupe(effect_or_world: 'Effect|World', joueur: 'Player', lieu: 'CardFace') -> bool:
        """Ce joueur occupe-t-il ce lieu ? (R3 : on n'interagit qu'avec le lieu qu'on occupe)."""
        case = Ville.Case(effect_or_world, joueur)
        return case is not None and case == Ville.CaseDe(effect_or_world, lieu)

    @staticmethod
    def Adjacentes(effect_or_world: 'Effect|World', case: Case) -> List[Case]:
        """Les cases orthogonalement voisines (nord/sud/est/ouest) qui portent un lieu (R2 : ni diagonale, ni hors grille)."""
        etat = Ville.Etat(effect_or_world)
        if etat is None:
            return []
        l, c = case
        voisines = [(l - 1, c), (l + 1, c), (l, c - 1), (l, c + 1)]
        return [v for v in voisines if v in etat.cases]

    ############################################################################
    # Agir
    @staticmethod
    def Deplacer(effect_or_world: 'Effect|World', joueur: 'Player', case: Case) -> bool:
        """Deplace le joueur sur une case ADJACENTE ; change de zone si la ligne change (R2, R4). Rend False (rien ne bouge) si la
        case n'est pas voisine. Le cout (epuiser un personnage ou 1 ressource) est paye par l'appelant (l'Action de The City)."""
        from game.operate.worlds import Worlds
        world = Worlds.CastWorld(effect_or_world)
        depuis = Ville.Case(world, joueur)
        if depuis is None or case not in Ville.Adjacentes(world, depuis):
            return False
        return Ville.Placer(world, joueur, case)

    @staticmethod
    def Placer(effect_or_world: 'Effect|World', joueur: 'Player', case: Case) -> bool:
        """Pose le joueur sur une case QUELCONQUE de la grille (« Move to a location », Red Herring), sans condition d'adjacence ; change de zone si
        la ligne change. Rend False si la case n'existe pas."""
        from game.operate.worlds import Worlds
        world = Worlds.CastWorld(effect_or_world)
        etat = Ville.Etat(world)
        depuis = Ville.Case(world, joueur)
        if etat is None or depuis is None or case not in etat.cases:
            return False
        etat.positions[joueur.player_id] = case
        if case[0] != depuis[0]:
            world.MovePlayerToGameArea(joueur, etat.zones[case[0]])
        from game.message import Message
        Message.AfterPlayerMovedInCity(joueur).Send()
        return True

    ############################################################################
    # Conditions des capacites de lieu
    @staticmethod
    def AuLieu(effect: 'Effect', message: 'Message2') -> bool:
        """Condition des capacites d'une carte de LIEU (R3 : « on n'interagit qu'avec le lieu qu'on occupe ») : le joueur qui declenche
        la capacite occupe-t-il cette carte ? A poser dans `conditions=[Ville.AuLieu]`. Une carte attachee a un lieu (M5) pose la meme
        condition sur le lieu qui la porte."""
        from game.player import Player
        joueur = message.GetToPlayer() if hasattr(message, 'GetToPlayer') else None
        if not isinstance(joueur, Player):
            initiateur = getattr(effect, 'initiator', None)
            joueur = initiateur if isinstance(initiateur, Player) else None
        return joueur is not None and Ville.Occupe(effect, joueur, effect.this)
