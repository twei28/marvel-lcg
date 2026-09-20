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


def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man",
                     sauvegarde=None, avant_reponse=None):
    """Demarre une partie et rend (jeu, monde, journal_des_questions).

    ⚠ Contrairement au harnais de la manigance, celui-ci enchaine sur
    `GameLoop()` : tout le sujet du mode manuel est CE QUE FAIT LA BOUCLE, on
    ne peut pas s'arreter a la mise en place.

    `avant_reponse` (tache 8 bis), s'il est fourni, est appele avec `jeu`
    juste avant chaque reponse du pilote -- donc a chaque question posee,
    mise en place comprise. C'est le seul point d'observation qui voit l'etat
    du monde PENDANT la mise en place : `monter_le_moteur` ne rend la main
    qu'apres `time.sleep(20)`, bien apres que la boucle manuelle a pris la
    main.
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

        if avant_reponse is not None:
            avant_reponse(jeu)

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

    if sauvegarde:
        # Une partie RECHARGEE : la scene porte deja ses regles et ses gestes.
        scene = SceneLoader.Load(sauvegarde)
        assert scene, f"sauvegarde illisible : {sauvegarde}"
    else:
        with open(_chemin_json("Campaign", scenario)) as f:
            campagne = f.read()
        with open(_chemin_json("Hero", heros)) as f:
            hero = f.read()
        scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, regles, {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        # Une partie peut REDEMARRER sur place : c'est ce que fait
        # `LoadScene`, donc ce que fait l'annulation d'un geste. `GameSetup`
        # appelle `state.ResetStartState()`, donc `start_state` est vide
        # pendant qu'on joue et repose des qu'une scene est rechargee.
        #
        # ⚠ CORRECTION (tache 7, ronde de correction 2, 19/09/2026) : la
        # version precedente arretait ce fil des que `GameLoop()` rendait la
        # main SANS que `start_state.state` soit deja repose - exactement ce
        # qui arrive quand la partie se termine NATURELLEMENT (`Puzzle.Win`/
        # `Lose`, ni annulation ni sortie), puisque personne n'a encore
        # appele `LoadScene`. Constate en ecrivant `cas_annulation_fin_declaree`
        # ci-dessous : le fil mourait avant meme que l'annulation n'arrive,
        # et `jeu.world` restait pour toujours l'ancien monde, fini. Aucun
        # cas existant ne pouvait le voir : aucun ne declare de VRAIE fin de
        # partie avant d'annuler.
        #
        # Le correctif copie l'idiome de la PRODUCTION (`Game.GameRun`,
        # `game/game.py`) au lieu d'en inventer un autre : apres un
        # `GameLoop()`, une reprise DEJA demandee (`start_state.state` pose,
        # ex. par une annulation en vol) relance tout de suite : sinon, le
        # fil attend sur `state.WaitUntilGameStart()` - LA MEME primitive
        # que le serveur reel, reveillee par le `condition.NotifyAll()` de
        # `SetStartState` (`game_state.py`) quand une annulation FUTURE
        # arrive. `threading.Condition.wait_for` verifie son predicat AVANT
        # de bloquer : un reveil deja arrive avant l'entree dans l'attente
        # n'est donc jamais perdu.
        import traceback
        while True:
            try:
                if jeu.GameSetup():
                    jeu.GameLoop()
            except BaseException:
                traceback.print_exc()
                return
            if jeu.state.start_state.state:
                continue
            jeu.state.SetRunningState(False)
            jeu.state.WaitUntilGameStart()

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


def basculer_pause(jeu, actif, qui=""):
    """Bascule la pause manuelle comme le ferait POST /manuel_pause.

    Appelle directement `World.BasculerPauseManuelle`, EXACTEMENT ce que fait
    la route : ne touche rien d'autre au monde depuis cet appel, tache 1
    oblige (cf. le commentaire en tete de `engine/device/manager/base.py`).
    Le court sommeil laisse au fil du jeu, reveille par l'appel, le temps
    d'en tirer les consequences avant l'assertion suivante -- meme idiome que
    `deposer` ci-dessus.

    `qui` (tache 3, optionnel) : le pseudo transmis par la route, relaye tel
    quel a `BasculerPauseManuelle`.
    """
    resultat = jeu.world.BasculerPauseManuelle(actif, qui)
    time.sleep(2)
    return resultat


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


def cas_manuel_actif_pas_avant_la_boucle(game_dir, port):
    """`manuel_actif` de la trame distingue la mise en place de la boucle.

    La REGLE (`mode_manuel`) est vraie des la creation de la partie ; l'ETAT
    (`manuel_actif`) ne doit devenir vrai qu'une fois la boucle manuelle
    entree, apres la mise en place -- sinon le plateau, qui se regle sur cet
    etat pour masquer les couches du moteur, masquerait deja le panneau qui
    pose le mulligan PENDANT la mise en place (tache 8 bis).

    Temoin : au moment de la toute PREMIERE question posee (donc pendant la
    mise en place, avant `World.ManualLoop`), le descripteur doit porter
    `manuel_actif` a FAUX. Une fois la partie retombee dans la boucle
    manuelle (silence retabli, `monde` rendu par `monter_le_moteur`), il doit
    porter `manuel_actif` a VRAI.
    """
    manuel_actif_vu = []

    def observateur(jeu):
        manuel_actif_vu.append(bool(jeu.world.render.descriptor.manuel_actif))

    _, monde, journal = monter_le_moteur(
        game_dir, port, ["mode_manuel"], avant_reponse=observateur)

    assert journal, "aucune question posee : la mise en place n'a pas eu lieu"
    assert manuel_actif_vu, "l'observateur n'a jamais ete appele"
    assert manuel_actif_vu[0] is False, (
        "le descripteur porte deja manuel_actif a vrai a la toute premiere "
        "question (donc pendant la mise en place) : le panneau qui la pose "
        "serait masque, et la partie resterait bloquee pour toujours"
    )
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "manuel_actif", None) is True, \
        "la trame ne publie pas manuel_actif une fois la boucle manuelle entree"
    return "manuel_actif distingue la mise en place (faux) de la boucle manuelle (vrai)"


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
    """Une capacite de carte DEJA ATTACHEE au vilain NE SE DECLENCHE PAS.

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
    `ForcedInterrupt`) qui, quand elle est en jeu ATTACHEE a Rhino, PREVIENT
    les degats qui lui sont infliges et les reporte en compteurs sur
    elle-meme. Ce genre de capacite est resolue par le chemin normal des
    effets locaux DANS `BroadcastMessage` (`find_local_effects`, priorites
    de resolution) : pas d'appel direct connu qui la contourne.

    ⚠ CORRECTIF DE PREMISE (revue finale du 18/09/2026, constat 7) : la
    version precedente de ce cas comptait sur la PROPRE capacite d'attache
    de la carte (« AttachToFace WhenPutIntoPlay ») pour la poser sur Rhino
    apres un simple `PutIntoPlay`. Mesure a l'execution : cette capacite
    d'attache est ELLE AUSSI un declenchement, donc ELLE AUSSI bloquee par
    la porte du silence - en mode manuel, `PutIntoPlay('01098')` seul ne
    l'attache JAMAIS a Rhino. L'assertion finale etait donc vraie, mais pour
    la mauvaise raison : elle prouvait que l'entree en jeu ne s'attache pas
    toute seule (deja couvert par `cas_deplacement_libre` et consorts), pas
    qu'une capacite DEJA EN PLACE reste muette - ce que ce cas pretend
    demontrer. Corrige en creant la suit A PART (`Puzzle.CreateCard`, comme
    `cas_attache`) puis en l'attachant A LA MAIN (`Puzzle.Attach`, tache 4),
    sans jamais passer par sa propre capacite d'attache ; et en VERIFIANT
    cette attache avant de mesurer quoi que ce soit : la premisse n'est plus
    supposee, elle est constatee.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    carte = monde.object_manager.card_dict[vilain]
    perdu_avant = carte.face.GetLostHealth()

    deposer(jeu, "Puzzle.CreateCard('01098')")
    suit = max(monde.object_manager.card_dict)
    deposer(jeu, f"Puzzle.Attach({suit}, {vilain})")

    # PREMISE VERIFIEE, PAS SUPPOSEE : sans ce controle, l'assertion finale
    # serait vraie meme si l'attache manuelle avait elle-meme echoue en
    # silence, ce qui ne prouverait plus rien sur une capacite deja en
    # place.
    suit_face = monde.object_manager.card_dict[suit].face
    assert suit_face in carte.face.GetInventoryDeck().GetAll(), \
        (f"la suit d'armure n'est pas dans l'inventaire de Rhino : ce cas ne "
         f"peut rien prouver sur une capacite deja en place "
         f"(IsFaceUp={suit_face.IsFaceUp()}, IsInPlay={suit_face.IsInPlay()})")

    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    delta = carte.face.GetLostHealth() - perdu_avant
    assert delta == 3, \
        ("les degats sur Rhino ont ete detournes : la capacite d'Armored "
         f"Rhino Suit, pourtant deja attachee, a agi malgre le mode manuel "
         f"(delta={delta})")
    return ("aucun declenchement en manuel : une capacite deja attachee a "
            "Rhino ne part pas, les degats le frappent tels quels")


def cas_declenchement_en_automatique(game_dir, port):
    """Le controle : sans la regle, la capacite agit des le seul PutIntoPlay.

    Sans ce cas, `cas_aucun_declenchement` passerait aussi sur une sequence de
    commandes qui n'aurait jamais pose la suit d'armure, ou sur une capacite
    qui n'existe pas / ne fait rien.

    ⚠ Sequence volontairement PLUS COURTE que `cas_aucun_declenchement`
    depuis le correctif du constat 7 (revue finale du 18/09/2026) : ici,
    `PutIntoPlay` seul suffit a attacher la suit (sa propre capacite
    d'attache tourne normalement, rien ne la bloque), donc pas besoin de
    l'explicite `Puzzle.Attach` que le cas manuel doit s'imposer. Les deux
    cas visent la meme chose - une capacite deja en place sur Rhino - par
    deux chemins d'attache differents, chacun le seul qui fonctionne dans
    son mode.

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


def cas_deplacement_libre(game_dir, port):
    """N'importe quelle carte va dans n'importe quelle pile, regles ou pas.

    On envoie une carte de la MAIN du heros dans le DECK RENCONTRE : aucune
    regle du jeu ne permet ca. C'est precisement le sujet.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    from game.operate.worlds import Worlds
    avant = len(Worlds.GetEncounterDeckCards(monde))

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'EncounterDeck')")

    apres = len(Worlds.GetEncounterDeckCards(monde))
    assert apres == avant + 1, \
        f"le deck rencontre devait passer de {avant} a {avant + 1}, il vaut {apres}"
    return "une carte de la main est allee dans le deck rencontre"


def cas_melange(game_dir, port):
    """Melanger une pile change son ordre, sans rien perdre."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    avant = [c.card.object_id for c in joueur.player_deck.GetAll()]
    assert len(avant) > 10, f"deck trop court pour un melange : {len(avant)}"

    deposer(jeu, "Puzzle.Shuffle('PlayerDeck')")

    apres = [c.card.object_id for c in joueur.player_deck.GetAll()]
    assert sorted(apres) == sorted(avant), "le melange a perdu ou ajoute des cartes"
    assert apres != avant, "le melange n'a rien change a l'ordre"
    return "le deck du joueur a ete melange sans rien perdre"


def cas_ecart(game_dir, port):
    """`AsideDeck` doit pointer sur la VRAIE pile des cartes ecartees.

    Ronde de correction 1 (18/09/2026) : `player.set_aside_deck` est un faux
    ami herite du moteur de base, il vaut `additional_discard_pile`
    (`DeckType.AdditionalDiscardPile`), pas `DeckType.AsideDeck`. La vraie
    pile typee `AsideDeck` est `player.set_aside_nemesis_sets`. Ce cas verifie
    a la fois l'arrivee dans la bonne pile ET l'absence dans le faux ami :
    une carte qui atterrit ailleurs sans erreur est exactement le defaut que
    cette table doit empecher.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    avant_ecart = len(joueur.set_aside_nemesis_sets.GetAll())
    avant_faux_ami = len(joueur.set_aside_deck.GetAll())

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'AsideDeck')")

    apres_ecart = len(joueur.set_aside_nemesis_sets.GetAll())
    apres_faux_ami = len(joueur.set_aside_deck.GetAll())
    assert apres_ecart == avant_ecart + 1, \
        (f"la pile des cartes ecartees devait passer de {avant_ecart} a "
         f"{avant_ecart + 1}, elle vaut {apres_ecart}")
    assert apres_faux_ami == avant_faux_ami, \
        (f"la carte a atterri dans le faux ami additional_discard_pile : "
         f"{avant_faux_ami} -> {apres_faux_ami}")
    return "AsideDeck envoie bien vers la pile des cartes ecartees, pas vers le faux ami"


