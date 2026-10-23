"""De `PuzzleData` a la scene que le moteur joue (sans dependance reseau).

Sorti de `server_new_game.py` le 22/10/2026 pour que le serveur ET les tests
montent un puzzle par le meme chemin, et pour mettre en place 1 a 4 heros.
"""
import json
from typing import Any, Dict, List

from game.puzzle.puzzle_data import PuzzleData

# `start_phase` du format -> `scene.reprise_auto` (voir World.OnGameLoop).
START_PHASE_TO_RESUME = {'': '', 'player': '', 'villain': 'mechant', 'end_round': 'tour'}


def BuildPuzzleCommands(puzzle: PuzzleData) -> List[str]:
    """Les commandes de mise en place, jouees AVANT `puzzle_command`.

    Un puzzle a un seul heros garde EXACTEMENT les commandes d'avant (sans `siege`) :
    ses comportements, et ceux des puzzles v1, ne changent pas. A plusieurs heros,
    chaque commande vise son siege (l'ordre des sieges ne bouge jamais).
    """
    commands: List[str] = []

    def add(command: str, cards: List[str], siege: Any = None) -> None:
        text = ",".join(f"'{x}'" for x in cards)
        if not text:
            return
        if siege is not None:
            text += f", siege={siege}"
        commands.append(f"{command}({text})")

    # ORDRE DES PILES. Le moteur empile : la DERNIERE carte creee est sur le DESSUS
    # (mesure du 22/10/2026). Les fichiers v1 donnent donc leurs piles du dessous
    # vers le dessus, et c'est conserve tel quel. Le format 2 les donne du DESSUS
    # vers le dessous (comme une liste a l'ecran) : on inverse ici.
    top_first = puzzle.format >= 2

    def pile(cards: List[str]) -> List[str]:
        return list(reversed(cards)) if top_first else list(cards)

    add("Puzzle.CreateEncounterDeck", pile(puzzle.encounter_deck))
    add("Puzzle.CreateEncounterDiscardPile", pile(puzzle.encounter_discard_pile))
    several = len(puzzle.players) > 1
    for index, player in enumerate(puzzle.players):
        siege = index if several else None
        add("Puzzle.CreateHandCards", player.hand_cards, siege)
        add("Puzzle.CreatePlayerDiscardPile", pile(player.player_discard_pile), siege)
        add("Puzzle.CreatePlayerDeck", pile(player.player_deck), siege)
        add("Puzzle.CreatePlayerAdditionalDeck", player.set_aside, siege)
    if puzzle.first_player:
        commands.append(f"Puzzle.SetFirstPlayer({int(puzzle.first_player)})")
    return commands


def BuildPuzzleScene(puzzle: PuzzleData) -> Dict[str, Any]:
    """Le dictionnaire de scene (a charger avec `Json.LoadsAs(..., Scene)`)."""
    return {
        "version": puzzle.version,
        "metadata": {
            "seed": puzzle.seed,
            "comment": puzzle.comment,
            "cover": puzzle.cover,
            "is_puzzle": True,
        },
        "campaign": {
            "version": puzzle.version,
            "name": "Villain",
            "villain": puzzle.villain,
            "expert": puzzle.expert,
            "schemes": puzzle.schemes,
            "set_aside": puzzle.set_aside,
            "encounters": [],
            "encounter_sets": [],
            "modular_sets": [],
        },
        "players": [
            {
                "version": puzzle.version,
                "name": f"Player {index}",
                "hero": puzzle.players[index].identities,
                "hero_deck": [],
                "obligations": [],
                "nemesis_set": [],
                "set_aside": puzzle.players[index].set_aside,
                "player_deck": [],
            }
            for index in range(len(puzzle.players))
        ],
        "puzzle": BuildPuzzleCommands(puzzle) + puzzle.puzzle_command,
        "reprise_auto": START_PHASE_TO_RESUME.get(puzzle.start_phase, ''),
        "puzzle_objectifs": [
            json.dumps({"kind": x.kind, "target": x.target, "text": x.text}, ensure_ascii=False)
            for x in puzzle.objectives
        ],
        "puzzle_objectifs_mode": puzzle.objectives_mode,
        "puzzle_info": json.dumps({
            "title": puzzle.title, "description": puzzle.description, "difficulty": puzzle.difficulty,
            "hints": puzzle.hints, "author": puzzle.author,
            "solution_text": puzzle.solution_text, "solution_visibility": puzzle.solution_visibility,
        }, ensure_ascii=False) if puzzle.format >= 2 and (puzzle.title or puzzle.description or puzzle.hints or puzzle.solution_text) else "",
    }
