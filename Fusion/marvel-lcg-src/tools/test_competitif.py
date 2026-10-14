"""Verificateur du mode competitif Civil War (livret mc56 p.14-17).

La sonde `sonde_competitif.py` DECRIT une partie a deux camps ; cet outil la
JUGE. Il monte de vraies parties et verifie, une regle du livret a la fois :

  * la mise en place (p.14) : deux tables, deux leaders, deux decks rencontre,
    les PV du leader comptes sur SA table, et les 4 cartes joueur du leader de
    chaque camp mises de cote ;
  * le jeton de premier joueur par camp (p.16), et sa rotation a la fin de la
    phase vilain de son camp ;
  * les trois conditions de victoire, la regle des phases egales et les cinq
    departages (p.17) ;
  * l'isolement des deux tables (p.16) : aucune carte d'un camp ne doit se
    retrouver dans la zone de l'autre, meme apres une partie entiere.

Chaque cas tourne dans son PROPRE processus : le moteur ne sait monter qu'une
partie par processus (`Engine.Initialize` + `os.chdir`).

    ~/marvel-work/python/bin/python3.10 tools/test_competitif.py <game_dir absolu>
    ... tools/test_competitif.py <game_dir> --cas preparation_1v1

Viser `.game-src` (liens vers `src/`), jamais `.game` qui n'est que du
bytecode. Python 3.10 : ~/marvel-work/python/bin/python3.10
"""
import argparse
import json
from typing import Dict, Tuple
import os
import subprocess
import sys

os.environ.setdefault("RELEASE", "1")

CAS = ["preparation_1v1", "preparation_2v2", "verdicts", "cartes_du_leader", "switching_sides",
       "partie_1v1", "partie_2v2", "phased_out_57076"]

# Les 4 leaders de Civil War et leurs 4 cartes joueur (relevees dans
# `data/cards.json`, set du leader, types joueur uniquement).
CARTES_DE_LEADER = {
    "iron_man": ["56129", "56130", "56131", "56132"],
    "captain_america": ["56207", "56208", "56209", "56210"],
    "captain_marvel": ["56133", "56134", "56135", "56136"],
    "spider_woman": ["56211", "56212", "56213", "56214"],
}

# PV imprimes des leaders, PAR JOUEUR de la table qui les affronte.
PV_DE_LEADER = {"iron_man": 12, "captain_america": 14, "captain_marvel": 13, "spider_woman": 11}


# Les sieges interroges par le moteur, dans l'ordre. Sert a prouver qu'une
# fenetre de decision a bien ete offerte a un joueur donne.
SIEGES_INTERROGES = []


class Echec(Exception):
    pass


def verifier(condition: bool, message: str) -> None:
    if not condition:
        raise Echec(message)


