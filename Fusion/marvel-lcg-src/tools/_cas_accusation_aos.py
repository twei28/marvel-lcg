"""Un cas d'accusation, dans SON processus. Lance par test_accusation_aos.py.

Le moteur est un singleton global : deux cas dans le meme processus se
marcheraient dessus. Meme parti pris que tools/test_capacites.py.

Usage : python3.10 _cas_accusation_aos.py <racine> <port>
  CAMPAIGN_LOG : le carnet ENTRANT
  ETAPE        : "setup" (s'arreter apres la mise en place),
                 "puiser" (vider l'enveloppe S.H.I.E.L.D. carte par carte),
                 "accuser" (avancer a 2A et laisser la chaine se derouler)
  RAPPORT      : ou ecrire le releve
"""
import json
import os
import sys

os.environ.setdefault("RELEASE", "1")

ROOT = os.path.abspath(sys.argv[1])
PORT = int(sys.argv[2])
CAMPAIGN_LOG = json.loads(os.environ.get("CAMPAIGN_LOG", "{}"))
ETAPE = os.environ.get("ETAPE", "setup")
RAPPORT = os.environ.get("RAPPORT", "/tmp/accusation.json")
RULES = json.loads(os.environ.get("RULES", '["mode_campaign"]'))

GAME = os.path.join(ROOT, ".game")
os.chdir(GAME)
sys.path.insert(0, GAME)

try:
    import winsound  # noqa: F401
except ModuleNotFoundError:
    import types
    ws = types.ModuleType("winsound")
    for nom in ("Beep", "PlaySound", "MessageBeep"):
        setattr(ws, nom, lambda *a, **k: None)
    for nom in ("SND_FILENAME", "SND_ALIAS", "SND_LOOP", "SND_MEMORY", "SND_PURGE",
                "SND_ASYNC", "SND_NODEFAULT", "SND_NOSTOP", "SND_NOWAIT",
                "SND_APPLICATION", "MB_ICONASTERISK", "MB_ICONEXCLAMATION",
                "MB_ICONHAND", "MB_ICONQUESTION", "MB_OK"):
        setattr(ws, nom, 0)
    sys.modules["winsound"] = ws

cfg = json.load(open("launch.json"))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open("launch.json", "w"), indent=2)

from engine.network.web_server import WebServer
WebServer.IsAuthenticate = lambda self, request=None: True
WebServer.IsVersionMatch = lambda self, request=None: True

from engine.device.manager.base import DeviceManager

etat = {"asks": 0}


def pilote(self, data, player_id, check):
    """Repond la premiere option legale, comme la sonde.

    Pour l'accusation, cela fixe les trois hypotheses a la premiere de chaque
    serie — Dossiers medicaux, Argent, Habilitation — ce qui suffit : le cas
    juste ou faux se regle en choisissant l'enveloppe A.I.M. du carnet.
    """
    etat["asks"] += 1
    if etat["asks"] > 4000:
        raise SystemExit("trop de questions")
    try:
        options = json.loads(data.options_json or "[]")
    except Exception:
        options = []
    for o in options:
        if isinstance(o, dict) and not o.get("failure_reason"):
            legales = [str(x) for x in (o.get("all_legal_targets") or [])]
            mini = (o.get("target_num_range") or [0, 0])[0]
            return json.dumps({"id": str(o.get("id", 0)),
                               "targets": legales[:mini] if mini else [],
                               "resources": []})
    return json.dumps({"id": "0", "targets": [], "resources": []})


DeviceManager.DoGetInput = pilote
DeviceManager.DoWaitConnect = lambda self, p, c: None
DeviceManager.DoWaitSync = lambda self, p, c: None

from engine import Engine
Engine.Initialize()

from game.scene.loader import SceneLoader

campaign_json = open(os.path.join(GAME, "data", "scenarios", "baron_zemo.json")).read()
deck = os.path.join(GAME, "deck", "starter", "maria_hill.json")
scene = SceneLoader.NewFromJson(campaign_json, None, [open(deck).read()], 42, RULES, CAMPAIGN_LOG)
jeu = Engine.game
jeu.session.SetScene(scene, "Load")

