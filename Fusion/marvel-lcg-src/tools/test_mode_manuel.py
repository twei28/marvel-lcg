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


def id_du_sbire(monde, code):
    """Retrouve en jeu la carte de code imprime `code` (ex. "01103").

    Ne passe pas par le nom affiche (localisation) : on relit
    `paper.card_id` sur chaque face en jeu, comme le fait deja
    `RunPuzzle.FindOrCreateFace` pour les cartes dont la face a change.
    """
    for object_id, objet in monde.object_manager.card_dict.items():
        face = objet.face
        if face is not None and face.IsInPlay() and \
                getattr(getattr(face, "paper", None), "card_id", None) == code:
            return object_id
    raise AssertionError(f"sbire {code} introuvable en jeu")


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
    assert monde.manuel_actif is True, "la boucle manuelle n'a pas demarre"
    assert monde.round_id == 0, \
        f"le moteur a demarre un tour tout seul : round_id={monde.round_id}"
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"la commande n'a pas ete executee : degats={carte.face.GetLostHealth()}"
    return "la boucle manuelle execute les commandes deposees"


def cas_aucun_declenchement(game_dir, port):
    """Une capacite de carte posee sur le vilain NE SE DECLENCHE PAS.

    ⚠ Deux temoins essayes et rejetes AVANT celui-ci (18/09/2026), par
    instrumentation directe du moteur (prints temporaires dans
    `EventManager.BroadcastMessage`, `Unit2.OnBeDefeated` et
    `Faces.DiscardAll`, retires ensuite) :

    1. Le vilain (brief d'origine) : Rhino a DEUX cartes (01094 puis 01095,
       cf. data/scenarios/rhino.json). Le vaincre fait PROGRESSER vers la
       seconde sans finir la partie, ET `Villain.OnBeDefeated` appelle
       `self.Advance(...)` en APPEL DIRECT, jamais via `Message.Send()`.
    2. Un sbire pose par le puzzle (Shocker, 01103) : meme souci. Constate a
       l'execution : `Unit2.OnBeDefeated` appelle `Faces.DiscardAll([self],
       by_effect)` en APPEL DIRECT des qu'un unit a 0 PV, JAMAIS via
       `Message.Send()`. La porte (qui ne ferme que `BroadcastMessage` et
       `BroadcastStackMessage`, exactement comme demande) ne voit donc jamais
       passer ce retrait : le sbire quitte la table MEME quand la porte est
       fermee (`manuel_actif=True` au moment de l'appel, verifie par log).
       Le corollaire du brief (« un sbire a zero point de vie n'est plus
       defausse tout seul ») ne tient donc PAS avec cette seule porte -
       signale au demandeur, pas bricole en douce.

    Temoin retenu, qui EVITE cette chaine d'appels directs : « Armored Rhino
    Suit » (01098, cf. src/cards/pack/core/rhino/01098.py). C'est une
    authentique CAPACITE DE CARTE (`AbilityFactory.WhenUnitWouldTakeDamage`,
    `ForcedInterrupt`) qui, quand elle est en jeu sur Rhino, PREVIENT les
    degats infliges a Rhino et les reporte en compteurs sur elle-meme. Ce
    genre de capacite est resolue par le chemin normal des effets locaux DANS
    `BroadcastMessage` (`find_local_effects`, priorites de resolution) : pas
    d'appel direct connu qui la contourne. Elle se pose SEULE (« AttachToFace
    WhenPutIntoPlay ») des qu'on la met en jeu pres de Rhino, et son
    declenchement n'attend aucune decision de joueur.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    carte = monde.object_manager.card_dict[vilain]
    perdu_avant = carte.face.GetLostHealth()
    deposer(jeu, "Puzzle.PutIntoPlay('01098')")
    # L'entree en jeu (attache a Rhino) prend une vingtaine de secondes de
    # traitement reel une fois la commande deposee (constate le 18/09/2026,
    # meme delai que la progression du vilain) : sans cette attente, les
    # degats ci-dessous arrivent AVANT que la capacite ne soit attachee, ce
    # qui fausserait ce cas dans les DEUX sens.
    time.sleep(20)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    delta = carte.face.GetLostHealth() - perdu_avant
    assert delta == 3, \
        ("les degats sur Rhino ont ete detournes : la capacite d'Armored "
         f"Rhino Suit a agi malgre le mode manuel (delta={delta})")
    return ("aucun declenchement en manuel : les degats frappent Rhino tels "
            "quels, la capacite de la suit d'armure ne part pas")


def cas_declenchement_en_automatique(game_dir, port):
    """Le controle : la MEME sequence, sans la regle, voit la capacite agir.

    Sans ce cas, `cas_aucun_declenchement` passerait aussi sur une sequence de
    commandes qui n'aurait jamais pose la suit d'armure, ou sur une capacite
    qui n'existe pas / ne fait rien.

    ⚠ `drainer_soi_meme=True` (correction du 18/09/2026, brief initial faux) :
    en automatique, `pilote` REMPLACE `DoGetInput`, qui etait le seul endroit
    a appeler `DrainSandboxCommands`. Sans ce drainage explicite, personne ne
    depile jamais les commandes deposees et ce cas de controle resterait
    bloque, pour la mauvaise raison.

    ⚠ Temoin corrige (18/09/2026, cf. `cas_aucun_declenchement` pour le detail
    des deux temoins rejetes) : le brief supposait que 999 degats sur le
    VILAIN terminent la partie (`is_game_over`). Remplace par la capacite
    d'« Armored Rhino Suit » (01098), qui evite la chaine d'appels directs de
    la defaite (`Death` / `OnBeDefeated` / `Faces.DiscardAll` /
    `Villain.Advance`), non couverte par cette porte.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    vilain = id_du_vilain(monde)
    carte = monde.object_manager.card_dict[vilain]
    # ⚠ Delta, pas valeur absolue (constate le 18/09/2026) : en automatique,
    # le heros pilote continue de jouer PENDANT le cas (il attaque Rhino
    # normalement). `GetLostHealth()` en fin de cas contient donc AUSSI les
    # degats de ce combat ordinaire, sans rapport avec ce cas.
    perdu_avant = carte.face.GetLostHealth()
    deposer(jeu, "Puzzle.PutIntoPlay('01098')", drainer_soi_meme=True)
    # Cf. cas_aucun_declenchement : meme delai reel d'attache a attendre ici.
    time.sleep(20)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)", drainer_soi_meme=True)
    delta = carte.face.GetLostHealth() - perdu_avant
    assert delta == 0, \
        ("en automatique, Armored Rhino Suit aurait du absorber les degats "
         f"deposes par ce cas (delta={delta})")
    return ("en automatique, la meme sequence voit la capacite de la suit "
            "d'armure absorber les degats de Rhino")


