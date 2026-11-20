"""La BOUCLE d'une campagne : ce qu'une partie laisse, la suivante le reprend.

POURQUOI CET OUTIL (19/09/2026)
-------------------------------
Tout le reste s'arrete a la derniere carte jouee. `test_capacites.py` monte UNE
partie et mesure un etat ; `autoplay.py` joue des parties mais ne lit aucun
carnet ; les tests d'ecran s'arretent au bouton « Lancer le scenario ». Il n'y
avait donc AUCUNE gate sur ce qui fait une campagne : gagner un scenario,
cocher ce qu'on emporte, et retrouver cet acquis a la mise en place du
scenario SUIVANT. Une recompense pouvait disparaitre en silence — c'est
exactement ce qui etait arrive a deux recompenses de `sm` (voir
docs/rapports/CAMPAGNES.md §11).

Chaque EPREUVE enchaine donc deux parties dans le meme processus :

  1. la partie 1 est montee en mode campagne avec un carnet ENTRANT ;
  2. on pose l'etat que la recompense demande (`avant`), puis on termine la
     partie a la demande (`Puzzle.Win()` / `Puzzle.Lose()`, ajoutes le meme
     jour : rien ne permettait de finir une partie) ;
  3. on relit le carnet SORTANT, celui que le moteur ecrit dans
     `campaign_log_last.json` et que l'ecran de campagne propose au joueur ;
  4. on y fusionne ce que le joueur COCHE (`choix`), comme le ferait le
     panneau de recompenses ;
  5. la partie 2 est montee avec ce carnet, et on mesure ce qu'il a change.

Emploi
------
    RELEASE=1 PARALLELES=4 CAS_PREFIX=camp python3.10 tools/test_campagnes.py \\
        <game_dir> <port_base> [rapport.json] ["filtre"]

`filtre` : sous-chaine cherchee dans le nom de l'epreuve (« trors », « fne »...).
Journaux : `/tmp/campagnes_<CAS_PREFIX><index>.log`.

⚠ Comme les autres harnais : un dossier de jeu par fils, jamais deux passes sur
le meme dossier, et Python 3.10 du moteur.

La table des epreuves vit a cote, dans `tools/epreuves_campagnes.py` : cet
outil-ci est generique, elle est la connaissance de chaque boite.
"""
import json
import os
import shutil
import subprocess
import sys
import time

CATEGORY = "CAMPAGNES"


# ---------------------------------------------------------------- verificateur
def _faces(monde):
    for objet in monde.object_manager.card_dict.values():
        face = getattr(objet, "face", None)
        if face is not None:
            yield face


def _id(face):
    return getattr(getattr(face, "paper", None), "card_id", None)


def _zone(monde, nom, joueur=0):
    """Les faces d'une zone nommee, du point de vue du joueur `joueur`."""
    p = monde.players[joueur] if joueur < len(monde.players) else monde.players[0]
    if nom == "main":
        return list(p.hand_cards.Get(True))
    if nom == "deck":
        return list(p.player_deck.Get(True))
    if nom == "defausse":
        return list(p.discard_pile.Get(True))
    if nom == "retirees":
        return list(monde.area_removed.Get(True))
    if nom == "victoire":
        return list(monde.victory_display.Get(True))
    if nom == "de_cote":
        return list(monde.aside_deck.Get(True)) + list(p.set_aside_deck.Get(True))
    if nom == "rencontres_recues":
        # Les cartes rencontre distribuees FACE CACHEE, en attente de
        # revelation : c'est la que « You Stand Accused! » atterrit au
        # scenario 5 de gmw.
        return list(p.dealt_encounter_cards.Get(True))
    if nom == "en_jeu":
        return [f for f in _faces(monde) if f.IsInPlay()]
    raise AssertionError(f"zone inconnue : {nom}")


