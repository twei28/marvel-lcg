"""Monte une VRAIE partie pour CHAQUE deck de depart et rapporte les echecs.

Pourquoi cet outil, en plus des autres etapes du §8 :

- `test_cards.py` construit les capacites de chaque carte, mais ne monte aucune
  partie : une carte dont les DONNEES font planter le setup (cle `Uses` sur un
  allie, `ATK` au lieu de `ATK+` sur un attachement) y passe inapercue.
- `test_newgame.py` ne monte qu'UNE partie, avec un seul heros.
- `test_capacites.py` ne touche que les cartes pour lesquelles un cas existe.

Ici on parcourt `deck/starter/*.json` : chaque deck est monte en partie contre
un scenario, ce qui exerce le setup de TOUTES ses cartes (identite, cartes
signature, obligation, set nemesis, deck d'aspect) d'un seul coup.

Un deck = un processus : le moteur est un singleton et une partie plantee ne
laisse pas le monde dans un etat reutilisable.

    python3.10 tools/verifier_tous_les_decks.py <game_dir> <port_base> [rapport]

⚠ Chaque deck ouvre le port `port_base + index`. Rester sous 65535.
"""
import sys, os, json, glob, subprocess, threading, time

SCENARIO = "rhino"
SECONDES_MAX = 45


