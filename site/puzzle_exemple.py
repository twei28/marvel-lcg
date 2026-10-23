"""Un puzzle de format 2 valide, pour les tests du serveur de puzzles."""

PUZZLE = {
    "version": "0.5.8", "author": "", "cover": "01094", "comment": "", "seed": 1,
    "villain": ["01094"], "schemes": ["01097a,01097b"], "encounter_deck": ["01110"],
    "encounter_discard_pile": [], "set_aside": [], "expert": False,
    "players": [{"identities": ["01001b"], "hand_cards": ["01071"], "player_deck": ["01072"],
                 "player_discard_pile": [], "set_aside": [], "deck_name": "Spider-Man"}],
    "puzzle_command": ["Puzzle.RestoreCard('e1', '01059', 'ally', siege=0, health=2)", "Puzzle.SetHealth('01094', 9)"],
    "format": 2, "title": "Mon puzzle", "description": "d", "difficulty": 2, "hints": ["h"],
    "objectives": [{"kind": "defeat_villain", "target": "", "text": ""}], "objectives_mode": "all",
    "start_phase": "", "start_step": "", "first_player": 0, "solution_visibility": "after", "has_solution": False,
}