def cas_ecart_scenario(game_dir, port):
    """`AsideScenario` doit remplir `world.aside_deck`, pas le set nemesis du heros.

    Tache 4 bis (19/09/2026) : `ZONES_MONDE` (`game/puzzle/puzzle.py`) n'avait
    aucune entree pour les mises de cote du SCENARIO. `_ZoneParNom` retombait
    donc sur `ZONES_JOUEUR['AsideDeck']`, c'est-a-dire `set_aside_nemesis_sets`
    du heros : une carte envoyee vers "les mises de cote du scenario" partait
    silencieusement dans le tas nemesis du heros. Ce cas verifie a la fois
    l'arrivee dans `world.aside_deck` ET l'absence dans le set nemesis : le
    second controle est le plus important, c'est lui qui prouve qu'on ne
    retombe plus sur la pile du joueur.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    avant_scenario = len(monde.aside_deck.GetAll())
    avant_nemesis = len(joueur.set_aside_nemesis_sets.GetAll())

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'AsideScenario')")

    apres_scenario = len(monde.aside_deck.GetAll())
    apres_nemesis = len(joueur.set_aside_nemesis_sets.GetAll())
    assert apres_scenario == avant_scenario + 1, \
        (f"les mises de cote du scenario devaient passer de {avant_scenario} "
         f"a {avant_scenario + 1}, elles valent {apres_scenario}")
    assert apres_nemesis == avant_nemesis, \
        (f"la carte a atterri dans le set nemesis du heros au lieu des mises "
         f"de cote du scenario : {avant_nemesis} -> {apres_nemesis}")
    return "AsideScenario envoie vers world.aside_deck, pas vers le set nemesis du heros"


def cas_dessous_sans_ordre(game_dir, port):
    """`position='Bottom'` sur une pile SANS ordre depose quand meme la carte.

    Ronde de correction 1 (18/09/2026) : `Card.MoveToBottom` ne fait rien et
    rend `False` en silence des que la pile visee n'est pas un deck ordonne
    (`DeckType.is_deck`/`is_dealt_encounter`). Sur `AlliesArea` (pas un deck
    ordonne), demander le dessous ne doit PAS laisser la carte immobile : le
    modificateur perd son sens, la carte doit quand meme arriver dans la
    pile par le chemin normal.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    avant = len(joueur.allies.GetAll())

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'AlliesArea', 'Bottom')")

    apres = len(joueur.allies.GetAll())
    assert apres == avant + 1, \
        f"la zone des allies devait passer de {avant} a {avant + 1}, elle vaut {apres}"
    return "position='Bottom' sur une pile sans ordre depose quand meme la carte dedans"


def cas_geste_enregistre(game_dir, port):
    """Un geste accepte entre dans la scene, donc dans la sauvegarde."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    gestes = jeu.session.scene.manuel_commands
    assert gestes == [f"Puzzle.Damage({vilain}, 3)"], \
        f"la scene n'a pas retenu le geste : {gestes}"
    return "le geste est enregistre dans la scene"


def cas_aller_retour(game_dir, port):
    """Geste, sauvegarde, rechargement : l'etat est identique.

    C'est LE cas qui leve le dernier doute du cadrage, celui sur la
    reproductibilite des identifiants d'objets : le rejeu vise la carte par son
    identifiant, et doit retomber sur la meme.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")

    # Nom NU, pas un chemin absolu (ecart au brief, constate le 18/09/2026) :
    # `SceneLoader.Load` resout par `FileManager.FindJsonPath('Replay', ...)`,
    # qui formate mal un chemin absolu SANS lettre de lecteur (FormatPath lui
    # colle un './' devant, ce qui sous WSL transforme '/mnt/c/...' en chemin
    # RELATIF invalide - une carte de reference n'existe que sous Windows,
    # ou `IsDrivePath` court-circuite ce meme code avant d'y arriver). On
    # ecrit et on relit un nom nu depuis la racine du dossier de jeu, la ou
    # `monter_le_moteur` a deja fait chdir dans les deux process (parent et
    # fils) : aucun besoin d'un chemin absolu.
    nom = "manuel-aller-retour.json"
    ecrit = jeu.session.SaveScene(name=nom, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    env["MC_VILAIN"] = str(vilain)
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_sauvegarde", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-3000:]}\n{fils.stderr[-3000:]}"
    return "aller-retour de sauvegarde : l'etat est identique"


def cas_relire_sauvegarde(game_dir, port):
    """Le fils de `cas_aller_retour` : il recharge et verifie les degats."""
    chemin = os.environ["MC_SAUVEGARDE"]
    vilain = int(os.environ["MC_VILAIN"])
    _, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin)
    assert bool(monde.rule.mode_manuel) is True, \
        "la sauvegarde a perdu la regle mode_manuel"
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"apres rechargement : degats={carte.face.GetLostHealth()}, attendu 3"
    return "la partie rechargee porte bien le geste"


def cas_annulation(game_dir, port):
    """Ctrl+Z : le dernier geste part, les precedents restent.

    Deux gestes, 3 puis 4 degats. Apres annulation il doit rester 3, et un seul
    geste dans la scene. Le monde est RECONSTRUIT par le rechargement : on
    relit `jeu.world`, jamais la reference d'avant.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    deposer(jeu, f"Puzzle.Damage({vilain}, 4)")
    carte = monde.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 7, \
        f"avant annulation : degats={carte.face.GetLostHealth()}, attendu 7"

    assert jeu.session.AnnulerDernierGeste() is True
    time.sleep(20)

    scene = jeu.session.scene
    assert len(scene.manuel_commands) == 1, \
        f"il devait rester 1 geste, il en reste {len(scene.manuel_commands)}"
    monde2 = jeu.world
    carte2 = monde2.object_manager.card_dict[vilain]
    assert carte2.face.GetLostHealth() == 3, \
        f"apres annulation : degats={carte2.face.GetLostHealth()}, attendu 3"
    return "l'annulation retire le dernier geste et garde les precedents"


def cas_annulation_ne_redemande_pas(game_dir, port):
    """Temoin honnete du constat 1 (revue finale du 18/09/2026).

    `cas_annulation`, juste au-dessus, ne peut PAS voir ce defaut : son
    pilote repond aux memes questions, dans le meme ordre, avec la meme
    graine - l'etat final de la carte est donc identique que la mise en
    place soit REJOUEE EN SILENCE depuis l'historique (correctif :
    `GameSession.AnnulerDernierGeste` appelle `Game.ApplyHistoryInput` avant
    de recharger, comme le fait deja `GameSession.Undo`) ou REDEMANDEE au
    pilote (bug : `scene.inputs` reste vide, `LoadScene` -> `GameSetup`
    fait tout rejouer depuis le debut).

    La difference se lit dans le JOURNAL DES QUESTIONS, pas dans les degats
    sur la carte. Quand `scene.inputs` est repeuplee, la reprise saute les
    etapes deja jouees en mode "skip" (`Controller.ChoiceOne`,
    `engine/controller/controller.py:269-276`) sans jamais rappeler
    `DeviceManager.DoGetInput` : le journal ne bouge plus pour la mise en
    place. Sans le correctif, chaque question de la mise en place est
    reposee a `pilote`, et le journal grossit d'autant.
    """
    jeu, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    avant_geste = len(journal)
    assert avant_geste > 0, \
        ("la mise en place n'a pose aucune question a `pilote` : ce temoin "
         "ne peut rien prouver sans au moins un choix (mulligan) pendant la "
         "mise en place")

    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    avant_annulation = len(journal)

    assert jeu.session.AnnulerDernierGeste() is True
    time.sleep(20)

    apres = len(journal)
    assert apres == avant_annulation, \
        (f"l'annulation a repose {apres - avant_annulation} question(s) a "
         "pilote : la mise en place a ete REDEMANDEE au lieu d'etre rejouee "
         "depuis l'historique (scene.inputs)")
    return "l'annulation ne redemande pas la mise en place : l'historique est rejoue en silence"


def cas_annulation_fin_declaree(game_dir, port):
    """Ctrl+Z defait aussi une fin de partie declaree (tache 7, ronde de
    correction 2, cote plateau).

    Le harnais React (`ui-app/src/board/CoucheTriche.test.tsx`) simule le
    reseau et repond toujours "d'accord" : il prouve seulement qu'aucune
    garde COTE CLIENT n'empeche le Ctrl+Z apres `Puzzle.Win()`/`Lose()` -
    utile, mais ca laisserait passer un refus qu'on ajouterait un jour cote
    MOTEUR (un 409 sur partie finie, par exemple) sans que rien ne bouge
    dans ce harnais-la puisque le simulacre repond toujours oui. La vraie
    promesse ("ta partie revient", ecrite dans `FinManuelle.tsx`) ne se
    prouve que la ou la partie revient reellement : ici.

    Meme gabarit que `cas_annulation`, juste au-dessus : le monde est
    RECONSTRUIT par l'annulation, on relit `jeu.world`, jamais la reference
    d'avant.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.is_game_over is False, \
        "la partie est donnee pour finie avant meme d'avoir declare Win()"

    deposer(jeu, "Puzzle.Win()")
    assert monde.is_game_over is True, \
        "Puzzle.Win() n'a pas termine la partie : rien a annuler"

    assert jeu.session.AnnulerDernierGeste() is True
    time.sleep(20)

    monde2 = jeu.world
    assert monde2.is_game_over is False, \
        "apres annulation, la partie est toujours donnee pour finie"
    assert monde2.manuel_actif is True, \
        "apres annulation, la boucle manuelle n'a pas repris : la partie ne revient pas"
    return "le Ctrl+Z defait une fin de partie declaree : la partie n'est plus finie et reprend"


def cas_attache(game_dir, port):
    """Attach pose bien l'amelioration SUR la carte visee.

    `CreateCard` place la carte A PART (`aside_deck`), sans l'attacher a
    rien : c'est `Attach`, seul, qui doit la faire arriver dans l'inventaire
    de la cible. On vise le vilain, exactement la pile qu'« Armored Rhino
    Suit » (01098) rejoint normalement via sa propre capacite
    (`cas_aucun_declenchement`) - ici on l'y met a la main, sans passer par
    aucune capacite.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)
    carte_vilain = monde.object_manager.card_dict[vilain]
    avant = len(carte_vilain.face.GetInventoryDeck().GetAll())

    deposer(jeu, "Puzzle.CreateCard('01098')")
    # La carte creee est la DERNIERE entree du dictionnaire des objets :
    # aucune autre commande n'a tourne depuis (meme principe que
    # `cas_geste_enregistre`, qui vise deja les cartes par cet identifiant).
    nouvelle = max(monde.object_manager.card_dict)

    deposer(jeu, f"Puzzle.Attach({nouvelle}, {vilain})")

    apres = len(carte_vilain.face.GetInventoryDeck().GetAll())
    assert apres == avant + 1, \
        f"l'inventaire du vilain devait passer de {avant} a {avant + 1}, il vaut {apres}"
    return "Attach pose l'amelioration sur la carte visee"


def cas_engagement(game_dir, port):
    """Engage engage un sbire, puis le meme geste le desengage.

    `Puzzle.PutIntoPlay` engage DEJA le sbire automatiquement
    (`Minion.OnPutIntoPlay` -> `EngagePlayer`, un appel direct comme celui
    documente dans `cas_aucun_declenchement`) : le point de depart est donc
    ramene a la main en zone de traitement AVANT de tester `Engage`, pour
    observer sans ambiguite les DEUX sens du geste demandes par la revue.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    deposer(jeu, "Puzzle.PutIntoPlay('01103')")
    sbire = id_du_sbire(monde, "01103")
    joueur = monde.const_players[0]
    carte = monde.object_manager.card_dict[sbire]

    deposer(jeu, f"Puzzle.MoveTo({sbire}, 'ProcessingArea')")
    assert carte.face.card.area is not joueur.engaged_minions, \
        "le sbire est reste engage : le point de depart n'est pas maitrise"

    deposer(jeu, f"Puzzle.Engage({sbire})")
    assert carte.face.card.area is joueur.engaged_minions, \
        "Engage n'a pas engage le sbire"

    deposer(jeu, f"Puzzle.Engage({sbire})")
    assert carte.face.card.area is monde.area_processing, \
        "un second Engage n'a pas desengage le sbire"
    return "Engage engage le sbire puis le desengage"


