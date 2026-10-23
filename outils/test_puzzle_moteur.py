#!/usr/bin/env python3
"""Tests du moteur sur les puzzles (E2) : on démarre le VRAI moteur, sans interface.

Lancement : python3 outils/test_puzzle_moteur.py [nom_du_cas]
Chaque cas tourne dans son propre processus : le moteur est un singleton global.
Le pilote ne répond à aucune question : dès que le moteur en pose une, la table
est figée et on l'observe. Le moteur est lu depuis les SOURCES (dossier de jeu en
liens symboliques, comme `.game-src`), pas depuis du code compilé.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import time

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTEUR = os.path.join(RACINE, "Fusion", "marvel-lcg-src")

SPIDER = "01001a,01001b"   # héros de gauche
AUTRE = "12001a,12001b,12001c"   # héros de droite


def puzzle_de_base(joueurs, **extra):
    d = {
        "version": "0.5.8", "author": "test", "cover": "01071", "comment": "essai", "seed": 7,
        "villain": ["01094"], "schemes": ["01097a,01097b"], "encounter_deck": [],
        "encounter_discard_pile": [], "set_aside": [], "expert": False,
        "players": joueurs, "puzzle_command": [],
    }
    d.update(extra)
    return d


def joueur(identite, main=(), deck=(), defausse=()):
    return {"identities": [identite], "hand_cards": list(main), "player_deck": list(deck),
            "player_discard_pile": list(defausse), "set_aside": []}


# --------------------------------------------------------------------------- moteur
def monter(puzzle_dict, attente=120, fin_ok=False):
    """Démarre le moteur sur ce puzzle ; rend (jeu, monde, vue_au_premier_choix)."""
    tmp = tempfile.mkdtemp(prefix="puzzle-moteur-")
    jeu_dir = os.path.join(tmp, "jeu")
    os.makedirs(jeu_dir)
    for nom in ("data", "deck", "assets", "public", "puzzle"):
        os.symlink(os.path.join(MOTEUR, nom), os.path.join(jeu_dir, nom))
    for nom in ("cards", "core", "editor", "engine", "game"):
        os.symlink(os.path.join(MOTEUR, "src", nom), os.path.join(jeu_dir, nom))
    shutil.copy(os.path.join(MOTEUR, ".game-src", "build.py"), jeu_dir)
    cfg = json.load(open(os.path.join(MOTEUR, ".game-src", "launch.json")))
    cfg.update({
        "server_addresses": ["127.0.0.1:%d" % (30000 + os.getpid() % 20000)],
        "check_for_new_version_on_startup": False,
        "game_statistics_file": os.path.join(tmp, "statistics.json"),
        "games_history_file": os.path.join(tmp, "games_history.json"),
        "replay_folders": [os.path.join(tmp, "replays") + "/"],
        "campaign_log_last_file": os.path.join(tmp, "campaign_log.json"),
        "statistics": False,
    })
    json.dump(cfg, open(os.path.join(jeu_dir, "launch.json"), "w"), indent=2)
    os.chdir(jeu_dir)
    sys.path.insert(0, jeu_dir)

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine.device.manager.base import DeviceManager

    vue = {}
    pret = threading.Event()

    def pilote(self, data, player_id=None, check=None):
        if not pret.is_set():
            monde = Engine.game.world
            vue.update(round_id=monde.round_id, phase_state=str(monde.phase.state),
                       joueur_courant=str(getattr(monde.current_player, "name", None)))
            pret.set()
        while True:          # table figée : on observe
            time.sleep(0.5)

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, *a, **k: None
    DeviceManager.DoWaitSync = lambda self, *a, **k: None

    from engine import Engine
    Engine.Initialize()
    from engine.lib.json import Json
    from game.scene.scene import Scene
    from game.puzzle.puzzle_data import PuzzleData
    from game.puzzle.puzzle_scene import BuildPuzzleScene
    from game.puzzle.puzzle_validation import validate_puzzle

    puzzle = Json.LoadsAs(json.dumps(puzzle_dict), PuzzleData)
    erreurs = validate_puzzle(puzzle)
    assert not erreurs, erreurs
    scene = Json.LoadsAs(Json.Dumps(BuildPuzzleScene(puzzle)), Scene)
    scene.UpdateVersion()
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    def run():
        import traceback
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
            monde = jeu.world
            if fin_ok and not pret.is_set():
                vue.update(fini=True, raison=monde.game_over.reason, gagne=bool(getattr(monde.game_over, "players_won", False)))
                pret.set()
            if not pret.is_set():
                print("La boucle s'est terminée sans question : partie finie=%s, round=%s, raison=%s"
                      % (monde.is_game_over, monde.round_id, (monde.game_over.reason, [str(x) for x in (monde.game_over.players_won or [])])),
                      file=sys.stderr, flush=True)
        except BaseException:
            traceback.print_exc()
            os._exit(2)

    threading.Thread(target=run, daemon=True).start()
    assert pret.wait(attente), "le moteur n'a jamais posé de question"
    return jeu, jeu.world, vue


def ids(zone):
    """Identifiants des cartes d'une zone, du dessus (index 0) vers le dessous."""
    return [f.paper.card_id for f in zone.GetAll() if f is not None]