def _ou_est(monde, card_id):
    """Ou se trouve REELLEMENT une carte, pour que l'echec soit lisible.

    Sans cela, un « 21183 n'est pas dans le deck » ne dit pas si la carte a
    ete melangee ailleurs, tiree en main, ou jamais creee — trois causes tres
    differentes.
    """
    connues = {}
    for i, p in enumerate(monde.players, start=1):
        connues[id(p.player_deck)] = f"deck du joueur {i}"
        connues[id(p.hand_cards)] = f"main du joueur {i}"
        connues[id(p.discard_pile)] = f"defausse du joueur {i}"
        connues[id(p.set_aside_deck)] = f"pile annexe du joueur {i}"
    connues[id(monde.area_removed)] = "cartes retirees"
    connues[id(monde.victory_display)] = "pile de victoire"
    connues[id(monde.aside_deck)] = "cartes de cote"
    lieux = []
    for face in _faces(monde):
        if _id(face) != card_id:
            continue
        aire = getattr(getattr(face, "card", None), "area", None)
        nom = connues.get(id(aire)) or getattr(aire, "name", None) or type(aire).__name__
        proprio = getattr(face, "GetOwner", None)
        proprio = proprio() if proprio else None
        lieux.append(f"{nom}{' (en jeu)' if face.IsInPlay() else ''}"
                     f"{'' if proprio is None else f', proprietaire {proprio}'}")
    return ", ".join(lieux) if lieux else "cette carte n'existe dans aucune pile"


ZONES = ("en_jeu", "main", "deck", "defausse", "retirees", "victoire", "de_cote",
         "rencontres_recues")


