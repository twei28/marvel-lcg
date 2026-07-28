# Testing Patterns

**Analysis Date:** 2026-07-28

## Test Architecture Overview

Tests **live outside the repo** in `/home/arnau/marvel-work/tools/`. The main game codebase at `/home/arnau/marvel-work/fusion/marvel-lcg-src/` is imported and initialized for in-process testing.

**Key Principle:** Tests modify the game at runtime (patch DeviceManager, mock auth) rather than using external frameworks like pytest or unittest. All tests run in-process with full game initialization.

**Since phase 01-01, a second, independent harness exists** for the UI redesign: `ui-check/` in the planning repo (`C:\Users\arnau\Desktop\Marvel LCG last try\ui-check`, a Windows-native path — `node` is Windows `node.exe`). It is Playwright-based visual regression testing against the running server on `http://127.0.0.1:2345`. It never touches the game codebase and is deliberately kept out of `marvel-lcg-src/` so it does not end up in the delivery zip. Entry point: `cd ui-check && npm run captures`. Screens are declared in `ui-check/ecrans.ts`; baselines live in `ui-check/references/<screen>/<viewport>.png` (versioned). Other commands: `npm run fixtures` (replayable `get_world` states), `npm run bascule` (old/new UI toggle), and `npm run lancement` (new-game contract). The latter freezes the undocumented `GET /new?data=` descriptor in `ui-check/contrat-nouvelle-partie.json` (8 keys + types, never values) and is the only ui-check command that mutates server state — it destroys the game in progress.

## Test Framework & Tools

**No External Framework:**
- No pytest, unittest, or similar
- Pure Python with manual orchestration
- Tests use `sys.path`, `importlib`, and `os.chdir()` to bootstrap the game environment

**Core Test Modules (in `src/game/test/`):**
- `test.py` - Test case discovery and orchestration (lists replay files)
- `test_run.py` - Runs individual replay-based tests

**Test Data:**
- Replay files in JSON format (configurable via `replay_folders` in `launch.json`)
- Structured as: `{scenario, hero, hero_deck, villain, schemes, encounters, ...}`

## Test File Organization

**Location:**
- External tools: `/home/arnau/marvel-work/tools/test_*.py`
- Internal framework: `src/game/test/test*.py`
- Test data: replay JSON files in configured `replay_folders`

**File Naming:**
- `test_cards.py` - Build all GetAbilities(), sanity check
- `test_generate_cards.py` - Real CardFactory.GenerateCard() calls
- `test_autoplay.py` - Bot plays full games
- `test_decks.py` - Generate deck cards from JSON
- `test_newgame.py` - New game initialization
- `test_server_port.py` - Port connection test

**Baseline Results (as of 2026-07-27):**
- `test_cards`: 3766 ok / 0 fail (ability module loading)
- `test_generate_cards`: 4331 ok / 0 fail (full card generation)

## Test Execution Flow

**Common Pattern for External Tests:**

1. **Setup (mandatory):**
   ```python
   import sys, os, json
   GAME_DIR = os.path.expanduser(sys.argv[1])
   PORT = int(sys.argv[2])
   
   os.chdir(GAME_DIR)
   sys.path.insert(0, GAME_DIR)
   ```

2. **Config Modification:**
   ```python
   cfg = json.load(open('launch.json'))
   cfg['server_addresses'] = [f'127.0.0.1:{PORT}']
   json.dump(cfg, open('launch.json', 'w'), indent=2)
   ```

3. **Stdout Capture:**
   ```python
   sys.stdout = open('/tmp/cards_stdout.log', 'w', buffering=1)
   sys.stderr = sys.stdout
   ```

4. **Engine Init:**
   ```python
   from engine import Engine
   ok_init = Engine.Initialize()
   print("INIT:", ok_init, flush=True)
   ```

5. **Test Execution:**
   ```python
   # [specific test logic]
   result = {...}
   json.dump(result, open(REPORT, 'w'), indent=1)
   print(f"RESULT ...", flush=True)
   os._exit(0)
   ```

