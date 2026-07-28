# Technology Stack

**Analysis Date:** 2026-07-28

## Languages

**Primary:**
- Python 3.10 - Backend game engine and web server (required, enforced at `src/launcher.py:11`)
- JavaScript (Vanilla) - Frontend UI in `public/` (no frameworks)
- HTML/CSS - Template and styling files in `public/`

## Runtime

**Environment:**
- Python 3.10 (bytecode reconstructed from original, compiled to `.pyc` at startup)

**Package Manager:**
- pip (dependencies installed via system Python environment)
- Lockfile: Not present (no `requirements.txt` or `pyproject.toml`)

## Frameworks

**Core:**
- aiohttp 3.x - Web server framework for handling HTTP requests and WebSocket connections
  - Used in `src/engine/network/web_server.py`
  - Provides `web.Application`, `web.Request`, async request handlers
  - Supports both GET and POST routes with security wrappers

**Image Processing:**
- Pillow/PIL - Image loading, rotation, manipulation
  - Imported as `from PIL import Image, ImageFont, ImageDraw, ImageOps`
  - Used in `src/engine/file/cache.py` for image format detection and processing
  - Handles formats: WEBP, JPG, PNG

**Async/Concurrency:**
- asyncio - Built-in async/await support (standard library)
- concurrent.futures.ThreadPoolExecutor - Thread pool for CPU-bound tasks
- threading - Background tasks (e.g., browser auto-launch in `launcher.py`)

**Console/Styling:**
- colorama - Colored console output for logging
  - Used in `src/engine/lib/check_new_version.py` for colored status messages

**System/Utilities:**
- psutil - System information (process monitoring)
  - Used in `src/engine/user/user_info.py`

## Key Dependencies

**Critical:**
- requests 2.x - HTTP client for external APIs
  - Version checking (`src/engine/lib/check_new_version.py`)
  - File uploads to Cloudflare, Pastebin, GitHub Gist (`src/engine/network/upload/`)
  - Image downloading from MarvelCDB, Cerebro (`src/engine/file/cache.py`)

- aiohttp - Async HTTP server and WebSocket support
  - Core server infrastructure
  - Handles all web routes (GET/POST)
  - Cookie-based authentication

**Standard Library Heavily Used:**
- json - Card data, scenario data, deck files, configuration
- gzip - Response compression (`src/engine/network/web_server.py`)
- hashlib - MD5 password hashing for authentication
- asyncio - Event loop and async task scheduling
- threading - Background threads (browser launcher, async task runners)
- collections, dataclasses, enum, typing - Type definitions and data structures
- html.parser - HTML parsing for version check page scraping
- re - Regular expressions for card ID validation, version parsing
- pathlib, os - File system operations
- uuid - Unique identifiers
- inspect, types - Python introspection
- cProfile - Performance profiling support

**Windows-Specific (with Cross-Platform Stub):**
- winsound - Windows audio alerts
  - Stub implementation in `launcher.py:60-72` for non-Windows platforms

## Configuration

**Environment Variables:**
- `RELEASE=1` - Set by launcher.py to enable release mode and load original bytecode (`src/launcher.py:17`)
- `PYTHONPATH` - Includes `.game/` directory for bytecode loading

**Configuration Files:**
- `launch.json` - Main configuration file at repository root
  - Server addresses (default: `127.0.0.1:2345`)
  - Authentication password (optional, MD5 hashed)
  - Image server URLs for card artwork
  - Asset folders (images, sounds, replays, decks, scenarios)
  - Statistics tracking toggles
  - Cache max age (default: 60 seconds)

**Build Configuration:**
- Bytecode compilation via `py_compile.compile()` in `launcher.py`
- Defective files list in `defectueux.json` - modules that failed compilation, replaced with original bytecode
- Compiled bytecode assembled in `.game/` directory (temporary, recreated on each launch)

**Dynamic Configuration:**
- `src/engine/config.py` - ConfigVariables system for runtime configuration
  - Reads from `launch.json` (primary)
  - Examples: `image_servers`, `password`, `cache_max_age`, `sound_folders`, `replay_folders`

## Platform Requirements

**Development:**
- Python 3.10 (strict requirement, no other versions supported)
- Standard C/C++ toolchain (for PIL/Pillow compilation)
- Unix/Linux environment or WSL2 (Windows Subsystem for Linux)

**Runtime:**
- Python 3.10 runtime with pip
- Network access (for version checks and image downloads)
- Local filesystem access for:
  - `data/*.json` - Card database, set information, scenarios
  - `assets/` - Images, sounds, textures
  - `public/` - Web frontend files
  - `deck/` - Deck definitions
  - `.game/` - Compiled bytecode (generated at startup)

**Production/Deployment:**
- Linux/Unix-based (supports WSL2, native Linux)
- Single-machine deployment (no distributed architecture)
- HTTP server on configurable IP/port (default: 127.0.0.1:2345)
- Local browser as client (auto-opened via subprocess)

## Build Process

**Entry Point:** `launcher.py`

**Build Steps:**
1. Python version validation (requires 3.10)
2. Directory cleanup: Remove `.game/` if exists
3. Compile all `.py` files in `src/` to `.pyc` bytecode
4. Overlay original bytecode for defective files (from `defectueux.json`)
5. Copy data directories (`data/`, `deck/`, `public/`, `puzzle/`, `assets/`)
6. Copy `launch.json` configuration
7. Stub `winsound` module for non-Windows platforms
8. Initialize Engine and start WebServer
9. Auto-open browser to `http://127.0.0.1:2345`

**Compilation Options:**
- `doraise=True` - Raise exceptions on compilation errors
- Bytecode stored in `.pyc` format (Python 3.10 compatible)

## Data Formats

**JSON-Based:**
- `data/cards.json` - Card definitions (~2.3 MB)
  - Contains: Card ID, costs, health, stats, abilities, pack references
  - Checksummed with SHA256 for integrity validation
  - Sections: Standard sets (mts, mut_gen, fne, aoa, cw, next_evol, etc.)

- `data/sets_info.json` - Set metadata (~19 KB)
  - Pack information, hero references, max card IDs
  - Checksummed for integrity

- `data/scenarios/*.json` - Campaign and scenario definitions
  - Villain stats, encounter sets, difficulty variations

- `data/encounter_sets/*.json` - Minion/side scheme definitions
  - Reusable encounter modules

- `deck/*.json` - Deck definitions
  - `deck/starter/*.json` - Hero starter decks (auto-discovered via `/list_starter_deck`)

- `data/translate_cn.json` - Chinese translations (optional)

- `launch.json` - Runtime configuration

**Text/Binary:**
- `assets/pics/*.{jpg,png,webp}` - Card images
- `assets/sounds/*.wav` - Audio effects
- `assets/textures/*` - UI textures
- `.pyc` files - Compiled Python bytecode in `.game/`

## Checksumming

**Integrity Validation:**
- Cards database and sets info require checksum field
- Formula: `SHA256(JSON.dumps(obj_without_checksum, sort_keys=True) + ' ' + CODE_KEY)`
- `CODE_KEY` defined in `src/core/utility/types.py`
- Validated on game initialization

---

*Stack analysis: 2026-07-28*
