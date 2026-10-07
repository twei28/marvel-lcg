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

# Le montage qui joue une VRAIE histoire (trois rounds, des cartes
# jouees) en pose bien plus : ce plafond-la lui est propre. Mesure du
# 20/09/2026 : atteindre le round 3 en demande un peu plus de 200.
PLAFOND_QUESTIONS_HISTOIRE = 600

# Combien de questions par round le pilote de ce montage consacre a JOUER
# avant de chercher a finir son tour. Assez pour que l'historique porte
# de vraies cartes jouees, assez peu pour que trois rounds tiennent dans
# le budget de temps d'un cas.
QUESTIONS_JOUEES_PAR_ROUND = 8

# Les options BRUTES de chaque question posee au pilote, dans l'ordre (lot 2
# du 06/10/2026). `journal` ne garde que les noms : pour savoir si une carte
# posee a la main propose bien SA capacite apres la reprise, il faut voir a
# quelle carte chaque option est rattachee.
OPTIONS_VUES = []


def monter_le_moteur(game_dir, port, regles, scenario="rhino", heros="spider_man",
                     sauvegarde=None, avant_reponse=None, rejouer_les_entrees=False):
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
        OPTIONS_VUES.append(options)

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
        # Un nom, ou une LISTE de noms pour une table a plusieurs heros (lot 2
        # du 06/10/2026 : les gestes visent un siege precis).
        liste = list(heros) if isinstance(heros, (list, tuple)) else [heros]
        decks = []
        for nom in liste:
            with open(_chemin_json("Hero", nom)) as f:
                decks.append(f.read())
        scene = SceneLoader.NewFromJson(campagne, None, decks, 42, regles, {})

    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    if rejouer_les_entrees:
        # LE REJEU SILENCIEUX DES ENTREES, celui d'une VRAIE ouverture de
        # sauvegarde (ronde de correction 1 du 20/09/2026).
        #
        # Sans cette ligne, `InitializeSkip` (engine/controller/manager.py)
        # laisse `skip_to` a 0 pour l'etat "Load" et le moteur REDEMANDE
        # chaque question au lieu de rejouer les reponses deja donnees --
        # c'est la meme convention, et le meme piege, que decrit
        # `GameSession.AnnulerDernierGeste`. La production, elle, passe par
        # `GameSession.Load` avec un chemin suffixe `:-1`, qui pose
        # exactement ce `-1` : on le pose ici a la main, faute de passer par
        # cette route. Indispensable des qu'un cas veut mesurer ce que le
        # REJEU fait de la table, et pas seulement ce qu'une partie rejouee
        # de zero produirait.
        jeu.controller_manager.skip.SetSkipTo(-1)

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


def signature_de_table(monde):
    """Une empreinte COMPARABLE de la table, pour mettre deux montages en
    regard (ronde de correction 1 du 20/09/2026).

    Ni exhaustive ni canonique : juste assez pour qu'une table VIERGE ne
    puisse pas passer pour celle du joueur. Trois familles, choisies parce
    que chacune casse sur un mecanisme different :

    - `round` : un rejeu qui n'a pas consomme ses entrees reste au round 1 ;
    - `cartes_en_jeu`, avec l'IDENTIFIANT D'OBJET de chaque carte : un geste
      rejoue trop tot fait naitre des objets qui volent les identifiants que
      le rejeu attribuera ensuite a d'autres cartes -- le decalage se lit
      ici, et nulle part ailleurs ;
    - les tailles de main, de deck et de defausse : un flux aleatoire decale
      (un `Shuffle`, un `Draw`, un `Reveal` rejoue au mauvais rang) les fait
      diverger meme quand la table a l'air juste.
    """
    def valeur(face):
        """Le compteur qui a un sens pour CETTE carte, ou None.

        Toutes les faces en jeu ne portent pas de points de vie : une
        machination n'a que de la menace (`face.threat`), et lui demander
        `GetLostHealth` leve un `AttributeError` -- constate le 20/09/2026,
        le premier jet de cette empreinte cassait sur la machination
        principale des la premiere mesure.
        """
        perte = getattr(face, "GetLostHealth", None)
        if callable(perte):
            return int(perte())
        menace = getattr(face, "threat", None)
        if isinstance(menace, int):
            return int(menace)
        return None

    cartes = []
    for object_id, objet in sorted(monde.object_manager.card_dict.items()):
        face = objet.face
        if face is None or not face.IsInPlay():
            continue
        cartes.append([int(object_id),
                       getattr(getattr(face, "paper", None), "card_id", ""),
                       valeur(face)])
    joueur = monde.players[0]
    return {
        "round": int(monde.round_id),
        "cartes_en_jeu": cartes,
        "main": joueur.hand_cards.GetSize(),
        "deck": joueur.player_deck.GetSize(),
        "defausse": joueur.discard_pile.GetSize(),
    }


def comparer_les_tables(attendue, obtenue):
    """Rend la liste des ecarts, en clair. Vide = tables identiques."""
    ecarts = []
    for cle in ("round", "main", "deck", "defausse"):
        if attendue.get(cle) != obtenue.get(cle):
            ecarts.append(f"{cle} : {attendue.get(cle)!r} attendu, "
                          f"{obtenue.get(cle)!r} obtenu")
    a = {tuple(c[:2]): c[2] for c in attendue.get("cartes_en_jeu", [])}
    b = {tuple(c[:2]): c[2] for c in obtenue.get("cartes_en_jeu", [])}
    for cle in sorted(set(a) | set(b), key=lambda k: (k[0], str(k[1]))):
        if a.get(cle) != b.get(cle):
            ecarts.append(f"carte c{cle[0]} ({cle[1]}) : compteur "
                          f"{a.get(cle, 'absente')!r} attendu, "
                          f"{b.get(cle, 'absente')!r} obtenu")
    return ecarts


def cas_drapeau_pose(game_dir, port):
    """Le drapeau existe, la liste de regles l'allume, et la trame le publie."""
    _, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert bool(monde.rule.mode_manuel) is True, \
        "la regle mode_manuel n'a pas ete posee"
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "mode_manuel", None) is True, \
        "la trame ne publie pas mode_manuel"
    return "le drapeau mode_manuel est pose et publie"


def cas_campagne_publiee(game_dir, port):
    """La regle `mode_campaign` est publiee a TOUS les sieges, et vraie ou fausse.

    Defaut du 07/10/2026 : une victoire en partie ORDINAIRE ouvrait les
    recompenses d'une campagne, parce que le plateau deduisait la campagne
    d'un etat durable (cle du navigateur, `partieEnCours` du serveur) qu'une
    partie ordinaire n'efface pas. Le plateau se regle desormais sur la regle du
    moteur ; ce cas verrouille qu'elle est bien publiee, DANS LES DEUX SENS
    (un descripteur qui rendrait toujours vrai ferait rouvrir le panneau partout).
    """
    _, monde, _ = monter_le_moteur(game_dir, port, ["mode_campaign"])
    assert bool(monde.rule.mode_campaign) is True, \
        "la regle mode_campaign n'a pas ete posee"
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "mode_campaign", None) is True, \
        "la trame ne publie pas mode_campaign pour une partie de campagne"
    return "mode_campaign est vrai dans la trame d'une partie de campagne"


def cas_campagne_absente_hors_campagne(game_dir, port):
    """Le temoin : une partie ordinaire publie `mode_campaign` FAUX."""
    _, monde, _ = monter_le_moteur(game_dir, port, [])
    assert bool(monde.rule.mode_campaign) is False
    descripteur = monde.render.descriptor
    assert getattr(descripteur, "mode_campaign", None) is False, \
        "la trame d'une partie ordinaire ne publie pas mode_campaign faux"
    return "mode_campaign est faux dans la trame d'une partie ordinaire"


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
    # `round_id` vaut 1 (le round joue a la main, cas_round_partie_declaree) :
    # c'est l'etat de phase qui dit si le moteur a demarre un tour.
    assert monde.phase.state == "Init Finished", \
        f"le moteur a demarre un tour tout seul : phase={monde.phase.state!r}"
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
    assert monde.phase.state == "Init Finished", \
        f"le moteur a demarre un tour tout seul : phase={monde.phase.state!r}"
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
        "epoch_pose": 0.0,
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
            assert not getattr(descripteur, "pause_epoch", 0.0), \
                "une partie jamais mise en pause publie deja pause_epoch"

        if not etat["pause_posee"] and etat["compte"] >= 5:
            etat["pause_posee"] = True
            jeu.world.BasculerPauseManuelle(True, "Nick Fury")
            assert jeu.world.scene.pause_par == "Nick Fury", \
                "pause_par n'a pas pris le pseudo transmis sur la scene"
            assert jeu.world.scene.pause_a != "", \
                "pause_a est reste vide sur la scene alors que la pause est posee"
            # L'instant, sans fuseau : c'est de LUI que le plateau tire
            # « depuis 12 min », l'heure murale du serveur ne voulant rien
            # dire pour un joueur distant (revue finale, 20/09/2026).
            assert jeu.world.scene.pause_epoch > 0, \
                "pause_epoch est reste a zero sur la scene alors que la pause est posee"
            etat["epoch_pose"] = jeu.world.scene.pause_epoch
            return

        if etat["pause_posee"] and not etat["vu_qui"]:
            if pause_par_publie == "Nick Fury":
                etat["vu_qui"] = True
                assert getattr(descripteur, "pause_a", None) not in (None, ""), \
                    "pause_par est publie mais pause_a reste vide"
                assert getattr(descripteur, "pause_epoch", 0.0) == etat["epoch_pose"], (
                    "la trame ne publie pas pause_epoch : le bandeau ne peut "
                    "pas dire « depuis » autrement qu'en heure du serveur"
                )
                jeu.world.BasculerPauseManuelle(False)
                etat["reprise_posee"] = True
            return

        if etat["reprise_posee"] and not etat["vu_vide_apres_reprise"]:
            if pause_par_publie == "":
                etat["vu_vide_apres_reprise"] = True
                assert getattr(descripteur, "pause_a", None) == "", \
                    "pause_a reste publie apres la reprise"
                assert not getattr(descripteur, "pause_epoch", 0.0), \
                    "pause_epoch reste publie apres la reprise"

    monter_le_moteur(game_dir, port, [], avant_reponse=observateur)

    assert etat["pause_posee"], \
        "la pause n'a jamais ete posee : ce cas n'a rien pu prouver"
    assert etat["vu_qui"], (
        "la trame n'a jamais publie pause_par='Nick Fury' apres la bascule"
    )
    assert etat["vu_vide_apres_reprise"], (
        "la trame n'a jamais republie pause_par vide apres la reprise"
    )
    return ("pause_par/pause_a/pause_epoch : vides par defaut, poses (qui, "
            "depuis) a la pause, RE-VIDES apres la reprise -- sur la scene et "
            "sur la trame")


class _RequeteFactice:
    """Un `web.Request` minimal : juste ce que lisent `tient_le_siege`,
    `nom_du_heros_qui_parle` (`server_base.py`) et `SpectateurPeutEcrire`
    (`web_server.py`) -- des cookies, un chemin, et un corps JSON. Pas de vrai
    socket : meme esprit que `cas_reveil_dogetinput`, qui construit un
    `DeviceManager` nu plutot que de monter un serveur complet.
    """
    def __init__(self, cookies, corps, chemin="/manuel_pause"):
        self.cookies = cookies
        self.path = chemin
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