**Environment Requirements:**
- `RELEASE=1` env var must be set in calling shell (blocks release-mode error handling)
- Working directory: game directory containing `launch.json`
- Available port: configurable per test, passed via CLI argument

## Test Types

### 1. Ability Module Tests (`test_cards.py`)

**Purpose:** Load all card modules and call `GetAbilities()` to catch import/syntax errors.

**Pattern:**
```python
import pkgutil, importlib
for mi in pkgutil.walk_packages(P.__path__, P.__name__ + "."):
    try:
        m = importlib.import_module(mi.name)
    except Exception:
        failures[mi.name] = "import: " + traceback.format_exc(limit=1).splitlines()[-1]
        err += 1
        continue
    if not hasattr(m, "GetAbilities"):
        no_ga += 1
        continue
    try:
        m.GetAbilities()
        ok += 1
    except Exception:
        failures[mi.name] = "abilities: " + traceback.format_exc(limit=1).splitlines()[-1]
        err += 1
```

**Scope:**
- Card module import (catches syntax, missing dependencies)
- `GetAbilities()` execution (catches AbilityFactory construction errors)
- Does NOT fully instantiate cards (no game world)

**Report:**
- JSON output with counts: `ok`, `err`, `sans_GetAbilities`, failures dict
- Failure details: 1-line error message per module

**Baseline:** 3766 modules ok, 0 errors (as of 2026-07-27)

### 2. Card Generation Tests (`test_generate_cards.py`)

**Purpose:** Fully instantiate cards via `CardFactory.GenerateCard()` to catch construction assertions.

**Pattern:**
```python
scene = SceneLoader.NewScene('rhino', None, ['spider_man'], 42)
game = Engine.game
game.session.SetScene(scene, 'Load')

# Start game loop in background thread with timeout
threading.Thread(target=run, daemon=True).start()
time.sleep(15)

# Generate each card
w = game.world
for card_id, paper in sorted(CardsDB.papers.items()):
    if not any(card_id.startswith(p) for p in PREFIXES):
        continue
    try:
        CardFactory.GenerateCard(card_id, w.area_removed, w)
        ok += 1
    except Exception as e:
        fail.append((card_id, repr(e)[:150]))
```

**Scope:**
- Requires full game initialization (world, players, areas)
- Runs game loop in background thread (provides game context)
- Generates each card and catches construction assertions
- Can filter by card ID prefix

**Why Needed:**
- `test_cards.py` doesn't create world objects
- Cards have assertions: e.g., "only 1 resource ability per card"
- These assertions fire during actual card construction

**Baseline:** 4331 cards ok, 0 errors (as of 2026-07-27)

### 3. Autoplay Bot Tests (`test_autoplay.py`)

**Purpose:** Play full games with a strategic bot to test game logic end-to-end.

**Key Technique - DeviceManager Patching:**
```python
from engine.device.manager.base import DeviceManager

def auto_input(self, data, player_id, check):
    # Parse options JSON
    try:
        options = json.loads(data.options_json)
    except Exception:
        options = []
    
    # Score and pick best option
    ranked = sorted(range(len(options)), 
                   key=lambda i: -score_option(options[i], data.event_name))
    idx = ranked[state['retries'] % len(ranked)]
    opt = options[idx]
    return build_answer(opt, extra_retry_count)

# Patch the device manager to use our bot
DeviceManager.DoGetInput = auto_input
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None
```

**Bot Strategy (v3):**

1. **Target Selection** (`pick_targets`)
   - Attack/Defense: prioritize Villain > Leader > Minion
   - Thwart: prioritize EncounterSideScheme > MainScheme
   - Scoring per target type: hardcoded dict

2. **Resource Allocation** (`build_answer`)
   - Read payment options from UI data
   - Allocate resources greedily (up to cost)
   - Special handling for overpay cards: `OVERPAY_CARDS = {'Ionic Blast', 'Active Altruism', 'Starstruck'}`

3. **Option Selection** (`score_option`)
   - Play (events, especially aspect events): score 90-96
   - Attack: score 88 in hero form, 40 in alter-ego
   - Defense: score 75
   - Thwart: score 60
   - Change form: strategic scoring based on hand
   - Optional responses: accept (score 70)

