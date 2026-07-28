# Codebase Structure

**Analysis Date:** 2026-07-28

## Directory Layout

```
marvel-lcg-src/
├── launcher.py                 # Entry point: compile bytecode, overlay defective files, init Engine
├── launcher_fast.py            # Fast launcher alternative (skip some compilation)
├── launch.json                 # Server config (port, addresses)
├── defectueux.json            # List of defective .py files (use bytecode overlay)
├── HANDOFF-V2.md              # Handoff notes from decompilation
├── QUALITE-V2.csv             # Code quality metrics
│
├── src/                        # Python backend
│   ├── main.py                # Alternative entry point
│   ├── game_entry.py          # Date check for game initialization
│   ├── build.py               # Build info (release vs dev mode)
│   │
│   ├── core/                  # Core types & utilities
│   │   ├── __init__.py
│   │   ├── lib/              # Base library (types, utility functions)
│   │   ├── meta_class/       # Metaclass definitions
│   │   └── utility/          # Shared utility functions
│   │
│   ├── engine/               # Platform/runtime engine
│   │   ├── engine.py         # Main Engine class (Initialize, EngineRun, Shutdown)
│   │   ├── config.py         # Configuration variables & command-line parsing
│   │   │
│   │   ├── device/           # Hardware/I/O abstraction
│   │   │   ├── manager/      # Device managers (web, keyboard)
│   │   │   │   ├── base.py
│   │   │   │   ├── web/      # Web device manager (HTTP polling, web server)
│   │   │   │   └── key/      # Keyboard device manager (dev/testing)
│   │   │   └── *.py          # Device-specific classes
│   │   │
│   │   ├── network/          # Web server & HTTP
│   │   │   └── web_server.py # HTTP server, auth stubs, request routing
│   │   │
│   │   ├── file/             # File I/O
│   │   │   └── *.py          # File operations (load, save, list)
│   │   │
│   │   ├── log/              # Logging
│   │   │   ├── log.py        # Log class (Info, Error, OnCrash, SaveCrashLog)
│   │   │   └── *.py          # Log formatting & sinks
│   │   │
│   │   ├── user/             # User profiles & fingerprinting
│   │   │   └── user_info.py  # UserInfo (Initialize, fingerprint)
│   │   │
│   │   ├── task/             # Async task management
│   │   │   └── *.py          # TaskManager (async/await support)
│   │   │
│   │   ├── job/              # Background job scheduling
│   │   │   └── *.py          # JobManager (AddJob, WaitForAllJobsToComplete)
│   │   │
│   │   ├── console/          # Console interface (debug)
│   │   │   └── *.py
│   │   │
│   │   ├── profile/          # Profiling & coverage tracking
│   │   │   └── *.py          # Coverage, Profile classes
│   │   │
│   │   ├── lib/              # Engine utilities
│   │   │   ├── trans_text.py # Translation text manager (TransText)
│   │   │   ├── image_creator.py # Image/asset creation (ImageCreator)
│   │   │   ├── ver.py        # Version info (Ver.ui_version_str)
│   │   │   └── check_new_version.py # Version checking
│   │   │
│   │   └── controller/       # Input controller & replay
│   │       ├── controller_manager.py # Manages input validation, replay, skip
│   │       ├── replay/       # Replay system (record, playback, skip to step)
│   │       └── *.py          # Controller implementation
│   │
│   ├── game/                 # Core game logic
│   │   ├── game.py           # Game class (GameSetup, GameLoop, GameRun)
│   │   ├── game_run/         # New game descriptor & game state
│   │   │   ├── game_new.py   # NewGameDescriptor (scenario, deck, difficulty)
│   │   │   ├── game_state.py # GameState (active game state)
│   │   │   └── game_session.py # GameSession (world, scene management)
│   │   │
│   │   ├── world/            # Game world & entities
│   │   │   ├── world.py      # World class (phase, players, scenario, encounter deck)
│   │   │   ├── world_action.py # World actions (MayChoose, ChooseAbilities, etc.)
│   │   │   ├── world_find.py # World queries (find card, find player, etc.)
│   │   │   ├── world_render.py # Render world state (PresentForceNoWait)
│   │   │   ├── world_rule.py # Rule engine (phase steps, game over logic)
│   │   │   ├── world_stat.py # Statistics tracking
│   │   │   ├── phase.py      # Phase enum & tracking
│   │   │   ├── variable.py   # Game variables (difficulty, modular sets)
│   │   │   ├── game_area/    # Player game area (hand, deck, discard, play area)
│   │   │   ├── limit_monitor/ # Ability limit enforcement
│   │   │   ├── cheat/        # Dev/test cheats
│   │   │   └── game_over.py  # GameOver state (victory, defeat, undo)
│   │   │
│   │   ├── player/           # Player entity
│   │   │   ├── player.py     # Player class (identity, deck, resources, actions)
│   │   │   ├── scenario.py   # Scenario class (villain, minions, schemes)
│   │   │   ├── user.py       # User info (player name)
│   │   │   ├── action/       # Player actions (play card, attack, thwart, etc.)
│   │   │   ├── element/      # Player sub-entities (resources, modular form)
│   │   │   ├── form/         # Identity form (hero, alter-ego)
│   │   │   ├── limit_monitor/ # Player ability limits
│   │   │   ├── model/        # Player model/attributes
│   │   │   ├── player_finder.py # Query player by condition
│   │   │   └── players.py    # Deprecated; use Players operate utility
│   │   │
│   │   ├── card/             # Card entity
│   │   │   ├── card.py       # Card class (id, name, faces, type)
│   │   │   ├── factory.py    # CardFactory (CreateCard, etc.)
│   │   │   ├── states.py     # Card states
│   │   │   ├── ui_effect_by.py # UI effect source tracking
│   │   │   ├── card_finder/  # Query cards by trait/type/state
│   │   │   └── face/         # Card face representations
│   │   │       ├── card_face.py # Base CardFace class
│   │   │       ├── base.py   # Unit2, Scheme2, Attachment2 base classes
│   │   │       ├── unit.py   # Character/ally
│   │   │       ├── minion.py # Minion unit
│   │   │       ├── scheme.py # Side scheme / main scheme
│   │   │       ├── support.py # Support card
│   │   │       └── upgrade.py # Upgrade attachment
│   │   │
│   │   ├── deck/             # Deck management
│   │   │   ├── deck.py       # Deck class
│   │   │   └── *.py          # Deck operations
│   │   │
│   │   ├── ability/          # Card abilities (triggered effects)
│   │   │   ├── ability.py    # Ability class (cost, trigger, handler)
│   │   │   ├── ability_type.py # AbilityType enum (ForcedResponse, etc.)
│   │   │   ├── ability_ignore.py # Ignore ability list
│   │   │   ├── cost_func.py  # Cost calculation (exhaust, pay resources)
│   │   │   ├── condition/    # Trigger conditions (filters)
│   │   │   └── factory/      # AbilityFactory (common ability patterns)
│   │   │       ├── __init__.py # Main factory methods
│   │   │       ├── campaign.py # Campaign-specific abilities
│   │   │       └── *.py       # Specialized factory methods
│   │   │
│   │   ├── message/          # Message/event system
│   │   │   ├── message.py    # Base Message2 class (Send, Resolve, related faces)
│   │   │   ├── message_type.py # Message subclasses & hierarchy
│   │   │   ├── on_event/     # Message trigger handlers
│   │   │   └── sender/       # Message senders (who can send what)
│   │   │
│   │   ├── effect/           # Effect resolution context
│   │   │   ├── effect.py     # Effect class (this, targets, initiator, source)
│   │   │   ├── rule/         # Rule effects (phase steps, damage, threat)
│   │   │   └── *.py          # Effect helpers
│   │   │
│   │   ├── buff/             # Buff system (stat modifications)
│   │   │   └── *.py          # Buff class & modifications
│   │   │
│   │   ├── element/          # Game elements
│   │   │   ├── resources.py  # Resources (mental, physical, energy, wild)
│   │   │   ├── cost.py       # Resource cost
│   │   │   ├── damage_property.py # Damage type (combat, etc.)
│   │   │   └── *.py          # Other elements
│   │   │
│   │   ├── selector/         # Target selection
│   │   │   └── *.py          # Select class (queries for targets)
│   │   │
│   │   ├── operate/          # High-level game operations
│   │   │   ├── faces.py      # Faces (move, discard, reveal, etc.)
│   │   │   ├── faces_counter.py # FacesCounter (calculate printed values)
│   │   │   ├── filter.py     # Filter (query with conditions)
│   │   │   ├── search.py     # Search (find card by ID/name)
│   │   │   ├── find.py       # Find (complex card queries)
│   │   │   ├── players.py    # Players (query by name/role)
│   │   │   ├── campaign_logs.py # Campaign log state tracking
│   │   │   ├── utility.py    # Utility operations
│   │   │   ├── rand.py       # Random operations
│   │   │   ├── setup_cards.py # Setup card placement
│   │   │   ├── worlds.py     # World queries
│   │   │   ├── modular_set.py # Modular set handling
│   │   │   ├── store.py      # Campaign store operations
│   │   │   ├── effects.py    # Effect utilities
│   │   │   └── run_at.py     # RunAt (execute at phase)
│   │   │
│   │   ├── scene/            # Scene management (load/save game)
│   │   │   ├── scene.py      # Scene class (load, save, inputs)
│   │   │   ├── loader.py     # SceneLoader (setup scenario from JSON)
│   │   │   └── replay/       # Replay system
│   │   │
│   │   ├── render/           # Render to frontend
│   │   │   ├── to_descriptor.py # Convert game state to JSON descriptors
│   │   │   └── symbol.py     # Symbol definitions
│   │   │
│   │   ├── rule/             # Game rules (phase flow, damage, etc.)
│   │   │   └── *.py          # Rule implementations
│   │   │
│   │   ├── test/             # Game testing utilities
│   │   │   └── *.py          # Test setup & helpers
│   │   │
│   │   ├── object/           # Generic object tracking
│   │   │   └── *.py
│   │   │
│   │   ├── event/            # Event system
│   │   │   └── *.py
│   │   │
│   │   ├── puzzle/           # Puzzle mode
│   │   │   └── *.py          # Puzzle scenario handling
│   │   │
│   │   ├── statistics/       # Game statistics & achievements
│   │   │   └── *.py          # Statistics tracking & display
│   │   │
│   │   └── game_run/         # Additional game state info
│   │       └── *.py
│   │
│   ├── cards/                # Card implementations (4600+ modules)
│   │   ├── database.py       # CardsDB (load cards.json, card lookup)
│   │   ├── __init__.py
│   │   │
│   │   └── pack/             # Card packs (sets of cards)
│   │       ├── __init__.py   # Import all packs, common card utilities
│   │       │
│   │       └── <pack>/       # Pack abbreviation (core, aoa, nova, etc.)
│   │           ├── __init__.py # Import all sets in pack
│   │           │
│   │           └── <set>/    # Set name (e.g., core, ant_man, angel, etc.)
│   │               ├── __init__.py # (usually empty)
│   │               └── <card_id>.py # Individual card module
│   │                   # Example: 01050.py (Hulk)
│   │                   # Contains single GetAbilities() function
│   │
│   └── editor/              # Card editor (dev mode)
│       ├── editor.py        # Main editor class
│       └── *.py             # Editor utilities
│
├── public/                  # Web frontend
│   ├── main.html            # Menu screen (deck builder, scenario selection)
│   ├── scene.html           # Main game board (~2000 lines, monolithic)
│   ├── marvel.html          # Scenario setup screen
│   ├── cards.html           # Card database viewer
│   ├── deck.html            # Deck builder
│   ├── puzzle_editor.html   # Puzzle scenario editor
│   ├── replay.html          # Game replay viewer
│   ├── authenticate.html    # Auth page (stub)
│   ├── report.html          # Game report viewer
│   │
│   ├── css/                 # Stylesheets
│   │   ├── marvel/          # Game board styles
│   │   ├── menu/            # Menu styles
│   │   └── prepare/         # Deck/scenario prep styles
│   │
│   ├── js/                  # JavaScript modules
│   │   ├── lib/             # Third-party libraries
│   │   │
│   │   ├── module/          # Reusable utility modules
│   │   │   ├── card_info.js # Card info display
│   │   │   ├── card_preview.js # Card preview
│   │   │   ├── card_statistics.js # Card stats
│   │   │   └── set_info.js  # Set info
│   │   │
│   │   ├── prepare/         # Deck builder & scenario setup JS
│   │   │   └── *.js         # Prepare-specific logic
│   │   │
│   │   └── marvel/          # Main game runtime
│   │       ├── marvel.js    # Entry point
│   │       ├── client.js    # Client state & input submission
│   │       ├── game.js      # Game state manager
│   │       ├── cards.js     # Card rendering & interaction
│   │       ├── effect.js    # Effect animation & visualization
│   │       ├── buttons.js   # UI button handling
│   │       ├── card_animation.js # Card animation effects
│   │       ├── auto_activate.js # Auto-activate ability checking
│   │       ├── auto_targeting.js # Auto-target suggestions
│   │       ├── move-card.js # Card dragging & movement
│   │       ├── hover.js     # Hover tooltips & info
│   │       ├── command.js   # Game commands (play, attack, etc.)
│   │       ├── message.js   # Message display
│   │       ├── history.js   # Game history tracking
│   │       ├── replay.js    # Replay controls
│   │       ├── notify.js    # Notifications
│   │       ├── music.js     # Music/sound controls
│   │       ├── data.js      # Data fetching
│   │       ├── descriptor.js # Descriptor parsing
│   │       ├── canvas.js    # Canvas rendering
│   │       ├── draggable.js # Drag & drop
│   │       ├── error_dialog.js # Error display
│   │       ├── class_name.js # CSS class management
│   │       └── btn_ok.js    # OK button logic
│   │
│   ├── fonts/               # Web fonts
│   │
│   ├── effects/             # Animation effects (CSS/JS)
│   │
│   └── (favicon.ico)        # Favicon
│
├── data/                    # Game data (JSON)
│   ├── cards.json           # Card database (name, type, cost, traits, etc.)
│   ├── sets_info.json       # Set metadata (name, count, order)
│   ├── cards_custom.json    # Custom/fan-made cards
│   ├── translate_cn.json    # Chinese translations
│   │
│   ├── scenarios/           # Official scenario definitions
│   │   ├── apocalypse.json  # Scenario setup, threat, cards, etc.
│   │   ├── *.json           # Other scenarios
│   │   └── ...
│   │
│   ├── scenarios_custom/    # Custom scenarios
│   │   └── *.json
│   │
│   ├── encounter_sets/      # Encounter set definitions
│   │   ├── basic.json       # Basic encounter cards
│   │   └── *.json           # Other encounter sets
│   │
│   ├── challenges/          # Challenge scenarios
│   │   └── *.json
│   │
│   ├── nemesis/             # Nemesis card definitions
│   │   └── *.json
│   │
│   └── (backups)            # Backup copies (.bak files)
│
├── deck/                    # Deck templates
│   └── starter/             # Starter deck templates
│       ├── captain_america.json # Pre-built decks
│       ├── ms_marvel.json
│       └── *.json
│
├── puzzle/                  # Puzzle scenarios (fixed game positions)
│   ├── puzzle-01050.json    # Puzzle setup (position, state, win conditions)
│   ├── *.json
│   ├── test/                # Puzzle tests
│   └── ...
│
├── tools/                   # Development utilities
│   ├── test_cards.py        # Test card implementations (3766 cards checked)
│   ├── test_newgame.py      # Test new game setup
│   ├── test_server_port.py  # Test server connectivity
│   ├── innocence_test.py    # Test card effects
│   ├── master_loop.py       # Master validation loop
│   ├── card_fix_loop.py     # Card bug fix loop
│   ├── tools_fix_pycdc.py   # Fix pycdc decompilation issues
│   └── quote_forward_refs.py # Fix forward references
│
├── assets/                  # Game assets
│   ├── textures/            # Texture files
│   ├── pics/                # Card images/artwork
│   └── sounds/              # Audio files
│
├── originals_pyc/           # Original decompiled bytecode (for defective files)
│   ├── game/
│   ├── cards/
│   └── engine/
│
└── .game/                   # Compiled game directory (generated at runtime)
    ├── src/                 # Compiled .pyc bytecode
    ├── data/                # Copy of data/
    ├── public/              # Copy of public/
    └── launch.json          # Server config
```