def cas_post_ferme_au_spectateur(game_dir, port):
    """AUCUNE route POST ne s'ouvre a un spectateur (I2 de la revue finale).

    ⚠ C'EST LE CAS QUI COMPTE, et il vise l'ENROBAGE, pas une route :
    `AddPostSecurity` ne verifiait que `IsAuthenticate` -- le mot de passe de
    la TABLE, que le spectateur possede (sa porte d'entree le lui pose). Seul
    `/post` se defendait, par un autre chemin (`get_player_ids`). Toutes les
    autres routes POST lui etaient ouvertes, `/manuel_passer` comprise, qui
    REPOND A LA PLACE du joueur interroge.

    On mesure donc la VRAIE `WebServer.AddPostSecurity` : on lui fait
    enregistrer une route, on recupere l'enrobage qu'elle pose dans le
    routeur, et on le frappe comme le ferait un `curl`.

    Trois temoins :
      1. le spectateur est refuse (403) ET le gestionnaire n'est JAMAIS
         atteint -- un 403 rendu par la route elle-meme ne prouverait rien de
         l'enrobage ;
      2. le meme appel SANS le temoin de spectateur passe (temoin de
         controle : sans lui, le 403 pourrait venir de n'importe quoi) ;
      3. une route ajoutee DEMAIN, dont personne n'a jamais entendu parler
         ici, est fermee elle aussi -- c'est tout l'interet du refus par
         defaut, et une liste d'interdits echouerait ce temoin-la.

    Aucun moteur monte : comme `cas_reveil_dogetinput`, ce cas n'a besoin que
    d'une classe, pas d'une partie.
    """
    import asyncio
    import sys
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.network.web_server import WebServer

    enregistrees = {}

    class _Routeur:
        def add_post(self, chemin, handle):
            enregistrees[chemin] = handle

    class _AppFactice:
        def __init__(self):
            self.router = _Routeur()

    serveur = WebServer.__new__(WebServer)
    serveur.web_app = _AppFactice()
    # Table SANS mot de passe : `IsAuthenticate` rend vrai pour tout le monde.
    # C'est le pire cas pour nous, et le cas reel d'une partie locale ouverte.
    serveur.hash_password = ""

    atteints = []

    async def gestionnaire(request):
        from aiohttp import web
        atteints.append(getattr(request, "path", "?"))
        return web.Response(status=200)

    serveur.AddPostSecurity("/manuel_passer", gestionnaire)
    serveur.AddPostSecurity("/route_ajoutee_demain", gestionnaire)
    assert set(enregistrees) == {"/manuel_passer", "/route_ajoutee_demain"}, \
        "AddPostSecurity n'a pas enregistre les routes attendues"

    spectateur = _RequeteFactice({"spectateur": "1"}, {}, "/manuel_passer")
    reponse = asyncio.run(enregistrees["/manuel_passer"](spectateur))
    assert reponse.status == 403, (
        f"le moteur laisse un spectateur appeler POST /manuel_passer "
        f"(HTTP {reponse.status}) : il repond a la place d'un joueur assis"
    )
    assert atteints == [], \
        f"le gestionnaire a ete atteint malgre le refus : {atteints}"

    # TEMOIN DE CONTROLE : exactement la meme requete, sans le temoin.
    ordinaire = _RequeteFactice({}, {}, "/manuel_passer")
    reponse = asyncio.run(enregistrees["/manuel_passer"](ordinaire))
    assert reponse.status == 200, (
        f"un client ordinaire est refuse lui aussi (HTTP {reponse.status}) : "
        f"le 403 du spectateur ne prouve rien"
    )
    assert atteints == ["/manuel_passer"], \
        f"le gestionnaire n'a pas ete atteint par le client ordinaire : {atteints}"

    # La route que personne n'a prevue : fermee d'office.
    demain = _RequeteFactice({"spectateur": "1"}, {}, "/route_ajoutee_demain")
    reponse = asyncio.run(enregistrees["/route_ajoutee_demain"](demain))
    assert reponse.status == 403, (
        f"une route POST ajoutee apres coup s'ouvre au spectateur "
        f"(HTTP {reponse.status}) : le refus n'est pas par defaut"
    )

    return ("AddPostSecurity ferme TOUTE route POST a un spectateur, y compris "
            "une route ajoutee apres coup, et laisse passer le client ordinaire")


def cas_pause_refusee_au_spectateur(game_dir, port):
    """Les routes de la pause exigent un SIEGE (I2), second verrou.

    `AddPostSecurity` arrete deja le spectateur en amont (cas ci-dessus).
    Celui-ci mesure la garde des ROUTES elles-memes, sur une vraie partie :
    elle tiendrait encore si l'enrobage venait a sauter, et elle vaut aussi
    pour un client qui connait le mot de passe de la table sans tenir aucun
    siege.

    ⚠ LE TEMOIN N'EST PAS SEULEMENT LE CODE HTTP : on verifie que la partie
    n'a RIEN garde du passage -- ni `manuel_actif`, ni la marque
    « corrigee a la main », qui ne s'efface jamais une fois posee et salirait
    pour toujours une partie a laquelle le spectateur n'a pas touche.

    ⚠ LES QUATRE SIEGES SONT PROTEGES ET TENUS (ronde de correction 1).
    Sinon le temoin de controle ne discrimine rien : `allowed_seats` accorde
    tout siege non protege A TOUT LE MONDE, et tout siege ORPHELIN a tout
    client authentifie (« reprise d'un siege abandonne »). L'appel de
    controle serait donc passe sans son cookie. La tenue des sieges est
    simulee sur NOTRE instance de serveur (`seat_orphelin`) : aucun socket
    n'existe dans ce harnais, et le moteur n'est pas touche. Voir
    `cas_gestes_refuses_sans_siege`, qui mesure les deux branches.
    """
    import asyncio

    jeu, monde, _ = monter_le_moteur(game_dir, port, [])

    from engine.device.web.server.server_get import GameServerGet
    from engine.device.web.server.server_base import SEAT_PASSWORDS

    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = jeu.world.controller_manager.device_manager

    ancien_mdp = list(SEAT_PASSWORDS.value)
    try:
        # Une table PROTEGEE, LES QUATRE SIEGES (ronde de correction 1).
        #
        # ⚠ NE PAS LAISSER UN SIEGE SANS MOT DE PASSE ICI. `allowed_seats`
        # accorde tout siege volontairement non protege a n'importe quel
        # client : avec ["secret-0", "secret-1", "", ""], le temoin de
        # controle plus bas passait par les sieges 2 et 3, donc MEME SANS le
        # cookie `seat_token_0`. Il prouvait encore « un non-spectateur
        # passe » (ce qui suffit a valider le 403), mais plus « le siege
        # PROUVE passe » -- c'est-a-dire la moitie qui nous interesse.
        SEAT_PASSWORDS.value = ["secret-siege-0", "secret-siege-1",
                                "secret-siege-2", "secret-siege-3"]
        # ... ET TENUS : sans cela, les quatre sieges orphelins de ce harnais
        # seraient accordes a n'importe quel client authentifie.
        serveur.seat_orphelin = lambda siege: False

        spectateur = {"spectateur": "1"}
        reponse = asyncio.run(
            serveur.manuel_pause(_RequeteFactice(spectateur, {"actif": True})))
        assert reponse.status == 403, (
            f"la route a accepte une pause venue d'un spectateur "
            f"(HTTP {reponse.status}) : il arrete la partie des autres"
        )
        assert monde.manuel_actif is False, \
            "le spectateur a quand meme mis la partie en pause"
        assert monde.scene.corrigee_a_la_main is False, (
            "la partie porte la marque « corrigee a la main » apres un refus : "
            "elle ne s'efface jamais, et le spectateur n'a rien corrige"
        )

        reponse = asyncio.run(serveur.manuel_passer(_RequeteFactice(spectateur, {})))
        assert reponse.status == 403, (
            f"la route a accepte un « passer la question » venu d'un "
            f"spectateur (HTTP {reponse.status}) : il repond a la place du "
            f"joueur interroge"
        )

        # ET LE CLIENT SANS SIEGE, qui n'est PAS un spectateur : il connait
        # le mot de passe de la table, rien de plus. C'est lui que la garde de
        # siege ajoute a ce que `SpectateurPeutEcrire` fermait deja.
        reponse = asyncio.run(
            serveur.manuel_pause(_RequeteFactice({}, {"actif": True})))
        assert reponse.status == 403, (
            f"un client sans siege arrete la partie de toute la table "
            f"(HTTP {reponse.status})"
        )
        assert monde.manuel_actif is False, \
            "un client sans siege a quand meme mis la partie en pause"

        # TEMOIN DE CONTROLE : le meme appel depuis un client qui PROUVE le
        # siege 0. Sans lui, le 403 ci-dessus pourrait venir d'autre chose --
        # et avec les quatre sieges tenus, il ne peut plus passer par un
        # siege laisse ouvert.
        import hashlib
        jeton = hashlib.md5("secret-siege-0".encode()).hexdigest()
        assis = _RequeteFactice({"seat_token_0": jeton}, {"actif": True})
        reponse = asyncio.run(serveur.manuel_pause(assis))
        assert reponse.status == 200, (
            f"un joueur assis est refuse lui aussi (HTTP {reponse.status}) : "
            f"le 403 du spectateur ne prouve rien"
        )
        assert monde.manuel_actif is True, \
            "le joueur assis n'a pas reussi a mettre la partie en pause"

        # Et « passer la question » depuis ce meme siege : refuse, mais pour
        # une AUTRE raison (aucune question en attente ici), jamais 403.
        reponse = asyncio.run(
            serveur.manuel_passer(_RequeteFactice({"seat_token_0": jeton}, {})))
        assert reponse.status != 403, (
            "un joueur assis recoit 403 sur /manuel_passer : la garde de "
            "siege refuse ceux qui en tiennent un"
        )
    finally:
        SEAT_PASSWORDS.value = ancien_mdp
        jeu.world.BasculerPauseManuelle(False)

    return ("/manuel_pause et /manuel_passer rendent 403 a qui ne tient aucun "
            "siege, sans rien laisser sur la partie, et acceptent le siege prouve")


def cas_gestes_refuses_sans_siege(game_dir, port):
    """`/sandbox_command` et `/manuel_undo` exigent un siege eux aussi.

    ⚠ C'EST LA PAUSE QUI REND CETTE SURFACE VIVANTE, et c'est pour cela
    qu'elle est de ce chantier. `/sandbox_command` depose des `Puzzle.*` sur
    la partie EN COURS et n'avait aucune garde : avant la pause, il fallait
    une partie en bac a sable ou declaree manuelle pour que le plateau l'arme.
    Depuis la pause, N'IMPORTE QUELLE table ordinaire peut se trouver dans cet
    etat -- un client sans siege pouvait y ecrire.

    ⚠ CE QUE LA GARDE FAIT, ET CE QU'ELLE NE FAIT PAS. `prouve_un_siege` juge
    par `allowed_seats`, exactement comme `/post` : elle rend l'ensemble VIDE
    a un spectateur (refus, toujours), et elle ouvre les sieges ORPHELINS a
    tout client authentifie (« reprise d'un siege abandonne ») -- sans quoi un
    joueur deconnecte bloquerait la table entiere. Un client sans cookie de
    siege est donc refuse quand les sieges sont TENUS, et accepte quand ils ne
    le sont pas. Ce cas mesure LES DEUX, pour que personne ne « corrige » plus
    tard l'un en croyant l'autre casse.

    ⚠ LES SIEGES SONT TENUS PAR SIMULATION. Aucun socket n'est ouvert dans ce
    harnais (`pilote` remplace `DoGetInput`), donc les quatre sieges sont
    orphelins pour de bon. On substitue `seat_orphelin` SUR NOTRE INSTANCE de
    serveur -- la chaine jugee (`allowed_seats` -> `prouve_un_siege` -> route)
    reste la vraie, et le moteur n'est pas touche.
    """
    import asyncio
    import hashlib

    jeu, monde, _ = monter_le_moteur(game_dir, port, [])

    from engine.device.web.server.server_get import GameServerGet
    from engine.device.web.server.server_base import SEAT_PASSWORDS

    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = jeu.world.controller_manager.device_manager
    gestionnaire = serveur.device_manager

    ancien_mdp = list(SEAT_PASSWORDS.value)
    try:
        # LES QUATRE sieges proteges : un seul siege laisse ouvert suffirait a
        # accorder `allowed_seats` a tout le monde, et les temoins ne
        # prouveraient plus rien (meme piege que
        # `cas_pause_refusee_au_spectateur`).
        SEAT_PASSWORDS.value = ["secret-siege-0", "secret-siege-1",
                                "secret-siege-2", "secret-siege-3"]
        commande = {"commands": ["Puzzle.Damage(1, 1)"]}
        jeton = hashlib.md5("secret-siege-0".encode()).hexdigest()

        # --- Les quatre sieges TENUS ---------------------------------------
        serveur.seat_orphelin = lambda siege: False

        gestionnaire.sandbox_commands = []
        sans_siege = _RequeteFactice({}, commande, "/sandbox_command")
        reponse = asyncio.run(serveur.sandbox_command(sans_siege))
        assert reponse.status == 403, (
            f"un client sans siege depose des Puzzle.* sur une table dont "
            f"tous les sieges sont tenus (HTTP {reponse.status}) : depuis la "
            f"pause, toute partie ordinaire peut se trouver dans cet etat"
        )
        assert gestionnaire.sandbox_commands == [], (
            f"la commande a quand meme ete deposee : "
            f"{gestionnaire.sandbox_commands}"
        )

        reponse = asyncio.run(
            serveur.manuel_undo(_RequeteFactice({}, {}, "/manuel_undo")))
        assert reponse.status == 403, (
            f"un client sans siege annule le dernier geste de la table "
            f"(HTTP {reponse.status})"
        )

        # TEMOIN DE CONTROLE : le siege 0, prouve par son cookie. Sans lui, le
        # 403 ci-dessus pourrait venir de n'importe quoi.
        assis = _RequeteFactice({"seat_token_0": jeton}, commande, "/sandbox_command")
        reponse = asyncio.run(serveur.sandbox_command(assis))
        assert reponse.status == 200, (
            f"un joueur assis est refuse lui aussi (HTTP {reponse.status}) : "
            f"le 403 ci-dessus ne prouve rien"
        )
        assert gestionnaire.sandbox_commands == ["Puzzle.Damage(1, 1)"], (
            f"le depot du joueur assis n'est pas arrive dans la file : "
            f"{gestionnaire.sandbox_commands}"
        )
        gestionnaire.sandbox_commands = []

        reponse = asyncio.run(
            serveur.manuel_undo(_RequeteFactice({"seat_token_0": jeton}, {}, "/manuel_undo")))
        assert reponse.status != 403, (
            "un joueur assis recoit 403 sur /manuel_undo : la garde de siege "
            "refuse ceux qui en tiennent un"
        )

        # --- Les sieges ORPHELINS (personne n'est connecte) -----------------
        # Le comportement VOULU, le meme que `/post` : un joueur deconnecte ne
        # doit pas bloquer la table. Le spectateur, lui, reste refuse -- c'est
        # le correctif du 15/09/2026, et il passe AVANT la reprise.
        del serveur.seat_orphelin

        gestionnaire.sandbox_commands = []
        reponse = asyncio.run(serveur.sandbox_command(
            _RequeteFactice({}, commande, "/sandbox_command")))
        assert reponse.status == 200, (
            f"un client authentifie est refuse alors que TOUS les sieges sont "
            f"abandonnes (HTTP {reponse.status}) : plus personne ne peut "
            f"reprendre une table dont les joueurs se sont deconnectes"
        )
        gestionnaire.sandbox_commands = []

        spectateur = _RequeteFactice({"spectateur": "1"}, commande, "/sandbox_command")
        reponse = asyncio.run(serveur.sandbox_command(spectateur))
        assert reponse.status == 403, (
            f"un spectateur depose des Puzzle.* sur une table aux sieges "
            f"abandonnes (HTTP {reponse.status}) : il herite de la place d'un "
            f"joueur deconnecte, defaut mesure le 15/09/2026"
        )
        assert gestionnaire.sandbox_commands == [], \
            "un spectateur a depose une commande malgre le refus"

        reponse = asyncio.run(serveur.manuel_undo(
            _RequeteFactice({"spectateur": "1"}, {}, "/manuel_undo")))
        assert reponse.status == 403, \
            f"un spectateur annule le dernier geste de la table (HTTP {reponse.status})"
    finally:
        SEAT_PASSWORDS.value = ancien_mdp
        gestionnaire.sandbox_commands = []

    return ("/sandbox_command et /manuel_undo : 403 a qui ne tient aucun siege "
            "quand ils sont tenus, 403 a un spectateur TOUJOURS, et le siege "
            "prouve passe")