def cas_sbire_reste_en_jeu(game_dir, port):
    """Un sbire (une UNITE, pas une capacite de carte) a zero PV reste en jeu.

    Ronde de correction 1 (18/09/2026) : `cas_aucun_declenchement` prouve
    qu'aucune CAPACITE DE CARTE ne part, mais pas que la defaite
    automatique elle-meme est bloquee - `Death` -> `Defeated` ->
    `WhenBeDefeated` -> `OnBeDefeated` -> `Faces.DiscardAll` s'enchainent en
    appel Python direct, jamais via `Message.Send()` (cf. rapport de
    tache 3). C'est le temoin explicitement demande par le donneur d'ordre
    pour couvrir ce trou : Shocker (01103) pose par le puzzle, reduit a 999
    degats, doit rester `IsInPlay()` en mode manuel.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    deposer(jeu, "Puzzle.PutIntoPlay('01103')")
    sbire = id_du_sbire(monde, "01103")
    carte = monde.object_manager.card_dict[sbire]
    deposer(jeu, f"Puzzle.Damage({sbire}, 999)")
    time.sleep(10)
    assert monde.is_game_over is False, \
        "le moteur a declare la partie finie : un effet de regle est parti"
    assert carte.face.IsInPlay(), \
        "le sbire a quitte la table tout seul : la defaite automatique n'est pas bloquee"
    return "le sbire a zero PV reste en jeu en mode manuel : la defaite automatique ne part pas"


def cas_sbire_vaincu_en_automatique(game_dir, port):
    """Le controle : la MEME sequence, sans la regle, vainc bien le sbire.

    Sans ce cas, `cas_sbire_reste_en_jeu` passerait aussi sur une sequence de
    commandes qui n'aurait jamais pose ou jamais blesse le sbire.

    `drainer_soi_meme=True` : meme raison que dans `cas_declenchement_en_automatique`
    (en automatique, `pilote` remplace `DoGetInput`, seul appelant de
    `DrainSandboxCommands`).
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    deposer(jeu, "Puzzle.PutIntoPlay('01103')", drainer_soi_meme=True)
    sbire = id_du_sbire(monde, "01103")
    carte = monde.object_manager.card_dict[sbire]
    deposer(jeu, f"Puzzle.Damage({sbire}, 999)", drainer_soi_meme=True)
    time.sleep(10)
    assert carte.face.IsInPlay() is False, \
        "en automatique, 999 degats auraient du faire quitter le sbire de la table"
    return "en automatique, la meme sequence fait quitter le sbire de la table"


CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "moteur_muet": cas_moteur_muet,
    "automatique_avance": cas_automatique_avance,
    "commande_executee": cas_commande_executee,
    "aucun_declenchement": cas_aucun_declenchement,
    "declenchement_en_automatique": cas_declenchement_en_automatique,
    "sbire_reste_en_jeu": cas_sbire_reste_en_jeu,
    "sbire_vaincu_en_automatique": cas_sbire_vaincu_en_automatique,
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
