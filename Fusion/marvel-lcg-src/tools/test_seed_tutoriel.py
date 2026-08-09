"""Garde-fou du mode Decouverte : la partie du tutoriel doit rester IDENTIQUE.

Le tutoriel NOMME des cartes precises (« joue Coup de pied volant ») parce que
la main de depart est garantie par le seed. Si le moteur change un jour son
tirage, les lecons deviennent fausses SANS que rien ne plante : ce test est le
seul endroit qui s'en apercevra.

Reference relevee le 3/8/2026 : Spider-Man contre Rhino, seed 42.
A relancer apres toute mise a jour du moteur. S'il tombe, ce ne sont pas les
lecons qui sont cassees, c'est leur postulat : relire
ui-app/src/board/lecons.ts avant de changer quoi que ce soit.

Usage: python3.10 tools/test_seed_tutoriel.py <game_dir> <port>
Viser .game-src, jamais .game (voir GUIDE-CREATION-CONTENU.md §8).
"""
import json
import os
import sys

os.environ.setdefault("RELEASE", "1")

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])

SCENARIO = "rhino"
HEROS = "spider_man"
SEED = 42

MAIN_ATTENDUE = ["01092", "01065", "01009", "01005", "01061", "01060"]
DECK_ATTENDU = ["01061", "01059", "01058", "01064", "01004"]

CONFIG = os.path.join(GAME_DIR, "launch.json")
CONFIG_ORIGINE = open(CONFIG, encoding="utf-8").read()

os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

cfg = json.loads(CONFIG_ORIGINE)
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
json.dump(cfg, open(CONFIG, "w", encoding="utf-8"), indent=2)

# Le moteur est bavard : on l'envoie dans un journal et on garde la sortie
# standard pour le compte rendu.
SORTIE = sys.stdout
sys.stdout = open("/tmp/test_seed_tutoriel_moteur.log", "w", buffering=1)
sys.stderr = sys.stdout


def restaurer_config():
    with open(CONFIG, "w", encoding="utf-8") as f:
        f.write(CONFIG_ORIGINE)


def conclure(main, deck):
    """Compare, rend compte, restaure la configuration et sort.

    Tout se fait ICI parce que la boucle de jeu ne rend jamais la main : on ne
    peut pas comparer « apres » GameLoop.
    """
    soucis = []
    if main != MAIN_ATTENDUE:
        soucis.append(f"main de depart = {main}\n         attendu = {MAIN_ATTENDUE}")
    if deck != DECK_ATTENDU:
        soucis.append(f"dessus du deck = {deck}\n         attendu = {DECK_ATTENDU}")

    restaurer_config()

    for souci in soucis:
        print("ECHEC " + souci, file=SORTIE)
    if not soucis:
        print("OK    la partie du tutoriel est inchangee", file=SORTIE)
        print(f"      main : {main}", file=SORTIE)
        print(f"      deck : {deck}", file=SORTIE)
    print(("\nTOUT PASSE" if not soucis else
           "\nLA PARTIE DU TUTORIEL A CHANGE."
           "\nLes lecons de ui-app/src/board/lecons.ts nomment des cartes precises :"
           "\nles relire AVANT de mettre a jour les valeurs attendues ci-dessus."),
          file=SORTIE)
    SORTIE.flush()
    # os._exit et pas sys.exit : le serveur web laisse des threads vivants.
    os._exit(0 if not soucis else 1)


releve = {}

try:
    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine.device.manager.base import DeviceManager
    DeviceManager.DoWaitConnect = lambda self, p, c: None
    DeviceManager.DoWaitSync = lambda self, p, c: None

    def pilote(self, data, player_id, check):
        # Des que le moteur demande quoi que ce soit, la mise en place est
        # faite : on releve la main, on conclut, on sort.
        from engine import Engine
        joueur = Engine.game.world.players[0]
        conclure(
            [getattr(f.paper, "card_id", "?") for f in joueur.hand_cards.GetAll()],
            [getattr(f.paper, "card_id", "?") for f in joueur.player_deck.Get()[:5]],
        )
        return json.dumps({"id": "0", "targets": [], "resources": []})

    DeviceManager.DoGetInput = pilote

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader
    scene = SceneLoader.NewScene(SCENARIO, None, [HEROS], SEED)
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")
    if jeu.GameSetup():
        jeu.GameLoop()
except Exception as exc:
    import traceback
    traceback.print_exc()
    restaurer_config()
    print(f"ECHEC le test lui-meme a plante : {type(exc).__name__}: {exc}", file=SORTIE)
    SORTIE.flush()
    os._exit(1)

restaurer_config()
print("ECHEC la partie s'est terminee sans jamais demander d'action", file=SORTIE)
SORTIE.flush()
os._exit(1)
