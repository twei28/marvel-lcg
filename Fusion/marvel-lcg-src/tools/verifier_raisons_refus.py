"""Un refus sans raison en francais, ca ne doit pas arriver.

    python3.10 tools/verifier_raisons_refus.py <game_dir> <port> [deck ...]

POURQUOI CET OUTIL EXISTE
-------------------------
Demande de l'utilisateur, 10/09/2026 : « quand on survole une carte qu'on ne
peut pas jouer, j'aimerais avoir la raison ». Puis, sur les motifs qu'on ne
saurait pas traduire : « ca ne doit pas arriver ».

Une consigne pareille ne se tient pas a la main. Le moteur refuse par deux
chemins : une valeur de `EffectFailure` (fini, 24 motifs) ou LE NOM DE LA
FONCTION de condition qui a dit non. Il y a 276 noms de conditions dans le
moteur et 248 de plus dans les modules de cartes : personne ne peut garantir
de tete qu'ils sont tous couverts, et surtout pas dans six mois, apres trente
cartes de plus.

CE QUE FAIT L'OUTIL
-------------------
Il monte de VRAIES parties, ecoute le canal `refus_json` que le moteur joint a
chaque question, et compare chaque code vu passer a la table de phrases du
plateau (`ui-app/src/board/raisons-refus.ts`). Un code sans phrase fait
ECHOUER l'outil, avec son nom et un exemple.

⚠ IL LIT LA TABLE DU PLATEAU, IL N'EN GARDE PAS DE COPIE. Deux listes
finiraient par diverger, et c'est justement le silence qu'on veut interdire.

CALIBRAGE (§9 de PROCESSUS-CARTE)
---------------------------------
Une gate qui repond OK ne prouve rien tant qu'on ne l'a pas vue ECHOUER.
Celle-ci a ete vue rouge le 10/09/2026 en retirant `check_can_pay` de la table
du plateau : « ECHEC : 1 code(s) sans phrase francaise : check_can_pay »,
sortie 1. Remise, elle repasse au vert.

⚠ LA CALIBRATION EXIGE LA LISTE COMPLETE DES DECKS, et cela a failli passer
inapercu. Les deux premieres tentatives, sur `spider_man` puis
`captain_marvel` SEULS, ont rendu « OK » alors que la phrase etait retiree :
ces deux decks ne produisent tout simplement pas `check_can_pay`. Une gate
verte sur un seul deck ne dit donc rien. C'est aussi pourquoi
`DECKS_PAR_DEFAUT` en compte quatre, aux couts et aux formes varies, et
pourquoi en ajouter un ne coute que 45 secondes.
"""
import collections
import json
import os
import re
import sys
import threading
import time

os.environ.setdefault("RELEASE", "1")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE_PLATEAU = os.path.join(
    os.path.dirname(os.path.dirname(RACINE)), "ui-app", "src", "board", "raisons-refus.ts"
)
SECONDES_PAR_DECK = 45
DECKS_PAR_DEFAUT = ["spider_man", "captain_marvel", "iron_patriot", "spider_woman_kajislav"]


def codes_du_plateau(chemin: str) -> set:
    """Les codes que le plateau sait mettre en francais.

    On lit le fichier TypeScript, sans l'executer : les clefs de l'objet
    `PHRASES`, plus les codes a parametres traites a part. Une expression
    reguliere suffit et evite de faire dependre une gate Python d'un runtime
    node.
    """
    texte = open(chemin, encoding="utf-8").read()
    debut = texte.index("const PHRASES")
    fin = texte.index("\n}", debut)
    corps = texte[debut:fin]
    codes = set()
    for m in re.finditer(r"^\s*(?:'([^']+)'|\"([^\"]+)\"|([A-Za-z_][A-Za-z_0-9]*))\s*:", corps,
                         re.M):
        codes.add(m.group(1) or m.group(2) or m.group(3))
    # Les codes a parametres : le plateau les reconnait par leur prefixe.
    for m in re.finditer(r"code\.startsWith\('([a-z_]+)\|'\)", texte):
        codes.add(m.group(1))
    return codes


