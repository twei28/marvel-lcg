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

    def UpdateVersion(self):
        pass

