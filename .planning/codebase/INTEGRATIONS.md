# External Integrations

**Analysis Date:** 2026-07-28

## APIs & External Services

**Version Management:**
- itch.io (https://irefrixs.itch.io/marvel-lcg)
  - What it's used for: Check for new game versions at startup
  - SDK/Client: `requests.post()`
  - Implementation: `src/engine/lib/check_new_version.py`
  - Authentication: None (public check)
  - Endpoint: POST request to itch.io page, HTML parsing for upload names
  - Version pattern: Extracts `v(X.Y.Z.W)` from upload release names
  - Configuration: Opt-in via `launch.json:check_for_new_version_on_startup` (default: false)

**Date/Time Synchronization:**
- itch.io (https://itch.io)
  - What it's used for: Validate current server date (security/licensing check)
  - SDK/Client: `requests.head()`
  - Implementation: `src/game_entry.py:get_current_date()`
  - Authentication: None (public HEAD request)
  - Usage: Reads HTTP `Date` header to prevent date-spoofing attacks
  - Fallback: Uses local system time if request fails or timeout occurs (3 second timeout)
  - Result requirement: Date timestamp must be > 1877777777 (approximately year 2030 guard)

## File Upload Services

**Cloudflare Workers:**
- Endpoint: https://marvel-lcg-reports.irefrixs.workers.dev/
  - What it's used for: Upload game reports, replays, error logs
  - SDK/Client: `requests.post()`
  - Implementation: `src/engine/network/upload/cloudflare.py:UploadToCloudflare()`
  - Authentication: None required (Worker URL validates requests)
  - Configuration: URL stored in `launch.json:cloudflare_worker_address` (env var override available)
  - Request Format: JSON with `description`, `public` (boolean), `files` dictionary
  - Response: Returns HTTP 201 on success with JSON containing uploaded file paths
  - Used for: Storing game statistics, debug reports, event logs
  - File size: Typically small text/JSON payloads

**GitHub Gists API:**
- Endpoint: https://api.github.com/gists
  - What it's used for: Upload decks, replays, annotations to GitHub Gists
  - SDK/Client: `requests.post()`
  - Implementation: `src/engine/network/upload/gist.py:UploadToGist()`
  - Authentication: Bearer token (GitHub API token required)
    - Env var: Passed as parameter `api_token`
    - Header: `Authorization: Bearer {api_token}`
    - Accept: `application/vnd.github.v3+json`
  - Request Format: JSON with `description`, `public` (boolean), `files` dictionary with content
  - Response: Returns HTTP 201 on success with JSON containing `html_url` for viewing
  - Used for: Sharing deck lists, replay records with public URLs
  - Requires: User GitHub API token (not automated)

**Pastebin API:**
- Endpoint: https://pastebin.com/api/api_post.php
  - What it's used for: Upload text content (logs, reports) to Pastebin
  - SDK/Client: `requests.post()`
  - Implementation: `src/engine/network/upload/pastebin.py:UploadToPastebin()`
  - Authentication: Two-part
    - `api_dev_key`: Application developer key
    - `api_user_key`: User login session key (for private pastes)
  - Request Format: Form-data POST with:
    - `api_paste_code`: Content to upload
    - `api_paste_name`: Paste title
    - `api_paste_expire_date`: Expiration (default 'N' = never)
    - `api_paste_format`: 'json'
  - Response: Returns HTTP 200 with paste URL on success
  - Used for: Temporary file sharing (default: never-expire)
  - Requires: User Pastebin account and API credentials

## Image Servers

**MarvelCDB:**
- Server: https://marvelcdb.com/bundles/cards/
  - What it's used for: Download official card artwork images
  - SDK/Client: `requests.get()` with Mozilla user-agent
  - Implementation: `src/engine/file/cache.py:Cache.LoadImage()`
  - Authentication: None (public CDN)
  - URL Pattern: `https://marvelcdb.com/bundles/cards/{card_id}.jpg`
  - Image Formats Supported: JPEG (Content-Type: `image/jpeg`)
  - Timeout: 3 seconds per request
  - Fallback: If MarvelCDB times out, tries Cerebro or local cache
  - Cache Strategy: Downloaded images stored in `./assets/cache/`
  - Usage: Card display images for all official Marvel Champions LCG cards

**Cerebro (Microsoft Azure):**
- Server: https://cerebrodatastorage.blob.core.windows.net/cerebro-cards/official/
  - What it's used for: Alternative CDN for official card artwork (high-quality HD scans)
  - SDK/Client: `requests.get()` with Mozilla user-agent
  - Implementation: `src/engine/file/cache.py:Cache.LoadImage()`
  - Authentication: None (public Azure Blob Storage)
  - URL Pattern: `https://cerebrodatastorage.blob.core.windows.net/cerebro-cards/official/{CARD_ID_UPPERCASE}.jpg`
  - Image Formats Supported: JPEG (Content-Type: `image/jpeg`)
  - Timeout: 3 seconds per request
  - Priority: Checked first in `launch.json:image_servers` list (before MarvelCDB)
  - Cache Strategy: Downloaded images stored in `./assets/cache/`
  - Usage: Preferred source for HD card scans when available

**Configuration:**
- `launch.json:image_servers` array contains URLs with template placeholders:
  - `{card_id}` - Lowercase card ID (e.g., "60037a")
  - `{card_id:U}` - Uppercase card ID (e.g., "60037A")
- Order in array determines lookup priority
- Supports multiple servers with automatic fallback
- Custom servers can be added via configuration

**Local Image Folders:**
- `./assets/pics/` - Primary local image cache (checked before network)
- `./assets/textures/` - UI texture assets
- `./assets/cache/` - Downloaded images from remote servers
- Can specify additional folders via `launch.json:image_folders` array
- Supports extensions: `.webp`, `.jpg`, `.png`
- Automatic image rotation applied if needed

## Data Storage

**Databases:**
- Not applicable - Uses JSON file-based storage
- `data/cards.json` - In-memory card database (loaded at initialization)
- `data/scenarios/*.json` - Campaign/scenario data
- `data/encounter_sets/*.json` - Reusable encounter definitions
- All data checksummed for integrity

**File Storage:**
- Local filesystem only - No cloud storage integration
- Directory structure:
  - `data/` - Static game data (cards, scenarios, encounter sets)
  - `assets/` - Images, sounds, textures
  - `deck/` - Deck definitions and starter decks
  - `public/` - Web frontend files
  - `replays/` - Game replays (if replay_folders configured)
  - `.game/` - Compiled bytecode (temporary, regenerated at launch)

**Caching:**
- `./assets/cache/` - Downloaded card images from MarvelCDB/Cerebro
- In-memory image cache (`Cache.cache` dictionary in `src/engine/file/cache.py`)
- Response body gzip compression with Cache-Control headers
- Cache max age: Configurable via `launch.json:cache_max_age` (default: 60 seconds)
- Browser cache: HTTP header `Cache-Control: public, max-age=31536000` for static assets

## Authentication & Identity

**Authentication Provider:**
- Custom session-based (no external provider)
  - Implementation: `src/engine/network/web_server.py:IsAuthenticate()`
  - Cookie: `session_token` (MD5 hash of password)
  - Optional: Password field in `launch.json:password` (empty string = disabled)

**Version Checking:**
- Custom client-side version validation
  - Cookie: `app_version` (sent by frontend)
  - Server compares against `Ver.ui_version_str`
  - Mismatch: Prompts cache clear via `clean_cache.html`
  - Configuration: `launch.json:detected_version` (default: true)

**Security Bypass (Development):**
- In launcher.py, authentication can be patched:
  - `WebServer.IsAuthenticate = lambda self, request=None: True` - Disable auth
  - `WebServer.IsVersionMatch = lambda self, request=None: True` - Disable version check
  - Used for local testing and development

## Webhooks & Callbacks

**Incoming Webhooks:**
- None detected - Server is pull-only (no external service pushes data)

**Outgoing Webhooks/Callbacks:**
- Passive uploads only:
  - Report uploads to Cloudflare Workers (one-way)
  - Gist creation to GitHub (one-way)
  - Pastebin creation (one-way)
  - Image downloads from CDNs (pull, not push)
- No subscription-based or event-driven callbacks

## CI/CD & Deployment

**Hosting:**
- Local HTTP server only
  - Single machine (no distributed deployment)
  - Embedded aiohttp server in Python process
  - Default: http://127.0.0.1:2345
  - Configurable via `launch.json:server_addresses` array

**Startup Process:**
- `launcher.py` - Entry point script
  - Compiles Python source to `.pyc`
  - Loads original bytecode for defective files
  - Initializes Engine and WebServer
  - Auto-opens browser via subprocess (`webbrowser.open()` or `cmd.exe /c start` on Windows)

**Browser Auto-Launch:**
- WSL2/Windows: Uses `cmd.exe /c start` to open Windows default browser
- Linux/macOS: Uses Python `webbrowser` module
- Fallback: Prints URL if auto-launch fails (user can open manually)
- Daemon thread: Background task polls server for readiness (600 × 0.5s = 5-min timeout)

**CI/CD System:**
- None detected - Manual testing and deployment
- Test utilities available:
  - `tools/test_cards.py` - Card import validation
  - `tools/test_generate_cards.py` - Full card generation testing
  - `tools/test_autoplay.py` - Bot gameplay testing

## Environment Configuration

**Required Environment Variables:**
- `RELEASE=1` - Must be set for production mode (enforced by launcher.py)
  - Effect: Loads original bytecode overlay for defective files
  - Prevents: ModuleNotFoundError in reconstructed codebase

**Optional Environment Variables:**
- None detected as required (all config via `launch.json`)

**Configuration Files:**
- `launch.json` - Primary configuration file
  - JSON format with typed values (strings, arrays, booleans, integers)
  - Located at repository root and copied to `.game/` at startup
  - Keys used:
    - `server_addresses` - Array of IP:port combinations
    - `password` - Optional authentication password
    - `translate_file` - Path to translation file (optional)
    - `game_statistics_file` - Statistics output filename
    - `statistics` - Boolean to enable/disable statistics tracking
    - `show_image_text` - Boolean for UI text overlay
    - `check_for_new_version_on_startup` - Boolean for version checking
    - `image_servers` - Array of CDN URLs with `{card_id}` placeholders
    - `image_folders` - Array of local image directory paths
    - `sound_folders` - Array of sound asset directories
    - `replay_folders` - Array of replay save directories
    - `starter_deck_folder` - Path to hero starter deck files
    - `cache_max_age` - HTTP cache duration in seconds

**Secrets Management:**
- Password stored as MD5 hash in cookie (not in config)
- External API tokens (GitHub, Pastebin): Passed as parameters at runtime (not stored)
- No `.env` file or secret management system detected
- Risk: Authentication password not persisted (single-use via MD5 hashing)

---

*Integration audit: 2026-07-28*
