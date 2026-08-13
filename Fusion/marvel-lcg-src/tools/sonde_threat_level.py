"""Le mot-cle ThreatLevel PORTE-t-il ? Preuve par substitution.

Un temoin sans le mot-cle et le MEME vilain avec, dans la meme mesure : sans
temoin, une sonde qui rend 0 partout ne se distingue pas d'une sonde cassee.

`CardFactory.CreateFace` a besoin d'un monde (il lit le nombre de joueurs) : la
sonde monte donc une vraie partie avant de mesurer.
"""
import os, sys
os.environ.setdefault("RELEASE", "1")
game_dir = os.path.abspath(sys.argv[1])
os.chdir(game_dir); sys.path.insert(0, game_dir)
sys.argv = [sys.argv[0], "-config_files", "launch.json", "-device", "key"]

import json
from engine.device.manager.base import DeviceManager
passer = json.dumps({"id": "0", "targets": [], "resources": []})
DeviceManager.DoGetInput = lambda self, data, player_id, check: passer
DeviceManager.DoWaitConnect = lambda self, player_id, check: None
DeviceManager.DoWaitSync = lambda self, player_id, check: None

from engine import Engine
Engine.Initialize()
from engine.file.manager import FileManager
from game.scene.loader import SceneLoader

def lire(genre, nom):
    chemin = FileManager.FindJsonPath(genre, nom)
    assert chemin, f"{genre} introuvable : {nom}"
    with FileManager.OpenFile(chemin, read=True) as f:
        return f.Read()

scene = SceneLoader.NewFromJson(lire("Campaign", "rhino"), None, [lire("Hero", "spider_man")], 1, [], {})
jeu = Engine.game
jeu.session.SetScene(scene, "Load")
# Le monde n'existe qu'apres la mise en place : `jeu.world` est None avant.
assert jeu.GameSetup(), "GameSetup a echoue"

from cards.database import CardsDB
from game.card.factory import CardFactory
from game.card.face.base import Villain

TEMOIN = "01094"  # Rhino I, un vilain officiel sans ThreatLevel
papier = CardsDB.papers[TEMOIN]

# On lit la valeur IMPRIMEE : c'est elle qui prouve que le `desc` atteint la
# face. Le mot-cle calcule (`threat_level`) demande une carte en jeu, pas une
# face nue -- une face fabriquee seule n'a pas de `card`.
temoin = CardFactory.CreateFace(papier, jeu.world).CastTo(Villain)
print(f"temoin    {TEMOIN} : printed_threat_level = {temoin.printed_threat_level}")

papier.desc["ThreatLevel"] = "2"
substitue = CardFactory.CreateFace(papier, jeu.world).CastTo(Villain)
print(f"substitue {TEMOIN} : printed_threat_level = {substitue.printed_threat_level}")

ok = temoin.printed_threat_level == 0 and substitue.printed_threat_level == 2
print("VERDICT :", "le desc ThreatLevel atteint la face" if ok else "ECHEC")
sys.exit(0 if ok else 2)
