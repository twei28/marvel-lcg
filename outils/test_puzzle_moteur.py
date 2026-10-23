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
def monter(puzzle_dict, attente=120):
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
    """La phase des héros est sautée (cartes sans surge : 01190 boucle sans némésis) ; la première question est celle du round 2
    (la phase du méchant et la fin de round ont été jouées)."""
    p = puzzle_de_base([joueur(SPIDER, main=["01071"])], start_phase="villain",
                       encounter_deck=["01191", "01191"])
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