def cas_pause_refusee_sur_partie_declaree(game_dir, port):
    """`/manuel_pause` ne touche pas a une partie DECLAREE manuelle.

    La garde symetrique de `/manuel_passer` (revue finale, 20/09/2026).
    `World.ManualLoop` pose `manuel_actif` une fois pour toutes sur une
    partie declaree manuelle et ne le REPOSE JAMAIS : un `{"actif": false}`
    l'eteindrait pour de bon, le plateau redeviendrait bavard sur une partie
    que le moteur ne conduit plus, et aucun bouton ne permettrait d'y revenir.

    Injoignable au clic (le bouton « Mettre en pause » est masque sur une
    partie declaree, et `BandeauPause` ne s'y affiche pas), fermee quand meme :
    la route est publique.
    """
    import asyncio

    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True, \
        "premisse cassee : la boucle manuelle n'a pas demarre"

    from engine.device.web.server.server_get import GameServerGet

    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = jeu.world.controller_manager.device_manager

    reponse = asyncio.run(
        serveur.manuel_pause(_RequeteFactice({}, {"actif": False})))
    assert reponse.status == 409, (
        f"la route a accepte de reprendre une partie DECLAREE manuelle "
        f"(HTTP {reponse.status}) : ManualLoop ne repose jamais manuel_actif, "
        f"la partie deviendrait bavarde sans moyen de revenir"
    )
    assert monde.manuel_actif is True, \
        "manuel_actif est retombe a faux sur une partie declaree manuelle"

    # L'autre sens est ferme aussi : il n'y a rien a « mettre en pause » sur
    # une table que le moteur tient deja muette.
    reponse = asyncio.run(
        serveur.manuel_pause(_RequeteFactice({}, {"actif": True})))
    assert reponse.status == 409, (
        f"la route accepte une pause sur une partie deja declaree manuelle "
        f"(HTTP {reponse.status})"
    )
    assert monde.scene.corrigee_a_la_main is False, (
        "une partie DECLAREE manuelle a recu la marque « corrigee a la main » "
        "par la route de pause : rien n'y a ete corrige a la main, c'est la "
        "nature de la partie"
    )

    return ("/manuel_pause rend 409 sur une partie DECLAREE manuelle, dans les "
            "deux sens, et n'y pose aucune marque")


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
    reponse = asyncio.run(serveur.manuel_passer(_RequeteFactice({}, {})))
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
    reponse = asyncio.run(serveur.manuel_passer(_RequeteFactice({}, {})))
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
    reponse = asyncio.run(serveur.manuel_passer(_RequeteFactice({}, {})))
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
    reponse = asyncio.run(serveur.manuel_passer(_RequeteFactice({}, {})))
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


def monter_avec_geste_par_le_vrai_dogetinput(game_dir, port, commande_pour, *,
                                             round_du_geste=1,
                                             round_de_la_pause=None):
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

    `round_du_geste` (defaut 1) : le pilote JOUE d'abord, normalement,
    jusqu'a ce round -- c'est ce qui donne a la sauvegarde une VRAIE
    histoire a rejouer. A 1, il met en pause au premier tour de heros venu,
    comme les trois premiers temoins de la tache 9.

    `round_de_la_pause` (defaut None) : quand il est fourni, la partie
    REPREND apres le geste et se joue encore jusqu'a ce round, avant la pause
    finale. Sans ca, le geste n'est suivi d'AUCUNE entree, et son rang dans
    l'histoire ne se mesure pas : rejoue a l'instant 0 ou a sa place, la
    table finale serait la meme.

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

    etat = {"etape": "attend_tour", "compte": 0, "commande": None, "gares": 0,
            "signature": None, "derniere_question": None, "repetitions": 0,
            "round_observe": -1, "questions_du_round": 0}

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
        if etat["compte"] > PLAFOND_QUESTIONS_HISTOIRE:
            return se_garer()

        monde = jeu.world

        if etat["etape"] == "attend_tour":
            if data.event_name == "WhenPlayerInTurn" and \
                    monde is not None and monde.round_id >= round_du_geste:
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
            if round_de_la_pause is None:
                etat["etape"] = "fini"
            else:
                # ON REPREND, ET C'EST TOUT L'INTERET (ronde de correction 1,
                # constat C2). Un geste suivi d'AUCUNE entree ne prouve rien
                # sur son rang : rejoue a l'instant 0 ou a sa place, le
                # resultat serait le meme. Il faut que la partie CONTINUE
                # apres lui, pour que les entrees suivantes soient jouees sur
                # la table qu'il a laissee.
                jeu.world.BasculerPauseManuelle(False)
                etat["etape"] = "rejoue_apres_le_geste"
            return retour

        elif etat["etape"] == "rejoue_apres_le_geste":
            if monde is not None and monde.round_id >= round_de_la_pause:
                # La pause finale : celle qui sera dans la sauvegarde.
                jeu.world.BasculerPauseManuelle(True, "Diagnostic")
                etat["etape"] = "purge_pause_finale"
                return None

        elif etat["etape"] == "purge_pause_finale":
            etat["etape"] = "fini"
            return vrai_dogetinput(self, data, player_id, check)

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

        try:
            options = json.loads(data.options_json or "[]") or []
        except Exception:
            options = []

        # ANTI-BOUCLE, repris mot pour mot de `monter_le_moteur` : le Rhino
        # porte « Enhanced Ivory Horn » (01100), une Hero Action a cout que ce
        # pilote ne sait pas payer. L'option reste legale, echoue a chaque
        # fois, et le moteur represente la MEME liste a l'identique. Sans
        # cette parade, ce montage ne depasse jamais le premier tour -- donc
        # ne produit jamais la VRAIE histoire qui est tout son objet ici.
        signature = tuple(o.get("name") for o in options if isinstance(o, dict))
        if signature == etat["derniere_question"]:
            etat["repetitions"] += 1
        else:
            etat["derniere_question"] = signature
            etat["repetitions"] = 1

        legales = [o for o in options
                   if isinstance(o, dict) and not o.get("failure_reason")]
        if not legales:
            return None

        # JOUER UN PEU, PUIS FINIR SON TOUR -- sans quoi on ne sort jamais du
        # round 1. Mesure du 20/09/2026 : le pilote greedy de
        # `monter_le_moteur` (toujours `legales[0]`) a pose plus de 600
        # questions sans depasser le round 1, en rejouant sans fin des
        # options de tour qui echouent (Enhanced Ivory Horn, Helicarrier...)
        # et que `PlayerAction` DEPILE aussitot (`replay.Pop()`), si bien que
        # le compteur d'entrees restait a 3.
        #
        # On garde donc le geste du joueur pressé : les premieres questions
        # du round servent a jouer des cartes (`legales[0]`, ce qui remplit
        # l'historique), les suivantes prennent la DERNIERE option, qui est
        # en pratique celle qui termine le tour -- meme parade, et meme
        # constat, que l'anti-boucle de `monter_le_moteur`.
        monde_du_tour = jeu.world
        round_courant = monde_du_tour.round_id if monde_du_tour else -1
        if round_courant != etat["round_observe"]:
            etat["round_observe"] = round_courant
            etat["questions_du_round"] = 0
        etat["questions_du_round"] += 1

        presse = (etat["questions_du_round"] > QUESTIONS_JOUEES_PAR_ROUND
                  or etat["repetitions"] > 3)
        if presse and data.show_cancel:
            # PASSER, C'EST FINIR SON TOUR. Il n'existe AUCUNE option
            # « fin de tour » dans la liste (mesure du 20/09/2026 : les
            # options d'un tour de heros s'appellent toutes « Play ») : ce
            # que le plateau montre comme « Terminer le tour », c'est la
            # reponse VIDE, celle que `ChoiceOne` lit comme `id == 0` et que
            # `show_cancel` autorise. C'est le meme chemin, exactement, que
            # `DeviceManager.PasserQuestionCourante`.
            #
            # Sans ca, ce montage ne sort jamais du round 1 : le pilote
            # rejoue indefiniment des options qui echouent (Enhanced Ivory
            # Horn, Helicarrier) et que `PlayerAction` depile aussitot.
            return "{}"
        o = legales[-1] if presse else legales[0]
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

    limite = time.time() + 180
    while not etat["gares"] and time.time() < limite:
        time.sleep(0.5)
    assert etat["gares"], (
        f"la sequence n'est jamais arrivee a la table figee (etape="
        f"{etat['etape']!r}, {etat['compte']} question(s) posees) : rien "
        "n'est prouve"
    )
    time.sleep(2)
    etat["signature"] = signature_de_table(jeu.world)
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