## Directory Purposes

**`src/`:**
- Purpose: All Python backend code (game engine, logic, card implementations)
- Contains: Engine, game state, card abilities, utilities
- Key files: `engine.py`, `game.py`, `world.py`, card modules

**`src/engine/`:**
- Purpose: Platform abstraction and runtime (device I/O, web server, logging, config)
- Contains: Web server, device managers, user profiles, file I/O
- Key files: `engine.py`, `config.py`, `network/web_server.py`

**`src/game/`:**
- Purpose: Core game logic (world, players, cards, abilities, effects)
- Contains: Game state, message/effect system, card abilities
- Key files: `game.py`, `world/world.py`, `ability/ability.py`

**`src/cards/pack/`:**
- Purpose: Individual card implementations (4600+ modules)
- Structure: `pack/<pack>/<set>/<card_id>.py` where each file exports `GetAbilities()`
- Key: One Python module per card; cards.json drives lookup

**`public/`:**
- Purpose: Web frontend (HTML, CSS, JavaScript)
- Contains: Game UI, deck builder, card viewer, game runtime
- Key: `scene.html` is main game board (2000 lines, monolithic)

**`public/js/marvel/`:**
- Purpose: Main game runtime JavaScript
- Contains: State management, rendering, input handling, animation
- Key files: `client.js`, `cards.js`, `effect.js`

