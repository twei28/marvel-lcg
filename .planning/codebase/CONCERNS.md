# Codebase Concerns

**Analysis Date:** 2026-07-28

## Bytecode-Reconstructed Codebase (Critical Constraint)

**Issue:** Entire Python codebase (~5500 files, 52k+ lines) recovered from bytecode disassembly (pycdc). Comments, original formatting, and variable names lost. Source of truth is the compiled bytecode, not the reconstructed code.

**Files:** `src/core/utility/types.py` (marker comment), all `src/` tree

**Impact:** 
- Refactoring is high-risk; changes may diverge from bytecode-original behavior
- No confidence in "dead code" removal without exhaustive testing
- Original logic intent obscured; reverse-engineering each function requires careful analysis

**Mitigation:** "Bytecode-fidelity policy" enforced. All voluntary divergences marked `# CORRECTIF` (currently ~8 instances). Test coverage (`test_cards`, `test_autoplay`) provides safety net.

**Recommendation:** Keep reconstruction as-is; only modify when bugs are proven. Document all divergences. Use in-process bot testing (`test_autoplay.py`) before release.

---

## Data Integrity: Checksummed JSON Files

**Issue:** Critical data files require SHA256 checksums computed from content + hardcoded CODE_KEY. Any manual edit invalidates checksum; game fails to load if mismatch detected.

**Files:** `data/cards.json` (2.3 MB), `data/sets_info.json` (19 KB), `data/puzzle/*.json` (8 files)

**Current Setup:**
- CODE_KEY defined in `src/core/utility/types.py:6` as obfuscated string
- Checksum formula: `sha256(json.dumps(obj, sort_keys=True) + ' ' + CODE_KEY)` 
- Checksum stored in each JSON root as `"checksum"` field

**Risks:**
1. Manual editing of JSONs without recomputing checksum → game won't start
2. CODE_KEY can be extracted from bytecode; not a security measure
3. Procedural error in checksum recomputation → silent data loss (game loads old version from fallback)
4. Backup strategy unclear: `data/cards.json.bak-daredevil` exists, but rollback procedure not documented

**Observations:**
- 5 card packs added (Daredevil 60001-60064, Echo 60037-60064) required manual checksum recomputation
- 75 campaign/PVP cards added with successful recomputation
- Process documented in TODO.md §1, step 3 but no automation

**Recommendation:** 
- Automate checksum computation in a tool (not yet done)
- Document rollback procedure clearly
- Version control original checksums; detect unexpected changes

---

## Monolithic UI: scene.html (2251 lines)

**Issue:** Game setup screen is single HTML+CSS+JS file. Tightly coupled, difficult to test, hard to refactor.

**File:** `public/scene.html`

**Current State:**
- 2251 lines of HTML with inline styles and scripts
- Recently refactored into 4-step wizard with splash screens
- Backup: `public/scene.html.bak-avant-ui` (~2100 lines) shows previous iteration
- CSS overlay: `public/css/menu/wizard.css` (surcouche premium)

**Known Issues:**
- Wizard CSS uses `display:none` hacks on inputs and divs
- Set picker flex layout relies on `width: 0px` hack comment
- Campaign log forms added recently (for MTS/MG/NeXt/AoA) but integration into form submission may be incomplete
- No component library; hard to reuse UI patterns

**Planned Refactoring:** PREPARE-UI-PLAN.md outlines 6-step wizard UI migration (Phase 0 analysis only, no implementation started). Plan includes:
- Extract data loading (TypeScript `api.ts`, `catalog.ts`, `state.ts`)
- Componentize (Web Components or similar)
- Multiple steps with persistent summary panel
- Validation layer

**Risk:** 
- Refactoring without proper testing could break game launch flow
- Campaign log form integration may have incomplete validation
- New UI plan (PREPARE-UI-PLAN.md §6) shows 6 phases; no timeline set

**Recommendation:** 
1. Add E2E tests for game launch flow (currently none exist in repo; tests in `/home/arnau/marvel-work/tools/` outside repo)
2. Refactor in phases as outlined, keeping old `scene.html` functional during transition
3. Extract form validation logic before UI refactor