def cas_annulation_geste_garde_la_pause(game_dir, port):
    """Ctrl+Z (`AnnulerDernierGeste`) sur une partie ORDINAIRE mise en pause :
    le geste part, et la table RESTE en pause.

    Lot 1 du plan du 06/10/2026 : dans le navigateur, sur une partie basculee
    en Manuel, Ctrl+Z repassait la table en Auto (captures manuel-80/81,
    `mode_manuel=false`, `restants: 0`). `cas_annulation` ne couvre que la
    partie manuelle DECLAREE, et `cas_annulation_ordinaire_garde_tout` le
    bouton « Annuler » ordinaire (`GameSession.Undo`), pas le Ctrl+Z.
    """
    jeu, commande, etat = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: f"Puzzle.Damage({id_du_vilain(jeu.world)}, 3)")

    vilain = id_du_vilain(jeu.world)
    monde_avant = jeu.world
    assert monde_avant.object_manager.card_dict[vilain].face.GetLostHealth() == 3, \
        "premisse cassee : le geste n'a pas ete applique avant l'annulation"
    assert jeu.session.scene.manuel_commands == [commande], \
        f"premisse cassee : le geste n'est pas dans la scene ({jeu.session.scene.manuel_commands})"

    etat["etape"] = "attend_regare"
    assert jeu.session.AnnulerDernierGeste() is True, "rien a annuler"

    limite = time.time() + 180
    while (jeu.world is monde_avant or etat["gares"] < 2) and time.time() < limite:
        time.sleep(0.5)
    time.sleep(3)
    monde_apres = jeu.world
    assert monde_apres is not monde_avant, \
        "premisse cassee : l'annulation n'a pas reconstruit le monde"

    assert jeu.session.scene.manuel_commands == [], \
        f"le geste n'a pas ete retire : {jeu.session.scene.manuel_commands}"
    assert jeu.session.scene.pause_en_cours is True, \
        "l'annulation a efface la pause de la scene (pause_a vide)"
    assert monde_apres.manuel_actif is True, (
        f"apres Ctrl+Z, la table est repassee en Auto (manuel_actif="
        f"{monde_apres.manuel_actif}, gares={etat['gares']}, etape={etat['etape']!r}, "
        f"mise_en_place_finie={jeu.session.mise_en_place_finie})"
    )
    # LA TRAME PUBLIEE, PAS SEULEMENT L'OBJET. C'est elle que lit le plateau
    # (`/get_world`) : dans le navigateur, le moteur etait bien muet apres le
    # Ctrl+Z, mais la trame servie disait encore `manuel_actif=false`, et la
    # table repassait en Auto a l'ecran (06/10/2026, cause etablie par un
    # second `/manuel_undo` qui repondait « rien a annuler », pas « pas une
    # partie manuelle »).
    publie = getattr(monde_apres.render.descriptor, "manuel_actif", None)
    assert publie is True, (
        f"la trame publiee apres Ctrl+Z dit manuel_actif={publie!r} alors que "
        "le moteur est muet : le plateau repasse en Auto"
    )
    return "Ctrl+Z sur une partie ordinaire en pause retire le geste et garde la pause, publiee"


def cas_reponse_refusee_pendant_la_pause(game_dir, port):
    """Pendant que la table est muette (`manuel_actif`), `/post` ne repond
    plus a la question garee du moteur.

    Lot 1 du plan du 06/10/2026 : sur une partie basculee en Manuel, le
    bouton flottant « Fin du tour » et la touche E repondaient a la question
    garee, et le moteur AVANCAIT (captures manuel-75/76). Le plateau ne les
    montre plus ; le moteur, lui, doit refuser quand meme (une garde qui ne
    vivrait que dans l'interface n'est pas une garde). `/manuel_passer`
    reste la seule echappatoire voulue : il passe par `PasserQuestionCourante`,
    pas par `/post`.

    Aucun moteur monte : on frappe la VRAIE `GameServerSync.handle_post`
    sur un serveur factice, comme `cas_post_ferme_au_spectateur`.
    """
    import asyncio
    import sys
    import types
    racine_src = os.path.join(RACINE, "src")
    if racine_src not in sys.path:
        sys.path.insert(0, racine_src)
    from engine.device.web.server.server_sync import GameServerSync

    def frapper(muet):
        recues = []
        serveur = GameServerSync.__new__(GameServerSync)
        serveur.get_player_ids = lambda request: [0]
        # `game` est une propriete (server_base.py) : elle lit le jeu du
        # premier controleur du gestionnaire.
        jeu_factice = types.SimpleNamespace(world=types.SimpleNamespace(manuel_actif=muet))
        serveur.device_manager = types.SimpleNamespace(
            asking_players=[0], WhenInput=lambda texte, joueur: recues.append(texte),
            controllers=[types.SimpleNamespace(game=jeu_factice)])

        class _Requete:
            async def text(self):
                return "{}"

        reponse = asyncio.run(serveur.handle_post(_Requete()))
        return reponse.status, recues

    statut, recues = frapper(False)
    assert statut == 200 and recues == ["{}"], \
        f"temoin : hors pause, /post doit transmettre la reponse (statut={statut}, recues={recues})"

    statut, recues = frapper(True)
    assert recues == [], \
        f"pendant la pause, /post a transmis une reponse au moteur : {recues}"
    assert statut == 409, f"pendant la pause, /post doit refuser (409), statut={statut}"
    return "pendant la pause, /post ne repond plus a la question garee du moteur"


def cas_histoire_rejouee_apres_pause(game_dir, port):
    """Une sauvegarde qui porte une VRAIE histoire se rouvre sur LA MEME
    table -- pas sur une table vierge. Constat C1 de la ronde de correction 1.

    ⚠ CE CAS A ETE ECRIT ROUGE, et il attrape un defaut que les trois
    premiers temoins de la tache 9 ne pouvaient pas voir : ils posaient la
    pause au tout PREMIER tour de heros, donc leur sauvegarde ne portait
    presque aucune entree a rejouer. Celui-ci joue trois rounds d'abord.

    Le defaut : `GameSetup` refermait la porte du silence (`manuel_actif`)
    AVANT que le rejeu des entrees n'ait lieu. Or cette porte est celle de
    `BroadcastMessage`/`BroadcastStackMessage` : aucun declencheur, aucun
    effet de regle, aucun sbire vaincu. Les entrees ne pouvaient donc plus
    etre consommees -- les questions ne naissaient meme pas -- et le joueur
    retrouvait une table VIERGE a la place de la sienne. La porte ne se
    referme desormais qu'une fois le rejeu epuise
    (`GameSession.FinirLeRejeuDesGestes`, appele par `Controller.ChoiceOne`).

    ⚠ LE FILS OUVRE LA SAUVEGARDE COMME LA PRODUCTION, avec
    `rejouer_les_entrees=True` : sans ca le moteur REDEMANDE toute la partie
    au lieu de la rejouer, et ce cas ne mesurerait rien du rejeu.
    """
    jeu, commande, etat = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: f"Puzzle.Damage({id_du_vilain(jeu.world)}, 3)",
        round_du_geste=3)

    attendue = etat["signature"]
    assert attendue["round"] >= 3, (
        f"premisse cassee : la sauvegarde ne porte pas d'histoire "
        f"(round {attendue['round']})"
    )
    entrees = len(jeu.controller_manager.replay.history_inputs)
    assert entrees >= 3, (
        f"premisse cassee : seulement {entrees} entree(s) a rejouer, c'est "
        "trop peu pour que ce cas prouve quoi que ce soit"
    )

    nom = "manuel-histoire-aller-retour.json"
    ecrit = jeu.session.SaveScene(name=nom, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    env["MC_COMMANDE"] = commande
    env["MC_SIGNATURE"] = json.dumps(attendue)
    env["MC_ENTREES"] = str(entrees)
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_histoire", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-4000:]}\n{fils.stderr[-3000:]}"
    return (f"une sauvegarde de {entrees} entrees, faite en pause au round "
            f"{attendue['round']}, se rouvre sur la meme table")


def cas_relire_histoire(game_dir, port):
    """Le fils de `cas_histoire_rejouee_apres_pause`."""
    chemin = os.environ["MC_SAUVEGARDE"]
    commande = os.environ["MC_COMMANDE"]
    attendue = json.loads(os.environ["MC_SIGNATURE"])
    entrees = int(os.environ["MC_ENTREES"])

    releve = {}

    def au_premier_reveil(jeu):
        # LE PREMIER APPEL EST LE BON MOMENT, ET C'EST LE SEUL. Le rejeu des
        # entrees ne passe PAS par `DoGetInput` (`ChoiceOne` se sert de
        # `fallthrough_input` tant qu'il saute) : la premiere question posee
        # au pilote est donc exactement celle sur laquelle le joueur s'etait
        # arrete. Une mesure prise plus tard verrait le pilote avoir deja
        # rejoue par-dessus.
        if "table" in releve:
            return
        releve["table"] = signature_de_table(jeu.world)
        releve["muet"] = bool(jeu.world.manuel_actif)

    jeu, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin,
                                     avant_reponse=au_premier_reveil,
                                     rejouer_les_entrees=True)

    assert jeu.session.scene.manuel_commands == [commande], \
        f"la sauvegarde ne porte pas le geste : {jeu.session.scene.manuel_commands}"
    assert "table" in releve, (
        "la partie rechargee n'a pose AUCUNE question : le rejeu des entrees "
        "s'est arrete en route -- exactement ce que produisait la porte du "
        "silence refermee trop tot"
    )

    obtenue = releve["table"]
    ecarts = comparer_les_tables(attendue, obtenue)
    assert not ecarts, (
        f"la table rechargee n'est pas celle du joueur, apres un rejeu de "
        f"{entrees} entrees. Ecarts :\n  - " + "\n  - ".join(ecarts[:12]) +
        (f"\n  (+{len(ecarts) - 12} autres)" if len(ecarts) > 12 else "") +
        "\nRegarder d'abord QUAND la porte du silence se referme : fermee "
        "avant le rejeu, elle ferme BroadcastMessage, donc les entrees ne "
        "sont jamais consommees et la table reste vierge."
    )
    assert releve["muet"] is True, (
        "la partie rechargee a repris toute seule : elle etait EN PAUSE au "
        "moment de la sauvegarde"
    )
    return (f"la table rechargee est identique apres un rejeu de {entrees} "
            "entrees, et elle revient en pause")


def cas_geste_au_bon_rang(game_dir, port):
    """Un geste AUTRE que `Damage`, fait au milieu de la partie, se rejoue a
    SON rang -- pas a l'instant 0. Constat C2 de la ronde de correction 1.

    ⚠ CE CAS A ETE ECRIT ROUGE. Le rejeu entassait tous les gestes a
    l'instant 0, avant la premiere entree. `Puzzle.Damage` y survit -- c'est
    le seul geste que la tache 9 avait mesure -- mais `/sandbox_command`
    accepte TOUT `Puzzle.<methode>`, et trois mecanismes faussent la table
    sans jamais lever :

    - la GRAINE : `Shuffle`, `Draw`, `Reveal`, `Boost`, `Deal` consommes a
      l'instant 0 decalent tout le flux aleatoire, et la rencontre du round
      suivant n'est plus la meme ;
    - les IDENTIFIANTS : `CreateCard`, `Reveal`, `PutIntoPlay` font naitre
      des objets qui prennent les identifiants que le rejeu attribuera
      ensuite a d'autres cartes -- un geste suivant qui vise `c49` ne vise
      plus la meme carte, et aucun `try/except` n'attrape ca : il n'y a pas
      d'erreur, seulement une cible fausse ;
    - la FIN DE PARTIE : `Puzzle.Win()`/`Lose()` rejoues a l'instant 0 posent
      `is_game_over` avant meme que `GameSetup` ne rende la main, et la
      sauvegarde ne s'ouvre plus.

    Le geste choisi ici est `Puzzle.Draw(2)` : il ne fait de mal a personne,
    mais il deplace des cartes entre le deck et la main et change donc ce que
    TOUTES les entrees suivantes ont sous les yeux.

    ⚠ ET LE GESTE EST SUIVI D'ENTREES, C'EST TOUT L'INTERET : on REPREND la
    partie apres lui et on joue encore un round avant de sauver. Un geste que
    plus rien ne suit ne prouve rien sur son rang -- rejoue a l'instant 0 ou
    a sa place, la table finale serait la meme.
    """
    jeu, commande, etat = monter_avec_geste_par_le_vrai_dogetinput(
        game_dir, port,
        lambda jeu: "Puzzle.Draw(2)",
        round_du_geste=2, round_de_la_pause=3)

    attendue = etat["signature"]
    rangs = jeu.session.scene.manuel_commands_step
    entrees = len(jeu.controller_manager.replay.history_inputs)
    assert jeu.session.scene.manuel_commands == [commande], \
        f"premisse cassee : le geste n'est pas dans la scene ({jeu.session.scene.manuel_commands})"
    assert rangs and 0 < rangs[0] < entrees, (
        f"premisse cassee : le geste doit etre fait AU MILIEU de l'histoire "
        f"pour que son rang compte -- rang {rangs!r}, {entrees} entrees au "
        "total"
    )

    nom = "manuel-rang-aller-retour.json"
    ecrit = jeu.session.SaveScene(name=nom, delete_old=False)
    assert ecrit, "la sauvegarde n'a pas ete ecrite"

    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    env["MC_COMMANDE"] = commande
    env["MC_SIGNATURE"] = json.dumps(attendue)
    env["MC_RANG"] = str(rangs[0])
    env["MC_ENTREES"] = str(entrees)
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_geste_au_bon_rang", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-4000:]}\n{fils.stderr[-3000:]}"
    return (f"un Puzzle.Draw(2) fait au rang {rangs[0]} sur {entrees} entrees "
            "se rejoue a son rang, et la table rechargee est identique")