**`data/`:**
- Purpose: Game data (JSON: cards, scenarios, encounter sets)
- Contains: `cards.json` (card database), `sets_info.json`, scenario definitions
- Key: Data is loaded by backend on startup

**`deck/starter/`:**
- Purpose: Pre-built starter decks
- Contains: JSON files with deck lists (cards by ID)

**`puzzle/`:**
- Purpose: Puzzle scenarios (fixed game positions for testing)
- Contains: Puzzle JSON definitions + test cases

**`tools/`:**
- Purpose: Development/testing utilities
- Contains: Card validation tests, server tests, decompilation fixes

**`originals_pyc/`:**
- Purpose: Original bytecode for defective files
- Contains: Decompiled .pyc files for ~28 modules that have reconstruction issues

## Key File Locations

**Entry Points:**
- `launcher.py`: Main entry point (compile, init Engine, serve)
- `launcher_fast.py`: Faster launcher (skip some compilation)
- `src/main.py`: Alternative entry point
- `public/main.html`: Frontend menu
- `public/scene.html`: Main game board

**Configuration:**
- `launch.json`: Server config (port, addresses)
- `defectueux.json`: List of defective .py files
- `src/engine/config.py`: Engine config variables

**Core Logic:**
- `src/engine/engine.py`: Engine lifecycle
- `src/game/game.py`: Game class
- `src/game/world/world.py`: World state
- `src/game/ability/ability.py`: Ability class
- `src/game/message/message.py`: Message base class