---

## Stubbed/Incomplete Engine Features

### Worlds.ScenarioArea() Not Implemented

**Issue:** `Worlds.ScenarioArea()` in `src/game/operate/worlds.py:480` raises `NotImplemented`. The engine never implemented the "mission area" concept, breaking AoA mission attempt feature.

**Files:** `src/game/operate/worlds.py` (line 480), `src/cards/pack/aoa/age_of_apocalypse/45164.py` (workaround)

**Impact:** Age of Apocalypse campaign missions cannot use the intended mission area. Workaround implemented (45164 line 9): missions use `mission` counter on existing cards instead of a separate area.

**Workaround:** `GetMissionScheme()`, `AllyToMission()`, `MinionToMission()` in `src/cards/pack/aoa/missions.py` simulates mission area using card counters.

**Observations:**
- TODO.md documents this as a "limitation" (assumed intentionally not implemented)
- Chirurgical test (28/07/2026) validates workaround for all mission paths
- Alternative: implement true mission area (large refactor, risky with bytecode constraint)

**Recommendation:** Keep workaround. Document as architectural decision. Monitor for edge cases in real gameplay.

---

## "Text Only" (Texte Seul) Incomplete Implementations

**Issue:** ~20+ card abilities documented in TODO.md as "texte seul" (text only) — rules printed but NOT wired into engine. Game rule applied via UI message only, or intentionally lenient implementation.

**Examples from TODO.md:**

| Card | Feature | Status |
|------|---------|--------|
| 58006 Energy Siphon | Bonus when spending overpay | V2 ✅ FAIT 28/07 |
| 58022 Swordsman | Response defender (no exhaust) | V2 ✅ FAIT 28/07 |
| 58031 Cameo | Search collection setup | V2 ✅ FAIT 28/07 |
| 58009 Mr. Hollywood | "Once per card" pay-effect limit | LENIENT: only offered once per payment anyway |
| 58032 Coordinated Effort | Shared resource payment (2+ players) | CORRECTIF ✅ FAIT 28/07; solo = no-op |
| 58008 Jet Belt | 2nd mode (exhaust tuckée) | V2 SIMPLIFIED: texte seul |
| 59036 Ares | Scheme-star boost | ALREADY WIRED (not texte seul) |
| 32177 Brawler, 59014 Golden Mace | Compared 'Attack' instead of 'ATK' | BUG FIXED 28/07 |
| 55029a Rascal | Boost-response (treachery choice) | LENIENT: ~ When Revealed only |
| All Synthezoid leader moves | "Your leader" targeting | No-op solo (GetYourTeamLeader returns None) |

**Risk:**
- Texte seul features may have edge cases in multiplayer or complex interactions
- Players expect printed rules to work; lenient implementations may cause confusion in live play
- New pack testing may uncover texte seul dependencies

**Observations:**
- TODO.md explicitly lists "v2" = full implementation; several completed by 28/07/2026
- Cross-checks in chirurgical tests validate each fix
- Baseline: test_cards = 3766 ok / 0 fail as of 28/07/2026

**Recommendation:** 
1. Prioritize remaining texte seul by impact (e.g., Jet Belt affects play flow)
2. Add explicit test case per texte seul feature (not currently in test_cards baseline)
3. Document in-game as feature limitation if not fixing

---

## Fragile Card Module Generation

**Issue:** Card-specific Python modules (`src/cards/pack/<pack>/<set>/<card_id>.py`) are manually written and error-prone. Generation process has caught multiple bugs that static testing missed.

**Recent Bugs Fixed (28/07/2026):**

| Card | Bug | Cause | Fix |
|------|-----|-------|-----|
| 60030 Contingency Planning | SetTarget('YourHand') invalid | Typo in from_where selector | → 'YourHandCards' |
| 21185, 32174b, 57063, 57072 | Missing GiveTo on obligation | Copy-paste oversight | + GiveTo "" |
| 59004 Protect Humanity | Uses "3,labor" (labor ∉ COUNTER_LIST) | Field validation gap | → "3,counter" |
| 60001b Sense Deck | Never populated; cards returned to wrong area | Multiple issues (BeginGameWithSetAside missing, broad LeavePlay interception, attachment target logic) | Corrected 5 issues |
| 60040b/c Photographic Reflexes | PR cards not tucked/playable | Complex tuck+play window timing | Validated in bot (28/07/2026) |
| 32177 Brawler, 59014 Golden Mace | Message comparisons ('Attack' vs 'ATK') | Enum code mismatch | Fixed (both cards are from earlier packs, latent bugs) |

