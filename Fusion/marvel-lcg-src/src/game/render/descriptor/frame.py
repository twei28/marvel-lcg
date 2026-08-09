from core import *

@dataclass
class FrameDescriptor:
    render_id           : int
    game_id             : int
    ask_players         : List[int]
    remaining_time      : float
    max_timeout         : float
    notify_texts        : List[str]
    debug_message       : str
    current_step_id     : int
    max_replay_step_id  : int
    player_id           : int
    total_players       : int
    # Ajout local : sieges SANS aucun client connecte.
    #
    # Le serveur le sait deja (client_manager.GetClients), mais rien ne le
    # disait au plateau : quand le moteur interrogeait un joueur parti, tout le
    # monde voyait la partie s'arreter sans un mot. Ce champ permet d'afficher
    # « X est deconnecte » et de proposer de jouer a sa place.
    sieges_absents      : List[int] = field(default_factory=lambda: [])
    # is_skipping         : bool

