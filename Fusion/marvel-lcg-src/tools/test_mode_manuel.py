"""Le mode manuel : le moteur se tait et ne fait plus que tenir l'etat.

Usage:
    ~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py \
        .game-src-par8 45200 [nom_du_cas]

Chaque cas tourne dans SON propre processus : le moteur est un singleton
global, impossible a reinitialiser proprement entre deux parties. On detourne
DeviceManager.DoGetInput pour repondre a la place du client, et on observe.
Meme gabarit que tools/test_manigance_face_a.py.
"""
import json
import os
import subprocess
import sys
import threading
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 120 questions suffisent largement a couvrir la mise en place et a atteindre
# le tour 1 (constate le 18/09/2026 : la mise en place a elle seule en pose
# une poignee). Au-dela, `pilote` ne repond plus jamais et pare le fil du jeu
# (voir plus bas) : c'est ce qui garde une execution a l'ordre de la minute.
PLAFOND_QUESTIONS = 120


def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man"):
    """Demarre une partie et rend (jeu, monde, journal_des_questions).

    ⚠ Contrairement au harnais de la manigance, celui-ci enchaine sur
    `GameLoop()` : tout le sujet du mode manuel est CE QUE FAIT LA BOUCLE, on
    ne peut pas s'arreter a la mise en place.
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
    derniere_signature = [None]
    repetitions = [0]

    def pilote(self, data, player_id=None, check=None):
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        noms = [o.get("name") for o in options if isinstance(o, dict)]
        journal.append(noms)

        # Anti-boucle : le Rhino porte "Enhanced Ivory Horn" (01100), une Hero
        # Action a cout (RRR) que ce pilote ne sait pas payer. L'option reste
        # "legale" (failure_reason vide) mais echoue a chaque fois, et le
        # moteur represente EXACTEMENT la meme liste d'options a l'identique -
        # constate le 18/09/2026, meme carte que le commentaire de
        # tools/test_manigance_face_a.py. Passe trois repetitions d'affilee de
        # la meme signature de question (le tuple des noms d'options), on
        # abandonne la premiere option (toujours la meme, toujours en echec)
        # pour la derniere : en pratique ca termine le tour et debloque la
        # partie.
        signature = tuple(noms)
        if signature == derniere_signature[0]:
            repetitions[0] += 1
        else:
            derniere_signature[0] = signature
            repetitions[0] = 1

        # Le plafond ne tue plus le processus : les cas ont besoin d'observer
        # le monde, pas d'une partie menee a son terme. Une fois atteint, le
        # pilote ne rend plus JAMAIS de reponse et dort par tranches de 0,5s
        # dans une boucle. Trois effets voulus : le fil du jeu reste "en
        # attente d'entree", il rend le GIL a chaque tranche, et l'attente
        # nominale de 20s redevient l'attente reelle. La version precedente
        # (plafond a 2000, parking en tranches de 3600s) laissait le pilote
        # continuer a jouer presque sans fin avant de parquer : le fil de fond,
        # jamais bloquant, affamait le GIL et retardait le reveil du fil
        # principal d'un facteur ~27x (~550s reels pour 20s nominales,
        # constate le 18/09/2026).
        if len(journal) > PLAFOND_QUESTIONS:
            while True:
                time.sleep(0.5)

        legales = [o for o in options
                   if isinstance(o, dict) and not o.get("failure_reason")]
        if not legales:
            return None
        o = legales[-1] if repetitions[0] > 3 else legales[0]
        cibles = [str(x) for x in (o.get("all_legal_targets") or [])]
        mini = (o.get("target_num_range") or [0, 0])[0]
        return json.dumps({"id": str(o.get("id", 0)),
                           "targets": cibles[:mini],
                           "resources": []})

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
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
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


def deposer(jeu, *commandes, drainer_soi_meme=False):
    """Depose des commandes comme le ferait /sandbox_command.

    `pilote` REMPLACE `DoGetInput` : plus personne n'appelle
    `DrainSandboxCommands` a sa place (c'etait le seul endroit qui le
    faisait, cf. `DeviceManager.DoGetInput` reel). `drainer_soi_meme` dit qui
    s'en charge :

    - Faux (par defaut) : on laisse le drainage a la boucle manuelle
      elle-meme (`World.ManualLoop`, tache 2). C'est exactement ce que le cas
      `commande_executee` doit prouver. Si ce harnais drainait ici a sa
      place, ce cas passerait au vert meme avec une boucle manuelle cassee -
      un faux temoin, le pire resultat possible.
    - Vrai : pour les cas de CONTROLE en automatique (le pilote roule tout
      seul, personne d'autre ne drainera jamais). Le harnais execute alors
      les commandes lui-meme, depuis le fil de test. Precedent deja pris par
      tools/test_manigance_face_a.py, qui manipule le monde depuis ce meme
      fil (`courante.Advance(...)`, cas_etape_suivante).
    """
    from game.puzzle import PuzzleHelper
    gestionnaire = jeu.controller_manager.device_manager
    gestionnaire.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
    gestionnaire.QueueSandboxCommands(list(commandes))
    if drainer_soi_meme:
        gestionnaire.DrainSandboxCommands()
    time.sleep(3)


def id_du_vilain(monde):
    from game.operate.worlds import Worlds
    vilains = Worlds.GetAllVillains(monde)
    assert vilains, "aucun vilain sur la table"
    return vilains[0].card.object_id


def cas_drapeau_pose(game_dir, port):
    """Le drapeau existe, la liste de regles l'allume, et la trame le publie."""
    _, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert bool(monde.rule.mode_manuel) is True, \
        "la regle mode_manuel n'a pas ete posee"
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "mode_manuel", None) is True, \
        "la trame ne publie pas mode_manuel"
    return "le drapeau mode_manuel est pose et publie"