def cas_geste_refuse_non_enregistre(game_dir, port):
    """Le seul temoin qui couvre les constats 2 et 3 (revue finale du
    18/09/2026) : un geste REFUSE n'entre PAS dans `manuel_commands`, et le
    geste valide qui le suit y entre bien.

    Sans lui, un lot partiellement applique (constat 2) ou une course entre
    l'instantane et le drainage (constat 3) pouvaient tous deux glisser une
    commande jamais appliquee - ou en manquer une - dans la sauvegarde sans
    qu'aucun cas ne le remarque.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)

    deposer(jeu, f"Puzzle.MoveTo({vilain}, 'ZoneInconnue')")
    gestes = jeu.session.scene.manuel_commands
    assert gestes == [], \
        f"un geste refuse est entre dans la sauvegarde : {gestes}"

    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    gestes = jeu.session.scene.manuel_commands
    assert gestes == [f"Puzzle.Damage({vilain}, 3)"], \
        f"le geste valide qui suit un refus n'est pas entre dans la sauvegarde : {gestes}"
    return "un geste refuse n'entre pas dans la sauvegarde, le geste valide qui le suit y entre"


def cas_ecart_modular(game_dir, port):
    """`AsideModular` doit remplir `world.aside_modular`, pas une autre pile.

    Jumeau de `cas_ecart_scenario` pour la seconde entree ajoutee par la
    tache 4 bis (`'AsideModular'`, `ZONES_MONDE`). Cette table a deja mordu
    trois fois sur ce chantier (`set_aside_deck`, `AsideDeck`/`AsideScenario`
    ronde 1 et tache 4 bis) : chaque entree merite son propre temoin. Verifie
    l'arrivee dans `world.aside_modular` ET l'absence dans les DEUX piles
    voisines - `world.aside_deck` (la ligne juste au-dessus dans la table) et
    le set nemesis du heros - une entree copiee-collee sur la mauvaise ligne
    n'y leve jamais d'erreur, elle y range juste la carte en silence.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    avant_modular = len(monde.aside_modular.GetAll())
    avant_scenario = len(monde.aside_deck.GetAll())
    avant_nemesis = len(joueur.set_aside_nemesis_sets.GetAll())

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'AsideModular')")

    apres_modular = len(monde.aside_modular.GetAll())
    apres_scenario = len(monde.aside_deck.GetAll())
    apres_nemesis = len(joueur.set_aside_nemesis_sets.GetAll())
    assert apres_modular == avant_modular + 1, \
        (f"les mises de cote modulaires devaient passer de {avant_modular} "
         f"a {avant_modular + 1}, elles valent {apres_modular}")
    assert apres_scenario == avant_scenario, \
        (f"la carte a atterri dans les mises de cote du scenario au lieu du "
         f"modulaire : {avant_scenario} -> {apres_scenario}")
    assert apres_nemesis == avant_nemesis, \
        (f"la carte a atterri dans le set nemesis du heros au lieu du "
         f"modulaire : {avant_nemesis} -> {apres_nemesis}")
    return "AsideModular envoie vers world.aside_modular, pas vers une autre pile"


def cas_refus_publie_puis_reparti(game_dir, port):
    """Le descripteur publie le motif d'un geste refuse, puis reparti a vide.

    Tache 4 ter. `sandbox_last_error` existait deja cote moteur
    (`DrainSandboxCommands`, engine/device/manager/base.py) mais
    `ToDescriptor.World` ne le lisait pas : la trace du refus etait orpheline.
    Ce cas prouve deux choses : le motif atteint bien
    `WorldDescriptor.manuel_refus`, et le geste VALIDE qui suit le vide -
    sans quoi le plateau afficherait pour toujours la meme erreur (mise en
    garde du brief).
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    vilain = id_du_vilain(monde)

    deposer(jeu, f"Puzzle.MoveTo({vilain}, 'ZoneInconnue')")
    refus = monde.render.descriptor.manuel_refus
    assert refus, "le refus n'a pas ete publie dans le descripteur"
    assert "ZoneInconnue" in refus, \
        f"le motif publie ne parle pas de la zone refusee : {refus!r}"

    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    refus_apres = monde.render.descriptor.manuel_refus
    assert refus_apres == "", \
        f"le refus est reste colle apres un geste valide : {refus_apres!r}"
    return "le refus est publie dans le descripteur, puis reparti a vide au geste valide suivant"


def cas_defausse_deck_special(game_dir, port):
    """`AdditionalDiscardPile` doit remplir la defausse du deck ANNEXE du
    heros, ni sa defausse ORDINAIRE, ni le deck annexe lui-meme.

    Ronde de correction 1 (tache 5, 19/09/2026) : cette pile est VISIBLE sur
    le plateau (a cote du deck special, quand le heros en a un) mais
    `RunPuzzle.ZONES_JOUEUR` n'avait aucune entree pour
    `player.additional_discard_pile` - `Puzzle.MoveTo` levait `KeyError` sur
    n'importe quelle tentative. Ce cas verifie l'arrivee dans la bonne pile
    ET l'absence dans les deux piles voisines qu'un nom mal choisi aurait pu
    confondre : la defausse ORDINAIRE (meme role, mauvais deck) et le deck
    annexe lui-meme (meme deck, mauvais role).
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_players[0]
    main = list(joueur.hand_cards.GetAll())
    assert main, "la main de depart est vide"
    carte = main[0].card.object_id

    avant_defausse_speciale = len(joueur.additional_discard_pile.GetAll())
    avant_defausse_ordinaire = len(joueur.discard_pile.GetAll())
    avant_deck_special = len(joueur.additional_deck.GetAll())

    deposer(jeu, f"Puzzle.MoveTo({carte}, 'AdditionalDiscardPile')")

    apres_defausse_speciale = len(joueur.additional_discard_pile.GetAll())
    apres_defausse_ordinaire = len(joueur.discard_pile.GetAll())
    apres_deck_special = len(joueur.additional_deck.GetAll())
    assert apres_defausse_speciale == avant_defausse_speciale + 1, \
        (f"la defausse du deck special devait passer de {avant_defausse_speciale} "
         f"a {avant_defausse_speciale + 1}, elle vaut {apres_defausse_speciale}")
    assert apres_defausse_ordinaire == avant_defausse_ordinaire, \
        (f"la carte a atterri dans la defausse ORDINAIRE du heros : "
         f"{avant_defausse_ordinaire} -> {apres_defausse_ordinaire}")
    assert apres_deck_special == avant_deck_special, \
        (f"la carte a atterri dans le DECK special au lieu de sa defausse : "
         f"{avant_deck_special} -> {apres_deck_special}")
    return "AdditionalDiscardPile envoie vers la defausse du deck special, pas vers une pile voisine"


def cas_pause_ferme_la_porte(game_dir, port):
    """Sur une partie ORDINAIRE (sans la regle), la pause ferme la meme porte
    que le mode declare.

    Meme temoin que `cas_aucun_declenchement` (voir son commentaire pour le
    detail des deux temoins rejetes avant lui, et pourquoi Armored Rhino
    Suit/01098 est le bon) : mais ici c'est `BasculerPauseManuelle(True)`
    depose EN COURS DE PARTIE qui doit fermer la porte, pas une regle posee a
    la creation.

    `drainer_soi_meme=True` partout : en partie ORDINAIRE, `pilote` remplace
    `DoGetInput`, seul appelant reel de `DrainSandboxCommands` -- comme dans
    `cas_declenchement_en_automatique`.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    vilain = id_du_vilain(monde)
    carte = monde.object_manager.card_dict[vilain]
    perdu_avant = carte.face.GetLostHealth()

    basculer_pause(jeu, True)
    assert monde.manuel_actif is True, "la pause n'a pas pose manuel_actif"

    deposer(jeu, "Puzzle.CreateCard('01098')", drainer_soi_meme=True)
    suit = max(monde.object_manager.card_dict)
    deposer(jeu, f"Puzzle.Attach({suit}, {vilain})", drainer_soi_meme=True)

    # PREMISE VERIFIEE, PAS SUPPOSEE (meme garde que cas_aucun_declenchement) :
    # sans ce controle, l'assertion finale serait vraie meme si l'attache
    # manuelle avait elle-meme echoue en silence.
    suit_face = monde.object_manager.card_dict[suit].face
    assert suit_face in carte.face.GetInventoryDeck().GetAll(), \
        (f"la suit d'armure n'est pas dans l'inventaire de Rhino : ce cas ne "
         f"peut rien prouver sur une capacite deja en place "
         f"(IsFaceUp={suit_face.IsFaceUp()}, IsInPlay={suit_face.IsInPlay()})")

    deposer(jeu, f"Puzzle.Damage({vilain}, 3)", drainer_soi_meme=True)
    delta = carte.face.GetLostHealth() - perdu_avant
    assert delta == 3, \
        ("les degats sur Rhino ont ete detournes pendant la pause : la "
         f"capacite d'Armored Rhino Suit a agi malgre la pause (delta={delta})")
    return ("la pause ferme la meme porte que le mode declare, sur une "
            "partie ordinaire : une capacite deja attachee reste muette")


def cas_reprise_rouvre_la_porte(game_dir, port):
    """LE cas du plan : apres la reprise, le meme geste declenche de nouveau.

    `manuel_actif` n'avait jusqu'ici JAMAIS ete remis a faux : le mode
    declare le pose et ne l'enleve plus, donc rien n'avait jamais verifie que
    la porte du silence se ROUVRE. Meme mise en place que
    `cas_pause_ferme_la_porte` (armure deja attachee pendant la pause, porte
    fermee, degats non detournes -- reverifie ici comme premisse) puis
    `BasculerPauseManuelle(False)` : le MEME geste (Puzzle.Damage) doit cette
    fois etre detourne par la capacite, la porte s'etant rouverte.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    vilain = id_du_vilain(monde)
    carte = monde.object_manager.card_dict[vilain]

    basculer_pause(jeu, True)
    deposer(jeu, "Puzzle.CreateCard('01098')", drainer_soi_meme=True)
    suit = max(monde.object_manager.card_dict)
    deposer(jeu, f"Puzzle.Attach({suit}, {vilain})", drainer_soi_meme=True)
    suit_face = monde.object_manager.card_dict[suit].face
    assert suit_face in carte.face.GetInventoryDeck().GetAll(), \
        "la suit d'armure n'est pas dans l'inventaire de Rhino avant la reprise"

    # PREMISE : la porte est bien fermee avant la reprise (memes chiffres que
    # cas_pause_ferme_la_porte). Sans ce controle, un delta nul mesure plus
    # bas apres la reprise ne prouverait rien : il faut savoir d'ou on part.
    perdu_avant_pause = carte.face.GetLostHealth()
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)", drainer_soi_meme=True)
    delta_pendant_pause = carte.face.GetLostHealth() - perdu_avant_pause
    assert delta_pendant_pause == 3, \
        (f"premisse fausse : la porte n'etait pas fermee avant la reprise "
         f"(delta={delta_pendant_pause})")

    resultat = basculer_pause(jeu, False)
    assert resultat is False, "la reprise n'a pas rendu manuel_actif a faux"
    assert monde.manuel_actif is False, "manuel_actif reste a vrai apres la reprise"

    perdu_avant_reprise = carte.face.GetLostHealth()
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)", drainer_soi_meme=True)
    delta_apres_reprise = carte.face.GetLostHealth() - perdu_avant_reprise
    assert delta_apres_reprise == 0, \
        ("apres la reprise, Armored Rhino Suit aurait du de nouveau absorber "
         f"les degats (delta={delta_apres_reprise}) : la porte ne s'est pas "
         "rouverte")
    return ("apres la reprise, le meme geste declenche de nouveau : la "
            "porte du silence se rouvre")


def cas_marque_survit_reprise(game_dir, port):
    """La marque `corrigee_a_la_main` : une TRACE, pas un ETAT (tache 2).

    A l'inverse de `manuel_actif` (`cas_reprise_rouvre_la_porte` juste
    au-dessus), qui repasse a faux a la reprise, `corrigee_a_la_main` ne doit
    JAMAIS s'eteindre : une partie qu'on a corrigee a la main l'a ete, meme
    apres la reprise. Temoin dans les DEUX sens attendus : fausse par defaut
    sur une partie ORDINAIRE (aucune regle `mode_manuel`) jamais mise en
    pause, vraie des la premiere pause, ENCORE vraie apres la reprise.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])

    assert monde.scene.corrigee_a_la_main is False, \
        "une partie ordinaire jamais mise en pause porte deja la marque"

    basculer_pause(jeu, True)
    assert monde.scene.corrigee_a_la_main is True, \
        "la pause n'a pas pose la marque corrigee_a_la_main"

    resultat = basculer_pause(jeu, False)
    assert resultat is False, "la reprise n'a pas rendu manuel_actif a faux"
    assert monde.scene.corrigee_a_la_main is True, \
        ("la reprise a eteint la marque corrigee_a_la_main : c'est une "
         "trace, pas un etat")

    return ("la marque corrigee_a_la_main : fausse par defaut, vraie apres "
            "la pause, ENCORE vraie apres la reprise")


def cas_marque_survit_sauvegarde(game_dir, port):
    """La marque `corrigee_a_la_main` survit a un aller-retour de sauvegarde.

    Meme gabarit que `cas_aller_retour`/`cas_relire_sauvegarde` : le fils
    relit la sauvegarde dans SON PROPRE processus et verifie la marque --
    seule facon de prouver qu'elle est bien ECRITE dans le fichier, pas
    seulement tenue en memoire par cet objet `Scene`.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])
    basculer_pause(jeu, True)
    assert monde.scene.corrigee_a_la_main is True, \
        "premisse fausse : la marque n'a pas ete posee avant la sauvegarde"

    nom = "manuel-marque-aller-retour.json"
    ecrit = jeu.session.SaveScene(name=nom, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_marque_survit", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-3000:]}\n{fils.stderr[-3000:]}"
    return "la marque corrigee_a_la_main survit a un aller-retour de sauvegarde"


def cas_relire_marque_survit(game_dir, port):
    """Le fils de `cas_marque_survit_sauvegarde` : il recharge et verifie."""
    chemin = os.environ["MC_SAUVEGARDE"]
    _, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin)
    assert monde.scene.corrigee_a_la_main is True, \
        "la sauvegarde a perdu la marque corrigee_a_la_main"
    return "la partie rechargee porte encore la marque corrigee_a_la_main"


