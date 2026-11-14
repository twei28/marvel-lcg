"""Lanceur du dépôt fusionné Marvel LCG.

Compile les sources Python en bytecode, superpose les bytecodes d'origine
pour les 28 fichiers encore défectueux (listés dans defectueux.json), puis
démarre le moteur et sert le jeu sur 127.0.0.1:<port de launch.json>.

Usage : python3.10 launcher.py    (Python 3.10 OBLIGATOIRE)
"""
import os, sys, json, py_compile, shutil, tempfile

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
os.environ["RELEASE"] = "1"

# Répertoire de jeu compilé (bytecode), assemblé à côté des données.
GAME = os.path.join(ROOT, ".game")
if os.path.exists(GAME):
    shutil.rmtree(GAME)
os.makedirs(GAME)

defective = set(json.load(open(os.path.join(ROOT, "defectueux.json")))["defectueux"])

# 1. compiler toutes les sources en .pyc dans GAME
for root, dirs, files in os.walk(SRC):
    for f in files:
        if not f.endswith(".py"):
            continue
        rel = os.path.relpath(os.path.join(root, f), SRC)
        dst = os.path.join(GAME, rel[:-3] + ".pyc")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            py_compile.compile(os.path.join(root, f), cfile=dst, doraise=True)
        except py_compile.PyCompileError:
            pass  # fichier défectueux : sera écrasé par le bytecode d'origine

# 2. superposer les bytecodes d'origine des fichiers défectueux
for rel in defective:
    pyc = rel[:-3] + ".pyc"
    op = os.path.join(ORIG, pyc)
    if os.path.exists(op):
        dst = os.path.join(GAME, pyc)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(op, dst)

# 3. données et ressources à la racine du répertoire de jeu (chemins relatifs)
for d in ("data", "deck", "public", "puzzle", "assets"):
    s = os.path.join(ROOT, d)
    if os.path.isdir(s):
        shutil.copytree(s, os.path.join(GAME, d), dirs_exist_ok=True)
shutil.copy(os.path.join(ROOT, "launch.json"), os.path.join(GAME, "launch.json"))

# 4. démarrage
os.chdir(GAME)
sys.path.insert(0, GAME)

# winsound n'existe que sous Windows ; stub neutre ailleurs (Linux/WSL/tests)
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

# Ouvre automatiquement le jeu dans le navigateur dès que le serveur répond.
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
        if shutil.which("cmd.exe"):  # WSL → navigateur Windows par défaut
            subprocess.Popen(["cmd.exe", "/c", "start", "", url], cwd="/mnt/c/")
        else:
            webbrowser.open(url)
        print(f"Navigateur ouvert sur {url}")
    except Exception as e:
        print(f"Impossible d'ouvrir le navigateur ({e}) — ouvre {url} manuellement.")

import threading
threading.Thread(target=_open_browser, daemon=True).start()

Engine.EngineRun()
