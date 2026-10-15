"""Une CHAINE de parties de campagne : N scenarios joues a la suite, l'etat reporte.

POURQUOI CET OUTIL (16/10/2026, campagne Skrull Menace)
-------------------------------------------------------
`tools/test_campagnes.py` enchaine DEUX parties (une victoire, une mise en place). Une
campagne de cinq scenarios dont l'etat voyage (zone de cooperation, Elites, Shaper...) se
prouve en jouant les scenarios a la suite, chacun monte avec ce que le panneau de recompenses
aurait reporte apres le precedent. Ce harnais le fait, avec UNE difference de fidelite voulue
avec `test_campagnes.py` :

  * le carnet qui passe d'une partie a la suivante est celui du PANNEAU, pas celui du moteur.
    Le panneau (`ui-app/src/board/campagne/preremplissage.ts`) ne reporte QUE les cles
    declarees dans `data/campagnes/<code>.json` (champs `victoire`, `victoire_commune`, et
    `victoire_commune_expert` en campagne experte, `parJoueur` developpe en « Player N <cle> »),
    ignore les champs d'un joueur ELIMINE, et fusionne le tout sur l'ancien carnet. Une cle que le
    moteur lit mais que le fichier ne declare pas est donc PERDUE a la partie suivante : on le
    voit ici, pas en jouant cinq scenarios pour rien.
  * un joueur peut CORRIGER le carnet avant de continuer (`choix`).

Les chaines vivent dans `tools/cas/<bloc>.py`, variable `CHAINES` (voir `campagne_mode.py`).

Emploi
------
    RELEASE=1 python3.10 tools/test_campagne_chaine.py <game_dir> <port_base> [rapport.json] [filtre]

Un fils par chaine (le moteur est un singleton), dossier de jeu propre par fils quand
`PARALLELES` > 1, comme `test_campagnes.py`. Journaux : `/tmp/chaine_<CAS_PREFIX><index>.log`.

Forme d'une chaine
------------------
    {
      "nom":       ce qui sera lu au rapport,
      "campagne":  code du fichier data/campagnes/<code>.json (filtre des cles reportees),
      "heros":     un deck de depart, ou une liste (multijoueur),
      "carnet":    carnet ENTRANT de la premiere partie (reglages de la campagne...),
      "preparation": fonction() jouee APRES le demarrage du moteur (cartes factices...),
      "purs":      fonction() -> (ok, message) jouee APRES le demarrage du moteur, sans partie
                   (fonctions pures du module de campagne),
      "etapes": [
        {
          "scenario": id du fichier data/scenarios/<id>.json (le `_expert` pour l'expert),
          "etape":    id du scenario dans la definition (defaut : `scenario` sans `_expert`),
          "regles":   regles supplementaires,
          "attendu":  etat du MONDE apres la mise en place (cles de `test_campagnes.etat_conforme`),
          "verifier": fonction(monde) -> (ok, message), au meme moment,
          "verifier_fin": fonction(monde) -> (ok, message), une fois la partie FINIE (apres `avant`),
          "carnet_verifier": fonction(suggestions, carnet_entrant) -> (ok, message) sur le carnet SORTANT,
          "questions_attendues": sous-chaines qui doivent apparaitre dans les options proposees,
          "preferer": sous-chaines : le pilote choisit la premiere option qui en contient une,
          "avant":    commandes Puzzle.* posant l'etat de fin de partie (ou fonction(monde) -> commandes),
          "fin":      "Win" (defaut), "Lose" ou "aucune" (la chaine s'arrete la),
          "carnet_attendu": {gagnee, scenario, cles, cles_presentes, cles_absentes},
          "carnet_reporte_attendu": {cle: valeur} : ce que le PANNEAU garde apres la partie,
          "choix":    {cle: valeur ou None} : corrections du joueur avant la partie suivante,
        }, ...
      ],
    }
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time

CATEGORY = "CAMPAGNES"
DOSSIER_OUTILS = os.path.dirname(os.path.abspath(__file__))
FICHIER_CAS = os.path.join(DOSSIER_OUTILS, "cas", "campagne_mode.py")


def charger_chaines():
    spec = importlib.util.spec_from_file_location("cas_campagne_mode_chaines", FICHIER_CAS)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.CHAINES


def cles_reportees(definition, etape_id, expert, total, elimines=()):
    """Les cles que le panneau de recompenses ECRIT apres une victoire de cette etape."""
    scenario = next(s for s in definition["scenarios"] if s["id"] == etape_id)
    champs = list(scenario.get("victoire") or [])
    if not scenario.get("final"):
        champs += list(definition.get("victoire_commune") or [])
        if expert:
            champs += list(definition.get("victoire_commune_expert") or [])
    cles = []
    for champ in champs:
        if champ.get("parJoueur"):
            for i in range(total):
                if i in elimines:
                    continue          # « Un héros éliminé ne participe à AUCUNE étape de victoire »
                cles.append(f"Player {i + 1} {champ['cle']}")
        else:
            cles.append(champ["cle"])
    return cles


# ------------------------------------------------------------ execution d'une
def executer_une_chaine(game_dir, port, index):
    sys.path.insert(0, DOSSIER_OUTILS)
    import test_campagnes as tc

    chaines = charger_chaines()
    chaine = chaines[index]
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    carnet_fichier = os.path.join(game_dir, f"campaign_log_chaine_{index}.json")
    cfg["campaign_log_last_file"] = carnet_fichier
    json.dump(cfg, open("launch.json", "w"), indent=2)

    prefixe = os.environ.get("CAS_PREFIX", "")
    journal = open(f"/tmp/chaine_{prefixe}{index}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    resultat = {"index": index, "nom": chaine["nom"]}

    def rendre(ok, message):
        resultat.update({"ok": bool(ok), "message": message})
        with open(f"/tmp/chaine_{prefixe}{index}.json", "w") as f:
            json.dump(resultat, f, ensure_ascii=False)
        print("RESULTAT:", resultat, flush=True)
        os._exit(0)

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine.device.manager.base import DeviceManager

    definition = None
    if chaine.get("campagne"):
        with open(os.path.join("data", "campagnes", chaine["campagne"] + ".json"), encoding="utf-8") as f:
            definition = json.load(f)

    etat = {"phase": "attente", "asks": 0, "fait": False, "questions": [], "etape": None}

    def premiere_option(data):
        """La premiere option jouable (avec le MINIMUM de cibles), ou celle que l'etape prefere."""
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        jouables = [o for o in options if isinstance(o, dict) and not o.get("failure_reason")]
        choisie = None
        for fragment in (etat["etape"] or {}).get("preferer") or []:
            choisie = next((o for o in jouables if fragment in str(o.get("name")).replace("_", " ")), None)
            if choisie is not None:
                break
        if choisie is None and jouables:
            choisie = jouables[0]
        if choisie is not None:
            o = choisie
            legales = [str(x) for x in (o.get("all_legal_targets") or [])]
            mini = (o.get("target_num_range") or [0, 0])[0]
            cibles = (etat["etape"] or {}).get("cibles") or []
            visees = legales[:mini]
            if cibles and mini >= 1 and legales:
                # `cibles` : des card_id, traduits en identifiants d'objet parmi les cibles legales.
                from engine import Engine
                trouvees = []
                for card_id in cibles:
                    for objet_id, objet in Engine.game.world.object_manager.card_dict.items():
                        face = objet.face
                        if face is not None and getattr(face.paper, "card_id", None) == card_id \
                                and str(objet_id) in legales:
                            trouvees.append(str(objet_id))
                            break
                if trouvees:
                    visees = trouvees[:mini]
            return json.dumps({"id": str(o.get("id", 0)), "targets": visees, "resources": []})
        return json.dumps({"id": "0", "targets": [], "resources": []})

    def noms_options(data):
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            return []
        return [str(o.get("name")).replace("_", " ") for o in options if isinstance(o, dict)]

    def pilote(self, data, player_id, check):
        etat["asks"] += 1
        etape = etat["etape"] or {}
        noms = noms_options(data)
        etat["questions"].append(noms)
        if etat["phase"] == "partie" and not etat["fait"]:
            if {"Attack", "Thwart", "Change_Form", "Change Form", "Recover"} & set(noms) \
                    or any(n.startswith("Change_To_") for n in noms):
                etat["fait"] = True
                from game.puzzle import PuzzleHelper
                from engine import Engine
                monde = Engine.game.world
                # ---- 1. l'etat du monde juste apres la mise en place
                try:
                    ok, message = tc.etat_conforme(monde, etape.get("attendu") or {})
                    if ok and etape.get("verifier"):
                        ok, message = etape["verifier"](monde)
                except BaseException as exc:
                    import traceback
                    traceback.print_exc()
                    rendre(False, f"{etape['nom']} : verification mal formee : {type(exc).__name__}: {exc}")
                if not ok:
                    rendre(False, f"{etape['nom']} : apres la mise en place : {message}")
                for fragment in etape.get("questions_attendues") or []:
                    if not any(fragment in n for question in etat["questions"] for n in question):
                        rendre(False, f"{etape['nom']} : aucune option « {fragment} » n'a ete proposee ; "
                                      f"vues : {sorted({n for q in etat['questions'] for n in q})[:12]}")
                for fragment in etape.get("questions_absentes") or []:
                    if any(fragment in n for question in etat["questions"] for n in question):
                        rendre(False, f"{etape['nom']} : l'option « {fragment} » ne devait pas etre proposee")
                # ---- 2. la fin de la partie
                fin = etape.get("fin", "Win")
                if fin == "aucune":
                    rendre(True, f"{etape['nom']} : etat apres mise en place conforme")
                # Les eliminations a noter AVANT la fin (la fin les fige).
                avant = etape.get("avant") or []
                commandes = list(avant(monde) if callable(avant) else avant)
                commandes.append("Puzzle.Lose()" if fin == "Lose" else "Puzzle.Win()")
                PuzzleHelper.Exec(commandes, monde)
                etat["elimines"] = [i for i, p in enumerate(monde.players) if p.is_eliminated]
                return premiere_option(data)
            if etat["asks"] > 600:
                rendre(False, f"{etape.get('nom')} : le tour du joueur n'a jamais ete atteint")
        if etat["asks"] > 1200:
            rendre(False, "trop de questions : la mise en place ne se termine pas")
        return premiere_option(data)

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader

    if chaine.get("preparation"):
        # Ex. : cartes FACTICES injectees dans CardsDB (donnees de test uniquement).
        chaine["preparation"]()

    if chaine.get("purs"):
        try:
            ok, message = chaine["purs"]()
        except BaseException as exc:
            import traceback
            traceback.print_exc()
            rendre(False, f"verification pure : {type(exc).__name__}: {exc}")
        if not ok:
            rendre(False, f"verification pure : {message}")
        if not chaine.get("etapes"):
            rendre(True, message)

    def monter(scenario, heros, carnet, regles, graine):
        scene = SceneLoader.NewScene(scenario, None, list(heros), graine)
        if carnet:
            scene.campaign.campaign_log |= {str(k): str(v) for k, v in carnet.items()}
        if "mode_campaign" not in scene.rules:
            scene.rules.append("mode_campaign")
        for regle in list(regles or []) + [r for r in os.environ.get("REGLES", "").split(",") if r]:
            if regle not in scene.rules:
                scene.rules.append(regle)
        jeu = Engine.game
        jeu.session.SetScene(scene, "Load")
        return jeu

    heros = chaine.get("heros") or ["hulkling_kajislav"]
    if isinstance(heros, str):
        heros = [heros]
    carnet = {str(k): str(v) for k, v in (chaine.get("carnet") or {}).items()}
    resume = []

    for numero, etape in enumerate(chaine["etapes"], start=1):
        etape.setdefault("nom", f"etape {numero} ({etape['scenario']})")
        etape["nom"] = f"[{numero}/{len(chaine['etapes'])}] {etape['nom']}" if not etape["nom"].startswith("[") else etape["nom"]
        etat.update({"phase": "partie", "fait": False, "questions": [], "etape": etape, "asks": 0, "elimines": []})
        if os.path.exists(carnet_fichier):
            os.remove(carnet_fichier)
        print(f"=== ETAPE {numero} : {etape['scenario']} avec le carnet {json.dumps(carnet, ensure_ascii=False)}", flush=True)
        try:
            jeu = monter(etape["scenario"], etape.get("heros") or heros, carnet, etape.get("regles"),
                         etape.get("graine", chaine.get("graine", 42)))
            if jeu.GameSetup():
                jeu.GameLoop()
        except SystemExit:
            raise
        except BaseException as exc:
            import traceback
            traceback.print_exc()
            rendre(False, f"{etape['nom']} : la partie a plante : {type(exc).__name__}: {exc}")
        if not etat["fait"]:
            rendre(False, f"{etape['nom']} : la partie ne s'est jamais terminee (fin forcee jamais atteinte)")
        if etape.get("verifier_fin"):
            # Le monde tel qu'il est a la FIN de la partie (apres `avant` et la victoire / defaite).
            try:
                ok, message = etape["verifier_fin"](Engine.game.world)
            except BaseException as exc:
                import traceback
                traceback.print_exc()
                rendre(False, f"{etape['nom']} : verification de fin mal formee : {type(exc).__name__}: {exc}")
            if not ok:
                rendre(False, f"{etape['nom']} : a la fin de la partie : {message}")

        sortant = None
        if os.path.exists(carnet_fichier):
            with open(carnet_fichier, encoding="utf-8") as f:
                sortant = json.load(f)
            print("CARNET SORTANT:", json.dumps(sortant, ensure_ascii=False), flush=True)
        if etape.get("carnet_attendu"):
            if sortant is None:
                rendre(False, f"{etape['nom']} : aucun carnet sortant ecrit")
            ok, message = tc.carnet_conforme(sortant, etape["carnet_attendu"])
            if not ok:
                rendre(False, f"{etape['nom']} : carnet sortant : {message}")

        if etape.get("carnet_verifier"):
            try:
                ok, message = etape["carnet_verifier"]((sortant or {}).get("suggestions") or {}, carnet)
            except BaseException as exc:
                import traceback
                traceback.print_exc()
                rendre(False, f"{etape['nom']} : verification du carnet mal formee : {type(exc).__name__}: {exc}")
            if not ok:
                rendre(False, f"{etape['nom']} : carnet sortant : {message}")

        if etape.get("fin", "Win") == "Lose":
            # « Une défaite n'écrit rien » : on rejoue sans pénalité, le carnet ne bouge pas.
            resume.append(f"{numero}: defaite, carnet intact")
            continue

        # ---- ce que le PANNEAU reporte
        etape_id = etape.get("etape") or etape["scenario"].replace("_expert", "")
        expert = "_expert" in etape["scenario"]
        suggestions = (sortant or {}).get("suggestions") or {}
        if definition is not None:
            cles = cles_reportees(definition, etape_id, expert, len(heros), tuple(etat["elimines"]))
            if (sortant or {}).get("scenario") != etape_id:
                rendre(False, f"{etape['nom']} : estampille {(sortant or {}).get('scenario')!r} != id d'etape {etape_id!r} "
                              f"(le panneau ignorerait tout le releve du moteur)")
            reporte = {k: suggestions[k] for k in cles if k in suggestions}
        else:
            reporte = dict(suggestions)
        carnet = {**carnet, **reporte}
        for cle, valeur in (etape.get("choix") or {}).items():
            if valeur is None:
                carnet.pop(cle, None)
            else:
                carnet[cle] = str(valeur)
        for cle, valeur in (etape.get("carnet_reporte_attendu") or {}).items():
            if carnet.get(cle) != valeur:
                rendre(False, f"{etape['nom']} : carnet reporte[{cle}] = {carnet.get(cle)!r} (attendu {valeur!r})")
        resume.append(f"{numero}: ok")

    rendre(True, f"chaine conforme ({'; '.join(resume)}) ; carnet final : "
                 f"{json.dumps({k: v for k, v in carnet.items() if not k.startswith('Player ')}, ensure_ascii=False)}")


