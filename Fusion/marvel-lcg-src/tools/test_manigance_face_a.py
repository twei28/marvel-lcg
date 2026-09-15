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


def cas_question_posee(game_dir, port):
    """Le client est VRAIMENT interroge sur la face A.

    ⚠ Ce cas existe parce que le contraire a ete mesure le 15/09/2026 : une
    question a une seule option avec `forced=True` (le defaut de
    `AskChooseOneText`) est resolue par le moteur SANS jamais atteindre le
    client. Le cas ne regarde donc pas l'etat final, il regarde le JOURNAL DES
    QUESTIONS.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    posees = [noms for noms in journal if "Reveal_Main_Scheme" in noms]
    assert len(posees) == 1, \
        f"la question devait etre posee 1 fois, journal={journal[:20]}"
    return "la question Reveal_Main_Scheme a atteint le client"


def cas_sans_drapeau_aucune_question(game_dir, port):
    """Une partie SANS la regle ne pose pas la question.

    C'est la garde qui protege les sauvegardes et les campagnes en cours : une
    scene ecrite avant ce changement ne porte pas `confirm_main_scheme`, sa
    liste d'operations rejouees ne doit donc pas bouger d'un cran.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, [])
    assert bool(monde.rule.confirm_main_scheme) is False
    posees = [noms for noms in journal if "Reveal_Main_Scheme" in noms]
    assert posees == [], f"question posee sans la regle : {posees}"
    from game.operate.worlds import Worlds
    schemes = Worlds.GetAllMainSchemes(monde)
    assert schemes and schemes[0].paper.card_id == "01097b", \
        f"la manigance devait etre retournee toute seule : {schemes}"
    return "sans la regle : aucune question, et la manigance est retournee"


def cas_etape_suivante(game_dir, port):
    """Une etape completee pose la meme question sur sa face A.

    Scenario Klaw : l'etape 1 est 01116a/b, l'etape 2 est 01117a/b. On force le
    passage plutot que de jouer la partie jusqu'au bout : c'est le meme appel
    (`MainScheme.Advance`) que celui d'une etape reellement completee.
    """
    _, monde, journal = monter_le_moteur(
        game_dir, port, ["confirm_main_scheme"], scenario="klaw")
    from game.operate.worlds import Worlds
    from game.effect.rule import GameRule

    avant = len([noms for noms in journal if "Reveal_Main_Scheme" in noms])
    assert avant == 1, f"mise en place : {avant} question(s)"

    courante = Worlds.GetAllMainSchemes(monde)[0]
    assert courante.paper.card_id == "01116b", courante.paper.card_id
    courante.Advance(None, GameRule(courante))
    time.sleep(3)

    apres = len([noms for noms in journal if "Reveal_Main_Scheme" in noms])
    assert apres == 2, f"changement d'etape : {apres} question(s) au total"
    suivante = Worlds.GetAllMainSchemes(monde)[0]
    assert suivante.paper.card_id == "01117b", suivante.paper.card_id
    return "l'etape 2 pose la question elle aussi, et se retourne ensuite"


def cas_regle_publiee(game_dir, port):
    """La trame dit si la question est attendue, pour que le plateau le sache.

    ⚠ Ne rappelle PAS `ToDescriptor.World(monde)` a cote : cette fonction
    prend en verite `(world, event_name, sound_name)`, et un appel invente ici
    construirait un second descripteur qui ne prouverait rien sur celui
    envoye au client. Le vrai descripteur, c'est `monde.render.descriptor`
    (`WorldRender.PresentInternal` l'y range a chaque rendu) : c'est
    EXACTEMENT l'objet que `server_sync.handle_get_world` sert tel quel a
    `GET /world` (voir `data = controller.world.render.descriptor`).
    """
    _, monde, _ = monter_le_moteur(game_dir, port, ["confirm_main_scheme"])
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "confirm_main_scheme", None) is True, \
        "la trame ne publie pas confirm_main_scheme"
    return "la trame publie confirm_main_scheme"


CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "question_posee": cas_question_posee,
    "sans_drapeau": cas_sans_drapeau_aucune_question,
    "etape_suivante": cas_etape_suivante,
    "regle_publiee": cas_regle_publiee,
}


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