def jouer(game_dir: str, port: int, deck: str) -> dict:
    """Monte une partie et rend les codes de refus vus passer."""
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    json.dump(cfg, open("launch.json", "w"), indent=2)

    journal = open(f"/tmp/raisons_refus_{deck}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True

    from engine import Engine
    assert Engine.Initialize()
    from game.scene.loader import SceneLoader
    scene = SceneLoader.NewScene("rhino", None, [deck], 42)
    jeu = Engine.game
    jeu.session.SetScene(scene, "Load")

    vus = collections.Counter()
    exemples = {}
    compteur = {"asks": 0}
    muettes = collections.Counter()
    exemples_muettes = {}
    sur_identite = collections.Counter()

    from engine.device.manager.base import DeviceManager

    def pilote(self, data, player_id, check):
        compteur["asks"] += 1
        try:
            refus = json.loads(getattr(data, "refus_json", None) or "[]")
        except Exception:
            refus = []
        try:
            ids_identites = {j.GetIdentity().card.object_id for j in jeu.world.players
                             if j.GetIdentity() is not None}
        except Exception:
            ids_identites = set()
        for o in refus:
            if not isinstance(o, dict):
                continue
            motif = (o.get("failure_reason") or "").strip()
            if not motif:
                continue
            if o.get("bind_id") in ids_identites:
                sur_identite[f"{o.get('name')} : {motif}"] += 1
            code = motif.split("|", 1)[0] if "|" in motif else motif
            vus[code] += 1
            exemples.setdefault(code, {"option": o.get("name"), "carte": o.get("bind_id")})
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        # CARTE MUETTE (30/09/2026) : pendant le tour, une carte de la main qui
        # n'a ni option (pas de halo) ni refus (pas d'encart) laisse le joueur
        # sans explication. On les compte, par nom d'evenement et par carte.
        evenement = getattr(data, "event_name", "") or ""
        if "Turn" in evenement:
            try:
                monde = jeu.world
                avec_option = {o.get("bind_id") for o in options if isinstance(o, dict)}
                avec_refus = {o.get("bind_id") for o in refus if isinstance(o, dict)}
                for joueur in monde.players:
                    for face in joueur.hand_cards.Get():
                        oid = face.card.object_id
                        if oid in avec_option or oid in avec_refus:
                            continue
                        cid = getattr(face.paper, "card_id", "?")
                        muettes[cid] += 1
                        exemples_muettes.setdefault(cid, {"evenement": evenement, "nom": getattr(face.paper, "name", "?")})
            except Exception as exc:
                muettes[f"(erreur {type(exc).__name__})"] += 1
        for o in options:
            if isinstance(o, dict) and not o.get("failure_reason"):
                legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                mini = (o.get("target_num_range") or [0, 0])[0]
                return json.dumps({"id": str(o.get("id", 0)), "targets": legales[:mini],
                                   "resources": []})
        return json.dumps({"id": "0", "targets": [], "resources": []})

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, pid, check: None
    DeviceManager.DoWaitSync = lambda self, pid, check: None

    def boucle():
        try:
            if jeu.GameSetup():
                jeu.GameLoop()
        except SystemExit:
            pass
        except Exception:
            import traceback
            traceback.print_exc()

    fil = threading.Thread(target=boucle, daemon=True)
    fil.start()
    debut = time.time()
    while time.time() - debut < SECONDES_PAR_DECK:
        time.sleep(0.5)

    return {"deck": deck, "asks": compteur["asks"], "vus": dict(vus), "exemples": exemples,
            "muettes": dict(muettes), "exemples_muettes": exemples_muettes,
            "sur_identite": dict(sur_identite)}


def main() -> None:
    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    decks = sys.argv[3:] or DECKS_PAR_DEFAUT

    # UN DECK = UN PROCESSUS : le moteur est un singleton global, une partie
    # montee ne laisse pas le monde reutilisable. Meme regle que
    # `verifier_tous_les_decks.py`.
    if os.environ.get("DECK_UNIQUE"):
        resultat = jouer(game_dir, port, os.environ["DECK_UNIQUE"])
        with open(f"/tmp/raisons_refus_{resultat['deck']}.json", "w") as f:
            json.dump(resultat, f, ensure_ascii=False)
        os._exit(0)

    import subprocess
    connus = codes_du_plateau(TABLE_PLATEAU)
    print(f"table du plateau : {len(connus)} codes connus")

    tous = collections.Counter()
    exemples = {}
    muettes = collections.Counter()
    exemples_muettes = {}
    sur_identite = collections.Counter()
    for index, deck in enumerate(decks):
        chemin = f"/tmp/raisons_refus_{deck}.json"
        if os.path.exists(chemin):
            os.remove(chemin)
        env = dict(os.environ, DECK_UNIQUE=deck)
        subprocess.run([sys.executable, os.path.abspath(__file__), game_dir,
                        str(port + index)],
                       env=env, timeout=SECONDES_PAR_DECK + 60, capture_output=True)
        if not os.path.exists(chemin):
            print(f"  {deck:26s} : AUCUNE PARTIE MONTEE")
            continue
        r = json.load(open(chemin))
        for code, n in r["vus"].items():
            tous[code] += n
        exemples.update(r["exemples"])
        for cid, n in (r.get("muettes") or {}).items():
            muettes[f"{deck}:{cid}"] += n
        for cid, ex in (r.get("exemples_muettes") or {}).items():
            exemples_muettes.setdefault(f"{deck}:{cid}", ex)
        for cle, n in (r.get("sur_identite") or {}).items():
            sur_identite[f"{deck} / {cle}"] += n
        print(f"  {deck:26s} : {r['asks']:5d} questions, {len(r['vus'])} codes")

    print()
    manquants = sorted(code for code in tous if code not in connus)
    for code, n in tous.most_common():
        etat = "OK " if code in connus else "SANS PHRASE"
        print(f"  {n:7d}  {etat:11s} {code}")

    if muettes:
        print()
        print("CARTES MUETTES (en main pendant le tour, ni jouables ni expliquees) :")
        for cle, n in muettes.most_common():
            print(f"  {n:7d}  {cle}   {exemples_muettes.get(cle)}")

    print()
    if sur_identite:
        print("ECHEC : un refus est attache a la carte d'IDENTITE (heros / alter ego), "
              "qui ne doit jamais porter l'encart « Injouable » :")
        for cle, n in sur_identite.most_common():
            print(f"  {n:7d}  {cle}")
        sys.exit(1)
    if manquants:
        print(f"ECHEC : {len(manquants)} code(s) sans phrase francaise :")
        for code in manquants:
            print(f"  - {code}   (exemple : {exemples.get(code)})")
        print()
        print("Ajouter la phrase dans ui-app/src/board/raisons-refus.ts,")
        print("et sa traduction anglaise dans ui-app/src/board/dico-en.ts.")
        sys.exit(1)

    if not tous:
        print("ECHEC : aucun refus vu passer. Le canal `refus_json` est-il")
        print("toujours branche ? (Controller.RendreLesRefus)")
        sys.exit(1)

    print(f"OK : les {len(tous)} codes rencontres ont tous leur phrase francaise.")


if __name__ == "__main__":
    main()
