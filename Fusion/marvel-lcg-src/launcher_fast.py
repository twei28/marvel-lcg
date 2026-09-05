"""Lanceur RAPIDE du dépôt fusionné Marvel LCG.

Même résultat que launcher.py, mais démarrage quasi-instantané après le
premier lancement :

  * compilation INCRÉMENTALE : seuls les .py modifiés depuis la dernière
    fois sont recompilés (le tout premier lancement compile les ~4500
    fichiers une fois, les suivants ne recompilent que ce qui a changé) ;
  * data/deck/public/puzzle/assets sont LIÉS (symlink) dans .game au lieu
    d'être recopiés à chaque fois — plus aucune copie d'images. Bonus : les
    modifications de public/ (interface) sont prises en compte sans rien
    recopier.

Usage : python3.10 launcher_fast.py    (Python 3.10 OBLIGATOIRE)

Le premier lancement peut rester long (compilation initiale) ; les suivants
sont rapides. Pour forcer une reconstruction complète : supprime le dossier
.game (ou lance avec l'argument  --clean).
"""
import os, sys, json, time, py_compile, shutil

# Python 3.10 MINIMUM. Le verrou était auparavant « exactement 3.10 », parce que
# les 28 fichiers défectueux étaient superposés en bytecode compilé pour cette
# version. `defectueux.json` est désormais VIDE : tout tourne depuis les sources,
# et une version plus récente n'est plus interdite par construction. Elle reste
# non vérifiée, d'où l'avertissement plutôt que le silence.
if sys.version_info[:2] < (3, 10):
    raise SystemExit(f"Python 3.10 minimum, détecté {sys.version.split()[0]}")
if sys.version_info[:2] != (3, 10):
    print(f"[info] Python {sys.version.split()[0]} : le jeu est éprouvé sur 3.10. "
          f"En cas d'erreur inattendue, réessayer avec Python 3.10 avant de chercher ailleurs.")

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
ORIG = os.path.join(ROOT, "originals_pyc")
GAME = os.path.join(ROOT, ".game")
os.environ["RELEASE"] = "1"

CLEAN = "--clean" in sys.argv[1:]
BUILD_ONLY = "--build-only" in sys.argv[1:]
NO_BROWSER = "--no-browser" in sys.argv[1:]

# --config <fichier> : sert CE fichier au lieu de launch.json, sans y toucher.
# Chemin relatif a ROOT. Inerte si absent : comportement solo/multi inchange.
CONFIG_ARG = None
if "--config" in sys.argv[1:]:
    _idx = sys.argv.index("--config")
    if _idx + 1 >= len(sys.argv):
        raise SystemExit("--config attend un chemin de fichier en argument")
    CONFIG_ARG = sys.argv[_idx + 1]

t0 = time.time()

# Reconstruction complète seulement si demandé ou si .game absent.
if CLEAN and os.path.exists(GAME):
    print("[fast] --clean : suppression de .game")
    shutil.rmtree(GAME)
os.makedirs(GAME, exist_ok=True)

defective_raw = json.load(open(os.path.join(ROOT, "defectueux.json")))["defectueux"]
defective = {d.replace("\\", "/") for d in defective_raw}

def rel_posix(path, start):
    return os.path.relpath(path, start).replace("\\", "/")

# ------------------------------------------------------------------ #
# 1. Compilation incrémentale des sources -> .game/*.pyc
# ------------------------------------------------------------------ #
compiled = skipped = overlaid = failed = 0
seen_pyc = set()

for root, dirs, files in os.walk(SRC):
    for f in files:
        if not f.endswith(".py"):
            continue
        srcp = os.path.join(root, f)
        rel = rel_posix(srcp, SRC)          # ex: engine/engine.py
        pyc_rel = rel[:-3] + ".pyc"
        dst = os.path.join(GAME, pyc_rel)
        seen_pyc.add(os.path.normpath(dst))

        # Fichiers défectueux : on pose le bytecode d'origine (une seule fois).
        if rel in defective:
            if not os.path.exists(dst):
                op = os.path.join(ORIG, pyc_rel)
                if os.path.exists(op):
                    os.makedirs(os.path.dirname(dst), exist_ok=True)
                    shutil.copy(op, dst)
                    overlaid += 1
            continue

        # Sinon : (re)compiler seulement si le .pyc est absent ou périmé.
        if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(srcp):
            skipped += 1
            continue

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            py_compile.compile(srcp, cfile=dst, doraise=True)
            compiled += 1
        except py_compile.PyCompileError:
            # fichier défectueux non listé : tentative d'overlay d'origine
            op = os.path.join(ORIG, pyc_rel)
            if os.path.exists(op):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy(op, dst)
                overlaid += 1
            else:
                failed += 1