**Files:** 
- `src/cards/pack/*/` (4633 .py modules, all 0-line or small)
- Generation validated by `tools/test_cards.py` (3766 cards)
- `tools/test_generate_cards.py` runs CardFactory.GenerateCard on each card (catches asserts)
- `tools/test_autoplay.py` bot plays real games (catches runtime errors)

**Test Coverage:**
- `test_cards`: Import + GetAbilities (syntax-level)
- `test_generate_cards`: CardFactory.GenerateCard (construction asserts)
- `test_autoplay`: Live gameplay (interaction bugs)
- Coverage gap: static type checking on module parameters

**Observations:**
- Old ChatGPT-recovered `.pyc` files in boot_sub (pre-28/07) had NameError/UnboundLocalError, never caught until headless setup reached initialization
- Sense deck had 5 interdependent bugs; none visible until live game

**Recommendation:** 
1. Add mypy-style type checking on card module signatures (currently missing)
2. Document expected patterns for new pack additions (copy from similar card, validate with test_generate_cards)
3. Expand test_autoplay to cover more packs/scenarios

---

## Large Monolithic Modules (High Complexity)

**Issue:** Core message-handling and ability-factory modules are very large (>600 lines each), making them difficult to navigate and extend.

**Largest modules:**
- `src/game/message/sender/sender_card.py` — 769 lines, 106 functions
- `src/game/message/sender/sender_damage.py` — 663 lines
- `src/game/ability/ability.py` — 716 lines
- `src/game/ability/cost_func.py` — 659 lines
- `src/game/ability/factory/ability_factory.py` — 583 lines

**Impact:**
- Hard to locate specific behavior (e.g., damage type comparisons: 'ATK'/'DEF'/'THW')
- Hard to add new ability types without breaking existing ones
- High risk of missed edge cases during refactoring

**Observation:**
- Bytecode constraint makes refactoring doubly risky
- No module-level docstrings or pattern guides

**Recommendation:** 
1. Document key patterns (e.g., message types, ability registration, cost calculation) in code comments or separate guide
2. Extract internal helpers into smaller modules (e.g., `_card_senders_helpers.py`) only if test coverage supports refactoring
3. Defer module splitting until critical bug identified

---

## Hardcoded Hack: HACK_HERO_ID = '3100'

**Issue:** Special hero ID hardcoded for identity form-change detection. May mask underlying design issue.

**Files:** 
- `src/game/player/element/player_setup.py:10` (definition)
- `src/game/player/element/player_setup.py:33, 101` (checks in SetupPlayerAbility, logic_name filter)
- `src/game/ability/factory/setup.py:27-28` (duplicate check)

**Purpose:** Skip face filtering logic when hero_id starts with '3100' (likely a development marker or test hero). Used to prevent duplicate "Change Form" options for certain identity types.

**Observations:**
- No comment explaining what '3100' is or why it exists
- Duplicated in two files (potential maintenance risk)
- Possible artifact from bytecode recovery or pycdc reconstruction

**Recommendation:** 
1. Document what '3100' hero is (test account? incomplete pack?)
2. Consolidate to single location (utility function)
3. Replace with explicit flag if logic is intentional, or remove if obsolete

---

## Campaign Log Complexity & Manual Bookkeeping

**Issue:** Four campaign formats (MTS, MG, NeXt, AoA) have complex, partially automated bookkeeping. Manual player input required; incomplete validation may lead to data loss.

**Files:**
- Campaign setup: `src/cards/pack/<pack>/campaign.py` + `campaign_setup.py` (AoA)
- Mission system: `src/cards/pack/aoa/missions.py` (AoA only)
- Log writer: Each CampaignSetup includes WriteCampaignLogAtGameEnd ability
- Frontend forms: `public/scene.html` (recently added campaign log forms for all 4 packs)
- Log reading: `/read_file?campaign_log_last.json` endpoint