def cas_relire_geste_au_bon_rang(game_dir, port):
    """Le fils de `cas_geste_au_bon_rang`.

    ⚠ CE CAS REGARDE AUSSI LE JOURNAL DU MOTEUR, pas seulement la table
    (ronde de correction 2 du 20/09/2026). La table peut etre PARFAITE et le
    rejeu quand meme faux : le moteur grave dans chaque entree un CRC de la
    table au moment ou il l'a enregistree, et le compare au rechargement. Si
    le geste est rejoue APRES ce calcul -- ne serait-ce que d'une question --
    le CRC de l'entree du rang ne correspond plus, `InputModule` ecrit un
    `Log.Assert` de niveau Error a chaque ouverture de la sauvegarde, et rend
    un `read_ok` qui ne reste vrai que par accident : `all(...)` sur un
    generateur vide vaut `True`, et `crc_ignore_ids` est vide par defaut. Le
    jour ou ce `read_ok` devient faux, `Controller.ChoiceOne` COUPE le rejeu
    en plein milieu -- c'est-a-dire la panne de la famille C1, revenue par la
    fenetre.
    """
    chemin = os.environ["MC_SAUVEGARDE"]
    commande = os.environ["MC_COMMANDE"]
    attendue = json.loads(os.environ["MC_SIGNATURE"])
    rang = int(os.environ["MC_RANG"])
    entrees = int(os.environ["MC_ENTREES"])

    # L'ESPION, POSE AVANT LE MONTAGE : le rejeu des entrees ne passe pas par
    # `DoGetInput` (`ChoiceOne` se sert de `fallthrough_input` tant qu'il
    # saute), donc `avant_reponse` ne serait appele qu'APRES, bien trop tard.
    # On fait ici le chdir et le sys.path que `monter_le_moteur` refera
    # ensuite a l'identique, juste pour pouvoir importer `Log`.
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    from engine.log import Log

    crc_fautifs = []
    _vrai_assert = Log.Assert

    def _assert_espion(categorie, *info):
        # `Log.Assert` sert a tout le moteur (un effet qui echoue pendant un
        # tour de heros en ecrit un a chaque fois) : on ne retient que la
        # categorie du rejeu des entrees, la seule qui parle de CRC.
        if categorie == "REPLAY":
            crc_fautifs.append(" ".join(str(x) for x in info))
        return _vrai_assert(categorie, *info)

    Log.Assert = _assert_espion

    releve = {}

    def au_premier_reveil(jeu):
        if "table" in releve:
            return
        releve["table"] = signature_de_table(jeu.world)

    jeu, monde, _ = monter_le_moteur(game_dir, port, [], sauvegarde=chemin,
                                     avant_reponse=au_premier_reveil,
                                     rejouer_les_entrees=True)

    scene = jeu.session.scene
    assert scene.manuel_commands == [commande], \
        f"la sauvegarde ne porte pas le geste : {scene.manuel_commands}"
    assert scene.manuel_commands_step == [rang], (
        f"la sauvegarde ne porte pas le RANG du geste : "
        f"{scene.manuel_commands_step!r} (attendu [{rang}]) -- sans lui, le "
        "rejeu ne peut que l'entasser a l'instant 0"
    )
    assert "table" in releve, \
        "la partie rechargee n'a pose aucune question : rien n'a pu etre mesure"

    assert not crc_fautifs, (
        f"le moteur a signale {len(crc_fautifs)} desaccord(s) de CRC en "
        f"rejouant la sauvegarde. La table peut etre juste : le rejeu, lui, "
        f"ne l'est pas. Le geste du rang {rang} est applique APRES le calcul "
        f"de `calculated_crc` (controller.py, en tete de `ChoiceOne`), donc "
        f"la table comparee a l'entree {rang} est celle d'AVANT le geste, "
        f"alors que le CRC grave dedans, lui, a ete calcule APRES. Premier "
        f"desaccord :\n{crc_fautifs[0][:800]}"
    )

    ecarts = comparer_les_tables(attendue, releve["table"])
    assert not ecarts, (
        f"la table rechargee differe apres un rejeu de {entrees} entrees avec "
        f"un Puzzle.Draw(2) au rang {rang}. Ecarts :\n  - " +
        "\n  - ".join(ecarts[:12]) +
        (f"\n  (+{len(ecarts) - 12} autres)" if len(ecarts) > 12 else "") +
        "\nUn geste rejoue au mauvais rang ne leve pas : il decale la graine "
        "et les identifiants d'objet, et tout ce qui suit est joue sur une "
        "table qui n'est plus la bonne."
    )
    return (f"le geste est rejoue a son rang ({rang}/{entrees}) : la table "
            "rechargee est identique")


# ---------------------------------------------------------------------------
# LA REPRISE EN AUTOMATIQUE d'une partie DECLAREE manuelle (POST /manuel_reprise)
# ---------------------------------------------------------------------------

def _serveur_factice(jeu):
    """Le VRAI `GameServerGet`, sans socket (meme montage que
    `cas_pause_par_nom_du_heros`)."""
    from engine.device.web.server.server_get import GameServerGet
    serveur = GameServerGet.__new__(GameServerGet)
    serveur.device_manager = jeu.world.controller_manager.device_manager
    return serveur


def _appeler_reprise(serveur, phase, cookies=None):
    import asyncio
    reponse = asyncio.run(serveur.manuel_reprise(
        _RequeteFactice(cookies or {}, {"phase": phase}, "/manuel_reprise")))
    return reponse.status, json.loads(reponse.text)


def _espionner_le_deroule(monde):
    """Note l'ORDRE dans lequel le moteur entre dans ses phases et clot un
    tour : c'est la seule facon de voir de quelle phase la reprise est
    repartie. A poser AVANT la reprise (le moteur la lit sur l'instance)."""
    ordre = []

    def envelopper(objet, nom, etiquette):
        vrai = getattr(objet, nom)

        def enveloppe(*a, **k):
            ordre.append(etiquette)
            return vrai(*a, **k)
        setattr(objet, nom, enveloppe)

    envelopper(monde, "PlayerPhase", "PlayerPhase")
    envelopper(monde, "VillainPhase", "VillainPhase")
    envelopper(monde.buff_manager, "OnRoundEnd", "FinDeTour")
    return ordre


def _reprendre_et_regarder(game_dir, port, phase):
    jeu, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True, "premisse cassee : la boucle manuelle n'a pas demarre"
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 3)")
    avant = len(journal)
    assert monde.phase.state == "Init Finished", f"premisse cassee : phase={monde.phase.state!r}"

    ordre = _espionner_le_deroule(monde)
    statut, corps = _appeler_reprise(_serveur_factice(jeu), phase)
    assert statut == 200, f"la reprise a ete refusee : {statut} {corps}"
    time.sleep(15)

    assert monde.scene.reprise_auto == phase, \
        f"la scene ne se souvient pas de la reprise : {monde.scene.reprise_auto!r}"
    assert monde.manuel_actif is False, \
        "le moteur est reste muet apres la reprise"
    assert len(journal) > avant, \
        "le moteur n'a repose aucune question apres la reprise : il ne conduit pas"
    assert monde.round_id >= 1, f"aucun tour demarre : round_id={monde.round_id}"
    descripteur = monde.render.descriptor
    assert descripteur.mode_manuel is False, \
        "la trame annonce encore une partie declaree manuelle apres la reprise"
    assert descripteur.manuel_actif is False, \
        "la trame annonce encore le moteur muet apres la reprise"
    assert monde.object_manager.card_dict[vilain].face.GetLostHealth() >= 3, \
        "le geste d'avant la reprise a disparu"
    return jeu, monde, ordre


def cas_reprise_heros(game_dir, port):
    """Reprise « phase heros » : le tour demarre, la phase heros est jouee
    en premier, et la partie est redevenue ordinaire (la pause rouvre)."""
    jeu, monde, ordre = _reprendre_et_regarder(game_dir, port, "heros")
    assert ordre and ordre[0] == "PlayerPhase", \
        f"la phase heros n'est pas la premiere jouee : {ordre!r}"
    assert "FinDeTour" not in ordre[:1], f"fin de tour avant le premier tour : {ordre!r}"

    import asyncio
    serveur = _serveur_factice(jeu)
    reponse = asyncio.run(serveur.manuel_pause(_RequeteFactice({}, {"actif": True})))
    assert reponse.status == 200, (
        f"la pause reste fermee apres la reprise (HTTP {reponse.status}) : la "
        "partie n'est pas redevenue ordinaire")
    assert monde.manuel_actif is True
    asyncio.run(serveur.manuel_pause(_RequeteFactice({}, {"actif": False})))
    return "reprise en phase heros : le moteur conduit, la pause se pose et se leve"


def cas_reprise_mechant(game_dir, port):
    """Reprise « phase mechant » : la phase heros, jouee a la main, est sautee."""
    _, _, ordre = _reprendre_et_regarder(game_dir, port, "mechant")
    assert ordre and ordre[0] == "VillainPhase", \
        f"la reprise en phase mechant n'a pas commence par elle : {ordre!r}"
    return "reprise en phase mechant : la phase heros est sautee"


def cas_reprise_tour(game_dir, port):
    """Reprise « nouveau tour » : le tour joue a la main est clos, puis un
    tour neuf commence par la phase heros."""
    _, _, ordre = _reprendre_et_regarder(game_dir, port, "tour")
    assert ordre[:2] == ["FinDeTour", "PlayerPhase"], \
        f"la reprise « nouveau tour » ne clot pas l'ancien puis ouvre le neuf : {ordre!r}"
    return "reprise en nouveau tour : fin de tour, puis phase heros"


def _rounds_aux_phases(monde):
    """Le numero de round AU MOMENT ou le moteur entre dans une phase ou clot
    un tour. Lu apres coup, `round_id` ne dirait rien : le moteur a pu jouer
    d'autres rounds pendant l'attente."""
    vus = []

    def envelopper(objet, nom, etiquette):
        vrai = getattr(objet, nom)

        def enveloppe(*a, **k):
            vus.append((etiquette, monde.round_id))
            return vrai(*a, **k)
        setattr(objet, nom, enveloppe)

    envelopper(monde, "PlayerPhase", "PlayerPhase")
    envelopper(monde, "VillainPhase", "VillainPhase")
    envelopper(monde.buff_manager, "OnRoundEnd", "FinDeTour")
    return vus


def cas_round_partie_declaree(game_dir, port):
    """Partie DECLAREE manuelle : le joueur est dans le round 1 des la fin de
    la mise en place, « Fin du round » le fait passer au round 2, et une
    reprise « phase heros » joue CE round 2, sans en compter un de plus
    (constat du passage navigateur final du 06/10/2026 : la barre restait
    vide au premier round et « Round 1 » s'affichait au debut du deuxieme)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True, "premisse cassee : la boucle manuelle n'a pas demarre"
    assert monde.round_id == 1, f"premier round joue a la main, round_id={monde.round_id}, attendu 1"
    deposer(jeu, "Puzzle.EndRound()")
    assert monde.round_id == 2, f"apres Fin du round, round_id={monde.round_id}, attendu 2"

    vus = _rounds_aux_phases(monde)
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, f"la reprise a ete refusee : {statut} {corps}"
    time.sleep(15)
    assert vus and vus[0] == ("PlayerPhase", 2), \
        f"la reprise en phase heros doit jouer le round 2 : {vus[:3]!r}"
    return "round 1 au depart, 2 apres Fin du round, la reprise joue ce round 2"


def cas_round_reprise_nouveau_tour(game_dir, port):
    """Reprise « nouveau tour » depuis le premier round joue a la main : le
    round 1 est clos, puis le round 2 commence. Temoin de l'autre branche :
    elle seule ajoute un round."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.round_id == 1, f"premier round joue a la main, round_id={monde.round_id}, attendu 1"
    vus = _rounds_aux_phases(monde)
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "tour")
    assert statut == 200, f"la reprise a ete refusee : {statut} {corps}"
    time.sleep(15)
    assert vus[:2] == [("FinDeTour", 1), ("PlayerPhase", 2)], \
        f"nouveau tour : fin du round 1 puis round 2 attendus : {vus[:3]!r}"
    return "nouveau tour : fin du round 1, puis round 2"