# 1b. Élaguer les .pyc orphelins (source .py supprimée/renommée)
pruned = 0
for root, dirs, files in os.walk(GAME):
    # ne pas descendre dans les répertoires de données liés
    dirs[:] = [d for d in dirs if not os.path.islink(os.path.join(root, d))]
    for f in files:
        if not f.endswith(".pyc"):
            continue
        p = os.path.normpath(os.path.join(root, f))
        if p not in seen_pyc:
            try:
                os.remove(p)
                pruned += 1
            except OSError:
                pass

# ------------------------------------------------------------------ #
# 2. Données/ressources : liens symboliques (pas de copie)
# ------------------------------------------------------------------ #
def link_dir(name):
    s = os.path.join(ROOT, name)
    link = os.path.join(GAME, name)
    if not os.path.isdir(s):
        return
    if os.path.islink(link):
        return  # déjà lié
    if os.path.exists(link):
        shutil.rmtree(link)  # ancien dossier copié par launcher.py -> on remplace
    try:
        os.symlink(s, link, target_is_directory=True)
    except OSError:
        shutil.copytree(s, link, dirs_exist_ok=True)  # repli si symlink impossible

for d in ("data", "deck", "public", "puzzle", "assets"):
    link_dir(d)

# Fichier source de la config : launch.json par defaut, ou celui donne par
# --config (chemin relatif a ROOT). Pas de repli silencieux si absent.
if CONFIG_ARG:
    config_src = os.path.join(ROOT, CONFIG_ARG)
    if not os.path.isfile(config_src):
        raise SystemExit(f"--config : fichier introuvable : {config_src}")
else:
    config_src = os.path.join(ROOT, "launch.json")
shutil.copy(config_src, os.path.join(GAME, "launch.json"))

print(f"[fast] compilés:{compiled} inchangés:{skipped} overlay:{overlaid} "
      f"élagués:{pruned} échecs:{failed}  ({time.time() - t0:.1f}s)")

if BUILD_ONLY:
    print("[fast] --build-only : construction terminée, moteur non démarré.")
    raise SystemExit(0)

# ------------------------------------------------------------------ #
# 3. Démarrage (identique à launcher.py)
# ------------------------------------------------------------------ #
os.chdir(GAME)
sys.path.insert(0, GAME)

try:
    import winsound  # noqa: F401
except ModuleNotFoundError:
    import types
    ws = types.ModuleType("winsound")
    for name in ("Beep", "PlaySound", "MessageBeep"):
        setattr(ws, name, lambda *a, **k: None)
    for name in ("SND_FILENAME", "SND_ALIAS", "SND_LOOP", "SND_MEMORY", "SND_PURGE",
                 "SND_ASYNC", "SND_NODEFAULT", "SND_NOSTOP", "SND_NOWAIT", "SND_APPLICATION",
                 "MB_ICONASTERISK", "MB_ICONEXCLAMATION", "MB_ICONHAND", "MB_ICONQUESTION", "MB_OK"):
        setattr(ws, name, 0)
    sys.modules["winsound"] = ws

from engine.network.web_server import WebServer
# ⚠ NE PAS REMETTRE `WebServer.IsAuthenticate = lambda ...: True` ICI.
#
# Cette ligne debranchait le mot de passe du moteur. Sans consequence tant que
# le jeu tournait sur la machine de son proprietaire ; desastreuse des qu'il est
# servi sur un domaine public, ou n'importe qui trouvant l'adresse entrait dans
# la partie sans rien presenter.
#
# La retirer ne change RIEN au jeu local : sans `password` dans la
# configuration, `hash_password` vaut None et `IsAuthenticate` rend True de
# lui-meme (engine/network/web_server.py). Le mot de passe n'est exige que
# lorsqu'il est configure, c'est-a-dire quand le site lance la partie — et le
# lien de siege pose alors le cookie tout seul (`handle_claim_seat`).
#
# `IsVersionMatch` reste debranchee : elle exige un cookie `app_version` que
# personne n'a a sa premiere visite, et renverrait chacun sur clean_cache.
WebServer.IsVersionMatch = lambda self, request=None: True
from engine import Engine
print("Engine.Initialize() ->", Engine.Initialize())

def _open_browser():
    import json as _json, time, urllib.request, shutil, subprocess, webbrowser
    try:
        addr = _json.load(open(os.path.join(GAME, "launch.json")))["server_addresses"][0]
    except Exception:
        addr = "127.0.0.1:2345"
    url = f"http://{addr}"
    for _ in range(600):
        try:
            urllib.request.urlopen(url, timeout=1)
            break
        except Exception:
            time.sleep(0.5)
    try:
        if shutil.which("cmd.exe"):
            subprocess.Popen(["cmd.exe", "/c", "start", "", url], cwd="/mnt/c/")
        else:
            webbrowser.open(url)
        print(f"Navigateur ouvert sur {url}")
    except Exception as e:
        print(f"Impossible d'ouvrir le navigateur ({e}) — ouvre {url} manuellement.")

import threading
# --no-browser : pas de fenetre. Sans lui, quatre places ouvriraient quatre
# fenetres de navigateur.
if not NO_BROWSER:
    threading.Thread(target=_open_browser, daemon=True).start()

Engine.EngineRun()
