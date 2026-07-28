# Architecture

**Analysis Date:** 2026-07-28

## Pattern Overview

**Overall:** Event-driven, message-based game engine with a layered backend (engine/core → game logic → card abilities) and a stateless web frontend that interprets rendering descriptors.

**Key Characteristics:**
- **Message/Effect System:** Card abilities are triggered by game messages (events). Effects propagate through a stack-based resolution system
- **Modular Card Implementation:** Each card is a standalone Python module containing `GetAbilities()` that returns a sequence of ability handlers
- **Rendering Abstraction:** Backend computes game state and serializes it as JSON descriptors; frontend renders from descriptors without game logic knowledge
- **Web-First Design:** Python backend communicates with vanilla JavaScript frontend via HTTP; stateless rendering model

## Layers

**Platform/Device Layer:**
- Purpose: Abstract hardware/network I/O (web server, keyboard input, rendering targets)
- Location: `src/engine/device/`, `src/engine/network/web_server.py`
- Contains: Device managers (web, keyboard), HTTP request handling, file I/O
- Depends on: Engine configuration, core types
- Used by: Engine initialization and game loop

**Engine Core:**
- Purpose: Initialize and orchestrate the runtime (config, logging, user profiles, background tasks, statistics)
- Location: `src/engine/engine.py`, `src/engine/config.py`, `src/engine/user/`, `src/engine/task/`, `src/engine/job/`
- Contains: Engine class lifecycle (Initialize → EngineRun → Shutdown), configuration variables, user management, async job/task scheduling
- Depends on: Device layer, game system
- Used by: `launcher.py` as entry point

**Game State & World:**
- Purpose: Represent the active game and all in-play entities (players, cards, scenario, phases)
- Location: `src/game/game.py`, `src/game/world/world.py`, `src/game/player/`
- Contains: Game instance, World (phase, game area, players, encounter deck), Player (identity, deck, resources, hand, character area), Scenario (villain, minions, schemes)
- Depends on: Message/effect system, card faces, render system
- Used by: Game loop, controller (input handling), scene loader

**Card Face System:**
- Purpose: Represent card instances with state and operations (damage, resources, engagement status)
- Location: `src/game/card/face/`
- Contains: Base classes (CardFace, Unit2 for characters/minions, Scheme2 for schemes), state tracking (health, threat, resources), card utility methods
- Depends on: World context, buff system
- Used by: All game logic, abilities

**Message & Effect System:**
- Purpose: Event-driven trigger resolution with stack-based effect resolution
- Location: `src/game/message/`, `src/game/effect/`
- Contains:
  - `message/message_type.py`: Message class hierarchy (TriggerPlayerMessage, TriggerUnitMessage, TargetsMessage, etc.)
  - `message/message.py`: Base Message2 class with send/resolve/related faces
  - `effect/`: Effect class representing a resolution context with this/targets/initiator/source tracking
- Depends on: Card faces, world state
- Used by: Ability factory, on_event handlers, rule engine

**Ability System:**
- Purpose: Define and execute card abilities (cost, trigger, effect)
- Location: `src/game/ability/`
- Contains:
  - `ability.py`: Ability class with cost, trigger condition, effect handler
  - `ability_type.py`: Enum of ability types (ForcedResponse, ChoiceAbility, etc.)
  - `cost_func.py`: Cost calculation functions (exhaust, pay resources, etc.)
  - `factory/`: AbilityFactory static methods for common ability patterns (ThisCanThwart, AfterUnitAttackEnd, etc.)
  - `condition/`: Conditional checks for ability triggers
- Depends on: Messages, effects, card faces
- Used by: Card modules (via factory), game loop

**Card Ability Modules:**
- Purpose: Implement game rules for individual cards
- Location: `src/cards/pack/<pack>/<set>/<card_id>.py` (4600+ modules, one per card)
- Contains: Single function `GetAbilities()` returning list of Ability instances
- Pattern: Use AbilityFactory methods and lambda closures for effect handlers
- Depends on: Ability factory, operate utilities (Faces, Filter, Search, Players, etc.)
- Example: `src/cards/pack/core/01050.py` (Hulk) demonstrates message dispatch, targeting, and conditional effects

**Operate Utilities Layer:**
- Purpose: High-level game operations (find cards, deal damage, discard, shuffle, etc.)
- Location: `src/game/operate/`
- Contains: Faces, FacesCounter, Filter, Search, Find, Players, CampaignLog, Utility, SetupCards, Worlds, Stores
- Pattern: Static utility classes with methods for common game actions
- Used by: Card ability implementations

**Scene & Render System:**
- Purpose: Load/save game state, serialize state to frontend-consumable descriptors
- Location: `src/game/scene/`, `src/game/render/`
- Contains:
  - `scene/scene.py`: Scene class managing game inputs, load/save files
  - `scene/loader.py`: Load scenario and deck setup
  - `render/to_descriptor.py`: Convert game state to JSON descriptors for frontend
- Depends on: World, card faces, game state
- Used by: Game loop for rendering, scene persistence

**Frontend (Vanilla JavaScript):**
- Purpose: Render game state from descriptors, handle player input, communicate with backend
- Location: `public/js/marvel/`, `public/js/module/`, `public/*.html`
- Contains: Game runtime (client.js, cards.js, effect.js), UI modules (buttons.js, card_animation.js), deck builder, card database viewer
- Pattern: Event-driven DOM manipulation, fetch-based HTTP polling/submission
- Key files:
  - `public/scene.html`: Main game board (~2000 lines monolithic)
  - `public/js/marvel/client.js`: Game state manager, input submission
  - `public/js/marvel/cards.js`: Card rendering and interaction
  - `public/js/marvel/effect.js`: Effect animation and visualization

