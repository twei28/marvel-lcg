# Coding Conventions

**Analysis Date:** 2026-07-28

## Overview

This codebase was reconstructed from Python 3.10 bytecode ("Recovered automatically from Python 3.10 bytecode" headers throughout). Bytecode-fidelity is critical. Intentional divergences from the original bytecode are marked with `CORRECTIF` comments explaining the change and rationale.

## Naming Patterns

**Classes:**
- PascalCase for all classes
- Examples: `Hero`, `Minion`, `Treachery`, `Event`, `Ally`, `Object`, `Message2`
- Message classes: named by trigger event (`WhenCardRevealed`, `AfterPlayerPlayedCard`, `AfterUnitAttackEnd`)
- Face types (card representations): `CardFace`, `Villain`, `Leader`, `EncounterSideScheme`

**Functions:**
- PascalCase for public functions and methods (bytecode-faithful)
- Examples: `GetAbilities()`, `CastTo()`, `DrawUp()`, `HealthUnits()`, `GetInitiator()`, `PlaceThreatOnSchemes()`
- Internal helpers: lowercase with underscores
- Card ability functions: lowercase snake_case for the handler function defined inside `GetAbilities()` 
  - Examples: `def angel(effect, message)`, `def psylocke(effect, message)`

**Variables:**
- snake_case for local variables: `this`, `player`, `identity`, `effect`, `message`
- snake_case for attributes: `object_id`, `object_category`, `once_per_event_effects`
- Unused parameters: explicitly marked with `Unused(variable)` call from core module
- Type-casting pattern: `this = effect.this.CastTo(CardType)`

**Constants:**
- UPPERCASE for configuration constants: `CATEGORY_NAME = 'ENGINE'`, `MAJOR = 0`, `MINOR = 5`
- File paths: use `ConfigVariables.Str()`, `ConfigVariables.Bool()`, `ConfigVariables.Folder()`

**Card IDs:**
- Numeric strings with leading zeros: `'42001a'`, `'45164'` (from card module filenames)
- Trait keywords: UPPERCASE: `'AERIAL'`, `'ELITE'`, `'ATTACK'`, `'MISSION'`

## Type Annotations

**Pattern:**
- All function signatures include type hints
- Type strings in quotes for forward references: `'Effect'`, `'Message.AfterPlayerPlayedCard'`, `'Ability'`
- Return type annotation: `-> ReturnType` (may be quoted)
- Sequence types: `Sequence['Ability']`, `Sequence[CardFace]`, `List[str]`
- Literal unions: `Literal[('option1', 'option2')]`
- Optional types: `Type | None` (Python 3.10 union syntax)

**Example from `src/cards/pack/angel/angel/42001a.py`:**
```python
def GetAbilities() -> Sequence['Ability']:
    def angel(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)
```

## Message/Ability Idioms

**Card Ability Structure (card modules):**

1. Import: `from . import *` pulls all dependencies from parent `__init__.py`
2. Export function: `GetAbilities() -> Sequence['Ability']`
3. Handler functions inside `GetAbilities()`:
   - Signature: `def handler_name(effect: 'Effect', message: 'Message.Type') -> None`
   - First action: cast to card type: `this = effect.this.CastTo(CardType)`
   - Mark unused: `Unused(this)` if not used
   - Extract context: `player = message.GetToPlayer()`, `initiator = effect.GetInitiator()`
4. Return: list of `AbilityFactory.MethodName(...)` calls chained with `.SetName()`, `.SetTarget(...)`, `.LimitOncePerPhase()`

**Example from `src/cards/pack/aoa/age_of_apocalypse/45164.py`:**
```python
def GetAbilities() -> Sequence['Ability']:
    def agent_of_apocalypse_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # CORRECTIF : original called Worlds.ScenarioArea('MissionArea'), a stub
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        choices = [AbilityFactory.ForChoiceAbility(...).SetTarget([this])]
        player.ChooseAbilities(effect, *choices)
    return [AbilityFactory.WhenThisRevealed(None, agent_of_apocalypse_revealed)]
```

**Message Objects:**
- All inherit from `Message2` (base message class)
- Naming: event-driven, e.g., `WhenCardRevealed`, `AfterPlayerPlayedCard`, `WhenCardBecomeBoost`
- Methods to retrieve context: `GetToPlayer()`, `GetInitiator()`, `GetReplayText()`
- Trigger registration: `TriggerOnEvent(on_event_type)`

**Effect Objects:**
- Passed to all ability handlers
- Provides access to: `this` (card executing), `targets` (selected targets)
- Chain game actions: `effect.GetInitiator()`, pass `effect` to all mutations

## Import Organization

**Card Module Imports:**
```python
from . import *  # Star import from parent __init__.py (contains all card framework)
```

**Parent __init__.py Pattern (e.g., `src/cards/pack/__init__.py`):**
1. Core framework: `from core import *`, `from game.ability import *`, `from game.message import *`
2. Factories: `from game.ability.factory import *`
3. Game systems: `from game.player import *`, `from game.world.game_area import GameArea`
4. Utilities: `from game.operate.faces import Faces`, `from game.selector import Select`
5. Mark unused imports: `Unused(ImportName)` to suppress warnings

**Path Structure:**
- No path aliases configured (all imports use relative or absolute paths)
- Relative imports within packages: `from . import *`, `from cards.pack import *`
- Absolute imports from src root: `from engine import Engine`, `from game.scene.loader import SceneLoader`

## Error Handling