def cas_qui_et_depuis_publies(game_dir, port):
    """La pause EN COURS (tache 3) : `pause_par` / `pause_a`, poses puis
    EFFACES a la reprise -- a l'inverse de `corrigee_a_la_main`
    (`cas_marque_survit_reprise` juste au-dessus), qui elle ne s'eteint
    jamais. Sans cette distinction, un joueur d'une table EN LIGNE ne peut
    pas savoir qui a arrete sa partie ni depuis quand.

    ⚠ MEME PIEGE QUE `cas_pause_publiee`, et le meme remede : la trame
    (`monde.render.descriptor`) n'est rafraichie qu'au PROCHAIN rendu, et
    rien ne le force sans une question posee entre-temps. Une premiere
    version de ce cas lisait le descripteur juste apres `basculer_pause`
    (comme les cas voisins le font pour `monde.scene.*`, jamais pour le
    descripteur) : ROUGE, non pas faute d'implementation mais parce
    qu'aucun rendu n'avait eu lieu entre la bascule et la lecture -- constate
    a l'execution : la partie automatique avait deja largement depasse
    PLAFOND_QUESTIONS a ce moment-la, `pilote` ne repondait plus, donc plus
    aucun rendu naturel n'avait lieu. Meme sequence que `cas_pause_publiee` :
    tout observe DEPUIS `avant_reponse`, sur la partie AUTOMATIQUE qui
    continue derriere, aucun `Puzzle.*` deppose.
    """
    etat = {
        "compte": 0, "pause_posee": False, "vu_qui": False,
        "reprise_posee": False, "vu_vide_apres_reprise": False,
    }

    def observateur(jeu):
        etat["compte"] += 1
        descripteur = jeu.world.render.descriptor
        pause_par_publie = getattr(descripteur, "pause_par", None)

        if etat["compte"] == 1:
            # PREMISE, verifiee sur la toute premiere trame : une partie
            # ordinaire jamais mise en pause ne porte pas deja ces champs.
            assert pause_par_publie == "", \
                f"une partie jamais mise en pause publie deja pause_par={pause_par_publie!r}"
            assert getattr(descripteur, "pause_a", None) == "", \
                "une partie jamais mise en pause publie deja pause_a"

        if not etat["pause_posee"] and etat["compte"] >= 5:
            etat["pause_posee"] = True
            jeu.world.BasculerPauseManuelle(True, "Nick Fury")
            assert jeu.world.scene.pause_par == "Nick Fury", \
                "pause_par n'a pas pris le pseudo transmis sur la scene"
            assert jeu.world.scene.pause_a != "", \
                "pause_a est reste vide sur la scene alors que la pause est posee"
            return

        if etat["pause_posee"] and not etat["vu_qui"]:
            if pause_par_publie == "Nick Fury":
                etat["vu_qui"] = True
                assert getattr(descripteur, "pause_a", None) not in (None, ""), \
                    "pause_par est publie mais pause_a reste vide"
                jeu.world.BasculerPauseManuelle(False)
                etat["reprise_posee"] = True
            return

        if etat["reprise_posee"] and not etat["vu_vide_apres_reprise"]:
            if pause_par_publie == "":
                etat["vu_vide_apres_reprise"] = True
                assert getattr(descripteur, "pause_a", None) == "", \
                    "pause_a reste publie apres la reprise"

    monter_le_moteur(game_dir, port, [], avant_reponse=observateur)

    assert etat["pause_posee"], \
        "la pause n'a jamais ete posee : ce cas n'a rien pu prouver"
    assert etat["vu_qui"], (
        "la trame n'a jamais publie pause_par='Nick Fury' apres la bascule"
    )
    assert etat["vu_vide_apres_reprise"], (
        "la trame n'a jamais republie pause_par vide apres la reprise"
    )
    return ("pause_par/pause_a : vides par defaut, poses (qui, depuis) a la "
            "pause, RE-VIDES apres la reprise -- sur la scene et sur la trame")


class _RequeteFactice:
    """Un `web.Request` minimal : juste ce que lisent `tient_le_siege` et
    `nom_du_heros_qui_parle` (`server_base.py`) -- des cookies, et un corps
    JSON. Pas de vrai socket : meme esprit que `cas_reveil_dogetinput`, qui
    construit un `DeviceManager` nu plutot que de monter un serveur complet.
    """
    def __init__(self, cookies, corps):
        self.cookies = cookies
        self._corps = corps

    async def json(self):
        return self._corps


def cas_pause_par_nom_du_heros(game_dir, port):
    """`pause_par` porte le NOM DU HEROS du siege qui PROUVE avoir demande la
    pause (ronde de correction 1, tache 3) -- plus un pseudo envoye par le
    plateau (retire : chemin mort, aucun pseudo n'y etait jamais atteignable
    de toute facon), et pas un siege choisi par defaut.

    Exerce le VRAI `GameServerGet.manuel_pause` (la route HTTP elle-meme),
    pas seulement `World.BasculerPauseManuelle` comme les autres cas de ce
    fichier : c'est justement la RESOLUTION DU SIEGE, faite dans le
    gestionnaire de route, qui est sous test ici. Instance construite via
    `__new__` (comme `_RequeteFactice` ci-dessus evite un vrai socket) :
    seul `self.game` est lu par ce chemin de code.

    Deux temoins : le siege PROTEGE (mot de passe pose) dont la requete
    prouve tenir le cookie recoit le nom du heros de CE siege ; une requete
    qui n'en prouve AUCUN (table sans siege protege, ou cookie absent/faux)
    recoit une chaine vide -- le cas honnete d'un siege indetermine, pas une
    panne.
    """
    import asyncio
    import hashlib

    # ⚠ APRES `monter_le_moteur`, PAS AVANT : c'est elle qui fait
    # `sys.path.insert(0, game_dir)` -- `engine` n'existe encore nulle part
    # avant cet appel (meme piege que cas_reveil_dogetinput, qui l'evite en
    # n'appelant jamais monter_le_moteur et en inserant son propre chemin).
    jeu, monde, _ = monter_le_moteur(game_dir, port, [])

    from engine.device.web.server.server_get import GameServerGet
    from engine.device.web.server.server_base import SEAT_PASSWORDS

    # `GameServerBase.game` est une PROPRIETE en lecture seule, deduite de
    # `self.device_manager.controllers[0].game` -- on branche donc le VRAI
    # gestionnaire de la partie, pas `.game` directement (non affectable).
    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = jeu.world.controller_manager.device_manager

    ancien_mdp = list(SEAT_PASSWORDS.value)
    try:
        mot_de_passe = "secret-siege-0"
        SEAT_PASSWORDS.value = [mot_de_passe, "", "", ""]
        jeton = hashlib.md5(mot_de_passe.encode()).hexdigest()

        nom_attendu = monde.render.descriptor.players[0].area_hero[0].name
        assert nom_attendu, \
            "premisse cassee : le siege 0 ne porte encore aucun heros"

        # TEMOIN 1 : cookie qui PROUVE le siege 0 -- pause_par prend le nom
        # de SON heros.
        requete_prouvee = _RequeteFactice({"seat_token_0": jeton}, {"actif": True})
        reponse = asyncio.run(serveur.manuel_pause(requete_prouvee))
        assert reponse.status == 200, f"la route a refuse la requete prouvee : {reponse.status}"
        assert monde.scene.pause_par == nom_attendu, (
            f"pause_par ne porte pas le nom du heros du siege prouve : "
            f"{monde.scene.pause_par!r} != {nom_attendu!r}"
        )

        # Reprise, sinon le second temoin ne pose rien (deja en pause).
        asyncio.run(serveur.manuel_pause(_RequeteFactice({}, {"actif": False})))
        assert monde.scene.pause_par == "", \
            "pause_par n'a pas ete efface a la reprise (chemin HTTP)"

        # TEMOIN 2 : aucun cookie ne prouve quoi que ce soit -- siege
        # indetermine, pause_par reste vide (« quelqu'un » cote plateau).
        requete_anonyme = _RequeteFactice({}, {"actif": True})
        reponse = asyncio.run(serveur.manuel_pause(requete_anonyme))
        assert reponse.status == 200, f"la route a refuse la requete anonyme : {reponse.status}"
        assert monde.scene.pause_par == "", (
            f"une requete qui ne prouve aucun siege a quand meme pose "
            f"pause_par={monde.scene.pause_par!r} : ce n'est pas un siege "
            f"determine, c'est vide qu'il fallait"
        )
    finally:
        SEAT_PASSWORDS.value = ancien_mdp
        # Reprise finale : ne pas laisser la partie en pause pour la suite
        # du processus (harmless ici, chaque cas est son propre processus,
        # mais garde la meme discipline que le reste du fichier).
        jeu.world.BasculerPauseManuelle(False)

    return ("pause_par porte le nom du heros du siege PROUVE par la requete "
            "HTTP reelle (route manuel_pause), vide si aucun siege n'est "
            "prouve")


def cas_pause_publiee(game_dir, port):
    """La trame publie manuel_actif SANS AUCUN AUTRE GESTE.

    ⚠ CORRECTIF DE PREMISE (ronde de correction 1, signale par le donneur
    d'ordre) : la version precedente deposait un geste (`Puzzle.Damage`,
    draine) entre la bascule et la lecture du descripteur. Ca prouvait
    qu'un geste manuel force un rendu -- deja vrai AVANT ce chantier, sans
    rapport avec ce qu'on ajoute ici -- pas que la bascule SEULE (sans rien
    deposer derriere) suffit a publier le nouvel etat. Corrige : aucun
    `deposer()` n'a lieu dans ce cas.

    Sans geste manuel a soi seul pour forcer un rendu, ce cas s'appuie sur
    la poursuite naturelle de la partie AUTOMATIQUE : constate a l'execution
    (18/09-20/09/2026) que la pause ne fige PAS la structure des tours (elle
    ferme seulement la porte des declencheurs, cf. `cas_pause_ferme_la_porte`)
    -- `pilote` continue donc d'etre sollicite, et chaque nouvelle question
    est precedee d'un rendu qui lit `world.manuel_actif` a l'instant meme.
    La bascule est donc posee TOT (via `avant_reponse`, a la 5e question),
    largement avant `PLAFOND_QUESTIONS` : au-dela, `pilote` ne repond plus
    jamais et plus aucun rendu naturel n'a lieu (cf. son commentaire).

    Sequence, entierement observee depuis `avant_reponse` (donc PENDANT
    `monter_le_moteur`, jamais apres) : bascule a vrai a la 5e question ->
    on attend de VOIR `manuel_actif` publie a vrai sur une question
    suivante -> bascule a faux des qu'on l'a vu -> on attend de le revoir
    publie a faux. Aucun `Puzzle.*` nulle part dans ce cas.
    """
    etat = {"compte": 0, "pause_posee": False, "vu_vrai": False,
            "reprise_posee": False, "vu_faux_apres_reprise": False}

    def observateur(jeu):
        etat["compte"] += 1
        manuel_actif_publie = getattr(jeu.world.render.descriptor, "manuel_actif", None)

        if not etat["pause_posee"] and etat["compte"] >= 5:
            etat["pause_posee"] = True
            jeu.world.BasculerPauseManuelle(True)
            return

        if etat["pause_posee"] and not etat["vu_vrai"]:
            if manuel_actif_publie is True:
                etat["vu_vrai"] = True
                jeu.world.BasculerPauseManuelle(False)
                etat["reprise_posee"] = True
            return

        if etat["reprise_posee"] and not etat["vu_faux_apres_reprise"]:
            if manuel_actif_publie is False:
                etat["vu_faux_apres_reprise"] = True

    monter_le_moteur(game_dir, port, [], avant_reponse=observateur)

    assert etat["pause_posee"], \
        "la pause n'a jamais ete posee : ce cas n'a rien pu prouver"
    assert etat["vu_vrai"], (
        "la trame n'a jamais publie manuel_actif=vrai apres la bascule, sans "
        "qu'aucun geste (Puzzle) n'ait ete depose entre-temps"
    )
    assert etat["vu_faux_apres_reprise"], (
        "la trame n'a jamais republie manuel_actif=faux apres la reprise, "
        "sans qu'aucun geste (Puzzle) n'ait ete depose entre-temps"
    )
    return ("la trame publie manuel_actif (vrai puis faux) sans qu'aucun "
            "geste manuel n'ait ete depose entre les deux bascules")