## Data Flow

**New Game Initialization:**

1. Frontend: User selects scenario + deck → calls backend via HTTP
2. Backend (scene loader): `src/game/scene/loader.py` loads scenario JSON, creates World with players/villain
3. Backend: InitializeWorld phase in rules engine sets up cards per scenario setup instructions
4. Backend: Serializes game state to JSON descriptor via `src/game/render/to_descriptor.py`
5. Frontend: Receives descriptor, renders initial board state

**Card Play / Ability Trigger:**

1. Frontend: Player clicks card → submits input (play, attack, thwart, etc.) via HTTP
2. Backend (controller): Validates action, creates message (e.g., Message.UnitAttacked)
3. Backend (effect system): Message triggers matching abilities via card `GetAbilities()` handlers
4. Backend (ability effect): Lambda closure in card module modifies game state (deal damage, discard, etc.)
5. Backend: Effect resolves, next message queued, repeat until no more triggered abilities
6. Backend: Renders new state, sends descriptor to frontend
7. Frontend: Animates changes and waits for next input

**State Management:**

- **Game State:** Stored in World instance in memory during play; serialized to JSON on save
- **Card State:** Tracked via CardFace instances (damage counters, exhaustion, resources, location)
- **Ability Resolution:** Stack-based; each effect is resolved immediately (no traditional stack, effects propagate synchronously)
- **Session Persistence:** Scene loader can save/load game snapshots to `./crash.json` or manual saves

## Key Abstractions

**Message2 Hierarchy:**
- Purpose: Represent game events that trigger abilities
- Base class: `src/game/message/message.py`
- Subclasses: TriggerPlayerMessage, TriggerUnitMessage, TriggerSchemeMessage, TargetsMessage, TextMessage, NoSendMessage
- Pattern: Each message type carries context (trigger face, targets, to_player) for ability handlers
- Examples: Message.AfterUnitAttackEnd, Message.BeforeThwart

**Ability:**
- Purpose: Define a card's interactive or forced behavior
- Location: `src/game/ability/ability.py`
- Structure: cost, trigger_condition, ability_type, handler_func
- Trigger: Fired when a matching message is sent
- Cost: Paid during resolution (resources, exhaust, etc.)
- Handler: Lambda in card module executes effect (call ChooseAbilities, DealDamage, etc.)

**Effect:**
- Purpose: Context for a single ability resolution
- Location: `src/game/effect/`
- Attributes: this (card executing), targets, initiator (player), source (triggering message)
- Pattern: Passed through all game operations to maintain resolution context

**CardFace:**
- Purpose: Represent a single card instance with state
- Location: `src/game/card/face/card_face.py`, `src/game/card/face/base.py`
- Subclasses: Unit2 (character/minion), Scheme2 (side scheme/main scheme)
- State: health, threat, resources, exhaustion, engagement, location (hand, field, deck, discard)

**CardFinder:**
- Purpose: Query cards by traits, type, or state
- Location: `src/game/card/card_finder/`
- Pattern: Chainable filter methods (filter_trait, filter_type, etc.)
- Used by: AbilityFactory conditions, operate utilities

## Entry Points

**Backend Entry:**
- Location: `launcher.py` (root)
- Triggers: User runs `python3.10 launcher.py`
- Responsibilities: Compile .py files to bytecode, overlay defective bytecode from originals_pyc/, copy data, initialize Engine, open browser
- Key: RELEASE=1 env var forces release mode (no editor, crash handling, statistics pause)

**Frontend Entry:**
- Location: `public/main.html`
- Triggers: Browser navigates to http://127.0.0.1:2345
- Responsibilities: Menu (deck builder, scenario selection, replay, reports)
- Transitions to: `public/scene.html` on game start, `public/marvel.html` on scenario setup

**Game Loop:**
- Location: `src/engine/engine.py::Engine.EngineRun()` → `src/game/game.py::Game.GameRun()`
- Cycle: Render state → wait for input (via web device manager) → apply input → check game over → repeat
- Web device manager: Long-polls for HTTP requests; each request is one game action

## Error Handling

**Strategy:** Try-catch at engine level with crash logging; fallback to safe state without losing progress

**Patterns:**
- **Release Mode:** Exception caught at `Engine.EngineRun()`, logged via `Log.OnCrash()`, game auto-saves scene
- **Dev Mode:** Exceptions propagate; optional DebugBreak() for inspection
- **Version Mismatch:** Detected during effect resolution; logged and handled per-effect
- **Invalid Input:** Rejected by controller validation; no state change

## Cross-Cutting Concerns

**Logging:** 
- Framework: `src/engine/log/` 
- Usage: Log.Info(), Log.Error(), Log.OnCrash()
- Categories: ENGINE, GAME, CONTROLLER, VERSION, STATISTICS, WEB
- Sink: Console in dev, crash log saved on release error

**Validation:**
- Controller input: Validates action against current game state (can play, can afford, target in range)
- Ability preconditions: CardFinder filters ensure conditions met before handler executes
- Message send: Only sent if sender and receiver exist

**Authentication:**
- Web device manager: `src/engine/network/web_server.py` has IsAuthenticate() and IsVersionMatch() stubs
- Release mode: Both return True (no auth); dev mode: hookable for custom logic

---

*Architecture analysis: 2026-07-28*