**Exception Hierarchy:**
- Base: `GameSignal(Exception)` for non-fatal signals
- Specialized: `GameSignal_UndoRequest()`, `GameSignal_InvalidMove()`
- Defined in: `src/game/exceptions/exceptions.py`

**Try-Catch Pattern (in engine):**
```python
if Build.release:
    try:
        return initialize()
    except Exception as exc:
        Log.OnCrash(CATEGORY_NAME, exc, '', None)
        return False
```

**Message Broadcasting Error Handling (from `src/game/message/message.py`):**
```python
try:
    self.world.event_manager.BroadcastMessage(self)
except Exception as exc:
    info = Log.OnCrash(CATEGORY_NAME, exc, self.name, None)
    self.world.render.ErrorOccurred(info)
```

**No Raise Pattern:**
- Most failures are silent (return False, empty list, or continue)
- Logs all crashes via `Log.OnCrash()` with category, exception, name, and context

## Logging

**Framework:** Custom `Log` class from `engine.log`

**Categories (CATEGORY_NAME constant):**
- `'ENGINE'` - initialization, device manager
- `'MESSAGE'` - message dispatch
- `'CARD'` - card factory, abilities
- Standard pattern: `Log.Info(CATEGORY_NAME, message_text)`

**Debug Output:**
- `Log.DebugSilent(category, object)` for verbose tracing
- `Log.Print(message)` for user-facing output
- `Log.OnCrash(category, exc, name, context)` on errors

**Example:**
```python
Log.Info(CATEGORY_NAME, game_name)
Log.DebugSilent('MESSAGE', self)  # Message2.__init__
```

## Comments

**CORRECTIF Pattern:**
- Format: `# CORRECTIF : explanation of change`
- Used when intentional divergence from original bytecode
- Must explain: what the original did, why it was wrong, what the fix does
- Example from 45164.py: `# CORRECTIF : l'original appelait Worlds.ScenarioArea('MissionArea'), un stub raise NotImplemented du moteur — le choix « mission area » crashait.`

**When to Comment:**
- Bytecode quirks or workarounds (use CORRECTIF)
- Non-obvious game logic (rare, most logic is in abilities)
- Complex conditionals or multi-step operations

**No Comment Style:**
- Docstrings not used (bytecode reconstruction doesn't preserve them)
- Inline comments kept minimal
- Self-documenting: function names and type hints carry most information

## Function Design

**Size:**
- Most ability handlers: 2-8 lines (handler + effect setup)
- Utility functions: keep under 20 lines
- Complex operations: break into named helper functions

**Parameters:**
- All explicitly typed
- Card handlers always take `(effect: 'Effect', message: 'Message.Type')`
- Utility functions may take multiple targets, conditions, or configuration objects

**Return Values:**
- Card ability handlers: always `-> None` (return values via mutations on effect)
- Factories: return types specified (`-> Ability`, `-> Sequence[Ability]`)
- Queries: return objects or sequences

**Mutations Over Returns:**
- Game state changes through method calls: `this.DrawUp(1, effect)`, `player.TakeDamage(this, 1, effect)`
- Effect carries the transaction context
- No explicit return of modified objects

## Module Design

**Barrel Files (__init__.py):**
- Star imports to expose all dependencies to children: `from core import *`
- Utility functions defined inline: `ShuffleThisCardIntoEncounter()`, `DiscardThisCard()`
- Constants and CardFinder helpers: `NonEliteMinion = CardFinder(...)`
- All imports marked `Unused()` to suppress warnings

**Card Module Structure:**
```
src/cards/pack/
├── [pack_name]/
│   ├── __init__.py       # from cards.pack import *
│   └── [card_id].py      # from . import *; def GetAbilities()
```

**Export Pattern:**
- Card modules export only `GetAbilities()` function
- No classes or other symbols exposed
- Framework imported via `from . import *` chain

## Frontend Conventions

**JavaScript (inline in HTML + modules):**
- camelCase for variables and methods: `card_id`, `buildAnswer()`, `pick_targets()`
- Constructor pattern: `class Card { constructor(card_id, type, ...) { this.card_id = card_id; } }`
- Object property access: `opt.get('name')`, `desc.get('Cost')`
- No strict typing (vanilla JavaScript)

**HTML Structure:**
- CSS custom properties: `--card--width`, `--card--height`, `--line-height`
- State tracking: `data` object with counters: `{ count, prev, retries, form }`

## Build Configuration

**Environment Variable:**
- `RELEASE=1` required to enable release build mode
- Checked via: `if 'RELEASE' in os.environ:` in `src/build.py`
- Controls crash handling (verbose logging disabled in release)

**Version Tracking:**
```python
class Build:
    release = ('RELEASE' in os.environ)
    MAJOR = 0
    MINOR = 5
    PATCH = 9
    BUILD = 200
```

## Configuration System

**Pattern:** `ConfigVariables.Type(key, default)`

**Types:**
- `ConfigVariables.Bool(key, default)`
- `ConfigVariables.Str(key, default)`
- `ConfigVariables.Folder(key)` - path configuration
- `ConfigVariables.Folders(key)` - multiple paths (for replay testing)

**Usage:**
```python
CHECK_FOR_NEW_VERSION_ON_STARTUP = ConfigVariables.Bool('check_for_new_version_on_startup', False)
DEVICE = ConfigVariables.Str('device', 'web')

if CHECK_FOR_NEW_VERSION_ON_STARTUP.value:
    # Use value
```

**Initialization:**
- `ConfigVariables.Initialize()` early in Engine.Initialize()
- Can override via command-line arguments
- Stored in `launch.json`

---

*Convention analysis: 2026-07-28*