################################################################################
# Montage d'une partie
def monter(game_dir: str, decks, camps, camp1: str, camp2: str, graine: int):
    """Monte une partie competitive et rend (jeu, monde). Le pilote repond a
    tout par la premiere option legale : une question forcee de mise en place
    n'accepte pas le vide."""
    game_dir = os.path.abspath(os.path.expanduser(game_dir))
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)
    sys.argv = [sys.argv[0], "-config_files", "launch.json", "-device", "key"]

    from engine.device.manager.base import DeviceManager

    passer = json.dumps({"id": "0", "targets": [], "resources": []})
    compteur = {"questions": 0}
    # Combien de fois la MEME question est deja revenue DANS LA MEME PHASE.
    #
    # Un pilote qui repond toujours la premiere option tourne en rond des
    # qu'une option ne change rien au plateau : il la rechoisit sans fin et la
    # partie n'avance plus. Mesure : a 4 joueurs, une capacite « Ask » visant
    # une autre identite revenait indefiniment pendant le tour de Tigra, et un
    # seul tour mangeait le plafond de questions. ⚠️ Ce n'est PAS propre au
    # mode competitif : une partie ORDINAIRE a 4 joueurs se bloque pareil.
    #
    # On repond donc la n-ieme option a la n-ieme repetition, puis on DECLINE
    # (« 0 ») au bout de trois. Mesure : la meme partie ordinaire a 4 joueurs
    # va alors jusqu'a sa fin en 226 questions.
    deja_vues: Dict[Tuple, int] = {}

    def pilote(self, data, player_id, check):
        compteur["questions"] += 1
        SIEGES_INTERROGES.append(player_id)
        if compteur["questions"] > 40000:
            raise SystemExit("plafond de questions atteint")
        brute = data.options_json or ""
        try:
            options = json.loads(brute or "[]")
        except Exception:
            return passer
        libres = [o for o in options
                  if isinstance(o, dict) and not o.get("failure_reason")]
        if not libres:
            return passer
        from engine import Engine
        monde = Engine.game.world
        clef = (monde.round_id, monde.phase_id, brute)
        vues = deja_vues.get(clef, 0)
        deja_vues[clef] = vues + 1
        if vues >= 3:
            return passer
        choix = libres[vues % len(libres)]
        legales = [str(x) for x in (choix.get("all_legal_targets") or [])]
        plage = choix.get("target_num_range") or [0, 0]
        mini = plage[0] if isinstance(plage[0], int) else 0
        return json.dumps({
            "id": str(choix.get("id", 0)),
            "targets": legales[:mini],
            "resources": [],
        })

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from engine.file.manager import FileManager
    from engine.lib import Json
    from game.scene.replay import CampaignDescriptor
    from game.game_run.game_new import NewGameDescriptor

    def lire_json(genre: str, nom: str) -> str:
        chemin = FileManager.FindJsonPath(genre, nom)
        assert chemin, f"{genre} introuvable : {nom}"
        with FileManager.OpenFile(chemin, read=True) as fichier:
            return fichier.Read()

    def sets_de_rencontre(texte: str):
        campagne = Json.LoadsAs(texte, CampaignDescriptor)
        campagne.UpdateVersion()
        vus, sortie = set(), []
        for nom in list(campagne.encounter_sets) + list(campagne.modular_sets):
            if nom not in vus:
                vus.add(nom)
                sortie.append(nom)
        return sortie

    texte1 = lire_json("Campaign", camp1)
    texte2 = lire_json("Campaign", camp2)

    descripteur = NewGameDescriptor(
        campaign_json=texte1,
        encounter_set_names=sets_de_rencontre(texte1),
        hero_json=[lire_json("Hero", x) for x in decks],
        seed=graine,
        timeout=0,
        challenges=[],
        rules=["mode_competitive"],
        campaign_log={},
        campaign_json_2=texte2,
        encounter_set_names_2=sets_de_rencontre(texte2),
        teams=list(camps),
    )

    jeu = Engine.game
    jeu.session.NewGame(descripteur)
    verifier(jeu.GameSetup(), "GameSetup a rendu faux")
    return jeu, jeu.world


################################################################################
# Les mesures communes
def mesurer_tables(monde, camp1: str, camp2: str, par_camp: int, dit) -> None:
    from game.operate.worlds import Worlds

    verifier(len(monde.game_areas) == 2, f"{len(monde.game_areas)} zone(s) de jeu au lieu de 2")

    leaders = {}
    for i, zone in enumerate(monde.game_areas):
        complots = Worlds.GetMainSchemes(zone)
        verifier(len(complots) == 1,
                 f"camp {i} : {len(complots)} complot principal au lieu de 1")
        leader = Worlds.FindVillainByGameArea(zone)
        verifier(leader is not None, f"camp {i} : aucun leader")
        leaders[i] = leader
        joueurs = monde.GetTeamPlayers(i)
        verifier(len(joueurs) == par_camp,
                 f"camp {i} : {len(joueurs)} joueur(s) au lieu de {par_camp}")

    verifier(leaders[0].name != leaders[1].name, "les deux camps ont le meme leader")
    verifier(id(leaders[0].encounter_deck) != id(leaders[1].encounter_deck),
             "les deux camps partagent le meme deck rencontre")

    # Les PV du leader se comptent sur SA table (mc56 p.14 : 1v1 ou 2v2).
    for i, nom in enumerate((camp1, camp2)):
        attendu = PV_DE_LEADER[nom] * par_camp
        verifier(leaders[i].health == attendu,
                 f"camp {i} : leader a {leaders[i].health} PV au lieu de {attendu}")
        dit(f"camp {i} : {leaders[i].name}, {leaders[i].health} PV, "
            f"{par_camp} joueur(s) en face")

    # Etape 3 : les 4 cartes joueur du leader APPORTE par chaque camp, c'est-a-dire
    # celui pose sur la table d'en face.
    apportes = {0: camp2, 1: camp1}
    for camp, nom in apportes.items():
        deck = monde.GetTeamSetAside(camp)
        ids = sorted(x.paper.card_id for x in deck.Get())
        verifier(ids == sorted(CARTES_DE_LEADER[nom]),
                 f"camp {camp} : cartes du leader mises de cote {ids} "
                 f"au lieu de {sorted(CARTES_DE_LEADER[nom])}")
        dit(f"camp {camp} : 4 cartes de {nom} mises de cote")

    # Un jeton de premier joueur PAR CAMP (p.16).
    for camp in (0, 1):
        actifs = [x for x in monde.GetTeamPlayers(camp) if x.GetIdentity().IsActive()]
        verifier(len(actifs) == 1,
                 f"camp {camp} : {len(actifs)} jeton(s) de premier joueur au lieu de 1")
    dit("un jeton de premier joueur par camp")

    # Le vocabulaire d'equipe, lu depuis chaque table (p.16).
    from game.effect.rule import GameRule
    for camp in (0, 1):
        effet = GameRule(leaders[camp])
        verifier(Worlds.GetEnemyLeader(effet) is leaders[camp],
                 f"camp {camp} : « the enemy leader » n'est pas le leader de cette table")
        verifier(Worlds.GetYourTeamLeader(effet) is leaders[1 - camp],
                 f"camp {camp} : « your leader » n'est pas celui d'en face")
        verifier(monde.GetTeamOfPlayer(Worlds.GetEnemyTeam(effet)) == 1 - camp,
                 f"camp {camp} : « the enemy team » n'est pas le camp d'en face")
    dit("« enemy leader », « your leader » et « enemy team » designent la bonne table")