def cas_moteur_muet(game_dir, port):
    """Apres la mise en place, plus rien ne bouge tout seul.

    Le temoin qui compte est le REFUS d'avancer : on regarde que le journal des
    questions ne grossit plus, et que le compteur de tours reste a zero. Un
    moteur qui conduit encore ferait les deux.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True, "la boucle manuelle n'a pas demarre"
    avant = len(journal)
    time.sleep(8)
    assert len(journal) == avant, \
        f"le moteur a repose {len(journal) - avant} question(s) apres la mise en place"
    assert monde.round_id == 0, \
        f"le moteur a demarre un tour tout seul : round_id={monde.round_id}"
    return "le moteur se tait apres la mise en place"


def cas_automatique_avance(game_dir, port):
    """Le controle : SANS la regle, le moteur conduit toujours.

    Sans ce cas, `cas_moteur_muet` passerait aussi sur un moteur casse qui ne
    demarre pas du tout.

    ⚠ Pas de fenetre de croissance ici (constate le 18/09/2026) : au-dela de
    `PLAFOND_QUESTIONS`, `pilote` cesse de repondre et le journal peut ne plus
    grossir dans une partie parfaitement normale. Le temoin est plutot « le
    moteur a conduit » : au moins un tour entame, et au moins une question
    posee.
    """
    _, monde, journal = monter_le_moteur(game_dir, port, [])
    assert getattr(monde, "manuel_actif", False) is False
    assert monde.round_id >= 1, \
        f"le moteur automatique n'a pas demarre de tour : round_id={monde.round_id}"
    assert len(journal) > 0, \
        "le moteur automatique n'a pose aucune question : le harnais est casse"
    return "sans la regle, le moteur conduit toujours"


def cas_commande_executee(game_dir, port):
    """La boucle manuelle execute bien ce qu'on lui depose.

    C'est la preuve que `PuzzleHelper.Exec` tourne hors de `DoGetInput` : le
    fil du jeu dort dans la boucle manuelle, pas dans une attente de reponse.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"la commande n'a pas ete executee : degats={carte.face.GetLostHealth()}"
    return "la boucle manuelle execute les commandes deposees"


CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "moteur_muet": cas_moteur_muet,
    "automatique_avance": cas_automatique_avance,
    "commande_executee": cas_commande_executee,
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
            cwd=RACINE, capture_output=True, text=True, timeout=300)
        verdict = "VERT" if fils.returncode == 0 else "ROUGE"
        print(f"{verdict} : {nom}")
        if fils.returncode != 0:
            print(fils.stdout[-3000:])
            print(fils.stderr[-3000:])
            sys.exit(1)


if __name__ == "__main__":
    if "--fils" in sys.argv:
        nom = sys.argv[3]
        # os._exit() dans les DEUX branches, jamais un retour normal de
        # l'interpreteur : le fil de fond du jeu est un daemon qui peut etre
        # PARQUE (plafond de `pilote` atteint, cf. plus haut) au moment ou ce
        # cas se termine. Un arret normal de Python (celui qu'on aurait sur
        # une exception non rattrapee, p.ex. l'AttributeError attendue en
        # ROUGE) declenche `threading._shutdown()` et les hooks `atexit` de
        # `concurrent.futures`, qui tentent de joindre les fils de travail du
        # moteur - et restent bloques indefiniment tant que le fil de fond
        # (parque ou non) ne rend pas la main. Constate le 18/09/2026 : sans
        # ce garde-fou, un cas ROUGE par exception ne se termine JAMAIS, meme
        # apres avoir imprime la bonne erreur.
        try:
            resultat = CAS[nom](sys.argv[1], int(sys.argv[2]))
        except BaseException:
            import traceback
            traceback.print_exc()
            os._exit(1)
        print(resultat)
        os._exit(0)
    main()
