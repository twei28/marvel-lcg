from core import *

# Format de puzzle v2 (22/10/2026). Tous les champs ajoutés ont une valeur par
# défaut : le chargeur (Json.ConvertDictToDataclass) ignore les clés inconnues et
# laisse les défauts aux clés absentes, donc un fichier v1 se lit tel quel et
# `format` vaut alors 1. Spécification : docs/puzzle/FORMAT-V2.md.

@dataclass
class PuzzleObjective:
    # 'defeat_villain' : vaincre le méchant ; 'survive' : aucun héros vaincu et complot
    # non perdu jusqu'à la fin du tour ; 'complete_scheme' : terminer le complot
    # désigné par `target` ; 'free_text' : objectif libre, validé à la main.
    kind: str = ""
    target: str = ""    # 'complete_scheme' : nom ou identifiant de la carte visée
    text: str = ""      # texte affiché au résolveur ('free_text' : obligatoire)

@dataclass
class PuzzleData:
    version: str
    author: str
    cover: str
    comment: str
    seed: int
    villain: List[str]
    schemes: List[str]
    encounter_deck: List[str]
    encounter_discard_pile: List[str]
    set_aside: List[str]
    expert: bool
    @dataclass
    class PlayerData:
        identities: List[str]
        hand_cards: List[str]
        player_deck: List[str]
        player_discard_pile: List[str]
        set_aside: List[str]
        # Deck de départ d'où vient le héros (information d'affichage seulement) ;
        # le contenu réel du puzzle est dans les champs ci-dessus.
        deck_name: str = ""
    players: List[PlayerData]
    puzzle_command: List[str]

    # --- v2 -------------------------------------------------------------
    format: int = 1                 # 1 = ancien fichier, 2 = format v2
    title: str = ""
    description: str = ""
    difficulty: int = 0             # 0 = non précisée, sinon 1 à 5
    hints: List[str] = field(default_factory=list)
    objectives: List[PuzzleObjective] = field(default_factory=list)
    objectives_mode: str = "all"    # 'all' : tous requis ; 'any' : au moins un
    # Où le tour démarre : '' = début de la phase joueur (comportement v1),
    # 'player', 'villain' ou 'end_round' ; `start_step` précise l'étape.
    start_phase: str = ""
    start_step: str = ""
    first_player: int = 0           # indice du premier joueur dans `players`
    # Visibilité de la solution de référence : 'after' (après résolution),
    # 'always' ou 'never'. La solution elle-même est stockée à part (replay).
    solution_visibility: str = "after"
    has_solution: bool = False