def mesurer_isolement(monde, dit) -> None:
    """Aucune carte d'un camp ne vit dans la zone de l'autre (p.16)."""
    from game.operate.worlds import Worlds

    fautes = []
    for player in monde.const_seat_order_players:
        if player.is_eliminated:
            continue
        zone = player.GetIdentity().card.GetGameArea()
        zones = {
            "allies": player.allies,
            "soutiens": player.supports,
            "sbires engages": player.engaged_minions,
            "environnement": player.area_environment,
            "obligations": player.obligations_area,
            "main": player.hand_cards,
            "deck": player.player_deck,
            "defausse": player.discard_pile,
        }
        for nom, deck in zones.items():
            for carte in deck.GetAll():
                if carte.card.GetGameArea() is not zone:
                    fautes.append(f"{player.name} : {nom} / {carte.name} est sur l'autre table")

    for i, zone in enumerate(monde.game_areas):
        for scheme in Worlds.GetMainSchemes(zone):
            if scheme.card.GetGameArea() is not zone:
                fautes.append(f"complot {scheme.name} hors de sa zone")
        leader = Worlds.FindVillainByGameArea(zone)
        if leader is not None and leader.encounter_deck is not None:
            for carte in leader.encounter_deck.GetAll():
                if carte.card.GetGameArea() is not zone:
                    fautes.append(f"camp {i} : {carte.name} du deck rencontre est sur l'autre table")

    verifier(not fautes, "isolement rompu : " + " / ".join(fautes[:5]))
    dit("isolement des deux tables : aucune carte hors de sa zone")


################################################################################
# Les cas
def cas_preparation(game_dir: str, par_camp: int, dit) -> None:
    decks = ["tigra", "hulkling"] if par_camp == 1 else \
            ["tigra", "spider_man", "hulkling", "captain_marvel"]
    camps = [0, 1] if par_camp == 1 else [0, 0, 1, 1]
    _, monde = monter(game_dir, decks, camps, "iron_man", "captain_america", 1)
    mesurer_tables(monde, "iron_man", "captain_america", par_camp, dit)
    mesurer_isolement(monde, dit)

    if par_camp > 1:
        # « Each team has its own first player token that passes at the end of
        # their villain phase » : le jeton tourne DANS le camp, et l'autre camp
        # ne bouge pas.
        from game.effect.rule import GameRule
        avant = {camp: [x.name for x in monde.GetTeamPlayers(camp)] for camp in (0, 1)}
        monde.PassFirstPlayerToken(0, GameRule(monde.const_players[0].GetIdentity()))
        apres = {camp: [x.name for x in monde.GetTeamPlayers(camp)] for camp in (0, 1)}
        verifier(apres[0] == avant[0][1:] + avant[0][:1],
                 f"le jeton du camp 0 n'a pas tourne : {avant[0]} -> {apres[0]}")
        verifier(apres[1] == avant[1], f"le camp 1 a bouge alors qu'il ne jouait pas")
        for camp in (0, 1):
            actifs = [x for x in monde.GetTeamPlayers(camp) if x.GetIdentity().IsActive()]
            verifier(len(actifs) == 1 and actifs[0] is monde.GetTeamPlayers(camp)[0],
                     f"camp {camp} : le jeton n'est pas sur son premier joueur")
        dit("le jeton tourne dans son camp, et seulement dans le sien")