4. **Retry Logic** (`state['retries']`)
   - Tracks if same options presented twice (stuck detection)
   - Cycles through ranked options on retry
   - Max retries: 16 before giving up (exit code 2)
   - Max asks: 900 (configurable, timeout at 7 minutes)

**Game Setup:**
```python
from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True

from engine import Engine
Engine.Initialize()

from game.scene.loader import SceneLoader
scene = SceneLoader.NewScene(SCENARIO, None, [HERO], 42)
game = Engine.game
game.session.SetScene(scene, 'Load')

# Run game in thread with timeout
def run():
    if game.GameSetup():
        game.GameLoop()

t = threading.Thread(target=run, daemon=True)
t.start()
t.join(420)  # 7-minute timeout
```

**Logging:**
- Stdout redirected to `/tmp/autoplay_{scenario}_{hero}.log`
- Bot actions logged: `[BOT] asks={count}`, `[BOT] STUCK: {prompt}`, `[BOT] FIN`
- Game over: `[BOT] GameLoop terminé (game over)`

**Exit Codes:**
- 0: Success or normal completion
- 2: Stuck (16+ retries on same prompt)
- 3: Timeout (7 minutes)

**Baseline:** Full games complete without stuck/timeout (v3 strategy)

### 4. Deck Generation Tests (`test_decks.py`)

**Purpose:** Generate all cards in starter decks and scenario decks from JSON.

**Pattern:**
```python
scene = SceneLoader.NewScene('rhino', None, ['spider_man'], 42)
game = Engine.game
game.session.SetScene(scene, 'Load')

# Run game loop in background
threading.Thread(target=run, daemon=True).start()
time.sleep(15)

w = game.world
for path in FILES:
    data = json.load(open(path))
    ids = []
    for key in ('hero', 'hero_deck', 'obligations', 'nemesis_set', 'player_deck',
                'villain', 'schemes', 'set_aside', 'encounters'):
        ids += data.get(key, [])
    
    for name in ids:
        try:
            CardFactory.GenerateCard(name, w.area_removed, w)
            ok += 1
        except Exception as e:
            total_fail.append((path, name, repr(e)[:180]))
```

**Scope:**
- Load deck JSON from configured paths (relative to game_dir)
- Common paths: `deck/starter/x.json`, `data/scenarios/y.json`
- Generate all card IDs found in deck
- Catch failures and report per-file

**Report:**
- Per-file: `{path}: {ok}/{len(ids)} cartes générées`
- Failures: `FAIL {path} {name} {error}`

### 5. Replay-Based Testing (Internal Framework)

**Location:** `src/game/test/test.py`, `src/game/test/test_run.py`

**Pattern:**
```python
class Test:
    test_cases: List[str]  # List of replay JSON filenames
    
    @staticmethod
    def GetTestCases(category: str | None = None) -> List[str]:
        # List all .json files in replay_folders from config
        # Filter by category if provided
        # Sort by version extracted from filename
        return sorted_cases
    
    @staticmethod
    def Run(game: 'Game') -> bool:
        if not game.state.start_state.is_in_testing:
            return False
        success = TestRun.Run(game, Test.test_cases, do_save=True)
        TestRun.RunEnd(game, success, exit_test)
        return True
```

**Discovery:**
- Scans `replay_folders` config (can be multiple paths)
- Finds all `.json` files not starting with `_`
- Sorts by version in brackets: `[0.5.9]` → (0, 5, 9) tuple

**Execution:**
- Integrated into game startup flow
- Runs during initialization if `is_in_testing` flag set
- Saves results back to replay JSON

**When Used:**
- Manual regression testing
- Version compatibility validation
- Can filter to specific category (in filename)

## Mocking & Patching

**What to Patch:**
- `DeviceManager.DoGetInput` - intercept user input requests
- `DeviceManager.DoWaitConnect` - skip network waiting
- `DeviceManager.DoWaitSync` - skip sync waiting
- `WebServer.IsAuthenticate` - bypass auth checks
- `WebServer.IsVersionMatch` - skip version validation