# --------------------------------------------------------------------------- cas
def cas_v1_un_heros():
    p = puzzle_de_base([joueur("01001b", main=["01071", "01072", "01072"], defausse=["12011"])],
                       puzzle_command=["Puzzle.Damage(c3, 12)"])
    jeu, monde, vue = monter(p)
    j = monde.const_seat_order_players[0]
    assert sorted(ids(j.hand_cards)) == ["01071", "01072", "01072"], ids(j.hand_cards)
    assert ids(j.discard_pile) == ["12011"], ids(j.discard_pile)
    return "ok"


def cas_deux_heros_zones_separees():
    p = puzzle_de_base([
        joueur(SPIDER, main=["01071", "01072"], deck=["01072", "01071", "01072"], defausse=["12011"]),
        joueur(AUTRE, main=["12007", "12009"], deck=["12003", "12007", "12009"], defausse=["12003"]),
    ])
    jeu, monde, vue = monter(p)
    s0, s1 = monde.const_seat_order_players[0], monde.const_seat_order_players[1]
    assert sorted(ids(s0.hand_cards)) == ["01071", "01072"], ("main 0", ids(s0.hand_cards))
    assert sorted(ids(s1.hand_cards)) == ["12007", "12009"], ("main 1", ids(s1.hand_cards))
    assert ids(s0.discard_pile) == ["12011"], ("défausse 0", ids(s0.discard_pile))
    assert ids(s1.discard_pile) == ["12003"], ("défausse 1", ids(s1.discard_pile))
    assert ids(s0.player_deck) == ["01072", "01071", "01072"], ("deck 0", ids(s0.player_deck))
    assert ids(s1.player_deck) == ["12003", "12007", "12009"], ("deck 1", ids(s1.player_deck))
    return "ok"


def haut_de(zone):
    return zone.GetTop().paper.card_id


def cas_ordre_v1_dernier_au_dessus():
    """Format 1 : la liste va du dessous vers le dessus (comportement historique)."""
    p = puzzle_de_base([joueur(SPIDER, deck=["01071", "01072", "12011"], defausse=["01071", "12011"])],
                       encounter_deck=["01110", "01190", "01154"])
    jeu, monde, vue = monter(p)
    s0 = monde.const_seat_order_players[0]
    assert haut_de(s0.player_deck) == "12011", haut_de(s0.player_deck)
    assert haut_de(s0.discard_pile) == "12011", haut_de(s0.discard_pile)
    from game.operate.worlds import Worlds
    rencontre = [f.paper.card_id for f in Worlds.GetEncounterDeckCards(monde)]
    assert sorted(rencontre) == ["01110", "01154", "01190"], rencontre
    return "ok"