**Current Gaps:**
- **MG Future Past deck** — 5 special scenario cards; setup reads campaign log to determine deck state. No validation that log keys exist.
- **MG Role selection** — Random role chosen at S1 if absent; no UI to preview roles before committing
- **NeXt Marauders/Hope tracking** — Manual bookkeeping (PDF p11/14/16/18); auto-writing of `Hope Summers's Damage Scenario 3|4` depends on log parsing
- **AoA Mission bookkeeping** — Must manually track `Mission Done: <name>`, `Overseer Defeated: <name>` to exclude future draws
- **Captive Allies (MG)** — Auto-written from `CAPTIVE` trait end-of-S2, but player may remove manually; no re-sync

**Observations:**
- Campaign log forms added to scene.html (recently refactored); integration may be incomplete
- No validation of log structure before passing to next scenario
- Each pack reads different log keys; cross-scenario corruption possible

**Test Coverage:**
- `test_autoplay.py` bot doesn't play full campaigns (single scenarios only)
- No cross-scenario campaign flow test in repo (tests in `/home/arnau/marvel-work/tools/`, outside repo)

**Recommendation:**
1. Add JSON schema validation for campaign_log dict (define required/optional keys per pack)
2. Implement campaign-flow test (e.g., MG S1 → S2 → S3 with role tracking)
3. Add UI help text for each campaign log field (currently form-only, no guidance)

---

## Missing Test Infrastructure in Main Repo

**Issue:** Core tests live outside the codebase in `/home/arnau/marvel-work/tools/`, not version-controlled with source.

**Test Files (outside repo):**
- `test_cards.py` — Import + GetAbilities (3766 ok / 0 fail baseline)
- `test_generate_cards.py` — CardFactory.GenerateCard validation
- `test_autoplay.py` — In-process bot gameplay (v3 with strategy, 7+ combos tested)
- `test_newgame.py`, `test_server_port.py`, `innocence_test.py` (misc.)

**Impact:**
- CI/CD cannot run tests (no test runner in repo)
- No automated regression detection on code changes
- Test data/scenarios hardcoded in tools (not in repo; e.g., 'rhino', 'daredevil', 'god_of_lies')

**Observations:**
- README.md missing; getting-started instructions only in TODO.md
- Launcher requires manual environment setup (`~/marvel-work/python/bin/python3.10`)
- No GitHub Actions or CI config

**Recommendation:**
1. Add `tests/` directory to repo; move or mirror test files
2. Add `pyproject.toml` + pytest config for local test discovery
3. Document test running in README.md

---

## Performance Concerns

### Encounter Deck Reshuffle (PopEncounterCards)

**File:** `src/game/operate/worlds.py:22-35`

**Issue:** PopEncounterCards checks deck size, reshuffles discard pile if needed. Process logic:
1. Pop N cards from encounter_deck
2. If empty, reshuffle from encounter_discard_pile
3. Continue until N cards obtained or both empty

No explicit performance constraints; large deck + repeated pops may accumulate overhead.

**Impact:** Likely low (encounter decks ~30-50 cards); tested in autoplay without timeout issues.

**Recommendation:** Defer unless gameplay reports lag.

### Card Generation (CardFactory)

**File:** `src/game/card/factory.py` (590 lines)

**Issue:** GenerateCard constructs full card state (faces, abilities, costs, counters). No lazy initialization; all abilities registered at card creation.

**Observation:** 4331 cards generated successfully in test (28/07/2026); no reported performance issues.

**Recommendation:** Profile on slow machines if needed.

---

## Data Validation Gaps

**Issue:** JSON data files lack explicit validation before loading. Typos in cards.json or sets_info.json silently fail or cause cryptic errors.

**Risk Examples:**
- Invalid `cost` value in cards.json → CardFace initialization fails late
- Missing `card_type` → type checking in card module fails
- Duplicate card_id in sets_info scenarios → encounter deck duplication

