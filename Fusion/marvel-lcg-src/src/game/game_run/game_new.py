from core import *

from game.game_run.game_challenge import GameChallenge

@dataclass
class NewGameDescriptor:
    campaign_json: str
    encounter_set_names: List[str]
    hero_json: List[str]
    seed: int
    timeout: float
    challenges: List['GameChallenge.CHALLENGE']
    rules: List[str]
    campaign_log: Dict[str, str]
    # MODE COMPETITIF. Vides en partie ordinaire, et le moteur se comporte
    # alors exactement comme avant.
    #
    # Chaque equipe apporte SON scenario et affronte celui de l'autre
    # (mc56 p.14, etape 4) : `campaign_json` est pose devant l'equipe 0,
    # `campaign_json_2` devant l'equipe 1, avec ses propres sets de rencontre.
    # `teams` donne le camp de chaque entree de `hero_json`, dans le meme ordre.
    campaign_json_2: str = field(default="")
    encounter_set_names_2: List[str] = field(default_factory=lambda: [])
    teams: List[int] = field(default_factory=lambda: [])
    # custom_script: str = field(default="")