def cas_ordre_v2_premier_au_dessus():
    """Format 2 : la liste va du dessus vers le dessous."""
    p = puzzle_de_base([joueur(SPIDER, deck=["01071", "01072", "12011"], defausse=["01071", "12011"])],
                       format=2, encounter_deck=["01110", "01190", "01154"])
    jeu, monde, vue = monter(p)
    s0 = monde.const_seat_order_players[0]
    assert haut_de(s0.player_deck) == "01071", haut_de(s0.player_deck)
    assert ids(s0.player_deck) == ["12011", "01072", "01071"], ids(s0.player_deck)
    assert haut_de(s0.discard_pile) == "01071", haut_de(s0.discard_pile)
    villain = __import__("game.operate.worlds", fromlist=["Worlds"]).Worlds.GetAllVillains(monde)[0]
    assert haut_de(villain.encounter_deck) == "01110", haut_de(villain.encounter_deck)
    return "ok"


def cas_premier_joueur():
    p = puzzle_de_base([joueur(SPIDER), joueur(AUTRE)], first_player=1)
    jeu, monde, vue = monter(p)
    assert monde.players[0] is monde.const_seat_order_players[1], "le siège 1 doit être premier"
    assert monde.GetFirstPlayer() is monde.const_seat_order_players[1]
    return "ok"


def cas_premier_joueur_par_defaut():
    p = puzzle_de_base([joueur(SPIDER), joueur(AUTRE)])
    jeu, monde, vue = monter(p)
    assert monde.GetFirstPlayer() is monde.const_seat_order_players[0]
    return "ok"


def cas_depart_phase_joueur():
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])])
    jeu, monde, vue = monter(p)
    assert vue["round_id"] == 1 and "PlayerTurn" in vue["phase_state"], vue
    return "vue=%s" % vue


def cas_depart_phase_mechant():
    """La phase des héros est sautée ; la première question est celle du round 2 (la phase du méchant et la fin de round ont été jouées).
    ⚠ Cartes de rencontre SANS Surge (01105 « I'm Tough » : un statut sur Rhino) : une carte à Surge (01191 Exhaustion) révèle la suivante,
    et avec un deck qui se remélange la boucle ne finit jamais (la phase du méchant « ne pose jamais de question »)."""
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], start_phase="villain",
                       encounter_deck=["01105", "01105"])
    jeu, monde, vue = monter(p)
    assert vue["round_id"] == 2 and "PlayerTurn" in vue["phase_state"], vue
    return "vue=%s" % vue


def cas_depart_phase_mechant_sans_deck_rencontre():
    """Deck rencontre vide : le moteur finit la partie (règle du jeu). Le puzzle doit
    donc avertir (`warn_puzzle`) plutôt que de planter."""
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], start_phase="villain")
    try:
        monter(p, attente=15)
    except AssertionError as e:
        assert "jamais posé" in str(e)
        return "ok (partie terminée par le moteur, comme prévu)"
    raise AssertionError("la partie aurait dû finir")


def cas_depart_fin_de_round():
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], start_phase="end_round")
    jeu, monde, vue = monter(p)
    assert vue["round_id"] == 2 and "PlayerTurn" in vue["phase_state"], vue
    return "vue=%s" % vue


HEROS3 = "01010a,01010b"
HEROS4 = "01029a,01029b"
HEROS5 = "01040a,01040b"


def cas_quatre_heros_zones_separees():
    """4 heros : chaque siege a SA main, SON deck et SA defausse (rien ne glisse chez le premier joueur)."""
    mains = [["01071"], ["01072", "01072"], ["12007"], ["12009", "12009", "12009"]]
    ident = [SPIDER, HEROS3, HEROS4, HEROS5]
    p = puzzle_de_base([joueur(ident[i], main=mains[i], defausse=[["12011"], ["01071"], ["01072"], ["12003"]][i]) for i in range(4)])
    jeu, monde, vue = monter(p)
    for i in range(4):
        siege = monde.const_seat_order_players[i]
        assert sorted(ids(siege.hand_cards)) == sorted(mains[i]), (i, ids(siege.hand_cards))
        assert ids(siege.discard_pile) == [["12011"], ["01071"], ["01072"], ["12003"]][i], (i, ids(siege.discard_pile))
    return "ok"


