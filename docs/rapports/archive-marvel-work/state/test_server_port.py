import sys, os, threading, time, json
PORT = int(sys.argv[1])
GAME_DIR = os.path.expanduser("~/marvel-work/boot_sub")
os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
cfg = json.load(open("launch.json"))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open("launch.json", "w"), indent=2)
sys.stdout = open('/tmp/game_stdout.log', 'w', buffering=1)
sys.stderr = sys.stdout
from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True
from engine import Engine
ok = Engine.Initialize()
print("INIT:", ok, flush=True)
if not ok:
    os._exit(1)
def check():
    time.sleep(12)
    import urllib.request
    try:
        r = urllib.request.urlopen(f"http://127.0.0.1:{PORT}/scene", timeout=10)
        body = r.read()
        print("SCENE HTTP", r.status, len(body), "octets", flush=True)
    except Exception as e:
        print("SCENE FAIL:", e, flush=True)
    time.sleep(1)
    os._exit(0)
threading.Thread(target=check, daemon=True).start()
Engine.EngineRun()