sortie = {"erreurs": [], "etape": ETAPE}
try:
    jeu.GameSetup()
except BaseException as exc:
    sortie["erreurs"].append(f"setup : {type(exc).__name__}: {exc}")

from game.operate.worlds import Worlds
from game.effect.rule import GameRule
from game.card.face.card_type import Evidence

monde = Engine.game.world


def effet():
    return GameRule(list(Worlds.GetAllMainSchemes(monde))[0])


def releve():
    eff = effet()
    membres = {}
    for face in Worlds.FindCardsOnField(eff):
        cid = face.paper.card_id
        if cid[:5] in ("50181", "50182", "50183"):
            membres[cid] = face.GetCounters("secret")
    # Les preuves se lisent dans l'aire des preuves, pas par FindCardsOnField :
    # celui-ci filtre sur la zone de jeu de l'effet qu'on lui donne, et une
    # sonde qui fabrique son effet a la main n'a aucune raison de tomber sur la
    # bonne. L'aire, elle, est ce que le joueur voit.
    preuves = list(monde.area_evidence.GetAll())
    attaches = {}
    for p in preuves:
        # GetBindFace() leve quand la carte n'est attachee a rien, ce qui est
        # le cas normal d'une preuve gagnee : on garde None.
        try:
            lie = p.GetBindFace()
        except AssertionError:
            lie = None
        attaches[p.paper.card_id] = lie.paper.card_id if lie else None
    return {
        "membres": membres,
        "preuves_en_jeu": sorted(p.paper.card_id for p in preuves),
        "preuves_attachees_a": attaches,
        "villains": [v.paper.card_id for v in Worlds.GetAllVillains(monde)],
        "manigances": [s.paper.card_id for s in Worlds.GetAllMainSchemes(monde)],
        "carnet_preuves": monde.store.dic.get("Evidence Gained"),
    }


def descripteur():
    from game.render.to_descriptor import ToDescriptor
    from engine.lib import Json
    return json.loads(Json.Dumps(ToDescriptor.World(monde, "sonde", "")))


try:
    if ETAPE == "puiser":
        from cards.pack.aos.baron_zemo import ShieldEnvelopeHasCards, GainCardsFromShieldEnvelope
        tirages = []
        for _ in range(8):
            reste = ShieldEnvelopeHasCards(effet())
            tirages.append({"enveloppe_non_vide": bool(reste),
                            "carnet": monde.store.dic.get("Evidence Gained")})
            if not reste:
                break
            GainCardsFromShieldEnvelope(1, effet())
        sortie["tirages"] = tirages
    elif ETAPE == "accuser":
        scheme = list(Worlds.GetAllMainSchemes(monde))[0]
        sortie["stage_avant"] = scheme.paper.card_id
        scheme.Advance("2A", GameRule(scheme))
except BaseException as exc:
    import traceback
    sortie["erreurs"].append(f"{ETAPE} : {type(exc).__name__}: {exc}\n{traceback.format_exc()[-1200:]}")

try:
    sortie.update(releve())
    monde_desc = descripteur()
    plat = [c for zone in ("additional_decks", "additional_discard_piles", "area_set_aside")
            for y in (monde_desc.get(zone) or [])
            for c in (y if isinstance(y, list) else [y]) if isinstance(c, dict)]
    sortie["preuves_dans_le_descripteur"] = sorted(
        {c.get("card_id") for c in plat if str(c.get("card_id", ""))[:5] in
         ("50185", "50186", "50187", "50188", "50189", "50190", "50191", "50192", "50193")})
    sortie["descripteur_contient_le_secret"] = "A.I.M. Envelope" in json.dumps(monde_desc)
    sortie["aire_des_preuves"] = sorted(c.get("card_id") for c in (monde_desc.get("area_evidence") or []))
except BaseException as exc:
    import traceback
    sortie["erreurs"].append(f"releve : {type(exc).__name__}: {exc}\n{traceback.format_exc()[-900:]}")

with open(RAPPORT, "w", encoding="utf-8") as f:
    json.dump(sortie, f, ensure_ascii=False)
os._exit(0)