def cas_set_health_absolu():
    """Puzzle.SetHealth regle les PV ACTUELS en absolu : vers le bas (degats) comme vers le haut (soin)."""
    p = puzzle_de_base([joueur(SPIDER)], puzzle_command=["Puzzle.SetHealth('01094', 9)"])
    jeu, monde, vue = monter(p)
    from game.operate.worlds import Worlds
    rhino = Worlds.GetAllVillains(monde)[0]
    assert rhino.health == 9, rhino.health
    q = puzzle_de_base([joueur(SPIDER)], puzzle_command=["Puzzle.SetHealth('01094', 5)", "Puzzle.SetHealth('01094', 11)"])
    return "ok (bas : %d ; la remontee est jouee dans le meme processus, voir cas suivant)" % rhino.health


def cas_set_health_remonte():
    p = puzzle_de_base([joueur(SPIDER)], puzzle_command=["Puzzle.SetHealth('01094', 5)", "Puzzle.SetHealth('01094', 11)"])
    jeu, monde, vue = monter(p)
    from game.operate.worlds import Worlds
    rhino = Worlds.GetAllVillains(monde)[0]
    assert rhino.health == 11, rhino.health
    return "ok"


def cas_gain_et_pioche_visent_un_siege():
    """`siege=` fait gagner / piocher le joueur voulu, pas celui dont c'est le tour."""
    p = puzzle_de_base(
        [joueur(SPIDER, deck=["01072", "01072", "01072"]), joueur(HEROS3, deck=["01071", "01071", "01071"])],
        puzzle_command=["Puzzle.Draw(2, siege=1)", "Puzzle.Gain('01072', siege=1)"],
    )
    jeu, monde, vue = monter(p)
    s0, s1 = monde.const_seat_order_players[0], monde.const_seat_order_players[1]
    assert sorted(ids(s1.hand_cards)) == ["01071", "01071", "01072"], ("main du siege 1", ids(s1.hand_cards))
    assert ids(s0.hand_cards) == [], ("main du siege 0", ids(s0.hand_cards))
    return "ok"


def cas_mise_en_jeu_avec_etats():
    """Un puzzle pose un allie en jeu avec ses degats et un statut, regle la menace du complot et ses jetons d'acceleration."""
    p = puzzle_de_base([joueur(SPIDER)], puzzle_command=[
        "Puzzle.PutIntoPlay('01059')", "Puzzle.Damage('01059', 1)", "Puzzle.Stun('01059')",
        "Puzzle.SetThreat('01097a', 4)", "Puzzle.Token('01097a', 'acceleration_token', 2)"])
    jeu, monde, vue = monter(p)
    from game.operate.worlds import Worlds
    joueur0 = monde.const_seat_order_players[0]
    allie = next(f for f in joueur0.allies.GetAll() if f.paper.card_id == "01059")
    assert allie.max_health - allie.health == 1, ("degats", allie.max_health - allie.health)
    complot = Worlds.GetAllMainSchemes(monde)[0]
    assert complot.threat == 4, complot.threat
    return "ok"


# --------------------------------------------------------------------------- E3 : objectifs et fin
def objectif(kind, target="", text=""):
    return {"kind": kind, "target": target, "text": text}