def etat_conforme(monde, attendu):
    """Les cles d'`attendu`, mesurees sur le monde de la partie 2.

    Volontairement proche de `etat_attendu` de `test_capacites.py`, mais
    autonome : cet outil ne doit pas dependre d'un fichier de 50 000 lignes.
    """
    soucis = []

    def ids(zone, joueur=0):
        return [_id(f) for f in _zone(monde, zone, joueur)]

    for zone in ZONES:
        for card_id in attendu.get(zone) or []:
            joueur = 0
            if isinstance(card_id, list):
                card_id, joueur = card_id
            if card_id not in ids(zone, joueur):
                soucis.append(f"{card_id} n'est pas dans « {zone} » (joueur {joueur}) ; "
                              f"elle est ici : {_ou_est(monde, card_id)}")

    for zone in ZONES:
        for card_id in attendu.get("pas_" + zone) or []:
            joueur = 0
            if isinstance(card_id, list):
                card_id, joueur = card_id
            if card_id in ids(zone, joueur):
                soucis.append(f"{card_id} EST dans « {zone} » alors qu'il ne devrait pas")

    # `parmi` : la carte doit etre dans l'UNE des piles citees. Indispensable
    # pour une carte melangee au deck du joueur a la mise en place : l'annexe
    # II du guide de reference place la mise en place de campagne (etape 13)
    # AVANT la pioche de la main de depart (etape 14), la carte peut donc tout
    # a fait se retrouver en main des la premiere seconde.
    for card_id, zones in attendu.get("parmi") or []:
        joueur = 0
        if isinstance(card_id, list):
            card_id, joueur = card_id
        if not any(card_id in ids(zone, joueur) for zone in zones):
            soucis.append(f"{card_id} n'est dans aucune de ces piles : {', '.join(zones)} ; "
                          f"elle est ici : {_ou_est(monde, card_id)}")

    # `un_parmi` : AU MOINS UNE des cartes citees est dans la pile. Le cas des
    # recompenses tirees au hasard (une amelioration de role de Mutant Genesis
    # parmi les cinq du role choisi) : la carte exacte n'est pas previsible,
    # mais le fait qu'il y en ait une, si.
    for zone, cartes in attendu.get("un_parmi") or []:
        joueur = 0
        if "@" in zone:
            zone, siege = zone.split("@", 1)
            joueur = int(siege) - 1
        presentes = [c for c in cartes if c in ids(zone, joueur)]
        if not presentes:
            soucis.append(f"aucune de ces cartes n'est dans « {zone} » : {', '.join(cartes)}")

    for zone, cartes in attendu.get("aucune_parmi") or []:
        joueur = 0
        if "@" in zone:
            zone, siege = zone.split("@", 1)
            joueur = int(siege) - 1
        presentes = [c for c in cartes if c in ids(zone, joueur)]
        if presentes:
            soucis.append(f"{', '.join(presentes)} ne devrai(en)t pas etre dans « {zone} »")

    for trait, mini in attendu.get("en_jeu_trait") or []:
        n = len([f for f in _zone(monde, "en_jeu") if f.HasTrait(trait)])
        if n < mini:
            soucis.append(f"{n} carte(s) de trait {trait} en jeu (au moins {mini} attendue)")

    # `avec_dos` : la carte en jeu est RECTO-VERSO (sa face arriere existe). Une manigance de campagne creee
    # d'une seule face se couche face cachee au lieu de se retourner (rapport #105, 21184a).
    for card_id in attendu.get("avec_dos") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (dos attendu)")
        elif not face.card.back_faces:
            soucis.append(f"{card_id} n'a pas de face arriere : « Flip this card over » la coucherait face cachee")

    for card_id, compteur, valeur in attendu.get("compteurs") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (compteur {compteur})")
        elif face.GetCounters(compteur) != valeur:
            soucis.append(f"{card_id}.{compteur} = {face.GetCounters(compteur)} (attendu {valeur})")

    # `jetons` : un JETON n'est pas un compteur. Le niveau d'alerte d'aos porte
    # des jetons de menace (`PlaceTokensOn`), lus par `GetTokens` ; les
    # chercher dans les compteurs donne zero a tous les coups.
    for card_id, jeton, valeur in attendu.get("jetons") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (jeton {jeton})")
        elif face.GetTokens(jeton) != valeur:
            soucis.append(f"{card_id}.{jeton} = {face.GetTokens(jeton)} jeton(s) (attendu {valeur})")

    # `compteurs_total` : la somme d'un compteur sur TOUTE la table. Le cas
    # des verrous de la cellule d'aos, poses sur la carte du dessus d'un deck
    # de scenario : on ne peut pas la nommer, on peut la compter.
    for compteur, valeur in attendu.get("compteurs_total") or []:
        total = sum(f.GetCounters(compteur) for f in _faces(monde) if f.IsInPlay())
        if total != valeur:
            soucis.append(f"total des compteurs « {compteur} » = {total} (attendu {valeur})")

    for card_id, statut in attendu.get("statuts") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (statut {statut})")
        elif not face.HasStatus(statut):
            soucis.append(f"{card_id} ne porte pas le statut {statut}")

    for card_id, valeur in attendu.get("menace") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (menace)")
        elif face.threat != valeur:
            soucis.append(f"menace sur {card_id} = {face.threat} (attendu {valeur})")

    for card_id, mini in attendu.get("menace_min") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (menace_min)")
        elif face.threat < mini:
            soucis.append(f"menace sur {card_id} = {face.threat} (au moins {mini} attendue)")

    for card_id, maxi in attendu.get("menace_max") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (menace_max)")
        elif face.threat > maxi:
            soucis.append(f"menace sur {card_id} = {face.threat} (au plus {maxi} attendue)")

    # Le deck RENCONTRE : une recompense peut y melanger des cartes (armes
    # experimentales de trors). Elles n'entrent pas en jeu, on ne les voit que
    # la.
    voulues = attendu.get("deck_rencontre") or []
    interdites = attendu.get("pas_deck_rencontre") or []
    if voulues or interdites:
        from game.operate.worlds import Worlds
        dedans = [_id(f) for f in Worlds.GetEncounterDeckCards(monde)]
        for card_id in voulues:
            if card_id not in dedans:
                soucis.append(f"{card_id} n'est pas dans le deck rencontre ({len(dedans)} cartes)")
        for card_id in interdites:
            if card_id in dedans:
                soucis.append(f"{card_id} EST dans le deck rencontre alors qu'il ne devrait pas")

    # Les TAILLES de pile : une punition de campagne peut defausser la moitie
    # du deck (« The Infinity Stones 1B completed » de mts) sans qu'aucune
    # carte precise soit attendue. On mesure alors le volume.
    for cle, compare in (("taille", "=="), ("taille_min", ">="), ("taille_max", "<=")):
        for zone, valeur in (attendu.get(cle) or {}).items():
            # « deck » vise le joueur 1 ; « deck@2 » vise le deuxieme siege.
            joueur = 0
            if "@" in zone:
                zone, siege = zone.split("@", 1)
                joueur = int(siege) - 1
            n = len(_zone(monde, zone, joueur))
            ok = (n == valeur) if compare == "==" else ((n >= valeur) if compare == ">=" else (n <= valeur))
            if not ok:
                soucis.append(f"« {zone} » (joueur {joueur}) = {n} carte(s), attendu {compare} {valeur} "
                              f": {[_id(f) for f in _zone(monde, zone, joueur)][:20]}")

    # `perdue` : la mise en place elle-meme peut PERDRE la partie (trois
    # membres du Conseil deja retournes, aos). Il faut pouvoir le mesurer.
    if "perdue" in attendu:
        fin = getattr(monde, "game_over", None)
        finie = bool(getattr(fin, "is_game_over", False))
        gagnee = bool(getattr(fin, "players_won", False))
        perdue = (finie and not gagnee)
        if perdue != bool(attendu["perdue"]):
            soucis.append(f"partie perdue a la mise en place = {perdue} "
                          f"(attendu {attendu['perdue']} ; finie={finie}, gagnee={gagnee})")

    if "taille_main" in attendu:
        n = len(_zone(monde, "main"))
        if n != attendu["taille_main"]:
            soucis.append(f"main = {n} carte(s) (attendu {attendu['taille_main']})")

    # `degats` : les degats subis par une carte qui n'est pas l'identite —
    # une alliee de scenario comme Hope Summers, dont l'etat se reporte d'un
    # scenario au suivant.
    for card_id, valeur in attendu.get("degats") or []:
        face = next((f for f in _faces(monde) if _id(f) == card_id and f.IsInPlay()), None)
        if face is None:
            soucis.append(f"{card_id} n'est pas en jeu (degats)")
        else:
            subis = face.max_health - face.health
            if subis != valeur:
                soucis.append(f"degats sur {card_id} = {subis} (attendu {valeur})")

    if "pv_identite" in attendu:
        identite = monde.players[0].GetIdentity()
        reste = identite.health
        if reste != attendu["pv_identite"]:
            soucis.append(f"PV de l'identite = {reste} (attendu {attendu['pv_identite']})")

    if "degats_identite" in attendu:
        identite = monde.players[0].GetIdentity()
        subis = identite.max_health - identite.health
        if subis != attendu["degats_identite"]:
            soucis.append(f"degats sur l'identite = {subis} (attendu {attendu['degats_identite']})")

    return (not soucis), " ; ".join(soucis)