def cas_reprise_refusee(game_dir, port):
    """Les refus de `/manuel_reprise`, chacun avec son code, et RIEN ne bouge.

    Le temoin qui compte est le REFUS : apres chaque refus, le moteur est
    toujours muet, aucun tour n'a demarre, la scene ne porte aucune reprise.
    """
    jeu, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    from engine.device.web.server.server_base import SEAT_PASSWORDS
    assert monde.manuel_actif is True
    serveur = _serveur_factice(jeu)
    avant = len(journal)

    def rien_n_a_bouge(contexte):
        assert monde.manuel_actif is True, f"{contexte} : le moteur a parle"
        assert monde.phase.state == "Init Finished", f"{contexte} : un tour a demarre"
        assert monde.scene.reprise_auto == "", f"{contexte} : la scene garde une reprise"
        assert monde.reprise_demandee is None, f"{contexte} : une reprise est restee en attente"
        assert len(journal) == avant, f"{contexte} : le moteur a repose une question"

    statut, corps = _appeler_reprise(serveur, "nimporte")
    assert (statut, corps.get("error")) == (409, "phase_inconnue"), (statut, corps)
    rien_n_a_bouge("phase inconnue")

    fini = jeu.session.mise_en_place_finie
    jeu.session.mise_en_place_finie = False
    try:
        statut, corps = _appeler_reprise(serveur, "heros")
    finally:
        jeu.session.mise_en_place_finie = fini
    assert (statut, corps.get("error")) == (409, "mise_en_place_non_finie"), (statut, corps)
    rien_n_a_bouge("mise en place non finie")

    ancien = list(SEAT_PASSWORDS.value)
    try:
        # Tous les sieges proteges : un siege orphelin s'ouvre a tout le monde.
        SEAT_PASSWORDS.value = ["secret-siege-0", "secret-siege-1",
                                "secret-siege-2", "secret-siege-3"]
        serveur.seat_orphelin = lambda siege: False
        statut, corps = _appeler_reprise(serveur, "heros")
    finally:
        SEAT_PASSWORDS.value = ancien
    assert statut == 403, f"un client sans siege a pu reprendre : {statut} {corps}"
    rien_n_a_bouge("sans siege")

    # Une fois repartie, la partie n'est plus « manuelle » : une 2e reprise est refusee.
    statut, corps = _appeler_reprise(serveur, "heros")
    assert statut == 200, (statut, corps)
    time.sleep(10)
    statut, corps = _appeler_reprise(serveur, "heros")
    assert (statut, corps.get("error")) == (409, "pas_manuel"), (statut, corps)
    return "refus : phase inconnue, mise en place non finie, sans siege, deja reprise"


def cas_reprise_refusee_hors_manuel(game_dir, port):
    """Sur une partie ordinaire (jamais declaree manuelle), pas de reprise :
    c'est `/manuel_pause` qui reprend. Refus `pas_manuel`, rien ne bouge."""
    jeu, monde, journal = monter_le_moteur(game_dir, port, [])
    assert bool(monde.rule.mode_manuel) is False
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert (statut, corps.get("error")) == (409, "pas_manuel"), (statut, corps)
    assert monde.scene.reprise_auto == "" and monde.reprise_demandee is None
    return "pas de reprise sur une partie ordinaire : 409 pas_manuel"


def cas_reprise_survit_sauvegarde(game_dir, port):
    """Une partie repartie en automatique se sauvegarde et se rouvre.

    Un geste (`Puzzle.Draw(2)`, qui change ce que toutes les entrees
    suivantes ont sous les yeux) est fait en manuel, puis la partie reprend
    en phase heros et joue une vingtaine de questions avant d'etre
    sauvegardee. Le fils (`relire_reprise`) la rouvre en rejouant les entrees.
    """
    global PLAFOND_QUESTIONS
    jeu, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    assert monde.manuel_actif is True
    deposer(jeu, "Puzzle.Draw(2)")
    PLAFOND_QUESTIONS = len(journal) + 25
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, (statut, corps)
    time.sleep(20)
    assert monde.round_id >= 1, "premisse cassee : aucun tour n'a demarre apres la reprise"

    entrees = len(jeu.controller_manager.replay.history_inputs)
    rang = jeu.session.scene.manuel_commands_step
    assert rang and entrees > rang[0], \
        f"premisse cassee : aucune entree apres la reprise (rang {rang}, {entrees} entrees)"

    nom = "manuel-reprise-aller-retour.json"
    assert jeu.session.SaveScene(name=nom, delete_old=False), \
        "la sauvegarde n'a pas ete ecrite"
    env = dict(os.environ)
    env["MC_SAUVEGARDE"] = nom
    env["MC_ENTREES"] = str(entrees)
    fils = subprocess.run(
        [sys.executable, os.path.abspath(__file__), game_dir,
         str(port + 1), "relire_reprise", "--fils"],
        cwd=RACINE, capture_output=True, text=True, timeout=300, env=env)
    assert fils.returncode == 0, \
        f"le rechargement a echoue :\n{fils.stdout[-4000:]}\n{fils.stderr[-3000:]}"
    return "la partie repartie en automatique se rouvre, rejeu sans desaccord de CRC"


def cas_relire_reprise(game_dir, port):
    """Le fils de `cas_reprise_survit_sauvegarde`."""
    chemin = os.environ["MC_SAUVEGARDE"]
    entrees = int(os.environ["MC_ENTREES"])

    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    from engine.log import Log

    crc_fautifs = []
    _vrai_assert = Log.Assert

    def _assert_espion(categorie, *info):
        if categorie == "REPLAY":
            crc_fautifs.append(" ".join(str(x) for x in info))
        return _vrai_assert(categorie, *info)

    Log.Assert = _assert_espion

    jeu, monde, journal = monter_le_moteur(game_dir, port, [], sauvegarde=chemin,
                                           rejouer_les_entrees=True)
    scene = jeu.session.scene
    assert scene.reprise_auto == "heros", \
        f"la sauvegarde a perdu la reprise : {scene.reprise_auto!r}"
    assert scene.manuel_commands == ["Puzzle.Draw(2)"], \
        f"la sauvegarde a perdu le geste : {scene.manuel_commands}"
    assert not crc_fautifs, (
        f"{len(crc_fautifs)} desaccord(s) de CRC au rejeu : le geste d'avant la "
        f"reprise n'est pas rejoue au meme moment que dans la partie vivante. "
        f"Premier :\n{crc_fautifs[0][:800]}")
    assert monde.manuel_actif is False, \
        "la partie rouverte est restee muette : la reprise n'a pas survecu"
    assert monde.render.descriptor.mode_manuel is False
    assert monde.round_id >= 1, f"le tour n'a pas ete rejoue : round_id={monde.round_id}"
    rejouees = len(jeu.controller_manager.replay.history_inputs)
    assert rejouees >= entrees, \
        f"le rejeu s'est arrete en route : {rejouees} entrees sur {entrees}"
    return "la reprise survit : tour rejoue, geste rejoue, aucun desaccord"


def cas_jeton_acceleration(game_dir, port):
    """Un jeton d'acceleration se pose ET se retire par Puzzle.Token.

    ⚠ ECRIT ROUGE (05/10/2026) : la branche negative passait `size` tel quel a
    `RemoveTokensOn` (valeur negative), seul `Counter` l'opposait. F4 / Maj+F4
    du mode manuel (OCTGN) reposent sur ce retrait.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    schemes = monde.area_schemes_main.Get()
    assert schemes, "aucun complot principal en jeu"
    carte = schemes[-1].card.object_id
    face = monde.object_manager.card_dict[carte].face

    deposer(jeu, f"Puzzle.Token({carte}, 'acceleration_token', 3)")
    assert face.GetTokens('acceleration_token') == 3, \
        f"3 jetons attendus, {face.GetTokens('acceleration_token')} trouves"
    deposer(jeu, f"Puzzle.Token({carte}, 'acceleration_token', -1)")
    assert face.GetTokens('acceleration_token') == 2, \
        f"2 jetons attendus apres le retrait, {face.GetTokens('acceleration_token')} trouves"
    return "Puzzle.Token pose puis retire un jeton d'acceleration"


# ---------------------------------------------------------------------------
# POSER UNE CARTE A LA MAIN, comme sur OCTGN (lot 2 du 06/10/2026)
# ---------------------------------------------------------------------------

def _carte_de_code_dans(pile, code):
    """L'identifiant d'objet de la carte de code imprime `code` dans `pile`.

    ⚠ Pas `max(card_dict)` : `MoveTo('01002', ...)` RETROUVE d'abord une carte
    de ce code deja dans la partie (le deck du heros, `FindOrCreateFace`) et ne
    la fabrique que si elle n'existe nulle part.
    """
    for face in pile.GetAll():
        if getattr(getattr(face, "paper", None), "card_id", None) == code:
            return face.card.object_id
    raise AssertionError(f"premisse cassee : aucune carte {code} dans la pile visee")


def _creer_en_main(jeu, monde, code, siege=0):
    """Amene la carte `code` dans la main du siege `siege` et rend son
    identifiant d'objet."""
    deposer(jeu, f"Puzzle.MoveTo('{code}', 'HandsArea', 'Top', siege={siege})")
    return _carte_de_code_dans(monde.const_seat_order_players[siege].hand_cards, code)


def cas_poser_depuis_la_main(game_dir, port):
    """Un allie et un soutien de la main, poses a la main, arrivent en jeu
    face visible, un geste chacun, sans capacite declenchee ; une amelioration
    a compteurs arrive avec eux (Uses) et un allie Toughness avec son statut
    Tenace, comme le fait le plugin OCTGN (question 5 du 06/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_seat_order_players[0]
    allie = _creer_en_main(jeu, monde, "01002")
    soutien = _creer_en_main(jeu, monde, "01006")
    tireur = _creer_en_main(jeu, monde, "01008")
    coriace = _creer_en_main(jeu, monde, "01076")
    identite = joueur.GetIdentity().card.object_id
    avant = len(jeu.session.scene.manuel_commands)

    zone_allie = os.environ.get("ZONE_POSE_ALLIE", "AlliesArea")
    deposer(jeu, f"Puzzle.MoveTo({allie}, '{zone_allie}', 'Top', siege=0)")
    deposer(jeu, f"Puzzle.MoveTo({soutien}, 'SupportsArea', 'Top', siege=0)")
    deposer(jeu, f"Puzzle.Attach({tireur}, {identite})")
    deposer(jeu, f"Puzzle.MoveTo({coriace}, 'AlliesArea', 'Top', siege=0)")

    cartes = monde.object_manager.card_dict
    assert cartes[allie].face.card.area is joueur.allies, \
        "l'allie n'est pas arrive dans les Allies du joueur"
    assert cartes[soutien].face.card.area is joueur.supports, \
        "le soutien n'est pas arrive dans les Soutiens du joueur"
    for nom, ident in (("allie", allie), ("soutien", soutien)):
        assert cartes[ident].face.IsInPlay(), f"{nom} pose mais pas en jeu"
        assert cartes[ident].face.card.IsFaceUp(), f"{nom} pose face cachee"
    gestes = len(jeu.session.scene.manuel_commands) - avant
    assert gestes == 4, f"4 gestes attendus, {gestes} enregistres"
    assert monde.manuel_actif is True, "le moteur a quitte le silence"

    compteurs = cartes[tireur].face.GetCounters("web")
    assert compteurs == 3, f"Web-Shooter devait arriver avec 3 compteurs, il en a {compteurs!r}"
    assert cartes[coriace].face.IsTough(), "Luke Cage devait arriver Tenace (Toughness)"
    return "allie et soutien poses depuis la main ; Uses et Tenace poses a l'arrivee"


def cas_manigance_posee_avec_sa_menace(game_dir, port):
    """Une manigance annexe posee a la main arrive avec sa menace de depart
    imprimee (question 5 du 06/10/2026), comme sur OCTGN."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    deposer(jeu, "Puzzle.MoveTo('01107', 'ProcessingArea', 'Top')")
    manigance = _carte_de_code_dans(monde.area_processing, "01107")
    deposer(jeu, f"Puzzle.MoveTo({manigance}, 'SideSchemesArea', 'Top')")
    face = monde.object_manager.card_dict[manigance].face
    assert face.card.area is monde.area_schemes_side, "la manigance n'est pas dans les annexes"
    assert face.threat == face.start_threat and face.threat > 0, \
        f"menace a l'arrivee {face.threat}, menace de depart imprimee {face.start_threat}"
    return f"manigance annexe posee avec sa menace de depart ({face.threat})"


