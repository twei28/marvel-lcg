import sys, os, threading, time
GAME_DIR = os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/marvel-work/boot_sub")
os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
sys.stdout = open('/tmp/game_stdout.log', 'w', buffering=1)
sys.stderr = sys.stdout
from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True
from engine import Engine
ok = Engine.Initialize()
print("INIT:", ok, flush=True)
from game.scene.loader import SceneLoader
scene = SceneLoader.NewScene('rhino', None, ['spider_man'], 42)
print("SCENE CREATED:", type(scene).__name__, flush=True)
game = Engine.game
game.session.SetScene(scene, 'Load')
def run():
    try:
        if game.GameSetup():
            game.GameLoop()
    except Exception:
        import traceback; traceback.print_exc()
t = threading.Thread(target=run, daemon=True)
t.start()
time.sleep(20)
w = game.world
print("WORLD:", bool(w), flush=True)
if w:
    try:
        print("PLAYERS:", len(w.players), flush=True)
        p = w.players[0]
        print("HERO faces:", [str(f) for f in [p.identity.hero]][:1], flush=True)
    except Exception as e:
        print("introspection:", type(e).__name__, e, flush=True)
os._exit(0)
