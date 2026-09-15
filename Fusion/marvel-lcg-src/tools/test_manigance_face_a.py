"""La face A de la manigance principale s'arrete et attend le premier joueur.

Usage:
    ~/marvel-work/python/bin/python3.10 tools/test_manigance_face_a.py \
        .game-src-par7 45100 [nom_du_cas]

Chaque cas tourne dans SON propre processus : le moteur est un singleton
global, impossible a reinitialiser proprement entre deux parties. Meme
technique que tools/test_capacites.py, en beaucoup plus petit : on detourne
DeviceManager.DoGetInput pour repondre a la place du client, et on observe.
"""
import json
import os
import subprocess
import sys
import threading
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man"):
    """Demarre une partie et rend (jeu, monde, journal_des_questions).

    `journal_des_questions` se remplit au fil des appels du moteur au client :
    une entree par question, avec les noms d'options publies.
    """
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    json.dump(cfg, open("launch.json", "w"), indent=2)

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine.device.manager.base import DeviceManager

    journal = []

    def pilote(self, data, player_id=None, check=None):
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        noms = [o.get("name") for o in options if isinstance(o, dict)]
        journal.append(noms)
        if len(journal) > 400:
            os._exit(3)
        for o in options:
            if isinstance(o, dict) and not o.get("failure_reason"):
                legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                mini = (o.get("target_num_range") or [0, 0])[0]
                return json.dumps({"id": str(o.get("id", 0)),
                                   "targets": legales[:mini],
                                   "resources": []})
        return None

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader

    with open(_chemin_json("Campaign", scenario)) as f:
        campagne = f.read()
    with open(_chemin_json("Hero", heros)) as f:
        hero = f.read()
    scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, regles, {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        # GameSetup() seul : "atteindre la mise en place" s'arrete la, pas au
        # bout d'une partie. Enchainer sur jeu.GameLoop() (gabarit d'origine)
        # fait entrer dans les tours normaux, ou le pilote nature (premiere
        # option sans failure_reason) boucle sans fin sur une capacite de
        # heros qui echoue systematiquement (Enhanced Ivory Horn, constate le
        # 15/09/2026) : hors sujet pour ce harnais, qui n'a besoin que de la
        # mise en place.
        try:
            jeu.GameSetup()
        except BaseException:
            import traceback
            traceback.print_exc()

    threading.Thread(target=run, daemon=True).start()
    time.sleep(20)
    return jeu, jeu.world, journal


def _chemin_json(genre, nom):
    from engine.file import FileManager
    chemin = FileManager.FindJsonPath(genre, nom)
    assert chemin, f"{genre} {nom} introuvable"
    return chemin


def cas_drapeau_pose(game_dir, port):
    """Le drapeau existe, et la liste de regles l'allume."""
    _, monde, _ = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    assert bool(monde.rule.confirm_main_scheme) is True, \
        "la regle confirm_main_scheme n'a pas ete posee"
    return "le drapeau confirm_main_scheme est pose"


CAS = {"drapeau_pose": cas_drapeau_pose}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    noms = [voulu] if voulu else list(CAS)
    for rang, nom in enumerate(noms):
        fils = subprocess.run(
            [sys.executable, os.path.abspath(__file__), game_dir,
             str(port + rang), nom, "--fils"],
            cwd=RACINE, capture_output=True, text=True, timeout=180)
        verdict = "VERT" if fils.returncode == 0 else "ROUGE"
        print(f"{verdict} : {nom}")
        if fils.returncode != 0:
            print(fils.stdout[-3000:])
            print(fils.stderr[-3000:])
            sys.exit(1)


if __name__ == "__main__":
    if "--fils" in sys.argv:
        # os._exit (pas un retour normal) : GameSetup demarre des threads du
        # moteur qui ne sont pas tous daemon (voir tools/test_capacites.py,
        # meme parade). Sans ca, le processus fils reste accroche apres le
        # print et le lanceur parent finit par expirer sur le timeout du
        # subprocess plutot que de lire un vrai code de sortie.
        nom = sys.argv[3]
        try:
            resultat = CAS[nom](sys.argv[1], int(sys.argv[2]))
        except BaseException:
            import traceback
            traceback.print_exc()
            os._exit(1)
        print(resultat)
        os._exit(0)
    main()