def cas_objectif_vaincre_le_mechant_gagne():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("defeat_villain")],
                       puzzle_command=["Puzzle.Damage('01094', 99)"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"] and vue["raison"] == "Players Won", vue
    return "vue=%s" % vue


def cas_sans_objectif_la_fin_du_moteur_reste():
    """Un puzzle sans objectif garde la fin d'avant (raison native du moteur)."""
    p = puzzle_de_base([joueur(SPIDER)], format=2, puzzle_command=["Puzzle.Damage('01094', 99)"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"] and vue["raison"] == "The Final Stage of the Villain was Defeated", vue
    return "vue=%s" % vue


def cas_objectif_tous_requis_la_partie_continue():
    """Mode `all` : vaincre le mechant ne suffit pas si « survivre » reste a faire."""
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], format=2,
                       objectives=[objectif("defeat_villain"), objectif("survive")],
                       puzzle_command=["Puzzle.Damage('01094', 99)"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert not vue.get("fini"), vue
    assert not monde.is_game_over
    assert [x["done"] for x in monde.puzzle_objectives.Status()] == [True, False], monde.puzzle_objectives.Status()
    return "ok"


def cas_objectif_un_seul_requis_mode_any():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives_mode="any",
                       objectives=[objectif("defeat_villain"), objectif("free_text", text="autre")],
                       puzzle_command=["Puzzle.Damage('01094', 99)"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"], vue
    return "ok"


def cas_objectif_survivre_gagne_a_la_fin_du_round():
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], format=2, start_phase="end_round",
                       objectives=[objectif("survive")], encounter_deck=["01105", "01105"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"] and vue["raison"] == "Players Won", vue
    return "vue=%s" % vue


def cas_objectif_non_atteint_a_la_fin_du_round_perd():
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], format=2, start_phase="end_round",
                       objectives=[objectif("defeat_villain")], encounter_deck=["01105", "01105"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and not vue["gagne"] and vue["raison"] == "The Puzzle Objectives were not Met", vue
    return "vue=%s" % vue


def cas_objectif_libre_valide_a_la_main():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("free_text", text="Garde Black Cat en vie")],
                       puzzle_command=["Puzzle.ValidateObjective(0)"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"], vue
    return "ok"


def cas_objectif_libre_refuse_sur_un_autre_type():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("survive")])
    jeu, monde, vue = monter(p)
    try:
        monde.puzzle_objectives.ValidateFree(0)
    except ValueError as e:
        return "refuse : %s" % e
    raise AssertionError("la validation manuelle d'un objectif automatique aurait du etre refusee")


def cas_objectif_terminer_le_complot_principal():
    """Cible = le complot principal : l'achever est la REUSSITE, pas la defaite."""
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("complete_scheme", "01097a")],
                       puzzle_command=["Puzzle.AdvanceMainScheme()"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and vue["gagne"] and vue["raison"] == "Players Won", vue
    return "vue=%s" % vue


def cas_complot_principal_achieve_sans_etre_l_objectif_perd():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("defeat_villain")],
                       puzzle_command=["Puzzle.AdvanceMainScheme()"])
    jeu, monde, vue = monter(p, fin_ok=True)
    assert vue.get("fini") and not vue["gagne"], vue
    return "vue=%s" % vue


def cas_objectif_terminer_un_complot_annexe():
    p = puzzle_de_base([joueur(SPIDER)], format=2, objectives=[objectif("complete_scheme", "01109")],
                       puzzle_command=["Puzzle.PutIntoPlay('01109')"])
    jeu, monde, vue = monter(p)
    from game.operate.worlds import Worlds
    from game.effect.rule import GameRule
    annexe = next(f for f in Worlds.GetAllSideSchemes(monde) if f.paper.card_id == "01109")
    assert not monde.is_game_over
    annexe.Defeated(None, GameRule(annexe))
    assert monde.is_game_over and monde.game_over.reason == "Players Won", (monde.game_over.reason,)
    return "ok"


def cas_puzzle_force_le_mode_automatique():
    p = puzzle_de_base([joueur(SPIDER)], format=2)
    jeu, monde, vue = monter(p)
    assert monde.scene.is_puzzle and not monde.rule.mode_manuel
    return "ok"


CAS = {n[4:]: f for n, f in sorted(globals().items()) if n.startswith("cas_")}


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--fils":
        try:
            print(CAS[sys.argv[2]](), flush=True)
        except BaseException:
            import traceback
            traceback.print_exc()
            os._exit(1)
        os._exit(0)
    choisis = [a for a in sys.argv[1:] if a in CAS] or list(CAS)
    echecs = 0
    for nom in choisis:
        t = time.time()
        r = subprocess.run([sys.executable, os.path.abspath(__file__), "--fils", nom],
                           capture_output=True, text=True, timeout=300)
        sortie = (r.stdout.strip().splitlines() or [""])[-1]
        etat = "OK  " if r.returncode == 0 else "ECHEC"
        print(f"{etat} {nom} ({time.time() - t:.0f}s) {sortie}")
        if r.returncode != 0:
            echecs += 1
            print("\n".join(r.stderr.strip().splitlines()[-12:]))
    print("TOUT PASSE" if not echecs else f"{echecs} cas en échec")
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