def executer_un_deck(game_dir, port, nom_deck):
    """Corps execute DANS LE PROCESSUS FILS."""
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    json.dump(cfg, open("launch.json", "w"), indent=2)

    journal = open(f"/tmp/deck_{nom_deck}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    resultat = {"deck": nom_deck, "ok": False, "message": "non demarre"}

    def rendre(ok, message):
        resultat.update(ok=bool(ok), message=message)
        with open(f"/tmp/deck_{nom_deck}.json", "w") as f:
            json.dump(resultat, f, ensure_ascii=False)
        print("RESULTAT:", resultat, flush=True)
        os._exit(0)

    try:
        from engine import Engine
        if not Engine.Initialize():
            rendre(False, "Engine.Initialize a echoue")
        from game.scene.loader import SceneLoader
        scene = SceneLoader.NewScene(SCENARIO, None, [nom_deck], 42)
        jeu = Engine.game
        jeu.session.SetScene(scene, "Load")
    except Exception as exc:
        import traceback
        traceback.print_exc()
        rendre(False, f"chargement : {type(exc).__name__}: {exc}")

    souci = {}
    compteur = {"asks": 0}

    # Le moteur reclame ses decisions via `DeviceManager.DoGetInput`. Sans
    # reponse, le setup s'arrete des le mulligan et rien ne se monte. Ce pilote
    # minimal accepte la premiere option jouable, et considere le setup REUSSI
    # des que le tour du joueur est atteint (des pouvoirs de base sont
    # proposes) : a ce stade toutes les cartes du deck ont ete manipulees.
    from engine.device.manager.base import DeviceManager

    def pilote(self, data, player_id, check):
        compteur["asks"] += 1
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        noms = {o.get("name") for o in options if isinstance(o, dict)}
        if {"Attack", "Thwart", "Change_Form", "Change Form", "Recover"} & noms \
                or any(str(n).startswith("Change_To_") for n in noms if n):
            # CORRECTIF (31/08/2026) : on releve la main ICI, au moment precis
            # ou le tour du joueur s'ouvre, et une seule fois.
            #
            # La boucle de controle plus bas sonde toutes les 0,5 s depuis un
            # AUTRE fil, pendant que ce pilote-ci continue de jouer des cartes.
            # Elle attrapait donc une main deja videe et rendait « main vide
            # apres le setup » — un ECHEC PUREMENT FAUX. Mesure du 31/08/2026 :
            # `magik` echouait dans la passe complete, puis passait 3 fois sur 3
            # en isole, avec des mains relevees a 3, 3 puis 1. La course etait
            # visible a l'oeil nu dans ces chiffres.
            if not souci.get("pret"):
                try:
                    joueur = jeu.world.players[0]
                    souci["main"] = len(list(joueur.hand_cards.Get()))
                    souci["deck"] = joueur.player_deck.GetSize()
                except Exception:
                    pass
            souci["pret"] = True
        if compteur["asks"] > 400:
            souci["exc"] = "le tour du joueur n'a jamais ete atteint"
        for o in options:
            if isinstance(o, dict) and not o.get("failure_reason"):
                legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                mini = (o.get("target_num_range") or [0, 0])[0]
                return json.dumps({"id": str(o.get("id", 0)),
                                   "targets": legales[:mini], "resources": []})
        return json.dumps({"id": "0", "targets": [], "resources": []})

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    def boucle():
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
        except SystemExit:
            pass
        except Exception as exc:
            import traceback
            traceback.print_exc()
            souci["exc"] = f"{type(exc).__name__}: {exc}"

    fil = threading.Thread(target=boucle, daemon=True)
    fil.start()

    # On laisse la partie se monter, puis on regarde l'etat du monde. Le setup
    # est le seul moment ou TOUTES les cartes du deck sont manipulees.
    debut = time.time()
    while time.time() - debut < SECONDES_MAX:
        if souci.get("exc"):
            rendre(False, f"setup : {souci['exc']}")
        monde = getattr(jeu, "world", None)
        if souci.get("pret") and monde is not None and getattr(monde, "players", None):
            # Le monde existe bien avant d'etre utilisable : `GetIdentity` va
            # lire `world.insert`, qui n'est pose qu'a la fin du setup. On
            # tolere donc l'echec et on repasse au tour suivant.
            try:
                joueur = monde.players[0]
                identite = joueur.GetIdentity()
                # Valeurs relevees par le pilote a l'ouverture du tour (voir le
                # CORRECTIF plus haut) ; on ne relit le monde que si, pour une
                # raison quelconque, elles manquent.
                taille = souci.get("main")
                reste = souci.get("deck")
                if taille is None:
                    taille = len(list(joueur.hand_cards.Get()))
                if reste is None:
                    reste = joueur.player_deck.GetSize()
            except Exception:
                identite = None
            if identite is not None:
                nom = getattr(identite.paper, "card_id", "?")
                if taille == 0:
                    rendre(False, f"main vide apres le setup (identite {nom})")
                rendre(True, f"identite {nom}, main {taille}, deck {reste}")
        time.sleep(0.5)

    rendre(False, f"aucune partie montee en {SECONDES_MAX} s")


def main():
    game_dir = os.path.expanduser(sys.argv[1])
    port_base = int(sys.argv[2])
    rapport = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rapport-decks.json"

    if os.environ.get("DECK_NOM"):
        executer_un_deck(game_dir, port_base, os.environ["DECK_NOM"])
        return

    decks = sorted(os.path.basename(p)[:-5]
                   for p in glob.glob(os.path.join(os.path.expanduser(game_dir),
                                                   "deck", "starter", "*.json")))
    resultats = []
    for index, nom in enumerate(decks):
        port = port_base + index
        assert port < 65500, f"port {port} hors plage, baisser port_base"
        chemin = f"/tmp/deck_{nom}.json"
        if os.path.exists(chemin):
            os.remove(chemin)
        env = dict(os.environ, DECK_NOM=nom)
        subprocess.run([sys.executable, os.path.abspath(__file__), game_dir,
                        str(port), rapport],
                       env=env, timeout=120, capture_output=True)
        if os.path.exists(chemin):
            resultats.append(json.load(open(chemin)))
        else:
            resultats.append({"deck": nom, "ok": False,
                              "message": f"processus mort (voir /tmp/deck_{nom}.log)"})
        etat = "OK   " if resultats[-1]["ok"] else "ECHEC"
        print(f"{etat} {nom:28s} {resultats[-1]['message']}", flush=True)

    reussis = sum(1 for r in resultats if r["ok"])
    print(f"\nBILAN : {reussis}/{len(resultats)} decks montent une partie")
    json.dump({"reussis": reussis, "total": len(resultats), "decks": resultats},
              open(rapport, "w"), indent=1, ensure_ascii=False)
    sys.exit(0 if reussis == len(resultats) else 1)


if __name__ == "__main__":
    main()