def carnet_conforme(carnet, attendu):
    """Le carnet SORTANT : `gagnee`, `scenario` (estampille), `cles`,
    `cles_presentes`, `cles_absentes`."""
    suggestions = (carnet or {}).get("suggestions") or {}
    soucis = []
    if "gagnee" in attendu and bool((carnet or {}).get("players_won")) != attendu["gagnee"]:
        soucis.append(f"players_won = {(carnet or {}).get('players_won')} (attendu {attendu['gagnee']})")
    if "scenario" in attendu and (carnet or {}).get("scenario") != attendu["scenario"]:
        soucis.append(f"estampille = {(carnet or {}).get('scenario')!r} (attendu {attendu['scenario']!r})")
    for cle, valeur in (attendu.get("cles") or {}).items():
        if suggestions.get(cle) != valeur:
            soucis.append(f"carnet[{cle}] = {suggestions.get(cle)!r} (attendu {valeur!r})")
    for cle in attendu.get("cles_presentes") or []:
        if cle not in suggestions:
            soucis.append(f"{cle} manque au carnet sortant")
    for cle in attendu.get("cles_absentes") or []:
        if cle in suggestions:
            soucis.append(f"{cle} = {suggestions[cle]!r} alors qu'il ne devrait pas y etre")
    return (not soucis), " ; ".join(soucis)