def cas_verdicts(game_dir: str, dit) -> None:
    """Les trois conditions, la regle des phases egales et les departages.

    On enregistre les faits sur un VRAI monde monte, sans jouer : jouer une
    partie jusqu'a chaque fin possible demanderait des heures et ne mesurerait
    pas mieux la regle."""
    _, monde = monter(game_dir, ["tigra", "hulkling"], [0, 1],
                      "iron_man", "captain_america", 1)
    competitif = monde.competitive

    def remettre():
        competitif.faits = {0: {}, 1: {}}
        competitif.by_effect = None
        competitif.camp_gagnant = -1

    # 1. Le complot principal d'une table accompli : c'est le camp d'EN FACE
    #    qui gagne, puisque ce complot est celui de SON leader.
    remettre()
    competitif.EnregistrerDefaite(0, "complot principal accompli", None)
    verifier(competitif.Verdict()[1] == "The Resistance Team Won",
             f"complot du camp 0 accompli -> {competitif.Verdict()}")

    # 2. Le leader d'une table vaincu : ce camp gagne.
    remettre()
    competitif.EnregistrerVictoire(1, "leader adverse vaincu", None)
    verifier(competitif.Verdict()[1] == "The Resistance Team Won",
             f"leader du camp 1 vaincu -> {competitif.Verdict()}")

    # 3. Les heros d'un camp tous vaincus : le camp d'en face gagne.
    remettre()
    competitif.EnregistrerDefaite(1, "tous les heros du camp sont vaincus", None)
    verifier(competitif.Verdict()[1] == "The Registration Team Won",
             f"heros du camp 1 vaincus -> {competitif.Verdict()}")

    # 4. Les deux camps perdus dans la meme fenetre : les deux perdent.
    remettre()
    competitif.EnregistrerDefaite(0, "complot principal accompli", None)
    competitif.EnregistrerDefaite(1, "tous les heros du camp sont vaincus", None)
    verifier(competitif.Verdict()[1] == "Both Teams Lost",
             f"les deux camps perdus -> {competitif.Verdict()}")

    # 5. Les deux leaders vaincus dans la meme fenetre : « the game is a tie »,
    #    et les cinq departages tranchent. Sur une partie neuve les trois
    #    premiers sont a egalite ; c'est le quatrieme (les PV restants) qui
    #    departage, Hulkling ayant 13 PV contre 10 a Tigra.
    remettre()
    competitif.EnregistrerVictoire(0, "leader adverse vaincu", None)
    competitif.EnregistrerVictoire(1, "leader adverse vaincu", None)
    for nom, mesure, _ in competitif.DEPARTAGES[:3]:
        verifier(mesure(competitif, 0) == mesure(competitif, 1),
                 f"depart de partie : « {nom} » n'est pas a egalite "
                 f"({mesure(competitif, 0)} contre {mesure(competitif, 1)})")
    verifier(competitif.Verdict()[1] == "The Resistance Team Won",
             f"departage par les PV restants -> {competitif.Verdict()}")

    # 6. Le meme cas, mais la table du camp 1 porte de la menace : le troisieme
    #    departage passe AVANT le quatrieme, et rend donc l'autre reponse.
    from game.operate.worlds import Worlds
    from game.operate.faces import Faces
    from game.effect.rule import GameRule
    complot = Worlds.GetMainSchemes(monde.game_areas[1])[0]
    Faces.PlaceCountersOn([complot], 3, 'threat', GameRule(complot))
    verifier(competitif.Verdict()[1] == "The Registration Team Won",
             f"departage par la menace -> {competitif.Verdict()}")
    dit("les cinq departages sont interroges dans l'ordre du livret")

    # 7. La regle des phases egales : une fin enregistree pendant la phase du
    #    camp qui joue en premier n'arrete rien ; celle du camp qui joue en
    #    dernier ferme la fenetre.
    remettre()
    competitif.EnregistrerDefaite(0, "complot principal accompli", None)
    competitif.AFinDePhase(0)
    verifier(not monde.is_game_over,
             "la partie s'est arretee sans que les deux camps aient joue autant de phases")
    competitif.AFinDePhase(1)
    verifier(monde.is_game_over, "la partie ne s'est pas arretee a la fin de la phase du camp 1")
    verifier(monde.game_over.reason == "The Resistance Team Won",
             f"raison de fin : {monde.game_over.reason}")
    verifier(competitif.camp_gagnant == 1, f"camp gagnant : {competitif.camp_gagnant}")
    dit("la partie ne se termine qu'a la fin de la phase du second camp")


