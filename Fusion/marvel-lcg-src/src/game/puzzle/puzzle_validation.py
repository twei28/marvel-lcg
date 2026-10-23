"""Validation stricte d'un puzzle (format v2), sans dépendance au reste du moteur.

À appeler sur tout puzzle qui ne vient pas de nous (publication, lecture par code).
`PuzzleHelper.Exec` ne contrôle que les appels de fonction : une commande sans appel
(`import os`, une affectation d'attribut…) passe ce filtre puis est exécutée.
Ici, une commande n'est acceptée que si c'est UN SEUL appel `Puzzle.<Méthode>(...)`
dont les arguments sont des littéraux (texte, entier, booléen, None), des références
de carte `cN`, ou des listes de ces valeurs.

Spécification : docs/puzzle/FORMAT-V2.md.
"""
import ast
import re
from typing import Any, Collection, List, Optional

MAX_PLAYERS = 4
MAX_CARDS_PER_ZONE = 200
MAX_COMMANDS = 2000
MAX_COMMAND_LENGTH = 400
MAX_STRING_LENGTH = 200
MAX_INT = 10 ** 6
MAX_DEPTH = 3
MAX_TITLE = 80
MAX_DESCRIPTION = 2000
MAX_HINTS = 10
MAX_HINT_LENGTH = 500
MAX_OBJECTIVES = 6

# Les seules commandes `Puzzle.<Méthode>` qu'un puzzle de format 2 peut appeler : de la MISE EN PLACE.
# Aucune ne termine la partie (Win, Lose, End), ne valide un objectif (ValidateObjective) ni ne sort de
# la table (AssembleeAutreTable). SOURCE UNIQUE : le serveur de puzzles (site/puzzles_publies.py) la lit
# ici, et `play_puzzle` s'en sert aussi pour refuser un puzzle venu d'ailleurs. Un test
# (outils/test_puzzle_format.py) vérifie que chaque nom existe dans `RunPuzzle`.
PUBLISHED_METHODS = frozenset("""
CreateEncounterDeck CreateEncounterDiscardPile CreateHandCards CreatePlayerDeck CreatePlayerDiscardPile
CreatePlayerAdditionalDeck SetFirstPlayer RestoreCard RestoreState AdvanceVillain AdvanceMainScheme
SetHealth SetThreat Damage Heal Stun Confuse Tough Cloak Daze Expose AddStatus AddTough AddCloak Intensify
Exhaust Ready Counter Token PlaceCounters PlaceThreat PutIntoPlay PlaceUnder Attach AttachReel Engage
MoveTo Shuffle Flip ChangeForm ChangeToFace Draw Gain Discard Remove EmptyHand EmptyPlayerDeck
EmptyPlayerDiscardPile EmptyEncounterDeck EmptyEncounterDiscardPile
""".split())

OBJECTIVE_KINDS = ('defeat_villain', 'survive', 'complete_scheme', 'free_text')
OBJECTIVE_MODES = ('all', 'any')
START_PHASES = ('', 'player', 'villain', 'end_round')
SOLUTION_VISIBILITIES = ('after', 'always', 'never')

_CARD_ID = re.compile(r'^[A-Za-z0-9_,\-]{1,40}$')
_CARD_REF = re.compile(r'^c\d{1,6}$')
_METHOD = re.compile(r'^[A-Z][A-Za-z0-9]{0,40}$')