def cas_reveil_dogetinput(game_dir, port):
    """Le VRAI `DoGetInput` se reveille quand une bascule de pause est
    signalee -- pas le `pilote` qui le remplace dans TOUS les autres cas de
    ce fichier.

    ⚠ ANGLE MORT DU RESTE DE CE HARNAIS (signale par le donneur d'ordre,
    ronde de correction 2 -- deja coute plusieurs defauts sur ce chantier,
    dont un plantage du moteur) : `monter_le_moteur` remplace
    `DeviceManager.DoGetInput` par `pilote` (repondeur SYNCHRONE, jamais de
    vraie attente sur `notify.input`) pour toute la duree du PROCESSUS. Un
    cas qui appelle `monter_le_moteur` ne peut donc JAMAIS observer un fil
    reellement parque dans `DoGetInput.Wait` -- `cas_pause_publiee` ne
    prouve que « l'etat finit par etre publie », ce qui etait deja vrai
    AVANT le correctif de la ronde 1. Ce cas-ci EVITE le piege en n'appelant
    JAMAIS `monter_le_moteur` : chaque cas de ce fichier tourne dans SON
    PROPRE PROCESSUS (cf. `main()`), donc `DeviceManager.DoGetInput` reste
    la VRAIE methode ici, intacte.

    Ni partie, ni scenario : `DoGetInput` ne touche que ses propres
    attributs (`asking_players`, `ask_options`, `notify`...). Import direct
    depuis `src/` (comme le moteur complet le fait depuis une copie jetable,
    mais un `DeviceManager` nu n'a besoin d'aucune copie).

    VERIFIE (rapport de tache, ronde 2) : ce cas est ROUGE si on retire la
    condition `if self.pause_a_publier: return True` de `check_fn` (ou la
    branche qui la consomme) dans `DoGetInput` -- le fil reste bloque, le
    `join` expire sans jamais avoir vu de retour. Il redevient VERT des
    qu'on la remet. C'est le seul cas de ce fichier qui rougirait sur le
    code d'hier (reveil nu, `notify.input.NotifyAll()` seul) et verdit sur
    celui d'aujourd'hui.
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager, AskOptionPayload

    device_manager = DeviceManager()
    player_id = 0
    device_manager.ask_options[player_id] = AskOptionPayload(
        options_json="[]", ability_type="", event_name="", prompt_text="",
        show_cancel=False, replay_input="")
    device_manager.asking_players.append(player_id)

    resultat = {"retour": "PAS_ENCORE", "eleve": None}

    def fil_du_jeu():
        try:
            resultat["retour"] = device_manager.DoGetInput(
                device_manager.ask_options[player_id], player_id, lambda: False)
        except BaseException as exc:
            resultat["eleve"] = exc

    fil = threading.Thread(target=fil_du_jeu, daemon=True)
    fil.start()
    time.sleep(0.3)  # laisse DoGetInput entrer dans son Wait
    assert fil.is_alive(), \
        "premisse cassee : le fil n'est meme pas entre dans l'attente"

    # Le geste, depuis un AUTRE fil -- exactement ce que fait /manuel_pause
    # depuis le fil HTTP (World.BasculerPauseManuelle appelle la meme methode).
    device_manager.SignalerPauseAPublier()

    fil.join(timeout=2.0)
    assert not fil.is_alive(), (
        "DoGetInput ne s'est jamais reveille : SignalerPauseAPublier n'a "
        "rien pose que check_fn sache reconnaitre -- exactement le bug "
        "signale en ronde de correction 2 (un reveil qui ne produit rien)"
    )
    if resultat["eleve"] is not None:
        raise resultat["eleve"]
    assert resultat["retour"] is None, \
        f"DoGetInput aurait du rendre la main sans entree (None) : {resultat['retour']!r}"
    return ("le VRAI DoGetInput se reveille et rend la main quand une "
            "bascule de pause est signalee depuis un autre fil")


def cas_geste_refuse_arme_le_rendu(game_dir, port):
    """Un geste manuel qui ECHOUE arme quand meme le rendu force -- sinon le
    joueur voit son geste refuse... sans jamais voir qu'il l'a ete.

    ⚠ CE CAS EST NE D'UNE REVUE (ronde de correction 1 de la tache 8), et
    c'est la MEME famille de defaut que celui que la tache 8 corrige.
    `DrainSandboxCommands` rend une liste VIDE quand la PREMIERE commande du
    lot leve, tout en posant `sandbox_last_error` : un `if
    self.DrainSandboxCommands():` est donc FAUX dans ce cas precis, rien
    n'etait arme, aucun rendu n'etait force, et `manuel_refus` restait
    invisible jusqu'a la reprise. Le bon predicat n'est pas « quelque chose
    a ete applique » mais « un drainage a eu lieu » -- ce que `ManualLoop`
    dit deja mot pour mot (world.py : « Force meme si RIEN n'a ete retenu
    [...] c'est le seul moyen pour le plateau de voir `sandbox_last_error` a
    jour »).

    ⚠ MEME MONTAGE QUE `cas_reveil_dogetinput`, ET POUR LA MEME RAISON : un
    `DeviceManager` NU, jamais `monter_le_moteur`, parce que ce dernier
    remplace `DoGetInput` par `pilote` pour toute la duree du processus --
    la branche testee ici ne serait alors JAMAIS executee. Rien n'est
    imite : c'est le VRAI `DoGetInput`, reellement parque dans son `Wait`,
    reveille depuis un AUTRE fil comme le fait la route HTTP
    `/sandbox_command`.

    DEUX TEMOINS :
    - TEMOIN 1 (le defaut) : l'executeur LEVE des la premiere commande.
      `DoGetInput` doit rendre la main sans entree ET laisser
      `rendu_a_forcer` arme, alors qu'AUCUNE commande n'a ete appliquee.
    - TEMOIN 2 (contraste) : un reveil ORDINAIRE, sans le moindre geste
      depose, ne doit RIEN armer. Sans lui, un predicat devenu « toujours
      vrai » passerait le temoin 1 sans rien prouver.
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager, AskOptionPayload

    def parquer(device_manager, check):
        """Gare le VRAI DoGetInput dans son Wait, sur un autre fil."""
        player_id = 0
        device_manager.ask_options[player_id] = AskOptionPayload(
            options_json="[]", ability_type="", event_name="", prompt_text="",
            show_cancel=False, replay_input="")
        device_manager.asking_players.append(player_id)
        resultat = {"retour": "PAS_ENCORE", "eleve": None}

        def fil_du_jeu():
            try:
                resultat["retour"] = device_manager.DoGetInput(
                    device_manager.ask_options[player_id], player_id, check)
            except BaseException as exc:
                resultat["eleve"] = exc

        fil = threading.Thread(target=fil_du_jeu, daemon=True)
        fil.start()
        time.sleep(0.3)  # laisse DoGetInput entrer dans son Wait
        assert fil.is_alive(), \
            "premisse cassee : le fil n'est meme pas entre dans l'attente"
        return fil, resultat

    # ------------------------------------------------------------------
    # TEMOIN 1 : le geste qui ECHOUE.
    # ------------------------------------------------------------------
    device_manager = DeviceManager()

    def executeur_qui_leve(commandes):
        raise RuntimeError("Puzzle.Damage: cible introuvable")

    device_manager.sandbox_executor = executeur_qui_leve

    fil, resultat = parquer(device_manager, lambda: False)
    # Le depot, depuis un AUTRE fil -- exactement ce que fait la route
    # POST /sandbox_command depuis le fil HTTP.
    device_manager.QueueSandboxCommands(["Puzzle.Damage(9999, 1)"])

    fil.join(timeout=2.0)
    assert not fil.is_alive(), \
        "DoGetInput ne s'est jamais reveille sur un geste depose"
    if resultat["eleve"] is not None:
        raise resultat["eleve"]
    assert resultat["retour"] is None, (
        f"DoGetInput aurait du rendre la main sans entree (None) apres un "
        f"drainage : {resultat['retour']!r}"
    )
    assert device_manager.sandbox_last_error, (
        "premisse cassee : l'executeur n'a pas leve, ce cas ne teste rien"
    )
    assert device_manager.rendu_a_forcer is True, (
        "LE REFUS NE SERA JAMAIS PUBLIE : un geste manuel a ete draine et a "
        f"ECHOUE (sandbox_last_error={device_manager.sandbox_last_error!r}), "
        "mais aucun rendu force n'a ete arme -- le plateau ne verra pas "
        "manuel_refus avant la reprise. Le predicat de DoGetInput teste le "
        "RETOUR de DrainSandboxCommands (vide quand la premiere commande "
        "leve) au lieu de tester qu'un drainage a eu lieu."
    )
    assert device_manager.ConsommerRenduAForcer() is True, \
        "ConsommerRenduAForcer n'a pas vu le marqueur arme"
    assert device_manager.ConsommerRenduAForcer() is False, (
        "ConsommerRenduAForcer ne consomme pas : un seul armement doit "
        "produire un seul rendu force, jamais un a chaque re-pose"
    )

    # ------------------------------------------------------------------
    # TEMOIN 2 (contraste) : un reveil ORDINAIRE n'arme rien.
    # ------------------------------------------------------------------
    autre = DeviceManager()
    pret = {"ok": False}
    fil2, _ = parquer(autre, lambda: pret["ok"])
    pret["ok"] = True
    autre.notify.input.NotifyAll()

    fil2.join(timeout=2.0)
    assert not fil2.is_alive(), \
        "premisse cassee : le reveil ordinaire n'a pas reveille DoGetInput"
    assert autre.rendu_a_forcer is False, (
        "MONTAGE SUSPECT : un reveil SANS le moindre geste depose arme quand "
        "meme le rendu force. Le predicat ne distingue plus rien, et le "
        "temoin 1 ne prouve donc rien."
    )

    return ("un geste manuel qui ECHOUE arme le rendu force au meme titre "
            "qu'un geste applique ; un reveil sans geste n'arme rien")


class _MondeFactice:
    """Juste ce que lit `GameServerGet.manuel_passer` : `manuel_actif`."""
    def __init__(self, manuel_actif):
        self.manuel_actif = manuel_actif


class _JeuFactice:
    def __init__(self, monde):
        self.world = monde


class _ControleurFactice:
    """Juste ce que lit `GameServerBase.game` : `controller.game`."""
    def __init__(self, monde):
        self.game = _JeuFactice(monde)


def _construire_route_passer(device_manager, manuel_actif):
    """Une VRAIE `GameServerGet.manuel_passer`, brancheee sur un
    `DeviceManager` nu -- meme esprit que `cas_pause_par_nom_du_heros`
    (`GameServerGet.__new__`, un seul attribut lu par ce chemin de code).
    """
    import sys
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.web.server.server_get import GameServerGet

    device_manager.controllers.append(_ControleurFactice(_MondeFactice(manuel_actif)))
    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = device_manager
    return serveur