def cas_partie(game_dir: str, par_camp: int, dit) -> None:
    """Une partie complete, menee par le pilote. Ce qui est mesure : la partie
    se termine par un verdict de camp, et elle se termine A LA FIN d'une phase
    du camp qui joue en dernier."""
    decks = ["tigra", "hulkling"] if par_camp == 1 else \
            ["tigra", "spider_man", "hulkling", "captain_marvel"]
    camps = [0, 1] if par_camp == 1 else [0, 0, 1, 1]
    jeu, monde = monter(game_dir, decks, camps, "iron_man", "captain_america", 1)

    journal = []
    vraie_fin = monde.competitive.AFinDePhase

    def espion(camp):
        avant = monde.is_game_over
        vraie_fin(camp)
        if monde.is_game_over and not avant:
            journal.append(camp)

    monde.competitive.AFinDePhase = espion
    jeu.GameLoop()

    verifier(monde.is_game_over, "la partie ne s'est pas terminee")
    verifier(monde.game_over.reason in (
        "The Registration Team Won", "The Resistance Team Won",
        "Both Teams Lost", "The Game is a Tie"),
        f"fin par une raison qui n'est pas celle d'une partie a deux camps : "
        f"{monde.game_over.reason}")
    verifier(journal == [1],
             f"la partie s'est terminee ailleurs qu'a la fin d'une phase du camp 1 : {journal}")
    dit(f"partie {par_camp}v{par_camp} : round {monde.round_id}, "
        f"fin = {monde.game_over.reason}, camp gagnant = {monde.competitive.camp_gagnant}")
    mesurer_isolement(monde, dit)


def cas_cartes_du_leader(game_dir: str, dit) -> None:
    """56128b « Now It's Personal » : chaque joueur du camp prend 2 des cartes
    mises de cote et les ajoute a sa main.

    La capacite est appelee directement : la declencher en partie demanderait
    de vaincre Choosing Sides, ce qu'aucun pilote ne sait faire a coup sur.
    Le COUT (retirer la carte de la partie) est porte par le moteur et n'est
    donc pas rejoue ici — c'est le gain qui est mesure."""
    import importlib

    _, monde = monter(game_dir, ["tigra", "hulkling"], [0, 1],
                      "iron_man", "captain_america", 1)
    from game.card.factory import CardFactory
    from game.effect.rule import GameRule

    joueur = monde.GetTeamPlayers(0)[0]
    carte = CardFactory.GenerateCard("56128b", joueur.obligations_area, monde)
    face = carte.face
    verifier(face.card.GetGameArea() is monde.GetTeamGameArea(0),
             "l'obligation n'est pas sur la table de son camp")

    reserve = monde.GetTeamSetAside(0)
    avant_reserve = len(reserve.Get())
    avant_main = joueur.hand_cards.GetSize()
    verifier(avant_reserve == 4, f"{avant_reserve} cartes de cote au lieu de 4")

    module = importlib.import_module("cards.pack.cw.standard_pvp.56128b")
    module.GetAbilities()[0].operation(GameRule(face), None)

    verifier(len(reserve.Get()) == avant_reserve - 2,
             f"{len(reserve.Get())} cartes restent de cote au lieu de 2")
    verifier(joueur.hand_cards.GetSize() == avant_main + 2,
             f"la main a {joueur.hand_cards.GetSize() - avant_main} carte(s) de plus au lieu de 2")

    gagnees = [x for x in joueur.hand_cards.Get()
               if x.paper.card_id in CARTES_DE_LEADER["captain_america"]]
    verifier(len(gagnees) == 2, f"{len(gagnees)} carte(s) du leader en main au lieu de 2")
    for face_gagnee in gagnees:
        verifier(face_gagnee.card.GetOwner() is joueur,
                 f"{face_gagnee.name} n'appartient pas au joueur qui l'a prise")
        verifier(face_gagnee.card.GetGameArea() is monde.GetTeamGameArea(0),
                 f"{face_gagnee.name} n'est pas sur la table de son camp")
    dit("le joueur prend 2 cartes de son leader, elles lui appartiennent")

    # Le camp d'en face n'a rien perdu : chaque camp a sa reserve.
    verifier(len(monde.GetTeamSetAside(1).Get()) == 4,
             "la reserve du camp d'en face a bouge")
    dit("la reserve du camp d'en face n'a pas bouge")