**Card System:**
- `src/cards/database.py`: Card database loader
- `src/cards/pack/<pack>/<set>/<card_id>.py`: Individual cards (4600+ files)
- `data/cards.json`: Card metadata

**Frontend:**
- `public/scene.html`: Main game UI
- `public/js/marvel/client.js`: Client state manager
- `public/js/marvel/cards.js`: Card rendering
- `public/js/marvel/effect.js`: Effect animation

**Testing:**
- `tools/test_cards.py`: Test all card implementations
- `tools/test_newgame.py`: Test new game setup
- `puzzle/`: Puzzle test scenarios

## Naming Conventions

**Files:**
- Python: `snake_case.py` (e.g., `web_server.py`, `card_face.py`)
- JavaScript: `snake_case.js` or `kebab-case.js` (e.g., `card_animation.js`, `move-card.js`)
- Data: lowercase with underscores (e.g., `cards.json`, `sets_info.json`)
- Card modules: numeric ID `<card_id>.py` (e.g., `01050.py` for card #1050)

**Directories:**
- Package modules: `snake_case/` (e.g., `web_server/`, `card_face/`)
- Card packs: abbreviated pack name (e.g., `core`, `aoa`, `nova`)
- Card sets: set name (e.g., `ant_man`, `angel`, `age_of_apocalypse`)

**Python Classes:**
- Public: PascalCase (e.g., `World`, `CardFace`, `Ability`)
- Private: `_leading_underscore_snake_case`
- Constants: ALL_CAPS_SNAKE_CASE (e.g., `MAX_HEALTH = 10`)

**Card Mapping Convention:**
- Python import: `cards.pack.<pack>.<set>.<card_id>::GetAbilities()`
- Example: `cards.pack.core.core.01050` → card ID 1050 (Hulk)
- Lookup: `cards.json` maps card ID to pack/set, then import dynamically

## Where to Add New Code

**New Card Implementation:**
1. Create card module: `src/cards/pack/<pack>/<set>/<card_id>.py`
2. Implement: `def GetAbilities() -> Sequence[Ability]:`
3. Use `AbilityFactory` methods for common patterns
4. Use operate utilities (Faces, Filter, Players, etc.) for game operations
5. Update `cards.json` with card metadata (name, type, cost, traits)
6. Test: `python tools/test_cards.py` validates GetAbilities() returns valid list

**New Game Feature (Backend):**
1. If state tracking: Add to `src/game/world/` or `src/game/player/`
2. If ability/trigger: Add to `src/game/ability/` or `src/game/message/`
3. If game operation: Add to `src/game/operate/`
4. If engine feature: Add to `src/engine/`
5. Test: Use `tools/test_newgame.py` or `tools/innocence_test.py`

**New Frontend Feature:**
1. If game logic: Add JS to `public/js/marvel/` (e.g., `public/js/marvel/new_feature.js`)
2. If menu/preparation: Add to `public/js/prepare/`
3. If reusable: Add to `public/js/module/`
4. Update HTML: Link in relevant `.html` file (scene.html, main.html, etc.)
5. Use fetch API to communicate with backend (HTTP GET/POST)

**New Scenario/Encounter Set:**
1. Create scenario JSON: `data/scenarios/<scenario_name>.json`
2. Define: encounter setup, threat level, victory/defeat conditions
3. Reference encounter sets: `data/encounter_sets/`
4. Test: Load in frontend scenario selector

**Development/Testing Utility:**
1. Create script: `tools/<utility_name>.py`
2. Entry point: Can be run standalone (`python tools/<utility_name>.py`)
3. Scope: Use for validation, decompilation fixes, card testing

## Special Directories

**`.game/`:**
- Purpose: Compiled bytecode directory (generated at launch)
- Generated: At runtime by `launcher.py`
- Committed: No (in `.gitignore`)
- Cleanup: `launcher.py` deletes and recreates on each run

**`originals_pyc/`:**
- Purpose: Original decompiled bytecode from reverse engineering
- Generated: No (committed as reference)
- Committed: Yes (archive of source of truth)
- Usage: `launcher.py` overlays these on top of compiled .py files for defective modules

**`__pycache__/`:**
- Purpose: Python bytecode cache
- Generated: By Python runtime
- Committed: No (in `.gitignore`)

**`assets/`:**
- Purpose: Game artwork, sounds, textures
- Contents: Card art, UI graphics, background music
- Management: External to source control (may be linked/compressed)

---

*Structure analysis: 2026-07-28*