# -------------------------------------------------------------------- lanceur
def main():
    chaines = charger_chaines()
    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    rapport = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rapport-chaines.json"
    filtre = sys.argv[4] if len(sys.argv) > 4 else None

    if os.environ.get("CHAINE_INDEX"):
        executer_une_chaine(game_dir, port, int(os.environ["CHAINE_INDEX"]))
        return

    selection = [(i, c) for i, c in enumerate(chaines) if not filtre or filtre in c["nom"]]
    if not selection:
        sys.exit("aucune chaine retenue")
    if filtre:
        print(f"FILTRE « {filtre} » : {len(selection)}/{len(chaines)} chaines retenues")

    paralleles = max(1, int(os.environ.get("PARALLELES", "1")))
    from test_campagnes import preparer_dossiers
    dossiers = preparer_dossiers(game_dir, paralleles)
    prefixe = os.environ.get("CAS_PREFIX", "")

    def lancer(rang_et_chaine):
        rang, (index, chaine) = rang_et_chaine
        dossier = dossiers[rang % len(dossiers)]
        chemin = f"/tmp/chaine_{prefixe}{index}.json"
        if os.path.exists(chemin):
            os.remove(chemin)
        env = dict(os.environ, CHAINE_INDEX=str(index))
        subprocess.run([sys.executable, os.path.abspath(__file__), dossier, str(port + index)],
                       env=env, timeout=1500, capture_output=True)
        if os.path.exists(chemin):
            with open(chemin, encoding="utf-8") as f:
                return json.load(f)
        return {"index": index, "nom": chaine["nom"], "ok": False,
                "message": f"aucun resultat (processus mort) : voir /tmp/chaine_{prefixe}{index}.log"}

    debut = time.time()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=paralleles) as pool:
        resultats = list(pool.map(lancer, enumerate(selection)))

    verts = 0
    for r in resultats:
        if r.get("ok"):
            verts += 1
            print(f"OK   {r['nom']}")
            print(f"      {r.get('message')}")
        else:
            print(f"ECHEC {r['nom']}")
            print(f"      {r.get('message')}")
    print(f"\nBILAN : {verts}/{len(resultats)} chaines passees en {int(time.time() - debut)}s")
    with open(rapport, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=1)
    sys.exit(0 if verts == len(resultats) else 1)


if __name__ == "__main__":
    main()