def cas_switching_sides(game_dir: str, dit) -> None:
    """56158 « Switching Sides » : defausser un allie, l'equipe adverse peut le
    racheter, et la carte deferle si aucun allie n'est parti.

    Comme pour 56128b, la capacite est appelee directement : attendre que le
    deck rencontre la sorte ne prouverait rien de reproductible."""
    import importlib

    _, monde = monter(game_dir, ["tigra", "hulkling"], [0, 1],
                      "iron_man", "captain_america", 1)
    from game.card.factory import CardFactory
    from game.effect.rule import GameRule

    joueur = monde.GetTeamPlayers(0)[0]
    module = importlib.import_module("cards.pack.cw.secret_avengers.56158")

    from game.operate.worlds import Worlds

    def revelation():
        """Une copie neuve de la carte, nee dans le deck rencontre du camp 0 :
        c'est ce deck qui lui donne sa table."""
        leader = Worlds.FindVillainByGameArea(monde.GetTeamGameArea(0))
        carte = CardFactory.GenerateCard("56158", leader.encounter_deck, monde)
        verifier(carte.GetGameArea() is monde.GetTeamGameArea(0),
                 "la traitrise n'est pas nee sur la table du camp 0")
        return carte.face

    # 1. Aucun allie a defausser : la carte deferle. C'est l'idiome du jeu, et
    #    il ne depend pas du mode.
    verifier(not joueur.GetControlAllies(), "le joueur a deja un allie en jeu")
    face = revelation()
    module.GetAbilities()[0].operation(GameRule(face), FausseRevelation(joueur))
    verifier(face.surge == 1, f"sans allie, la carte n'a pas deferle ({face.surge})")
    dit("sans allie a defausser, la carte deferle")

    # 2. Un allie en jeu : il est defausse, et la carte NE deferle PAS.
    allie = CardFactory.GenerateCard("56052", joueur.player_deck, monde).face  # Iron Lad
    allie.PutIntoPlay(joueur, GameRule(allie))
    verifier(joueur.GetControlAllies(), "l'allie n'est pas entre en jeu")
    face = revelation()
    SIEGES_INTERROGES.clear()
    module.GetAbilities()[0].operation(GameRule(face), FausseRevelation(joueur))
    verifier(not joueur.GetControlAllies(), "l'allie n'a pas ete defausse")
    verifier(face.surge == 0, f"avec un allie defausse, la carte a deferle ({face.surge})")
    dit("avec un allie, il est defausse et la carte ne deferle pas")

    # Le point qui manquait au moteur : la fenetre de paiement est offerte a un
    # joueur d'une AUTRE table. Le pilote ne paie pas (il ne compose jamais de
    # ressources), mais la question lui a bien ete posee.
    sieges = set(SIEGES_INTERROGES)
    adversaires = {x.player_id for x in monde.GetTeamPlayers(1)}
    verifier(sieges & adversaires,
             f"aucun joueur du camp d'en face n'a ete interroge (sieges vus : {sieges})")
    dit("la fenetre de rachat est offerte a un joueur de l'autre table")