def _check_value(node: ast.AST, depth: int = 0) -> Optional[str]:
    if isinstance(node, ast.Constant):
        value = node.value
        if value is None or isinstance(value, bool):
            return None
        if isinstance(value, int):
            return None if abs(value) <= MAX_INT else "entier trop grand"
        if isinstance(value, str):
            return None if len(value) <= MAX_STRING_LENGTH else "texte trop long"
        return "type de valeur non permis"
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
        operand = node.operand
        if isinstance(operand, ast.Constant) and isinstance(operand.value, int) \
                and not isinstance(operand.value, bool):
            return None if abs(operand.value) <= MAX_INT else "entier trop grand"
        return "signe permis seulement devant un entier"
    if isinstance(node, ast.Name):
        return None if _CARD_REF.match(node.id) else f"nom '{node.id}' non permis"
    if isinstance(node, (ast.List, ast.Tuple)):
        if depth >= MAX_DEPTH:
            return "liste trop imbriquée"
        if len(node.elts) > MAX_CARDS_PER_ZONE:
            return "liste trop longue"
        for element in node.elts:
            error = _check_value(element, depth + 1)
            if error:
                return error
        return None
    return f"expression '{type(node).__name__}' non permise"


def validate_command(command: str, allowed_methods: Optional[Collection[str]] = None) -> Optional[str]:
    """None si la commande est acceptable, sinon la raison du refus.

    `allowed_methods` : les méthodes publiques de `RunPuzzle` (à fournir côté serveur
    pour refuser aussi un nom inconnu) ; sans elle, seule la forme du nom est vérifiée.
    """
    if not isinstance(command, str):
        return "la commande n'est pas du texte"
    if len(command) > MAX_COMMAND_LENGTH:
        return "commande trop longue"
    source = command.strip()
    while source.endswith(';'):
        source = source[:-1].rstrip()
    if not source:
        return "commande vide"
    try:
        tree = ast.parse(source, mode='exec')
    except (SyntaxError, ValueError, RecursionError):
        return "syntaxe invalide"
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
        return "une commande doit être un seul appel"
    call = tree.body[0].value
    if not isinstance(call, ast.Call):
        return "une commande doit être un appel"
    func = call.func
    if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name)
            and func.value.id == 'Puzzle'):
        return "seuls les appels Puzzle.<méthode>(...) sont permis"
    if not _METHOD.match(func.attr):
        return f"méthode '{func.attr}' non permise"
    if allowed_methods is not None and func.attr not in allowed_methods:
        return f"méthode '{func.attr}' inconnue"
    for argument in call.args:
        if isinstance(argument, ast.Starred):
            return "arguments étoilés non permis"
        error = _check_value(argument)
        if error:
            return error
    for keyword in call.keywords:
        if keyword.arg is None:
            return "arguments ** non permis"
        error = _check_value(keyword.value)
        if error:
            return error
    return None


def _check_cards(errors: List[str], label: str, cards: Any) -> None:
    if not isinstance(cards, list):
        errors.append(f"{label} : une liste est attendue")
        return
    if len(cards) > MAX_CARDS_PER_ZONE:
        errors.append(f"{label} : plus de {MAX_CARDS_PER_ZONE} cartes")
    for card in cards:
        if not isinstance(card, str) or not _CARD_ID.match(card):
            errors.append(f"{label} : identifiant de carte invalide ({str(card)[:30]!r})")
            return