def cas_passer_annule_le_moteur(game_dir, port):
    """« Passer la question fautive » (tache 5) : une question qui OFFRE une
    annulation (`show_cancel` vrai) est vraiment passee -- le VRAI
    `DoGetInput`, pare dans son `Wait`, se reveille et rend la main, EXACTEMENT
    comme le ferait un clic normal sur le bouton « Passer » du joueur.

    Meme technique que `cas_reveil_dogetinput` (le seul cas de ce fichier a
    exercer une VRAIE attente sans monter de moteur) : un `DeviceManager` nu,
    un fil separe pare dans `DoGetInput`, et le geste depuis CE fil-ci (celui
    du test, qui joue le role du fil HTTP) -- pas de moteur, pas de partie.

    ⚠ DISCRIMINANT (constate ROUGE avant l'ecriture de
    `DeviceManager.PasserQuestionCourante`/la route : `AttributeError`, la
    methode n'existe pas encore). Discriminant aussi contre un refus
    SYSTEMATIQUE (bug oppose a `cas_passer_refuse_question_forcee` juste en
    dessous) : si la route refusait tout, le fil resterait bloque et ce cas
    rougirait sur l'assertion `not fil.is_alive()`.
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager, AskOptionPayload

    device_manager = DeviceManager()
    player_id = 0
    # ⚠ NE PAS pre-remplir `asking_players` ICI : `DoGetInput` (plus bas,
    # sur le fil du jeu) le fait deja lui-meme des son entree. Une seconde
    # entree ici dupliquerait le joueur dans la liste, et `WhenInput` (qui ne
    # retire qu'UNE occurrence) laisserait l'autre trainer -- le predicat
    # `self.asking_players == []` de `DoGetInput.Wait` resterait donc FAUX
    # et ce cas resterait ROUGE meme sur une route parfaitement correcte
    # (constate en ecrivant ce cas : diagnostique avant d'ecrire le rapport).
    device_manager.ask_options[player_id] = AskOptionPayload(
        options_json="[]", ability_type="", event_name="", prompt_text="",
        show_cancel=True, replay_input="")

    resultat = {"retour": "PAS_ENCORE", "eleve": None}

    def fil_du_jeu():
        try:
            resultat["retour"] = device_manager.DoGetInput(
                device_manager.ask_options[player_id], player_id, lambda: False)
        except BaseException as exc:
            resultat["eleve"] = exc

    fil = threading.Thread(target=fil_du_jeu, daemon=True)
    fil.start()
    time.sleep(0.3)  # laisse DoGetInput entrer dans son Wait
    assert fil.is_alive(), \
        "premisse cassee : le fil n'est meme pas entre dans l'attente"

    import asyncio
    serveur = _construire_route_passer(device_manager, manuel_actif=True)
    reponse = asyncio.run(serveur.manuel_passer(None))
    assert reponse.status == 200, \
        f"la route a refuse une question qui offrait pourtant une annulation : {reponse.status} {reponse.text}"

    fil.join(timeout=2.0)
    assert not fil.is_alive(), (
        "DoGetInput ne s'est jamais reveille : la route n'a rien pose que "
        "check_fn sache reconnaitre"
    )
    if resultat["eleve"] is not None:
        raise resultat["eleve"]
    assert resultat["retour"] == "{}", (
        f"DoGetInput aurait du rendre la main avec le meme corps qu'un "
        f"clic Annuler/Passer reel (\"{{}}\") : {resultat['retour']!r}"
    )
    return ("une question qui offre une annulation est vraiment passee : le "
            "VRAI DoGetInput se reveille et rend le meme corps qu'un clic "
            "Annuler/Passer reel")


def cas_passer_refuse_question_forcee(game_dir, port):
    """« Passer la question fautive » (tache 5) : une question qui N'OFFRE
    PAS d'annulation (`show_cancel` faux, question FORCEE) est REFUSEE, avec
    un motif lisible -- jamais une reponse fabriquee a sa place.

    ⚠ DISCRIMINANT contre le defaut le plus dangereux de cette tache :
    fabriquer une reponse a une question forcee. Si la route acceptait quand
    meme, le fil se reveillerait (comme dans `cas_passer_annule_le_moteur`)
    et l'assertion `fil.is_alive()` rougirait ici. Complementaire du cas
    ci-dessus : aucun des deux ne serait vert sur une route qui accepte ou
    refuse TOUJOURS, quel que soit `show_cancel`.
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager, AskOptionPayload

    device_manager = DeviceManager()
    player_id = 0
    device_manager.ask_options[player_id] = AskOptionPayload(
        options_json="[]", ability_type="", event_name="", prompt_text="",
        show_cancel=False, replay_input="")
    # Meme remarque que `cas_passer_annule_le_moteur` : `DoGetInput`
    # remplit `asking_players` lui-meme, pas besoin (et pas question) de
    # le faire ici.

    resultat = {"retour": "PAS_ENCORE", "eleve": None}

    def fil_du_jeu():
        try:
            resultat["retour"] = device_manager.DoGetInput(
                device_manager.ask_options[player_id], player_id, lambda: False)
        except BaseException as exc:
            resultat["eleve"] = exc

    fil = threading.Thread(target=fil_du_jeu, daemon=True)
    fil.start()
    time.sleep(0.3)
    assert fil.is_alive(), \
        "premisse cassee : le fil n'est meme pas entre dans l'attente"

    import asyncio
    import json as json_lib
    serveur = _construire_route_passer(device_manager, manuel_actif=True)
    reponse = asyncio.run(serveur.manuel_passer(None))
    assert reponse.status == 409, \
        f"la route aurait du refuser une question forcee : {reponse.status}"
    corps = json_lib.loads(reponse.text)
    assert corps.get("error") == "question_forcee", (
        f"le motif de refus n'est pas le code stable attendu : {corps!r} -- "
        f"pas un code d'erreur nu, un motif que le plateau sait traduire"
    )

    fil.join(timeout=1.0)
    assert fil.is_alive(), (
        "le fil s'est reveille alors que la question etait FORCEE : une "
        "reponse a ete fabriquee a la place du joueur"
    )
    assert player_id in device_manager.asking_players, (
        "la question forcee a ete retiree de asking_players malgre le refus"
    )
    return ("une question forcee (sans annulation) est refusee avec un "
            "motif lisible ('question_forcee'), et le moteur reste "
            "vraiment pare dessus -- rien n'est fabrique a sa place")