def cas_phased_out_57076(game_dir: str, dit) -> None:
    """57076 « Phased Out », errata RR 1.8 : « Hero Interrupt » devient « Hero Action ».

    Le leader ennemi porte Taskmaster's Sword (« Hero Action ») et Cap's Helmet
    (« Hero Response »). Avant l'errata, seule la seconde etait visee. La
    capacite est appelee directement, comme pour 56128b."""
    _, monde = monter(game_dir, ["tigra", "hulkling"], [0, 1],
                      "iron_man", "captain_america", 1)
    from game.card.factory import CardFactory
    from game.effect.rule import GameRule
    from game.operate.faces import Faces
    from game.operate.worlds import Worlds
    joueur = monde.GetTeamPlayers(0)[0]
    leader = Worlds.FindVillainByGameArea(monde.GetTeamGameArea(0))
    verifier(leader is not None, "pas de leader sur la table du camp 0")
    # Le leader arrive deja equipe (Powered Gauntlets, « Hero Response ») : on
    # le deshabille pour que l'epee soit la SEULE cible possible.
    deja = list(leader.GetAttachedAttachments())
    if deja:
        Faces.DiscardAll(deja, GameRule(leader))
    verifier(not leader.GetAttachedAttachments(), "le leader porte encore une piece jointe")
    epee = CardFactory.GenerateCard("57023", leader.encounter_deck, monde).face
    Faces.MoveAllTo([epee], leader.components.inventory.deck, GameRule(epee))
    verifier(epee in leader.GetAttachedAttachments(), "l'epee n'est pas attachee au leader")

    carte = CardFactory.GenerateCard("57076", joueur.hand_cards, monde).face
    from game.message import Message
    effets = carte.effect.Find(func_name="Play", when=Message.WhenPlayerInTurn)
    verifier(len(effets) == 1, f"{len(effets)} capacite(s) Play au lieu de 1")
    effet = effets[0]
    effet.context.initiator = joueur
    effet.ability.operation(effet, None)
    verifier(epee not in leader.GetAttachedAttachments(),
             "la piece jointe « Hero Action » est restee sur le leader")
    dit("la piece jointe « Hero Action » du leader est defaussee")


class FausseRevelation:
    """Le message que la capacite lit : seul `GetToPlayer` lui sert."""

    def __init__(self, player) -> None:
        self.player = player

    def GetToPlayer(self):
        return self.player


################################################################################
def lancer_un_cas(game_dir: str, nom: str) -> int:
    def dit(message: str) -> None:
        print(f"  . {message}")

    try:
        if nom == "preparation_1v1":
            cas_preparation(game_dir, 1, dit)
        elif nom == "preparation_2v2":
            cas_preparation(game_dir, 2, dit)
        elif nom == "verdicts":
            cas_verdicts(game_dir, dit)
        elif nom == "cartes_du_leader":
            cas_cartes_du_leader(game_dir, dit)
        elif nom == "switching_sides":
            cas_switching_sides(game_dir, dit)
        elif nom == "phased_out_57076":
            cas_phased_out_57076(game_dir, dit)
        elif nom == "partie_1v1":
            cas_partie(game_dir, 1, dit)
        elif nom == "partie_2v2":
            cas_partie(game_dir, 2, dit)
        else:
            print(f"cas inconnu : {nom}")
            return 2
    except Echec as erreur:
        print(f"  x {erreur}")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("game_dir")
    ap.add_argument("--cas", default="")
    args = ap.parse_args()

    if args.cas:
        return lancer_un_cas(args.game_dir, args.cas)

    resultats = {}
    for nom in CAS:
        print(f"[{nom}]")
        sortie = subprocess.run(
            [sys.executable, os.path.abspath(__file__), args.game_dir, "--cas", nom],
            capture_output=True, text=True)
        for ligne in sortie.stdout.splitlines():
            if ligne.startswith("  "):
                print(ligne)
        resultats[nom] = sortie.returncode
        if sortie.returncode != 0:
            queue = sortie.stdout.splitlines()[-15:] + sortie.stderr.splitlines()[-15:]
            for ligne in queue:
                print(f"    | {ligne}")
        print(f"  => {'OK' if sortie.returncode == 0 else 'ECHEC'}")

    rates = [nom for nom, code in resultats.items() if code != 0]
    print()
    print(f"{len(CAS) - len(rates)}/{len(CAS)} cas OK" + (f", rates : {rates}" if rates else ""))
    return 1 if rates else 0


if __name__ == "__main__":
    sys.exit(main())