# ------------------------------------------------------------ execution d'une
def executer_une_epreuve(game_dir, port, index):
    """Corps execute DANS LE PROCESSUS FILS : deux parties, un carnet entre."""
    from epreuves_campagnes import EPREUVES  # noqa: E402  (apres le chdir)

    epreuve = EPREUVES[index]
    game_dir = os.path.abspath(game_dir)
    os.chdir(game_dir)
    sys.path.insert(0, game_dir)

    cfg = json.load(open("launch.json"))
    cfg["server_addresses"] = [f"127.0.0.1:{port}"]
    cfg["check_for_new_version_on_startup"] = False
    # Le carnet sortant est ecrit LA : un fichier par fils, sinon deux epreuves
    # simultanees se relisent l'une l'autre.
    carnet_fichier = os.path.join(game_dir, f"campaign_log_epreuve_{index}.json")
    cfg["campaign_log_last_file"] = carnet_fichier
    json.dump(cfg, open("launch.json", "w"), indent=2)
    if os.path.exists(carnet_fichier):
        os.remove(carnet_fichier)

    prefixe = os.environ.get("CAS_PREFIX", "")
    journal = open(f"/tmp/campagnes_{prefixe}{index}.log", "w", buffering=1)
    sys.stdout = journal
    sys.stderr = journal

    resultat = {"index": index, "nom": epreuve["nom"]}

    def rendre(ok, message):
        resultat.update({"ok": bool(ok), "message": message})
        with open(f"/tmp/campagnes_{prefixe}{index}.json", "w") as f:
            json.dump(resultat, f, ensure_ascii=False)
        print("RESULTAT:", resultat, flush=True)
        os._exit(0)

    from engine.network.web_server import WebServer
    WebServer.IsAuthenticate = lambda self, request=None: True
    WebServer.IsVersionMatch = lambda self, request=None: True
    from engine.device.manager.base import DeviceManager

    etat = {"phase": "attente", "asks": 0, "fait": False}

    def premiere_option(data):
        """Repond la premiere option jouable, avec le MINIMUM de cibles.

        Repondre « aucune cible » a un choix qui en exige une fait reposer la
        meme question a l'infini (piege paye par `test_capacites`).
        """
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            options = []
        for o in options:
            if isinstance(o, dict) and not o.get("failure_reason"):
                legales = [str(x) for x in (o.get("all_legal_targets") or [])]
                mini = (o.get("target_num_range") or [0, 0])[0]
                return json.dumps({"id": str(o.get("id", 0)),
                                   "targets": legales[:mini],
                                   "resources": []})
        return json.dumps({"id": "0", "targets": [], "resources": []})

    def noms_options(data):
        try:
            options = json.loads(data.options_json or "[]")
        except Exception:
            return set()
        return {o.get("name") for o in options if isinstance(o, dict)}

    def pilote(self, data, player_id, check):
        etat["asks"] += 1
        if etat["phase"] == "partie1" and not etat["fait"]:
            noms = noms_options(data)
            # Le tour du joueur est atteint des que les pouvoirs de base sont
            # proposes : le monde est alors dans un etat stable, et le carnet
            # sortant portera les PV, la main et le terrain d'une vraie fin.
            if {"Attack", "Thwart", "Change_Form", "Change Form", "Recover"} & noms \
                    or any(str(n).startswith("Change_To_") for n in noms if n):
                etat["fait"] = True
                from game.puzzle import PuzzleHelper
                from engine import Engine
                commandes = list(epreuve.get("avant") or [])
                commandes.append("Puzzle.Lose()" if epreuve.get("fin") == "Lose" else "Puzzle.Win()")
                PuzzleHelper.Exec(commandes, Engine.game.world)
                # ⚠ NE PAS remonter la boucle par une exception : la fin de
                # partie ouvre encore des fenetres (capacites optionnelles,
                # `WhenGameOver`), et lever depuis `DoGetInput` les coupe au
                # milieu — le moteur ecrivait alors un `crash.json`. On repond
                # normalement, la boucle s'arrete d'elle-meme.
                return premiere_option(data)
            if etat["asks"] > 400:
                rendre(False, "le tour du joueur n'a jamais ete atteint (partie 1)")
        if etat["asks"] > 800:
            rendre(False, "trop de questions : la mise en place ne se termine pas")
        return premiere_option(data)

    DeviceManager.DoGetInput = pilote
    DeviceManager.DoWaitConnect = lambda self, player_id, check: None
    DeviceManager.DoWaitSync = lambda self, player_id, check: None

    from engine import Engine
    Engine.Initialize()
    from game.scene.loader import SceneLoader

    def monter(scenario, heros, carnet):
        scene = SceneLoader.NewScene(scenario, None, list(heros), epreuve.get("graine", 42))
        if carnet:
            scene.campaign.campaign_log |= {str(k): str(v) for k, v in carnet.items()}
        if "mode_campaign" not in scene.rules:
            scene.rules.append("mode_campaign")
        # REGLES=confirm_main_scheme,confirm_side_scheme,confirm_scheme_setup_order :
        # les regles que launcher.js pose sur une partie neuve.
        for regle in filter(None, os.environ.get("REGLES", "").split(",")):
            if regle not in scene.rules:
                scene.rules.append(regle)
        jeu = Engine.game
        jeu.session.SetScene(scene, "Load")
        return jeu

    heros = epreuve.get("heros") or ["spider_man"]
    if isinstance(heros, str):
        heros = [heros]

    # ---- partie 1 : jusqu'au tour du joueur, puis fin forcee
    etat["phase"] = "partie1"
    try:
        jeu = monter(epreuve["scenario"], heros, epreuve.get("carnet"))
        if jeu.GameSetup():
            jeu.GameLoop()
    except SystemExit:
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        rendre(False, f"la partie 1 a plante : {type(exc).__name__}: {exc}")

    if not etat["fait"]:
        rendre(False, "la partie 1 ne s'est jamais terminee (fin forcee jamais atteinte)")

    # ---- le carnet sortant
    #
    # ⚠ TOUTES LES BOITES N'EN ECRIVENT PAS. Seules celles qui posent
    # `WriteCampaignLogAtGameOver` (mts et ses suivantes) laissent un fichier ;
    # pour les trois premieres (trors, sm, web_of_deceit) c'est le PANNEAU du
    # plateau qui devine les valeurs en relisant le monde (`detection` dans
    # data/campagnes/*.json, eprouve par `preremplissage.test.ts`). Une epreuve
    # sans `carnet_attendu` se contente donc du carnet ENTRANT plus ce que le
    # joueur coche : on mesure alors la seule chose qui reste au moteur, ce que
    # le carnet CHANGE a la mise en place suivante.
    carnet_sortant = None
    if os.path.exists(carnet_fichier):
        with open(carnet_fichier, encoding="utf-8") as f:
            carnet_sortant = json.load(f)
        print("CARNET SORTANT:", json.dumps(carnet_sortant, ensure_ascii=False), flush=True)
    elif epreuve.get("carnet_attendu"):
        rendre(False, f"aucun carnet sortant ecrit ({os.path.basename(carnet_fichier)}) : "
                      f"cette boite ne pose pas `WriteCampaignLogAtGameOver`, "
                      f"l'epreuve ne doit pas declarer `carnet_attendu`")
    else:
        print("CARNET SORTANT: aucun (boite sans WriteCampaignLogAtGameOver)", flush=True)

    if epreuve.get("carnet_attendu"):
        ok, message = carnet_conforme(carnet_sortant, epreuve["carnet_attendu"])
        if not ok:
            rendre(False, "carnet sortant : " + message)

    if not epreuve.get("suivant"):
        rendre(True, f"carnet sortant conforme : {(carnet_sortant or {}).get('suggestions')}")

    # ---- partie 2 : montee avec ce que la premiere a laisse, plus les choix
    carnet2 = dict(((carnet_sortant or {}).get("suggestions")
                    or dict(epreuve.get("carnet") or {})))
    for cle, valeur in (epreuve.get("choix") or {}).items():
        if valeur is None:
            carnet2.pop(cle, None)
        else:
            carnet2[cle] = valeur
    print("CARNET DE LA PARTIE 2:", json.dumps(carnet2, ensure_ascii=False), flush=True)

    etat["phase"] = "partie2"
    etat["fait"] = True   # plus aucune fin forcee
    heros2 = epreuve.get("heros_suivant") or heros
    if isinstance(heros2, str):
        heros2 = [heros2]
    try:
        jeu = monter(epreuve["suivant"], heros2, carnet2)
        jeu.GameSetup()
    except SystemExit:
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        rendre(False, f"la partie 2 a plante a la mise en place : {type(exc).__name__}: {exc}")

    monde = Engine.game.world
    # Un defaut DANS l'epreuve elle-meme (une cle inconnue, un couple mal
    # forme) doit echouer bruyamment : sans ce filet, l'exception remontait
    # sans que `rendre` soit jamais appele, et le fils restait pendu jusqu'a
    # la fin des temps au lieu de rapporter.
    try:
        ok, message = etat_conforme(monde, epreuve.get("attendu") or {})
    except SystemExit:
        raise
    except BaseException as exc:
        import traceback
        traceback.print_exc()
        rendre(False, f"l'attendu de l'epreuve est mal forme : {type(exc).__name__}: {exc}")
    if not ok:
        rendre(False, "partie 2 : " + message)
    rendre(True, f"boucle conforme (carnet : {carnet2})")