**Files:** 
- Loader: `src/engine/lib/*.py` (JSON parsing)
- No schema validation before use

**Recommendation:** Add schema validator (JSON Schema or Pydantic) at game startup; reject with clear error messages.

---

## Security: Obfuscated CODE_KEY

**Issue:** CODE_KEY in `src/core/utility/types.py` appears to be obfuscated string `''.join([x[0] for x in 'Integrated...'.split()])`, but it's extracted as plaintext in Python. Checksum not cryptographically secure.

**Files:** `src/core/utility/types.py:6`

**Impact:** LOW (not for protecting against tampering; only for data integrity check). If attacker knows CODE_KEY, they can forge checksums.

**Observation:** Bytecode recovery means CODE_KEY is visible in all compiled .pyc files anyway.

**Recommendation:** Treat checksums as corruption detection only, not tamper-proofing. Consider removing obfuscation (not worth the complexity).

---

## Compiled Python Cache (4686 .pyc files)

**Issue:** Many compiled `.pyc` files and `__pycache__` directories accumulated. Old files (pre-28/07 ChatGPT recovery) had bugs (NameError, UnboundLocalError) not caught until headless initialization.

**Files:** Throughout `src/` and subdirectories

**Impact:** 
- Stale cache can hide source changes (Python may load old .pyc instead of new .py)
- Old .pyc files (pre-28/07) still present; could be accidentally loaded

**Procedure:**
- Launcher.py recompiles before running (see TODO.md)
- Manual cleanup: `find . -name "*.pyc" -delete`

**Observation:** Fusion/boot_sub recompilation (28/07/2026) solved old .pyc bugs (achievement.py NameError, event/manager.py UnboundLocalError).

**Recommendation:**
1. Add `.pyc` cleanup step to launcher if not already present
2. Document in README that `python -m py_compile` is required after source changes
3. Consider `.gitignore` pattern for __pycache__

---

## Full_Link Card References (Dependency Fragility)

**Issue:** Some cards reference another card's data via `full_link` field. Reduces JSON size but creates hidden dependencies.

**File:** `src/cards/database.py:23-68` (full_link handling)

**Examples:** 
- Daredevil pack (60051 → 32014, 60056 → 40059, 60057/58/59 → 01088/89/90)
- Synthezoid pack (57078-57081 → 57036-57039)
- Total: ~10 full_link cards documented

**Risk:**
- Deleting or renaming target card breaks all full_link references silently
- No validation that target exists before linking
- Circular full_links not detected

**Current Validation:** CardsDB.FindCardPaper checks full_link but returns target paper silently; no warning if target missing.

**Recommendation:**
1. Validate all full_link targets at game startup
2. Add error message if target not found
3. Document full_link rules in cards.json schema

---

## Known Unimplemented / Deferred Features

| Feature | Status | Notes |
|---------|--------|-------|
| Fear No Evil scenarios (Kingpin, Electro, Mysterio) | NOT IN MARVELCDB | Recheck periodically; only 10 nemesis cards found |
| Deck Future Past (MG) | ✅ IMPLEMENTED 28/07 | 5 special cards; log-driven deck assembly |
| Mission area (true engine support) | NOT IMPLEMENTED | Workaround via counters in 45164 |
| Cross-table multiplayer (2+ tables PVP) | NOT IMPLEMENTED | Synthezoid competitive ~= 1 table only |
| Expert campaign (stat carry-over) | PARTIAL | MG/NeXt/AoA only; MTS unclear |
| Set Future Past (MG S2 outcome) | LENIENT | Depends on campaign log accuracy |

---

## Recommendations Summary

**Priority: High**
1. Add E2E tests for game launch flow (scene.html → game start)
2. Migrate campaign log forms to typed/validated subsystem
3. Validate JSON schemas on startup

**Priority: Medium**
1. Move tests from tools/ to repo; add CI runner
2. Document all texte seul features with test cases
3. Consolidate HACK_HERO_ID to single utility function

**Priority: Low**
1. Refactor large message modules (only if new bug requires it)
2. Profile card generation on slow machines
3. Clean up legacy .pyc files

---

*Concerns audit: 2026-07-28*