def cas_manigance_retournee_pose_sa_menace(game_dir, port):
    """Le double-clic d'OCTGN sur une manigance la retourne (`revealHide`) :
    cachee, elle perd sa menace ; revelee sans menace, elle repose sa menace de
    depart (`placeThreatOnScheme`). Lot 6 du 06/10/2026 : le plateau envoie
    `Puzzle.Flip`, et le moteur repose la menace (`Scheme2.OnFlip`)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    deposer(jeu, "Puzzle.MoveTo('01107', 'ProcessingArea', 'Top')")
    ident = _carte_de_code_dans(monde.area_processing, "01107")
    deposer(jeu, f"Puzzle.MoveTo({ident}, 'SideSchemesArea', 'Top')")
    face = monde.object_manager.card_dict[ident].face
    assert face.start_threat > 0, "premisse cassee : menace de depart nulle, le cas ne prouverait rien"
    deposer(jeu, f"Puzzle.SetThreat({ident}, 0)")
    assert face.threat == 0, "premisse cassee : la menace n'est pas a 0"
    deposer(jeu, f"Puzzle.Flip({ident})")
    deposer(jeu, f"Puzzle.Flip({ident})")
    face = monde.object_manager.card_dict[ident].face
    assert face.card.IsFaceUp(), "deux retournements ne ramenent pas la manigance face visible"
    assert face.threat == face.start_threat, \
        f"menace apres retournement {face.threat}, menace de depart {face.start_threat}"
    return f"manigance retournee : menace de depart reposee ({face.threat})"


def cas_poser_face_cachee(game_dir, port):
    """Maj pendant le glisser, ou Ctrl+U sur une pile : la carte arrive FACE
    CACHEE, en une seule commande (lot 6 du 06/10/2026). Rouge sur l'ancien
    `puzzle.py` : `MoveTo` ne connait pas `face_cachee`."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    soutien = _creer_en_main(jeu, monde, "01006")
    avant = len(jeu.session.scene.manuel_commands)
    deposer(jeu, f"Puzzle.MoveTo({soutien}, 'SupportsArea', 'Top', siege=0, face_cachee=True)")
    carte = monde.object_manager.card_dict[soutien]
    joueur = monde.const_seat_order_players[0]
    assert carte.area is joueur.supports, "la carte n'est pas arrivee dans les soutiens"
    assert not carte.IsFaceUp(), "la carte est arrivee face visible"
    assert len(jeu.session.scene.manuel_commands) == avant + 1, "le geste a pris plus d'une commande"
    deposer(jeu, f"Puzzle.MoveTo({soutien}, 'SupportsArea', 'Top', siege=0)")
    return "carte posee face cachee en une commande"


def cas_carte_boost_face_cachee(game_dir, port):
    """Double-clic sur le mechant, ou Alt+Entree : la carte du dessus du deck
    Rencontre va FACE CACHEE dans la zone de boost, a cote du mechant, comme
    `villainBoost` d'OCTGN (actions.py:693). Rouge sur l'ancien `puzzle.py` :
    `BoostArea` n'etait pas une zone connue (07/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    deck = monde.GetScenario().encounter_deck
    dessus = deck.GetTop()
    assert dessus is not None, "premisse cassee : deck Rencontre vide"
    ident = dessus.card.object_id
    deposer(jeu, f"Puzzle.MoveTo({ident}, 'BoostArea', 'Top', face_cachee=True)")
    carte = monde.object_manager.card_dict[ident]
    assert carte.area is monde.area_boosting, "la carte n'est pas dans la zone de boost"
    assert not carte.IsFaceUp(), "la carte boost est arrivee face visible"
    return "carte boost posee face cachee a cote du mechant"


def cas_remelanger_defausse_une_commande(game_dir, port):
    """« Remelanger la defausse dans le deck » (`shuffleDiscardIntoDeck`
    d'OCTGN) est UNE commande : un seul Ctrl+Z la defait entiere (lot 6 du
    06/10/2026). Le plateau envoyait un `MoveTo` par carte, puis `Shuffle`."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    joueur = monde.const_seat_order_players[1]
    a = _creer_en_main(jeu, monde, "01002", siege=1)
    b = _creer_en_main(jeu, monde, "01006", siege=1)
    deposer(jeu, f"Puzzle.MoveTo({a}, 'DiscardPile', 'Top', siege=1)",
            f"Puzzle.MoveTo({b}, 'DiscardPile', 'Top', siege=1)")
    assert len(joueur.discard_pile.GetAll()) >= 2, "premisse cassee : defausse du siege 1 trop courte"
    avant = len(jeu.session.scene.manuel_commands)
    deposer(jeu, "Puzzle.ShuffleDiscardIntoDeck('DiscardPile', siege=1)")
    assert joueur.discard_pile.GetAll() == [], "la defausse du siege 1 n'est pas vide"
    zones = {monde.object_manager.card_dict[x].area for x in (a, b)}
    assert zones == {joueur.player_deck}, "les cartes ne sont pas dans le deck du siege 1"
    assert len(jeu.session.scene.manuel_commands) == avant + 1, "le geste a pris plus d'une commande"
    return "defausse remelangee dans le deck du siege 1, en une commande"


def cas_refus_jetons_carte_incompatible(game_dir, port):
    """En manuel, un degat ou un soin sur une carte qui n'a pas de points de
    vie (un soutien) est REFUSE, pas avale en silence : sinon le journal du
    plateau affirme un geste qui n'a rien change (lot 6 du 06/10/2026). Rouge
    sur l'ancien `puzzle.py` : aucune erreur, `sandbox_last_error` vide."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    soutien = _creer_en_main(jeu, monde, "01006")
    deposer(jeu, f"Puzzle.MoveTo({soutien}, 'SupportsArea', 'Top', siege=0)")
    gestionnaire = monde.controller_manager.device_manager
    for commande in (f"Puzzle.Damage({soutien}, 2)", f"Puzzle.Heal({soutien}, 1)"):
        gestionnaire.sandbox_last_error = ""
        deposer(jeu, commande)
        assert gestionnaire.sandbox_last_error, f"{commande} sur un soutien n'a pas ete refuse"
    vilain = id_du_vilain(monde)
    gestionnaire.sandbox_last_error = ""
    deposer(jeu, f"Puzzle.Damage({vilain}, 1)")
    assert not gestionnaire.sandbox_last_error, \
        f"temoin : un degat sur le mechant est refuse ({gestionnaire.sandbox_last_error!r})"
    return "degat et soin refuses sur un soutien, acceptes sur le mechant"


def cas_echanger_avec_le_dessus_du_deck(game_dir, port):
    """« Switch Card with top Deck Card » d'OCTGN (menu de la main) : la carte
    de la main part sur le deck, le dessus du deck vient en main, en UNE
    commande (lot 6 du 06/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    joueur = monde.const_seat_order_players[1]
    carte = _creer_en_main(jeu, monde, "01006", siege=1)
    dessus = joueur.player_deck.GetAll()[-1].card.object_id
    avant = len(jeu.session.scene.manuel_commands)
    deposer(jeu, f"Puzzle.SwapWithDeckTop({carte}, siege=1)")
    cartes = monde.object_manager.card_dict
    assert cartes[carte].area is joueur.player_deck, "la carte de la main n'est pas partie sur le deck"
    assert joueur.player_deck.GetAll()[-1].card.object_id == carte, "elle n'est pas sur le DESSUS du deck"
    assert cartes[dessus].area is joueur.hand_cards, "l'ancien dessus du deck n'est pas venu en main"
    assert len(jeu.session.scene.manuel_commands) == avant + 1, "le geste a pris plus d'une commande"
    return "carte de la main echangee avec le dessus du deck, en une commande"


def cas_mulligan_une_commande(game_dir, port):
    """« Mulligan Hand » d'OCTGN : les cartes choisies vont en defausse, on en
    repioche autant, en UNE commande (lot 6 du 06/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    joueur = monde.const_seat_order_players[1]
    a = _creer_en_main(jeu, monde, "01002", siege=1)
    b = _creer_en_main(jeu, monde, "01006", siege=1)
    taille = len(joueur.hand_cards.GetAll())
    attendues = [f.card.object_id for f in joueur.player_deck.GetAll()[-2:]]
    avant = len(jeu.session.scene.manuel_commands)
    deposer(jeu, f"Puzzle.Mulligan({a}, {b}, siege=1)")
    cartes = monde.object_manager.card_dict
    assert {cartes[a].area, cartes[b].area} == {joueur.discard_pile}, "les cartes choisies ne sont pas en defausse"
    assert len(joueur.hand_cards.GetAll()) == taille, "la main n'a pas retrouve sa taille"
    assert all(cartes[x].area is joueur.hand_cards for x in attendues), "on n'a pas repioche le dessus du deck"
    assert len(jeu.session.scene.manuel_commands) == avant + 1, "le geste a pris plus d'une commande"
    return "mulligan de 2 cartes en une commande"


def cas_piocher_jusqu_a_la_main_remelange(game_dir, port):
    """F12 d'OCTGN (`doEndHeroPhase`, `drawMany`, `checkDeckRemainingCards`) :
    on pioche jusqu'a la taille de main, et un deck vide se reconstitue en
    remelangeant la defausse. UNE commande par heros (lot 6 du 06/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    joueur = monde.const_seat_order_players[1]
    for face in list(joueur.hand_cards.GetAll()):
        deposer(jeu, f"Puzzle.MoveTo({face.card.object_id}, 'DiscardPile', 'Top', siege=1)")
    deck = list(joueur.player_deck.GetAll())
    for face in deck[:-2]:
        deposer(jeu, f"Puzzle.MoveTo({face.card.object_id}, 'DiscardPile', 'Top', siege=1)")
    assert len(joueur.player_deck.GetAll()) == 2, "premisse cassee : le deck du siege 1 n'a pas 2 cartes"
    voulu = joueur.hand_size
    assert voulu > 2, f"premisse cassee : taille de main {voulu}"
    avant = len(jeu.session.scene.manuel_commands)
    deposer(jeu, "Puzzle.DrawUpToHandSize(siege=1)")
    assert len(joueur.hand_cards.GetAll()) == voulu, \
        f"main de {len(joueur.hand_cards.GetAll())} carte(s), attendu {voulu}"
    assert len(jeu.session.scene.manuel_commands) == avant + 1, "le geste a pris plus d'une commande"
    return f"pioche jusqu'a {voulu} cartes, defausse remelangee quand le deck s'est vide"


def cas_fin_de_round(game_dir, port):
    """Second F12 d'OCTGN (`advanceGame`, phase du mechant) : le jeton de
    premier joueur passe et le compteur de rounds avance (lot 6 du
    06/10/2026)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    premier = monde.players[0]
    round_avant = monde.round_id
    deposer(jeu, "Puzzle.EndRound()")
    assert monde.round_id == round_avant + 1, f"round {monde.round_id}, attendu {round_avant + 1}"
    assert monde.players[0] is not premier, "le jeton de premier joueur n'a pas passe"
    return f"round {monde.round_id}, premier joueur suivant"


def cas_moveto_par_siege(game_dir, port):
    """`MoveTo(..., siege=1)` vise le SIEGE 1, quel que soit l'ordre du moment.

    On tourne l'ordre des joueurs (le jeton de premier joueur) avant le
    geste : `player=1` viserait alors le siege 0, `siege=1` reste le siege 1.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    sieges = monde.const_seat_order_players
    assert len(sieges) == 2, f"premisse cassee : {len(sieges)} siege(s)"
    allie = _creer_en_main(jeu, monde, "01002", siege=1)
    monde.players.reverse()
    assert monde.const_players[1] is sieges[0], "premisse cassee : l'ordre n'a pas tourne"

    deposer(jeu, f"Puzzle.MoveTo({allie}, 'AlliesArea', 'Top', siege=1)")
    zone = monde.object_manager.card_dict[allie].face.card.area
    assert zone is sieges[1].allies, \
        "le geste n'a pas pose l'allie chez le siege 1"
    return "MoveTo(siege=1) vise le siege 1 meme quand l'ordre des joueurs a tourne"


def cas_piocher_chez_le_proprietaire(game_dir, port):
    """Piocher la carte du dessus du deck du siege 1 la met dans la main du
    SIEGE 1, pas dans celle du joueur courant (lot 5 du 06/10/2026). Le plateau
    piochait par `Puzzle.Gain`, qui donne au joueur courant (`puzzle.py`,
    `GetCurrentPlayer`). Rouge par substitution : `PIOCHE_COMMANDE=gain`."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    sieges = monde.const_seat_order_players
    assert len(sieges) == 2, f"premisse cassee : {len(sieges)} siege(s)"
    carte = _creer_en_main(jeu, monde, "01002", siege=1)
    deposer(jeu, f"Puzzle.MoveTo({carte}, 'PlayerDeck', 'Top', siege=1)")
    assert monde.object_manager.card_dict[carte].face.card.area is sieges[1].player_deck, \
        "premisse cassee : la carte n'est pas sur le deck du siege 1"
    assert monde.GetCurrentPlayer() is not sieges[1], \
        "premisse cassee : le siege 1 est le joueur courant, le cas ne prouverait rien"

    if os.environ.get("PIOCHE_COMMANDE") == "gain":
        deposer(jeu, f"Puzzle.Gain({carte})")
    else:
        deposer(jeu, f"Puzzle.MoveTo({carte}, 'HandsArea', 'Top', siege=1)")
    zone = monde.object_manager.card_dict[carte].face.card.area
    assert zone is sieges[1].hand_cards, \
        "la carte piochee n'est pas arrivee dans la main du siege 1"
    return "la carte piochee arrive dans la main de son proprietaire (siege 1)"


def cas_rejeu_geste_avec_siege(game_dir, port):
    """Un geste avec `siege` se rejoue chez le meme siege, meme si l'ordre des
    joueurs n'est plus celui du moment du geste (l'annulation recharge la
    partie et rejoue les gestes restants)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"],
                                     heros=["spider_man", "captain_marvel"])
    allie = _creer_en_main(jeu, monde, "01002", siege=1)
    monde.players.reverse()
    deposer(jeu, f"Puzzle.MoveTo({allie}, 'AlliesArea', 'Top', siege=1)")
    vilain = id_du_vilain(monde)
    deposer(jeu, f"Puzzle.Damage({vilain}, 1)")

    assert jeu.session.AnnulerDernierGeste() is True
    time.sleep(20)
    monde2 = jeu.world
    zone = monde2.object_manager.card_dict[allie].face.card.area
    assert zone is monde2.const_seat_order_players[1].allies, \
        "au rejeu, l'allie n'est pas revenu chez le siege 1"
    return "le geste avec siege est rejoue chez le meme siege"