def validate_puzzle(puzzle: Any, allowed_methods: Optional[Collection[str]] = None) -> List[str]:
    """Liste des erreurs d'un `PuzzleData` (vide si le puzzle est acceptable)."""
    errors: List[str] = []

    def text(label: str, value: Any, limit: int) -> None:
        if not isinstance(value, str):
            errors.append(f"{label} : du texte est attendu")
        elif len(value) > limit:
            errors.append(f"{label} : plus de {limit} caractères")

    if puzzle.format not in (1, 2):
        errors.append(f"format {puzzle.format!r} inconnu")
    text("titre", puzzle.title, MAX_TITLE)
    text("description", puzzle.description, MAX_DESCRIPTION)
    text("auteur", puzzle.author, MAX_TITLE)
    if not isinstance(puzzle.difficulty, int) or not 0 <= puzzle.difficulty <= 5:
        errors.append("difficulté : un entier de 0 à 5 est attendu")

    if not isinstance(puzzle.hints, list) or len(puzzle.hints) > MAX_HINTS:
        errors.append(f"indices : une liste de {MAX_HINTS} au plus est attendue")
    else:
        for hint in puzzle.hints:
            text("indice", hint, MAX_HINT_LENGTH)

    if puzzle.objectives_mode not in OBJECTIVE_MODES:
        errors.append(f"mode d'objectifs {puzzle.objectives_mode!r} inconnu")
    if not isinstance(puzzle.objectives, list) or len(puzzle.objectives) > MAX_OBJECTIVES:
        errors.append(f"objectifs : une liste de {MAX_OBJECTIVES} au plus est attendue")
    else:
        for objective in puzzle.objectives:
            if objective.kind not in OBJECTIVE_KINDS:
                errors.append(f"objectif de type {objective.kind!r} inconnu")
                continue
            text("objectif (texte)", objective.text, MAX_HINT_LENGTH)
            text("objectif (cible)", objective.target, MAX_STRING_LENGTH)
            if objective.kind == 'free_text' and not objective.text.strip():
                errors.append("objectif libre : le texte est obligatoire")
            if objective.kind == 'complete_scheme' and not objective.target.strip():
                errors.append("objectif « terminer le complot » : la cible est obligatoire")

    if puzzle.start_phase not in START_PHASES:
        errors.append(f"phase de départ {puzzle.start_phase!r} inconnue")
    if puzzle.solution_visibility not in SOLUTION_VISIBILITIES:
        errors.append(f"visibilité de la solution {puzzle.solution_visibility!r} inconnue")

    _check_cards(errors, "méchant", puzzle.villain)
    _check_cards(errors, "complots", puzzle.schemes)
    _check_cards(errors, "deck rencontre", puzzle.encounter_deck)
    _check_cards(errors, "défausse rencontre", puzzle.encounter_discard_pile)
    _check_cards(errors, "rencontre mise de côté", puzzle.set_aside)

    if not isinstance(puzzle.players, list) or not 1 <= len(puzzle.players) <= MAX_PLAYERS:
        errors.append(f"joueurs : de 1 à {MAX_PLAYERS} sont attendus")
    else:
        if not isinstance(puzzle.first_player, int) or not 0 <= puzzle.first_player < len(puzzle.players):
            errors.append("premier joueur : indice hors de la liste des joueurs")
        for index, player in enumerate(puzzle.players, start=1):
            _check_cards(errors, f"héros {index} (identités)", player.identities)
            if not player.identities:
                errors.append(f"héros {index} : aucune identité")
            _check_cards(errors, f"héros {index} (main)", player.hand_cards)
            _check_cards(errors, f"héros {index} (deck)", player.player_deck)
            _check_cards(errors, f"héros {index} (défausse)", player.player_discard_pile)
            _check_cards(errors, f"héros {index} (mis de côté)", player.set_aside)

    if not isinstance(puzzle.puzzle_command, list) or len(puzzle.puzzle_command) > MAX_COMMANDS:
        errors.append(f"commandes : une liste de {MAX_COMMANDS} au plus est attendue")
    else:
        for number, command in enumerate(puzzle.puzzle_command, start=1):
            reason = validate_command(command, allowed_methods)
            if reason:
                errors.append(f"commande {number} : {reason}")
                if len(errors) >= 30:
                    break
    return errors


def warn_puzzle(puzzle: Any) -> List[str]:
    """Avertissements NON bloquants (l'assistant les montre, il ne refuse rien)."""
    warnings: List[str] = []
    if not puzzle.encounter_deck and not puzzle.encounter_discard_pile:
        warnings.append(
            "Le deck rencontre est vide : la partie se termine dès que le méchant doit "
            "révéler une carte rencontre (règle du moteur).")
    for index, player in enumerate(puzzle.players, start=1):
        if not player.player_deck and not player.player_discard_pile:
            warnings.append(f"Héros {index} : deck et défausse vides, il ne pourra rien piocher.")
    if not puzzle.objectives:
        warnings.append("Aucun objectif : le puzzle ne pourra pas être déclaré réussi.")
    return warnings