# -------------------------------------------------------------------- lanceur
def preparer_dossiers(game_dir, nombre):
    """Un dossier de jeu par fils : `launch.json` est unique par dossier, deux
    fils sur le meme dossier s'ecrasent leur port (piege paye par les autres
    harnais). Les dossiers de jeu sont des liens symboliques RELATIFS : on les
    recopie tels quels avec `os.readlink`."""
    game_dir = os.path.abspath(game_dir)
    if nombre <= 1:
        return [game_dir]
    dossiers = []
    for i in range(nombre):
        cible = f"{game_dir}-camp{i}"
        if not os.path.isdir(cible):
            os.makedirs(cible)
            for nom in os.listdir(game_dir):
                src = os.path.join(game_dir, nom)
                dst = os.path.join(cible, nom)
                if os.path.islink(src):
                    os.symlink(os.readlink(src), dst)
                elif os.path.isfile(src):
                    shutil.copy2(src, dst)
        dossiers.append(cible)
    return dossiers


def main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from epreuves_campagnes import EPREUVES

    game_dir = os.path.expanduser(sys.argv[1])
    port = int(sys.argv[2])
    rapport = sys.argv[3] if len(sys.argv) > 3 else "/tmp/rapport-campagnes.json"
    filtre = sys.argv[4] if len(sys.argv) > 4 else None

    if os.environ.get("EPREUVE_INDEX"):
        executer_une_epreuve(game_dir, port, int(os.environ["EPREUVE_INDEX"]))
        return

    selection = [(i, e) for i, e in enumerate(EPREUVES)
                 if not filtre or filtre in e["nom"]]
    if filtre:
        print(f"FILTRE « {filtre} » : {len(selection)}/{len(EPREUVES)} epreuves retenues")
    if not selection:
        sys.exit("aucune epreuve retenue")

    paralleles = max(1, int(os.environ.get("PARALLELES", "1")))
    dossiers = preparer_dossiers(game_dir, paralleles)
    prefixe = os.environ.get("CAS_PREFIX", "")

    def lancer(rang_et_epreuve):
        rang, (index, epreuve) = rang_et_epreuve
        dossier = dossiers[rang % len(dossiers)]
        for vieux in (f"/tmp/campagnes_{prefixe}{index}.json",):
            if os.path.exists(vieux):
                os.remove(vieux)
        env = dict(os.environ, EPREUVE_INDEX=str(index))
        subprocess.run([sys.executable, os.path.abspath(__file__), dossier, str(port + index)],
                       env=env, timeout=900, capture_output=True)
        chemin = f"/tmp/campagnes_{prefixe}{index}.json"
        if os.path.exists(chemin):
            with open(chemin, encoding="utf-8") as f:
                return json.load(f)
        return {"index": index, "nom": epreuve["nom"], "ok": False,
                "message": "aucun resultat (processus mort) : voir "
                           f"/tmp/campagnes_{prefixe}{index}.log"}

    debut = time.time()
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=paralleles) as pool:
        resultats = list(pool.map(lancer, enumerate(selection)))

    verts = 0
    for r in resultats:
        if r.get("ok"):
            verts += 1
            print(f"OK   {r['nom']}")
        else:
            print(f"ECHEC {r['nom']}")
            print(f"      {r.get('message')}")
    print(f"\nBILAN : {verts}/{len(resultats)} epreuves passees "
          f"en {int(time.time() - debut)}s")
    with open(rapport, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=1)
    sys.exit(0 if verts == len(resultats) else 1)


if __name__ == "__main__":
    main()
