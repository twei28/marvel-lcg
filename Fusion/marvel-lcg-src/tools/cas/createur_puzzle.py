# Cas test_capacites : le mode « Puzzle » de la preparation (createur de puzzle, 24/10/2026). Prefixe `[crepuz]`.
# La regle `mode_createur_puzzle` ouvre le plateau en mode editeur ; `/puzzle_capture` rend `CapturePuzzle(monde)`.
CAS = [
    {"nom": "[crepuz] regle mode_createur_puzzle : posee, et la capture du plateau rend un puzzle v2 jouable (1 joueur, un vilain)",
     "pourquoi": "la route /puzzle_capture lit `world.rule.mode_createur_puzzle` puis `CapturePuzzle(world)`",
     "scenario": "rhino", "heros": "spider_man", "regles": ["mode_createur_puzzle"],
     "mise_en_place": ["Puzzle.PutIntoPlay('01103')", "Puzzle.Damage('01103', 1)", "Puzzle.CreateEncounterDeck('01110', '01101', '01103')"],
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
    # Les decks du plateau doivent se retrouver dans la capture (rapport d'essai reel du 24/10/2026 : deck rencontre capture vide).
    taille_rencontre = monde.GetScenario().encounter_deck.GetSize()
    if len(puzzle.get("encounter_deck") or []) != taille_rencontre:
        soucis.append(f"deck rencontre : {len(puzzle.get('encounter_deck') or [])} carte(s) capturee(s), {taille_rencontre} sur le plateau")
    tailles_joueur = monde.players[0].player_deck.GetSize()
    if len(puzzle["players"][0]["player_deck"]) != tailles_joueur:
        soucis.append(f"deck du heros : {len(puzzle['players'][0]['player_deck'])} carte(s) capturee(s), {tailles_joueur} sur le plateau")
    commandes = " ".join(puzzle.get("puzzle_command") or [])
    if "01103" not in commandes:
        soucis.append("le sbire pose en jeu (01103) n'est pas dans les commandes capturees")
    return (False, " ; ".join(soucis)) if soucis else (True, "regle posee, capture v2 conforme")
'''