def cas_evenement_en_resolution_du_joueur(game_dir, port):
    """Un evenement pose a la main reste a cote de SON heros, en cours de
    resolution (question 4 du 06/10/2026), jusqu'a ce qu'on le defausse."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_seat_order_players[0]
    evenement = _creer_en_main(jeu, monde, "01087")
    deposer(jeu, f"Puzzle.MoveTo({evenement}, 'PlayerProcessingArea', 'Top', siege=0)")
    carte = monde.object_manager.card_dict[evenement]
    assert carte.face.card.area is joueur.area_processing, \
        "l'evenement n'est pas dans la resolution du joueur"
    deposer(jeu, f"Puzzle.Discard({evenement})")
    assert carte.face.card.area is joueur.discard_pile, \
        "Suppr (Discard) n'a pas envoye l'evenement dans la defausse du joueur"
    return "evenement pose en resolution du joueur, puis defausse"


def _option_de(options, object_id):
    """Vrai si une option est rattachee a la carte `object_id`."""
    for o in options:
        if not isinstance(o, dict) or o.get("failure_reason"):
            continue
        for cle in ("bind_id", "card_id", "object_id", "source_id", "this_id"):
            if o.get(cle) == object_id:
                return True
    return False


def cas_allie_pose_agit_apres_reprise(game_dir, port):
    """Un allie pose a la main pendant le manuel peut agir quand le moteur
    reprend (preuve reclamee par la fiche du 05/10, lignes 50-51)."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    allie = _creer_en_main(jeu, monde, "01002")
    deposer(jeu, f"Puzzle.MoveTo({allie}, 'AlliesArea', 'Top', siege=0)")
    debut = len(OPTIONS_VUES)
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, f"reprise refusee : {statut} {corps}"
    time.sleep(15)
    vues = OPTIONS_VUES[debut:]
    assert vues, "aucune question posee apres la reprise"
    assert any(_option_de(opts, allie) for opts in vues), (
        "aucune option rattachee a l'allie pose a la main. Premiere question : "
        + json.dumps(vues[0][:4])[:900])
    return "l'allie pose a la main propose ses actions apres la reprise"


def cas_amelioration_posee_modifie_apres_reprise(game_dir, port):
    """Une amelioration attachee a la main modifie la statistique de l'identite
    une fois le moteur repris (Captain Marvel's Helmet : +1 DEF).

    Rouge jusqu'au 06/10/2026 (« DEF 1 avant, 1 apres reprise ») : les
    capacites constantes s'ARMENT sur `WhenCardEnterPlay`
    (`AbilityFactory.WhileValid`) et la porte du silence jetait ce message.
    Corrige par `EventManager.ReconcilierApresSilence`, appelee au premier
    message qui repasse la porte.

    Pas Superhuman Strength (+2 ATK a She-Hulk) : constate le 06/10/2026, le
    pilote joue une attaque des la reprise et la Forced Response de la carte
    la defausse aussitot, conformement au texte.
    """
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"], heros="captain_marvel")
    joueur = monde.const_seat_order_players[0]
    # Le geste manuel de changement de forme (Ctrl+F) : `Puzzle.Flip` sur
    # l'identite.
    if not hasattr(joueur.GetIdentity(), "defense"):
        deposer(jeu, f"Puzzle.Flip({joueur.GetIdentity().card.object_id})")
    identite = joueur.GetIdentity()
    assert hasattr(identite, "defense"), "premisse cassee : Captain Marvel n'est pas en forme heros"
    avant = identite.defense
    casque = _creer_en_main(jeu, monde, "01016")
    deposer(jeu, f"Puzzle.Attach({casque}, {identite.card.object_id})")
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, f"reprise refusee : {statut} {corps}"
    time.sleep(15)
    # Le pilote repond a la premiere option legale, qui peut etre « changer
    # de forme » (constate le 06/10/2026 : Carol Danvers au moment de la
    # mesure). Une face inactive ne porte aucun modificateur : on remet la
    # forme heros depuis ce fil (le moteur conduit, personne d'autre ne
    # drainera la commande), puis on lit la DEF de la face visible.
    monde2 = jeu.world
    joueur2 = monde2.const_seat_order_players[0]
    zone = monde2.object_manager.card_dict[casque].face.card.area
    assert zone is not joueur2.discard_pile, "le casque a ete defausse apres la reprise"
    if not hasattr(joueur2.GetIdentity(), "defense"):
        deposer(jeu, f"Puzzle.Flip({joueur2.GetIdentity().card.object_id})", drainer_soi_meme=True)
    identite2 = joueur2.GetIdentity()
    assert hasattr(identite2, "defense"), "premisse cassee : pas de forme heros apres la reprise"
    apres = identite2.defense
    assert apres == avant + 1, f"DEF {avant} avant, {apres} apres reprise : +1 attendu"
    return f"l'amelioration attachee a la main compte apres la reprise (DEF {avant} -> {apres})"


def cas_entree_en_jeu_pas_relancee_a_la_reprise(game_dir, port):
    """Temoin de `ReconcilierApresSilence` : elle arme les constantes, mais
    ne relance AUCUN effet d'entree en jeu. Hawkeye (01066) « entre en jeu
    avec 4 fleches » ; pose a la main, le joueur lui met 2 fleches lui-meme.
    Apres la reprise, il en a toujours 2, jamais 6."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    tireur = _creer_en_main(jeu, monde, "01066")
    deposer(jeu, f"Puzzle.MoveTo({tireur}, 'AlliesArea', 'Top', siege=0)",
            f"Puzzle.Counter({tireur}, 'arrow', 2)")
    face = monde.object_manager.card_dict[tireur].face
    assert face.GetCounters("arrow") == 2, \
        f"premisse cassee : 2 fleches posees a la main, {face.GetCounters('arrow')} trouvees"
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, f"reprise refusee : {statut} {corps}"
    time.sleep(5)
    monde2 = jeu.world
    assert monde2.manuel_actif is False, "le moteur est reste muet"
    assert monde2.event_manager.silence_a_reconcilier is False, \
        "la porte n'a pas reconcilie apres la reprise : le temoin ne prouve rien"
    fleches = monde2.object_manager.card_dict[tireur].face.GetCounters("arrow")
    assert fleches == 2, f"2 fleches attendues apres la reprise, {fleches} trouvees"
    return "un effet d'entree en jeu n'est pas relance a la reprise (2 fleches gardees)"


def cas_reprise_avec_evenement_en_resolution(game_dir, port):
    """Un evenement laisse en resolution du joueur ne bloque pas la reprise :
    le moteur reprend la main et pose des questions."""
    jeu, monde, journal = monter_le_moteur(game_dir, port, ["mode_manuel"])
    evenement = _creer_en_main(jeu, monde, "01087")
    deposer(jeu, f"Puzzle.MoveTo({evenement}, 'PlayerProcessingArea', 'Top', siege=0)")
    avant = len(journal)
    statut, corps = _appeler_reprise(_serveur_factice(jeu), "heros")
    assert statut == 200, f"reprise refusee : {statut} {corps}"
    time.sleep(15)
    assert monde.manuel_actif is False, "le moteur est reste muet"
    assert len(journal) > avant, "le moteur n'a repose aucune question apres la reprise"
    return "la reprise conduit la partie malgre un evenement laisse en resolution"


def cas_deux_gestes_meme_carte(game_dir, port):
    """Deux gestes de suite sur la meme carte : le DERNIER gagne."""
    jeu, monde, _ = monter_le_moteur(game_dir, port, ["mode_manuel"])
    joueur = monde.const_seat_order_players[0]
    allie = _creer_en_main(jeu, monde, "01002")
    deposer(jeu, f"Puzzle.MoveTo({allie}, 'AlliesArea', 'Top', siege=0)",
            f"Puzzle.MoveTo({allie}, 'SupportsArea', 'Top', siege=0)")
    zone = monde.object_manager.card_dict[allie].face.card.area
    assert zone is joueur.supports, "le dernier geste n'a pas gagne"
    return "deux gestes sur la meme carte : le dernier gagne"


CAS = {
    "drapeau_pose": cas_drapeau_pose,
    "campagne_publiee": cas_campagne_publiee,
    "campagne_absente_hors_campagne": cas_campagne_absente_hors_campagne,
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
    "post_ferme_au_spectateur": cas_post_ferme_au_spectateur,
    "pause_refusee_au_spectateur": cas_pause_refusee_au_spectateur,
    "pause_refusee_sur_partie_declaree": cas_pause_refusee_sur_partie_declaree,
    "gestes_refuses_sans_siege": cas_gestes_refuses_sans_siege,
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
    "annulation_geste_garde_la_pause": cas_annulation_geste_garde_la_pause,
    "reponse_refusee_pendant_la_pause": cas_reponse_refusee_pendant_la_pause,
    "histoire_rejouee_apres_pause": cas_histoire_rejouee_apres_pause,
    "relire_histoire": cas_relire_histoire,
    "geste_au_bon_rang": cas_geste_au_bon_rang,
    "relire_geste_au_bon_rang": cas_relire_geste_au_bon_rang,
    "reprise_heros": cas_reprise_heros,
    "reprise_mechant": cas_reprise_mechant,
    "reprise_tour": cas_reprise_tour,
    "round_partie_declaree": cas_round_partie_declaree,
    "round_reprise_nouveau_tour": cas_round_reprise_nouveau_tour,
    "reprise_refusee": cas_reprise_refusee,
    "reprise_refusee_hors_manuel": cas_reprise_refusee_hors_manuel,
    "reprise_survit_sauvegarde": cas_reprise_survit_sauvegarde,
    "relire_reprise": cas_relire_reprise,
    "jeton_acceleration": cas_jeton_acceleration,
    "poser_depuis_la_main": cas_poser_depuis_la_main,
    "manigance_posee_avec_sa_menace": cas_manigance_posee_avec_sa_menace,
    "manigance_retournee_pose_sa_menace": cas_manigance_retournee_pose_sa_menace,
    "poser_face_cachee": cas_poser_face_cachee,
    "carte_boost_face_cachee": cas_carte_boost_face_cachee,
    "remelanger_defausse_une_commande": cas_remelanger_defausse_une_commande,
    "refus_jetons_carte_incompatible": cas_refus_jetons_carte_incompatible,
    "echanger_avec_le_dessus_du_deck": cas_echanger_avec_le_dessus_du_deck,
    "mulligan_une_commande": cas_mulligan_une_commande,
    "piocher_jusqu_a_la_main_remelange": cas_piocher_jusqu_a_la_main_remelange,
    "fin_de_round": cas_fin_de_round,
    "moveto_par_siege": cas_moveto_par_siege,
    "piocher_chez_le_proprietaire": cas_piocher_chez_le_proprietaire,
    "rejeu_geste_avec_siege": cas_rejeu_geste_avec_siege,
    "evenement_en_resolution_du_joueur": cas_evenement_en_resolution_du_joueur,
    "allie_pose_agit_apres_reprise": cas_allie_pose_agit_apres_reprise,
    "amelioration_posee_modifie_apres_reprise": cas_amelioration_posee_modifie_apres_reprise,
    "entree_en_jeu_pas_relancee_a_la_reprise": cas_entree_en_jeu_pas_relancee_a_la_reprise,
    "reprise_avec_evenement_en_resolution": cas_reprise_avec_evenement_en_resolution,
    "deux_gestes_meme_carte": cas_deux_gestes_meme_carte,
}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    # Les cas appeles par un AUTRE cas, jamais tout seuls.
    SUR_DEMANDE = {"relire_sauvegarde", "relire_marque_survit",
                   "relire_geste_ordinaire", "relire_histoire",
                   "relire_geste_au_bon_rang", "relire_reprise"}
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