def cas_passer_aucune_question(game_dir, port):
    """« Passer la question fautive » (tache 5) : aucune question en
    attente -- refus avec son propre motif, distinct de « question_forcee ».
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager

    import asyncio
    import json as json_lib
    device_manager = DeviceManager()
    serveur = _construire_route_passer(device_manager, manuel_actif=True)
    reponse = asyncio.run(serveur.manuel_passer(None))
    assert reponse.status == 409
    corps = json_lib.loads(reponse.text)
    assert corps.get("error") == "aucune_question", corps
    return ("aucune question en attente -> refus avec le motif "
            "'aucune_question', distinct de 'question_forcee'")


def cas_passer_hors_pause(game_dir, port):
    """« Passer la question fautive » (tache 5) : la route est REFUSEE hors
    pause, meme quand une question EN COURS offre une annulation.

    ⚠ DISCRIMINANT contre l'oubli de la garde `world.manuel_actif` : sans
    elle, cette route deviendrait un raccourci pour sauter n'importe quelle
    decision de jeu ORDINAIRE (« joue cette carte ou passe ») a la place du
    joueur, hors de toute pause -- pas l'echappatoire de dernier recours que
    demande le brief.
    """
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.manager.base import DeviceManager, AskOptionPayload

    import asyncio
    device_manager = DeviceManager()
    player_id = 0
    device_manager.ask_options[player_id] = AskOptionPayload(
        options_json="[]", ability_type="", event_name="", prompt_text="",
        show_cancel=True, replay_input="")
    device_manager.asking_players.append(player_id)

    serveur = _construire_route_passer(device_manager, manuel_actif=False)
    reponse = asyncio.run(serveur.manuel_passer(None))
    assert reponse.status == 409, \
        f"la route aurait du refuser hors pause : {reponse.status}"
    assert player_id in device_manager.asking_players, (
        "la question a ete touchee alors que la partie n'etait pas en pause"
    )
    return ("hors pause, la route refuse meme une question qui offrirait "
            "une annulation -- ce n'est pas un raccourci de jeu ordinaire")


def cas_pause_publiee_pendant_question_ouverte(game_dir, port):
    """La pause posee PENDANT une question deja ouverte doit se PUBLIER --
    c'est le cas d'usage central du chantier (« je suis coince sur une
    question, je mets en pause pour corriger a la main »).

    ⚠ CE CAS A ETE ECRIT ROUGE, IL EST LA GARDE DU CORRECTIF (diagnostic
    du 20/09/2026, apres la mesure de bout en bout de la tache 7 : « poser
    la pause pendant le mulligan ou une fenetre d'interruption ne publie
    jamais `manuel_actif` cote /get_world, immobile jusqu'a 60 s »).
    Constate rouge -- trame (30, False) -> (30, False) -- puis passe au vert
    par la tache 8 : `Controller.ChoiceOne` force desormais un rendu quand
    il rend la main sans entree pour une cause qui a mute le monde. Ce cas
    redevient rouge des que ce rendu force disparait : c'est sa seule
    raison d'etre.

    ⚠ POURQUOI IL N'UTILISE PAS `monter_le_moteur`. Le `pilote` de ce
    harnais REPOND toujours : il ne peut pas jouer le seul scenario qui
    compte ici, celui ou `DoGetInput` RE-POSE la meme question sans reponse.
    Ce cas monte donc la partie lui-meme, avec son propre pilote -- meme
    scenario (rhino/spider_man, graine 42) et meme boucle `run()` que
    `monter_le_moteur`, a la seule difference du pilote.

    ⚠ CE QUE LE PILOTE IMITE, ET AVEC QUELLE FIDELITE. Au moment choisi, il
    fait DANS L'ORDRE ce que font les deux vrais fils :
      1. `World.BasculerPauseManuelle(True)` -- exactement ce que fait le
         fil HTTP (route POST /manuel_pause), a l'identique ;
      2. consommer `pause_a_publier` puis rendre `None` -- exactement la
         branche du VRAI `DoGetInput` (base.py, « Meme protocole que
         ci-dessus, pour la pause »), dont `cas_reveil_dogetinput` prouve
         deja qu'elle est bien atteinte sur le vrai fil parque.
    Tout le reste (le retour `None` remonte dans `Controller.ChoiceOne`, la
    boucle qui RE-POSE la question, et le rendu qui a lieu ou non entre les
    deux) est le VRAI code du moteur, pas une imitation.

    DEUX TEMOINS, et le second est ce qui rend le premier credible :
    - TEMOIN 1 (le defaut) : pause posee sur la question du MULLIGAN. A la
      question suivante -- la MEME, re-posee -- la trame doit porter
      `manuel_actif` vrai. C'etait ce temoin, et lui seul, qui rougissait :
      la trame ne bougeait pas d'un numero et publiait toujours faux, alors
      que `world.manuel_actif` etait deja vrai.
    - TEMOIN 2 (contraste) : la meme sequence sur une question de TOUR DE
      HEROS (`WhenPlayerInTurn`) publiait, elle, deja tout de suite -- le
      seul chemin ou `SenderPlayer.PlayerOnEvent_Text` appelait `Present`.
      Sans ce temoin, un montage casse rougirait pareil ; avec lui, on sait
      que le montage sait voir une publication quand elle a lieu. Il doit
      rester vert : c'est lui qui prouve qu'on a corrige le defaut au lieu
      de rendre le cas insensible.
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

    # `etape` mene la sequence ; les deux temoins sont des couples
    # (numero de trame, manuel_actif publie) releves a la question SUIVANTE.
    etat = {"etape": "attend_mulligan", "compte": 0,
            "defaut": None, "contraste": None,
            "avant_defaut": None, "avant_contraste": None, "fini": False}

    def poser_la_pause(gestionnaire, actif):
        """Les deux vrais fils, dans l'ordre (voir l'en-tete)."""
        jeu.world.BasculerPauseManuelle(actif, "Diagnostic")
        assert gestionnaire.pause_a_publier, (
            "premisse cassee : BasculerPauseManuelle n'a pas pose le "
            "marqueur que DoGetInput consomme"
        )
        gestionnaire.pause_a_publier = False

    def pilote(self, data, player_id=None, check=None):
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        etat["compte"] += 1
        if etat["compte"] > PLAFOND_QUESTIONS:
            while True:
                time.sleep(0.5)

        rendu = jeu.world.render
        trame = (rendu.last_render_id,
                 getattr(rendu.descriptor, "manuel_actif", None))
        evenement = data.event_name

        if etat["etape"] == "attend_mulligan":
            if evenement == "WhenPlayerChooseAbility":
                assert trame[1] is False, (
                    f"premisse cassee : la trame publie deja "
                    f"manuel_actif={trame[1]!r} avant toute pause"
                )
                etat["avant_defaut"] = trame
                etat["question_visee"] = evenement
                poser_la_pause(self, True)
                etat["etape"] = "releve_defaut"
                return None

        elif etat["etape"] == "releve_defaut":
            assert evenement == etat["question_visee"], (
                f"premisse cassee : le moteur n'a pas re-pose la MEME "
                f"question ({evenement} au lieu de {etat['question_visee']})"
            )
            etat["defaut"] = trame
            # On reprend, sinon la porte des declencheurs reste fermee
            # (cf. cas_pause_ferme_la_porte) et le tour du heros ne poserait
            # plus aucune question -- le temoin 2 n'aurait plus de support.
            poser_la_pause(self, False)
            etat["etape"] = "attend_tour"
            return None

        elif etat["etape"] == "attend_tour":
            if evenement == "WhenPlayerInTurn":
                etat["avant_contraste"] = trame
                etat["question_visee"] = evenement
                poser_la_pause(self, True)
                etat["etape"] = "releve_contraste"
                return None

        elif etat["etape"] == "releve_contraste":
            etat["contraste"] = trame
            poser_la_pause(self, False)
            etat["etape"] = "fini"
            etat["fini"] = True
            return None

        # Reponse ordinaire : la premiere option jouable.
        legales = [o for o in options
                   if isinstance(o, dict) and not o.get("failure_reason")]
        if not legales:
            return None
        o = legales[0]
        cibles = [str(x) for x in (o.get("all_legal_targets") or [])]
        mini = (o.get("target_num_range") or [0, 0])[0]
        return json.dumps({"id": str(o.get("id", 0)),
                           "targets": cibles[:mini], "resources": []})

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader

    with open(_chemin_json("Campaign", "rhino")) as f:
        campagne = f.read()
    with open(_chemin_json("Hero", "spider_man")) as f:
        hero = f.read()
    scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, [], {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        import traceback
        while True:
            try:
                if jeu.GameSetup():
                    jeu.GameLoop()
            except BaseException:
                traceback.print_exc()
                return
            if jeu.state.start_state.state:
                continue
            jeu.state.SetRunningState(False)
            jeu.state.WaitUntilGameStart()

    threading.Thread(target=run, daemon=True).start()

    limite = time.time() + 90
    while not etat["fini"] and time.time() < limite:
        time.sleep(0.5)

    assert etat["defaut"] is not None, (
        "la sequence n'a jamais atteint le premier releve : rien n'est prouve"
    )
    assert etat["contraste"] is not None, (
        "la sequence n'a jamais atteint le releve de contraste : rien n'est "
        "prouve"
    )

    # TEMOIN 2 d'abord : il valide le montage.
    assert etat["contraste"][1] is True, (
        f"MONTAGE SUSPECT : meme sur une question de tour de heros, la "
        f"pause n'a pas ete publiee (trame {etat['avant_contraste']} -> "
        f"{etat['contraste']}). Ce cas ne peut rien prouver dans cet etat."
    )

    # TEMOIN 1 : le defaut.
    assert etat["defaut"][1] is True, (
        f"LE PLATEAU NE DEVIENT PAS MUET : pause posee pendant une question "
        f"deja ouverte (mulligan), la question est re-posee a l'identique "
        f"mais AUCUN rendu n'a lieu entre les deux -- trame "
        f"{etat['avant_defaut']} -> {etat['defaut']} (numero de trame "
        f"inchange, manuel_actif publie toujours faux), alors que "
        f"world.manuel_actif={jeu.world.manuel_actif}. Le meme geste sur une "
        f"question de tour de heros publie bien "
        f"({etat['avant_contraste']} -> {etat['contraste']}). Regarder "
        f"d'abord le rendu force de Controller.ChoiceOne sur "
        f"`if user_input == None` (tache 8) : sans lui, le seul rendu de ce "
        f"chemin est SenderPlayer.PlayerOnEvent_Text, qui n'appelle Present "
        f"que si le message est un WhenPlayerInTurn."
    )
    return ("la pause posee pendant une question deja ouverte est publiee "
            "sur la trame suivante, mulligan compris")


def monter_avec_geste_par_le_vrai_dogetinput(game_dir, port, commande_pour):
    """Monte une partie ORDINAIRE, la met en pause, et y fait passer UN geste
    manuel par le VRAI `DeviceManager.DoGetInput` -- la branche de drainage
    qu'emprunte une pause de partie ORDINAIRE, et qu'aucun autre cas de ce
    fichier ne traverse.

    ⚠ POURQUOI PAS `monter_le_moteur`. Celui-ci REMPLACE `DoGetInput` par son
    `pilote` pour toute la duree du processus (cf. son en-tete) : les cas qui
    passent par lui observent le drainage de `World.ManualLoop`, jamais celui
    de `DoGetInput`. Or c'est exactement l'inverse qu'il faut ici. Une partie
    ORDINAIRE n'entre JAMAIS dans `ManualLoop` (`World.OnGameLoop` n'y va que
    sous `rule.mode_manuel`) : son fil de jeu est gare dans une QUESTION, et
    c'est `DoGetInput`, et lui seul, qui draine les gestes. Ce montage garde
    donc le VRAI `DoGetInput` et s'en sert comme d'un DELEGUE : le pilote
    local repond a sa place pour les questions ordinaires, et lui rend la
    main aux deux moments qui comptent.

    Meme scenario, meme graine et meme boucle `run()` que `monter_le_moteur`,
    a la seule difference du pilote -- meme parti pris que
    `cas_pause_publiee_pendant_question_ouverte`.

    `commande_pour(jeu)` rend la commande `Puzzle.*` a deposer ; il n'est
    appele qu'une fois la table montee, seul moment ou l'identifiant du
    vilain est lisible.

    Rend `(jeu, commande, etat)`. A la sortie, la table est EN PAUSE, le
    geste est applique, et le pilote est GARE sur une question ouverte : plus
    rien ne bouge tant que personne n'agit. C'est l'image exacte d'une vraie
    table en pause, et la seule facon d'avoir un etat STABLE a sauvegarder ou
    a annuler -- un pilote qui continuerait a jouer ferait varier les points
    de vie du vilain entre la mesure et la sauvegarde.
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

    # LE VRAI, capture AVANT tout remplacement : c'est lui, et lui seul, qui
    # porte la branche de drainage que ce montage existe pour traverser.
    vrai_dogetinput = DeviceManager.DoGetInput

    etat = {"etape": "attend_tour", "compte": 0, "commande": None, "gares": 0}

    def deposer_depuis_le_fil_http():
        """Ce que fait la route POST /sandbox_command, depuis un AUTRE fil.

        Le court sommeil laisse au fil du jeu le temps d'entrer reellement
        dans le `Wait` du vrai `DoGetInput` : sans lui, on deposerait avant
        l'attente et on ne prouverait rien du reveil.
        """
        from game.puzzle import PuzzleHelper
        time.sleep(1.0)
        gestionnaire = jeu.controller_manager.device_manager
        gestionnaire.sandbox_executor = lambda cmds: PuzzleHelper.Exec(cmds, jeu.world)
        gestionnaire.QueueSandboxCommands([etat["commande"]])

    def se_garer():
        """Le pilote cesse de repondre : la table est figee sur une question.

        ⚠ RESPONSABLE D'UNE SORTIE, a la difference du parking de
        `monter_le_moteur` : `GameSession.Undo` (le bouton « Annuler ») pose
        `is_game_over` puis reveille le fil du jeu, et un parking qui dort
        pour toujours ne lui rendrait JAMAIS la main -- l'annulation ne se
        produirait pas et le cas mesurerait du vide. On rend donc `None` des
        que la partie est donnee pour finie : `ChoiceOne` le remonte, et
        `PlayerAction` (player_action.py, juste apres `ChoiceOne`) sort sur
        `if message.world.is_game_over`.
        """
        etat["gares"] += 1
        while True:
            monde = jeu.world
            if monde is None or monde.is_game_over:
                return None
            time.sleep(0.2)

    def pilote(self, data, player_id=None, check=None):
        etat["compte"] += 1
        if etat["compte"] > PLAFOND_QUESTIONS:
            return se_garer()

        if etat["etape"] == "attend_tour":
            if data.event_name == "WhenPlayerInTurn":
                # Le moment ou un vrai joueur cliquerait « Mettre en pause » :
                # une question l'attend, et c'est elle qui le bloque.
                etat["commande"] = commande_pour(jeu)
                jeu.world.BasculerPauseManuelle(True, "Diagnostic")
                etat["etape"] = "purge_pause"
                return None

        elif etat["etape"] == "purge_pause":
            # La bascule a arme `pause_a_publier` : le vrai `DoGetInput` le
            # consomme et rend la main SANS attendre. On le laisse faire --
            # sinon il ne s'endormirait jamais pour attendre le geste.
            etat["etape"] = "depose"
            return vrai_dogetinput(self, data, player_id, check)

        elif etat["etape"] == "depose":
            threading.Thread(target=deposer_depuis_le_fil_http, daemon=True).start()
            etat["etape"] = "draine"
            # LE CHEMIN MESURE : le fil du jeu se gare dans le vrai
            # `DoGetInput`, un autre fil depose la commande, `DoGetInput` se
            # reveille, draine, et rend la main sans entree. L'enregistrement
            # du geste, lui, a lieu APRES ce retour (dans `ChoiceOne`) : on
            # ne le lit donc jamais d'ici.
            retour = vrai_dogetinput(self, data, player_id, check)
            etat["etape"] = "fini"
            return retour

        elif etat["etape"] in ("draine", "fini", "regare"):
            return se_garer()

        elif etat["etape"] == "attend_regare":
            # Un remontage vient d'avoir lieu (« Annuler ») : ce harnais voit
            # alors la mise en place REDEMANDEE question par question (cf.
            # `cas_annulation_ne_redemande_pas` : le rejeu silencieux des
            # entrees demande un `skip_to` deja negatif, ce que ce montage ne
            # pose pas). On y repond comme au premier passage, puis on se gare
            # de nouveau des que le round 1 a commence : les gestes sont alors
            # rejoues (`GameSession.GameSetup` le fait avant la boucle) et la
            # table est de nouveau mesurable.
            #
            # ⚠ PAS « au prochain WhenPlayerInTurn », ESSAYE ET FAUX : une
            # table qui revient EN PAUSE n'en pose plus aucun. La porte des
            # declencheurs etant fermee, le message du tour de heros ne
            # produit aucun effet et le tour se termine sans rien demander
            # (constate le 20/09/2026 : « Tour de Spider-Man (1) » suivi
            # immediatement de « Fin du tour »). Attendre ce signal-la,
            # c'etait attendre la preuve que la pause a ETE PERDUE.
            monde = jeu.world
            if monde is not None and monde.round_id >= 1:
                etat["etape"] = "regare"
                return se_garer()

        legales = [o for o in (json.loads(data.options_json or "[]") or [])
                   if isinstance(o, dict) and not o.get("failure_reason")]
        if not legales:
            return None
        o = legales[0]
        cibles = [str(x) for x in (o.get("all_legal_targets") or [])]
        mini = (o.get("target_num_range") or [0, 0])[0]
        return json.dumps({"id": str(o.get("id", 0)),
                           "targets": cibles[:mini], "resources": []})

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader

    with open(_chemin_json("Campaign", "rhino")) as f:
        campagne = f.read()
    with open(_chemin_json("Hero", "spider_man")) as f:
        hero = f.read()
    # AUCUNE regle : une partie ORDINAIRE, celle du joueur qui tombe sur un
    # bug en pleine partie -- pas la partie manuelle DECLAREE.
    scene = SceneLoader.NewFromJson(campagne, None, [hero], 42, [], {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        import traceback
        while True:
            try:
                if jeu.GameSetup():
                    jeu.GameLoop()
            except BaseException:
                traceback.print_exc()
                return
            if jeu.state.start_state.state:
                continue
            jeu.state.SetRunningState(False)
            jeu.state.WaitUntilGameStart()

    threading.Thread(target=run, daemon=True).start()

    limite = time.time() + 120
    while not etat["gares"] and time.time() < limite:
        time.sleep(0.5)
    assert etat["gares"], (
        f"la sequence n'est jamais arrivee a la table figee (etape="
        f"{etat['etape']!r}, {etat['compte']} question(s) posees) : rien "
        "n'est prouve"
    )
    time.sleep(2)
    assert jeu.world.manuel_actif is True, \
        "premisse cassee : la table n'est pas en pause apres la bascule"
    return jeu, etat["commande"], etat


def cas_geste_ordinaire_entre_dans_la_scene(game_dir, port):
    """Un geste fait pendant la pause d'une partie ORDINAIRE entre dans la
    scene -- donc dans la sauvegarde. Constat C1 de la revue finale.

    ⚠ CE CAS A ETE ECRIT ROUGE (mesure du 20/09/2026). La branche de drainage
    de `DoGetInput` appelait bien `DrainSandboxCommands` mais JETAIT son
    retour : elle ne s'en servait que comme d'un booleen (« un drainage a eu
    lieu »). `World.ManualLoop`, elle, fait `scene.manuel_commands +=
    appliquees` depuis toujours (world.py). Les gestes d'une partie manuelle
    DECLAREE survivaient donc, ceux d'une pause de partie ORDINAIRE non.

    C'est le pendant exact de `cas_geste_enregistre` (qui couvre, lui, la
    partie DECLAREE), sur l'autre chemin de drainage.
    """
    jeu, commande, _ = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: f"Puzzle.Damage({id_du_vilain(jeu.world)}, 3)")

    vilain = id_du_vilain(jeu.world)
    carte = jeu.world.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, (
        f"premisse cassee : le geste n'a meme pas ete applique au monde "
        f"(degats={carte.face.GetLostHealth()}, attendu 3) -- ce n'est pas "
        "l'enregistrement qui manque, c'est le drainage"
    )

    gestes = jeu.session.scene.manuel_commands
    assert gestes == [commande], (
        f"la correction faite pendant la pause d'une partie ORDINAIRE n'est "
        f"pas entree dans la scene : {gestes} (attendu [{commande!r}]). Elle "
        "disparaitra donc a la premiere sauvegarde, au premier rechargement "
        "et au premier « Annuler ». Regarder la branche de drainage de "
        "`DeviceManager.DoGetInput` : elle jette le retour de "
        "`DrainSandboxCommands`, la ou `World.ManualLoop` l'enregistre."
    )
    return ("un geste fait pendant la pause d'une partie ordinaire entre "
            "dans la scene, comme en partie manuelle declaree")


def cas_geste_ordinaire_survit_sauvegarde(game_dir, port):
    """« Sauver » puis recharger ne perd ni la correction ni la pause.

    ⚠ CE CAS A ETE ECRIT ROUGE (constat C1 de la revue finale). Une
    sauvegarde n'est PAS un instantane de la table : `Scene` ne porte que la
    graine, les regles, les joueurs, les entrees -- et `GameSetup` REJOUE.
    Deux choses manquaient sur le chemin d'une partie ordinaire : le geste
    n'entrait pas dans `scene.manuel_commands` (cf.
    `cas_geste_ordinaire_entre_dans_la_scene`), et le rejeu au montage etait
    garde par `if self.world.rule.mode_manuel` -- la REGLE, jamais vraie sur
    une partie ordinaire -- au lieu de la presence de gestes a rejouer.

    Meme gabarit que `cas_aller_retour`/`cas_relire_sauvegarde` : le fils
    relit la sauvegarde dans SON PROPRE processus, seule facon de prouver que
    le geste est ECRIT dans le fichier et REJOUE au montage, et pas seulement
    tenu en memoire par cet objet `Scene`.
    """
    jeu, commande, _ = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: f"Puzzle.Damage({id_du_vilain(jeu.world)}, 3)")

    vilain = id_du_vilain(jeu.world)
    carte = jeu.world.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() == 3, \
        f"premisse cassee : degats={carte.face.GetLostHealth()}, attendu 3"

    # Nom NU, pas un chemin absolu : meme raison que `cas_aller_retour`, dont
    # le commentaire detaille le piege de `FileManager.FindJsonPath` sous WSL.
    nom = "manuel-ordinaire-aller-retour.json"
    ecrit = jeu.session.SaveScene(name=nom, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    env["MC_VILAIN"] = str(vilain)
    env["MC_COMMANDE"] = commande
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_geste_ordinaire", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-3000:]}\n{fils.stderr[-3000:]}"
    return ("la correction faite pendant la pause d'une partie ordinaire "
            "survit a une sauvegarde puis un rechargement")


def cas_relire_geste_ordinaire(game_dir, port):
    """Le fils de `cas_geste_ordinaire_survit_sauvegarde`.

    ⚠ OU SE PREND LA MESURE, ET POURQUOI PAS A LA FIN. `cas_relire_sauvegarde`
    peut lire les degats 20 s apres le montage parce que sa partie est
    DECLAREE manuelle : `ManualLoop` fige tout, plus rien ne bouge. Une partie
    ORDINAIRE, elle, continue de derouler ses tours meme en pause (la pause ne
    ferme que la porte des declencheurs, cf. `cas_pause_ferme_la_porte`) : le
    pilote joue, le heros frappe, et les degats du vilain ne valent plus 3
    depuis longtemps. On releve donc a la PREMIERE question posee apres le
    debut du round 1 -- le rejeu des gestes a lieu dans `GameSetup`, donc
    avant, et le heros n'a encore rien fait, donc les 3 degats ne peuvent
    venir que du geste rejoue.
    """
    chemin = os.environ["MC_SAUVEGARDE"]
    vilain = int(os.environ["MC_VILAIN"])
    commande = os.environ["MC_COMMANDE"]

    releve = {}

    def au_premier_tour(jeu):
        if "pv" in releve:
            return
        monde = jeu.world
        if monde is None or monde.round_id < 1:
            return
        carte = monde.object_manager.card_dict.get(vilain)
        releve["pv"] = carte.face.GetLostHealth() if carte is not None else None
        releve["muet"] = bool(monde.manuel_actif)

    jeu, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin,
                                     avant_reponse=au_premier_tour)

    assert bool(monde.rule.mode_manuel) is False, \
        "premisse cassee : la sauvegarde relue est une partie manuelle DECLAREE"

    gestes = jeu.session.scene.manuel_commands
    assert gestes == [commande], \
        f"la sauvegarde ne porte pas le geste : {gestes} (attendu [{commande!r}])"

    assert "pv" in releve, (
        "la partie rechargee n'a pose aucune question apres le debut du "
        "round 1 : rien n'a pu etre mesure"
    )
    assert releve["pv"] == 3, (
        f"la correction n'a pas ete rejouee au montage : degats="
        f"{releve['pv']!r}, attendu 3. Le rejeu de `GameSetup` est garde par "
        "la REGLE `mode_manuel`, jamais vraie sur une partie ordinaire, au "
        "lieu de la presence de gestes a rejouer."
    )
    assert releve["muet"] is True, (
        "la partie rechargee a repris toute seule : elle etait EN PAUSE au "
        "moment de la sauvegarde, elle revient bavarde -- le joueur retombe "
        "dans le bug qu'il venait de contourner"
    )
    return ("la partie ordinaire rechargee porte la correction et revient "
            "encore en pause")


def cas_annulation_ordinaire_garde_tout(game_dir, port):
    """« Annuler » ne fait disparaitre ni les corrections ni la pause.

    ⚠ CE CAS A ETE ECRIT ROUGE, et c'est le pire des trois chemins du constat
    C1. Le bouton « Annuler » du plateau appelle `/debug?/undo auto`, donc
    `Cheat.do_undo`, donc `GameSession.Undo`, qui rejoue les ENTREES du
    joueur : toutes les corrections s'evaporaient d'un coup, pas seulement la
    derniere. Et comme il RECONSTRUIT le `World`, `manuel_actif` retombait a
    faux par defaut : le clic reprenait AUSSI la partie en silence, bandeau
    compris. Le joueur revenait exactement dans le bug qu'il venait de
    contourner, apres avoir clique sur un bouton qui n'avait rien a voir.

    ⚠ `GameSession.Undo` ET PAS `AnnulerDernierGeste` (cf. `cas_annulation`) :
    ce sont deux boutons differents. `AnnulerDernierGeste` est le Ctrl+Z du
    mode manuel DECLARE (`/manuel_undo`), qui retire le dernier geste ; celui
    d'ici est l'« Annuler » ordinaire de la barre du haut, qui ne connait que
    les entrees et n'a jamais rien su des gestes.

    ⚠ CE QUE CE HARNAIS NE REPRODUIT PAS, dit ici plutot que devine plus
    tard : apres l'annulation, la mise en place est REDEMANDEE question par
    question au lieu d'etre rejouee en silence depuis `scene.inputs` -- meme
    limite, et meme cause, que celle que decrit `cas_annulation_ne_redemande_pas`
    (le rejeu silencieux exige un `skip_to` deja negatif, que ce montage ne
    pose pas). Cela ne change rien a ce qui est mesure ici (les gestes, la
    pause, les degats au premier tour de heros), mais cela explique pourquoi
    le pilote doit rejouer la mise en place avant de se garer une seconde fois.
    """
    jeu, commande, etat = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: f"Puzzle.Damage({id_du_vilain(jeu.world)}, 3)")

    vilain = id_du_vilain(jeu.world)
    monde_avant = jeu.world
    assert monde_avant.object_manager.card_dict[vilain].face.GetLostHealth() == 3, \
        "premisse cassee : le geste n'a pas ete applique avant l'annulation"

    # Le dernier maillon de `Cheat.do_undo`, celui que le bouton atteint.
    # Le pilote, gare sur sa question, rend la main des que l'annulation pose
    # `is_game_over`, rejoue la mise en place redemandee, puis se gare de
    # nouveau au premier tour de heros -- la table est alors figee une
    # seconde fois, donc de nouveau mesurable.
    etat["etape"] = "attend_regare"
    jeu.session.Undo(1)

    limite = time.time() + 180
    while etat["gares"] < 2 and time.time() < limite:
        time.sleep(0.5)
    assert etat["gares"] >= 2, (
        f"la partie n'est jamais revenue a une table figee apres "
        f"l'annulation (etape={etat['etape']!r}, {etat['compte']} question(s) "
        "posees) : rien n'est prouve"
    )
    time.sleep(2)

    monde_apres = jeu.world
    assert monde_apres is not monde_avant, (
        "premisse cassee : l'annulation n'a PAS reconstruit le monde, ce cas "
        "ne mesure donc rien du defaut qu'il vise"
    )

    gestes = jeu.session.scene.manuel_commands
    assert gestes == [commande], (
        f"« Annuler » a efface les corrections : {gestes} (attendu "
        f"[{commande!r}])"
    )

    carte = monde_apres.object_manager.card_dict[vilain]
    assert carte.face.GetLostHealth() >= 3, (
        f"« Annuler » a perdu la correction sur la table : degats="
        f"{carte.face.GetLostHealth()}, au moins 3 attendus"
    )

    assert monde_apres.manuel_actif is True, (
        "« Annuler » a REPRIS la partie en silence : personne ne l'a demande, "
        "le bandeau de pause disparait, et le joueur retombe dans le bug "
        "qu'il venait de contourner"
    )
    return ("« Annuler » garde les corrections ET la pause : la partie ne "
            "reprend pas toute seule")

CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "manuel_actif_pas_avant_la_boucle": cas_manuel_actif_pas_avant_la_boucle,
    "moteur_muet": cas_moteur_muet,
    "automatique_avance": cas_automatique_avance,
    "commande_executee": cas_commande_executee,
    "aucun_declenchement": cas_aucun_declenchement,
    "declenchement_en_automatique": cas_declenchement_en_automatique,
    "sbire_reste_en_jeu": cas_sbire_reste_en_jeu,
    "sbire_vaincu_en_automatique": cas_sbire_vaincu_en_automatique,
    "deplacement_libre": cas_deplacement_libre,
    "melange": cas_melange,
    "ecart": cas_ecart,
    "ecart_scenario": cas_ecart_scenario,
    "dessous_sans_ordre": cas_dessous_sans_ordre,
    "geste_enregistre": cas_geste_enregistre,
    "aller_retour": cas_aller_retour,
    "relire_sauvegarde": cas_relire_sauvegarde,
    "annulation": cas_annulation,
    "annulation_ne_redemande_pas": cas_annulation_ne_redemande_pas,
    "annulation_fin_declaree": cas_annulation_fin_declaree,
    "attache": cas_attache,
    "engagement": cas_engagement,
    "geste_refuse_non_enregistre": cas_geste_refuse_non_enregistre,
    "ecart_modular": cas_ecart_modular,
    "refus_publie_puis_reparti": cas_refus_publie_puis_reparti,
    "defausse_deck_special": cas_defausse_deck_special,
    "pause_ferme_la_porte": cas_pause_ferme_la_porte,
    "reprise_rouvre_la_porte": cas_reprise_rouvre_la_porte,
    "marque_survit_reprise": cas_marque_survit_reprise,
    "marque_survit_sauvegarde": cas_marque_survit_sauvegarde,
    "relire_marque_survit": cas_relire_marque_survit,
    "qui_et_depuis_publies": cas_qui_et_depuis_publies,
    "pause_par_nom_du_heros": cas_pause_par_nom_du_heros,
    "pause_publiee": cas_pause_publiee,
    "reveil_dogetinput": cas_reveil_dogetinput,
    "geste_refuse_arme_le_rendu": cas_geste_refuse_arme_le_rendu,
    "passer_annule_le_moteur": cas_passer_annule_le_moteur,
    "passer_refuse_question_forcee": cas_passer_refuse_question_forcee,
    "passer_aucune_question": cas_passer_aucune_question,
    "passer_hors_pause": cas_passer_hors_pause,
    "pause_publiee_pendant_question_ouverte": cas_pause_publiee_pendant_question_ouverte,
    "geste_ordinaire_entre_dans_la_scene": cas_geste_ordinaire_entre_dans_la_scene,
    "geste_ordinaire_survit_sauvegarde": cas_geste_ordinaire_survit_sauvegarde,
    "relire_geste_ordinaire": cas_relire_geste_ordinaire,
    "annulation_ordinaire_garde_tout": cas_annulation_ordinaire_garde_tout,
}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    # Les cas appeles par un AUTRE cas, jamais tout seuls.
    SUR_DEMANDE = {"relire_sauvegarde", "relire_marque_survit",
                   "relire_geste_ordinaire"}
    noms = [voulu] if voulu else [n for n in CAS if n not in SUR_DEMANDE]
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