**Example:**
```python
from engine.device.manager.base import DeviceManager
from engine.network.web_server import WebServer

WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True
DeviceManager.DoGetInput = custom_input_function
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None
```

**What NOT to Mock:**
- Game world (CardFactory, Faces, Effects) — use real game logic
- Player/Hero logic — test actual gameplay
- Message dispatch — test full event chain

## Fixtures & Test Data

**Card Definition:**
- Source: `src/cards/database.py` (CardsDB)
- Access: `CardsDB.papers` dict (card_id → paper metadata)
- Card paper contains: name, desc (attributes), traits, text

**Scenario/Deck Data:**
- Source: JSON files
- Structure: `{ hero, hero_deck, nemesis_set, player_deck, villain, schemes, encounters, ... }`
- Paths: `deck/starter/*.json`, `data/scenarios/*.json`

**Test Resolution Helper (in autoplay):**
```python
def resolve(obj_id):
    w = game.world
    card = w.object_manager.card_dict.get(int(obj_id))
    if card is None:
        return ('?', '?')
    f = card.face
    return (type(f).__name__, f.paper.name)
```

## Coverage & Baselines

**Acceptance Criteria (as of 2026-07-27):**
- `test_cards`: 3766 modules, 0 failures
- `test_generate_cards`: 4331 cards, 0 failures
- `test_autoplay`: completes scenarios without stuck/timeout

**What IS Covered:**
- Module loading (card imports, type checks)
- Card construction (AbilityFactory chains, assertions)
- Full game flow (game setup, event dispatch, decisions)
- Card generation from deck JSON

**What NOT Explicitly Tested:**
- Individual ability logic (tested implicitly via autoplay)
- UI rendering (frontend JS not tested)
- Network communication (mocked in tests)
- Specific game rules edge cases (manual via replay records)

## Running Tests

**External Test Scripts (from `/home/arnau/marvel-work/tools/`):**

```bash
# Test ability loading
python3.10 test_cards.py $GAME_DIR $PORT [report.json]

# Test card generation (4331 cards)
python3.10 test_generate_cards.py $GAME_DIR $PORT [card_id_prefix ...]

# Play full game with bot
python3.10 test_autoplay.py $GAME_DIR $PORT $SCENARIO $HERO [max_asks]

# Generate deck cards
python3.10 test_decks.py $GAME_DIR $PORT <path1.json> <path2.json> ...

# Check new game init
python3.10 test_newgame.py $GAME_DIR $PORT

# Test server port availability
python3.10 test_server_port.py $GAME_DIR $PORT
```

**Environment:**
```bash
export RELEASE=1
GAME_DIR="/home/arnau/marvel-work/fusion/marvel-lcg-src"
PORT=8765
python3.10 tools/test_cards.py $GAME_DIR $PORT /tmp/report.json
```

**Parallel Testing:**
- Each test uses separate PORT to avoid conflicts
- Tests modify `launch.json` config (write-once per test)
- stdout captured to `/tmp/` (per test)

## Common Test Patterns

**Port Rotation:**
```python
# Caller assigns unique port per test invocation
GAME_DIR = sys.argv[1]
PORT = int(sys.argv[2])  # Must differ across parallel runs
cfg['server_addresses'] = [f'127.0.0.1:{PORT}']
```

**Output Logging:**
```python
sys.stdout = open('/tmp/{test}_stdout.log', 'w', buffering=1)
sys.stderr = sys.stdout
print("STATUS", flush=True)  # Always flush for streaming
```

**Game Loop in Background:**
```python
def run():
    try:
        if game.GameSetup():
            game.GameLoop()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()

t = threading.Thread(target=run, daemon=True)
t.start()
t.join(timeout)  # Wait with timeout
```

**Result Reporting:**
```python
result = {
    'init': bool(ok_init),
    'ok': ok_count,
    'err': error_count,
    'failures': {module_name: error_message}
}
json.dump(result, open(REPORT, 'w'), indent=1)
print(f"RESULT ok={ok} err={err}", flush=True)
os._exit(0)
```

---

*Testing analysis: 2026-07-28*
