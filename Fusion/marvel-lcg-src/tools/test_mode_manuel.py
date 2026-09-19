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
                     sauvegarde=None):
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
        import traceback
        premier = True
        while premier or jeu.state.start_state.state:
            premier = False
            try:
                if jeu.GameSetup():
                    jeu.GameLoop()
            except BaseException:
                traceback.print_exc()
                return

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


CAS = {
    "drapeau_pose": cas_drapeau_pose,
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
    "attache": cas_attache,
    "engagement": cas_engagement,
    "geste_refuse_non_enregistre": cas_geste_refuse_non_enregistre,
    "ecart_modular": cas_ecart_modular,
    "refus_publie_puis_reparti": cas_refus_publie_puis_reparti,
    "defausse_deck_special": cas_defausse_deck_special,
}


def main():
    game_dir = sys.argv[1]
    port = int(sys.argv[2])
    voulu = sys.argv[3] if len(sys.argv) > 3 else None
    # Les cas appeles par un AUTRE cas, jamais tout seuls.
    SUR_DEMANDE = {"relire_sauvegarde"}
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
