from core import *

@dataclass
class HeroDescriptor:
    version: str
    name: str
    hero: List[str]
    hero_deck: List[str]
    obligations: List[str]
    nemesis_set: List[str]
    player_deck: List[str] = field(default_factory=lambda: [])
    # IDENTITE LIEE. Certains packs physiques font piloter DEUX heros par un
    # seul joueur (Cloak & Dagger) : chaque identite garde son mini-deck, sa
    # main et sa defausse. Le moteur sait deja tenir cela pour deux JOUEURS ;
    # l'identite liee est donc developpee en un second joueur au chargement
    # (voir `SceneLoader.NewFromJson`), ce qui evite de redefinir ce que
    # `player.GetIdentity()` renvoie dans les ~770 endroits qui l'appellent.
    linked_identity: Dict[str, Any] = field(default_factory=lambda: {})
    # CAMP. 0 en partie ordinaire : tous les joueurs sont dans la meme zone
    # de jeu et rien ne change. En mode competitif (livret mc56 p.14), 0 est
    # l'equipe qui joue en premier chaque round et 1 l'equipe adverse ;
    # chaque camp a sa zone, son leader et son deck rencontre.
    team: int = 0

    def UpdateVersion(self):
        pass

