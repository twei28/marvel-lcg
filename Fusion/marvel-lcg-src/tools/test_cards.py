"""Teste la construction des capacités de toutes les cartes d'un dossier de jeu.

Usage: python3.10 test_cards.py <game_dir> <port> [rapport.json]
"""
import sys, os, json, importlib, pkgutil, traceback

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
REPORT = sys.argv[3] if len(sys.argv) > 3 else "/tmp/cards_report.json"

os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
cfg_path = os.path.join(GAME_DIR, "launch.json")
cfg = json.load(open(cfg_path))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open(cfg_path, "w"), indent=2)

sys.stdout = open("/tmp/cards_stdout.log", "w", buffering=1)
sys.stderr = sys.stdout

from engine import Engine
ok_init = Engine.Initialize()
print("INIT:", ok_init, flush=True)

import cards.pack as P
ok, err, no_ga = 0, 0, 0
failures = {}
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

result = {"init": bool(ok_init), "ok": ok, "err": err, "sans_GetAbilities": no_ga,
          "failures": failures}
json.dump(result, open(REPORT, "w"), indent=1, ensure_ascii=False)
print(f"RESULT ok={ok} err={err} no_ga={no_ga}", flush=True)
os._exit(0)
