# Cas test_capacites : le mode « Puzzle » de la preparation (createur de puzzle, 24/10/2026). Prefixe `[crepuz]`.
# La regle `mode_createur_puzzle` ouvre le plateau en mode editeur ; `/puzzle_capture` rend `CapturePuzzle(monde)`.
CAS = [
    {"nom": "[crepuz] regle mode_createur_puzzle : posee, et la capture du plateau rend un puzzle v2 jouable (1 joueur, un vilain)",
     "pourquoi": "la route /puzzle_capture lit `world.rule.mode_createur_puzzle` puis `CapturePuzzle(world)`",
     "scenario": "rhino", "heros": "spider_man", "regles": ["mode_createur_puzzle"],
     "mise_en_place": ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 1)"],
     "declencher": [], "verifier": "createur_puzzle_capture", "attendu": {}, "main_exclusive": ["01088"]},
    {"nom": "[crepuz] SANS la regle : mode_createur_puzzle reste faux (la route refuse)",
     "pourquoi": "garde de la route : 409 hors table du createur",
     "scenario": "rhino", "heros": "spider_man",
     "mise_en_place": [], "declencher": [], "verifier": "createur_puzzle_capture", "attendu": {"sans_regle": True}, "main_exclusive": ["01088"]},
]

VERIFICATIONS = r'''
def createur_puzzle_capture(monde, aides):
    attendu = aides["cas"].get("attendu") or {}
    active = bool(monde.rule.mode_createur_puzzle)
    if attendu.get("sans_regle"):
        return (not active), ("la regle est posee alors qu'elle n'a pas ete demandee" if active else "regle absente, comme attendu")
    if not active:
        return False, "mode_createur_puzzle n'est pas pose par la liste de regles"
    from game.puzzle.puzzle_capture import CapturePuzzle
    capture = CapturePuzzle(monde)
    puzzle = capture["puzzle"]
    soucis = []
    if puzzle.get("format") != 2:
        soucis.append(f"format = {puzzle.get('format')} (attendu 2)")
    if len(puzzle.get("players") or []) != 1:
        soucis.append(f"{len(puzzle.get('players') or [])} joueur(s) captures (attendu 1)")
    if not puzzle.get("villain"):
        soucis.append("aucun vilain capture")
    commandes = " ".join(puzzle.get("puzzle_command") or [])
    if "01103" not in commandes:
        soucis.append("le sbire pose en jeu (01103) n'est pas dans les commandes capturees")
    return (False, " ; ".join(soucis)) if soucis else (True, "regle posee, capture v2 conforme")
'''
