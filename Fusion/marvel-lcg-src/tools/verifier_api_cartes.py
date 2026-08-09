"""Verifie que les scripts de cartes n'appellent que des API qui existent.

Usage: python3.10 tools/verifier_api_cartes.py <game_dir> <port> [rapport.json]

POURQUOI CET OUTIL. `test_cards.py` ne construit que les capacites : il
n'execute jamais le corps des handlers. `test_capacites.py` ne joue que ce que
l'API Puzzle sait declencher, et jamais ce qui se cache derriere un choix
optionnel (le pilote decline systematiquement). Entre les deux, un appel a une
methode qui n'existe pas passe inapercu jusqu'a la partie reelle.

Cinq defauts trouves ainsi le 4/8/2026, invisibles pour les deux autres
outils, dans quatre packs differents :
- `identity.ChangeForm(effect)` dans les obligations de jessica_jones et
  agent_anti_venom : la bonne methode est `ChangeToForm(Hero|AlterEgo, effect)` ;
- `Worlds.RevealEncounterCard` dans le Homme-Pourpre 73019 : la bonne est
  `RevealEncounterDeckTopCard` ;
- `Faces.DiscardStatus` dans True Grit 67007 (the_thing) : ce sont des methodes
  de la FACE, `hero.DiscardStunned(...)` / `DiscardConfused(...)` ;
- `Worlds.RemoveAccelerationToken` dans De-escalation 60024 (fne) : passer par
  `GetAccelerationTokenFaces` puis `Faces.RemoveTokensOn` ;
- `Worlds.FindAttachedUnit` dans Jaw Lock 78004 (lockjaw), garde par un
  `hasattr` : ne plantait pas, mais ne faisait JAMAIS rien. `GetBindFace()`.

Ce dernier cas est le plus instructif : un appel inexistant protege par un
`hasattr` ne leve aucune erreur, il rend juste la carte inerte. Aucun test ne
peut voir la difference entre « la capacite n'a pas encore ete declenchee » et
« la capacite ne fera jamais rien ».

CE QU'IL COUVRE. Les appels sur les espaces de noms statiques
(`Worlds.`, `Faces.`, `Search.`, `Filter.`, `AbilityFactory.`, `CostFunc.`,
`Message.`), plus une liste noire d'appels d'instance connus pour etre faux.
Il ne fait PAS d'inference de types : `x.Truc()` sur une variable locale n'est
pas verifie, sauf s'il figure dans APPELS_INTERDITS.
"""
import sys, os, json, ast, re, importlib

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
REPORT = sys.argv[3] if len(sys.argv) > 3 else "/tmp/verifier_api_cartes.json"

# Appels d'instance connus pour etre faux, avec leur remplacant.
APPELS_INTERDITS = {
    ".ChangeForm(": "ChangeToForm(Hero|AlterEgo, effect) — voir 72012",
    ".GetTarget(": "message.attacked (AfterUnitAttackUnit) ou message.attacked_targets",
    ".BeInstead(": "SetBeInstead(effect)",
    # Trouve le 4/8/2026 : quatre cartes plantaient sur cet appel, dans trois
    # packs. Aucune face du moteur n'expose IsInField.
    ".IsInField(": "IsInPlay()",
    ".GetAttachedTo(": "GetBindFace()",
}

RACINES = ("Worlds", "Faces", "Search", "Filter", "AbilityFactory", "CostFunc",
           "Message", "FacesCounter", "Condition", "Select")

os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)
cfg_path = os.path.join(GAME_DIR, "launch.json")
cfg = json.load(open(cfg_path))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open(cfg_path, "w"), indent=2)

vrai_stdout = sys.stdout
sys.stdout = open("/tmp/verifier_api_cartes.log", "w", buffering=1)
sys.stderr = sys.stdout

from engine import Engine
Engine.Initialize()

from game.operate.worlds import Worlds
from game.operate.faces import Faces
from game.operate.search import Search
from game.operate.filter import Filter
from game.ability.factory import AbilityFactory
from game.ability.cost_func import CostFunc
from game.message import Message
from game.operate.faces_counter import FacesCounter
from game.ability.condition.condition import Condition
from game.selector.factory import Select

ESPACES = {
    "Worlds": Worlds, "Faces": Faces, "Search": Search, "Filter": Filter,
    "AbilityFactory": AbilityFactory, "CostFunc": CostFunc, "Message": Message,
    "FacesCounter": FacesCounter, "Condition": Condition, "Select": Select,
}

# Tous les attributs connus des classes de messages et de faces, pour juger les
# gardes `hasattr` posees sur des variables locales (`message`, `this`, `face`).
ATTRIBUTS_CONNUS = set()
def _collecter(module_ou_classe):
    for nom in dir(module_ou_classe):
        valeur = getattr(module_ou_classe, nom, None)
        if isinstance(valeur, type):
            ATTRIBUTS_CONNUS.update(dir(valeur))
        ATTRIBUTS_CONNUS.add(nom)
_collecter(Message)
import game.card.face as _face_mod
_collecter(_face_mod)
import game.card.face.card_type as _type_mod
_collecter(_type_mod)

# Signatures des constructeurs et fabriques dont un argument mal nomme ne se
# voit qu'a l'execution. On collecte les noms d'arguments acceptes.
import inspect
SIGNATURES = {}
def _signer(nom, cible):
    try:
        SIGNATURES[nom] = set(inspect.signature(cible).parameters)
    except (TypeError, ValueError):
        pass
from game.card.card_finder import CardFinder
_signer("CardFinder", CardFinder.__init__)

# Methodes d'INSTANCE verifiables. Liste VOLONTAIREMENT COURTE : on n'y met
# qu'une methode dont la signature est exhaustive, c'est-a-dire sans `**kwargs`.
# Un balayage automatique de tout le moteur a produit 65 faux positifs, parce
# que la plupart des methodes relaient leurs arguments a CardFinder sans les
# declarer. Un controle bruyant finit ignore : mieux vaut trois noms surs.
#
# `GainUntilRoundEnd` n'acceptait pas `retaliate` alors que `GainUntilPhaseEnd`
# si : Guard Protocol 62003 (pack albert) plantait a chaque utilisation.
METHODES_INSTANCE = {}
from game.card.face.model.face_action import ModelAction
for _nom in ("GainUntilRoundEnd", "GainUntilPhaseEnd", "TemporaryGain"):
    _m = getattr(ModelAction, _nom, None)
    if _m is not None:
        try:
            METHODES_INSTANCE[_nom] = set(inspect.signature(_m).parameters)
        except (TypeError, ValueError):
            pass

racine_cartes = os.path.join(GAME_DIR, "cards", "pack")

# Noms visibles depuis un fichier de carte : tout ce que son paquet expose via
# le `from . import *` de son `__init__.py`, plus les builtins.
import builtins
_CACHE_PAQUETS = {}
def _noms_du_paquet(chemin_fichier):
    dossier = os.path.dirname(chemin_fichier)
    if dossier in _CACHE_PAQUETS:
        return _CACHE_PAQUETS[dossier]
    # Le module importable est `cards.pack.<pack>.<set>` : on part donc de
    # GAME_DIR, deux crans au-dessus de `cards/pack`. Avec un cran de moins,
    # l'import echouait en silence et TOUT le controle etait saute sans que
    # rien ne le signale (verifie en cassant une carte volontairement).
    relatif = os.path.relpath(dossier, os.path.dirname(os.path.dirname(racine_cartes)))
    module = relatif.replace(os.sep, ".")
    try:
        paquet = importlib.import_module(module)
        noms = set(dir(paquet)) | set(dir(builtins))
    except Exception:
        noms = None
    _CACHE_PAQUETS[dossier] = noms
    return noms
problemes = {}
fichiers = 0

for dossier, _, noms in os.walk(racine_cartes):
    if "__pycache__" in dossier:
        continue
    for nom in noms:
        if not nom.endswith(".py"):
            continue
        chemin = os.path.join(dossier, nom)
        relatif = os.path.relpath(chemin, racine_cartes)
        try:
            source = open(chemin, encoding="utf-8").read()
        except Exception:
            continue
        fichiers += 1
        trouves = []

        # 1. Espaces de noms statiques
        try:
            arbre = ast.parse(source)
        except SyntaxError:
            problemes.setdefault(relatif, []).append("syntaxe illisible")
            continue
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Attribute) and isinstance(noeud.value, ast.Name):
                racine = noeud.value.id
                if racine in ESPACES and not hasattr(ESPACES[racine], noeud.attr):
                    trouves.append(f"{racine}.{noeud.attr} n'existe pas")

        # 2. Liste noire d'appels d'instance
        for motif, remplacant in APPELS_INTERDITS.items():
            if motif in source:
                # `SetBeInstead` contient `.BeInstead(` : on l'exclut.
                if motif == ".BeInstead(" and re.search(r"Set" + re.escape("BeInstead("), source):
                    reste = re.sub(r"SetBeInstead\(", "", source)
                    if ".BeInstead(" not in reste:
                        continue
                trouves.append(f"{motif.strip('.')} interdit -> {remplacant}")

        # 3. Gardes `hasattr` : elles ETOUFFENT l'erreur au lieu de la lever.
        #    C'est ce qui rendait Jaw Lock 78004 definitivement inerte sans
        #    qu'aucun test ne puisse s'en apercevoir.
        for m in re.finditer(r"hasattr\(\s*(\w+)\s*,\s*[\"'](\w+)[\"']\s*\)", source):
            porteur, attribut = m.group(1), m.group(2)
            if porteur in ESPACES:
                existe = hasattr(ESPACES[porteur], attribut)
            else:
                # `message`, `this`, `face`... : on cherche l'attribut sur
                # l'ensemble des classes de messages et de faces. S'il existe
                # quelque part, la garde n'est que du bruit ; s'il n'existe
                # nulle part, la branche est morte (cas Jaw Lock 78004).
                existe = attribut in ATTRIBUTS_CONNUS
            if not existe:
                trouves.append(
                    f"garde hasattr({porteur}, '{attribut}') : l'API n'existe nulle "
                    f"part, la branche est MORTE")

        # 4. Arguments nommes passes aux fabriques et selecteurs les plus
        #    utilises. Un nom d'argument faux leve un TypeError A L'EXECUTION
        #    seulement : `CardFinder(has_res="B")` dans Ben's Cure 65013 faisait
        #    planter l'obligation a chaque revelation depuis sa livraison, sans
        #    qu'aucun autre outil ne puisse le voir.
        for noeud in ast.walk(arbre):
            if not isinstance(noeud, ast.Call):
                continue
            # Il faut le RECEPTEUR, pas seulement le nom : plusieurs fabriques
            # partagent leur nom avec un constructeur de message
            # (`Message.WhenScenarioEvent` accepte `world=`, la fabrique non).
            nom_appele = None
            if isinstance(noeud.func, ast.Name):
                nom_appele = noeud.func.id          # CardFinder(...)
            elif isinstance(noeud.func, ast.Attribute) and \
                    isinstance(noeud.func.value, ast.Name) and \
                    noeud.func.value.id == "AbilityFactory":
                nom_appele = noeud.func.attr        # AbilityFactory.Xxx(...)
            signature = SIGNATURES.get(nom_appele)
            if signature is None and isinstance(noeud.func, ast.Attribute):
                # Methode d'instance a nom unique : `hero.GainUntilRoundEnd(...)`
                signature = METHODES_INSTANCE.get(noeud.func.attr)
                if signature is not None:
                    nom_appele = noeud.func.attr
            if signature is None:
                continue
            for mot_cle in noeud.keywords:
                if mot_cle.arg and mot_cle.arg not in signature:
                    trouves.append(
                        f"{nom_appele}(..., {mot_cle.arg}=...) : argument inconnu")

        # 5. Ordre SetTarget / SetLabel. `ability.py` asserte que SetLabel
        #    precede SetTarget ; dans l'autre ordre l'AssertionError part a
        #    l'execution et la carte se defausse sans rien faire (It's
        #    Clobberin' Time! 67010, invisible jusqu'au 4/8/2026).
        for m in re.finditer(r"\.SetTarget\d?\([^\n]*\)\s*\.SetLabel\(", source):
            trouves.append(
                "`.SetTarget(...).SetLabel(...)` : ordre interdit, SetLabel doit "
                "venir AVANT SetTarget (assertion dans ability.py)")

        # 6. Fonctions appelees mais definies NULLE PART : NameError garanti a
        #    l'execution. `ChangerDeForme` et `YouMayChangeForm` etaient appeles
        #    par trois cartes du pack lockjaw sans exister : elles se
        #    defaussaient sans rien faire.
        disponibles = _noms_du_paquet(chemin)
        if disponibles is not None:
            # Un fichier peut ajouter d'AUTRES `from X import *` apres celui de
            # son paquet (`from cards.pack.trors.campaign import *` chez Zola).
            # Sans les suivre, on signalait 9 faux positifs sur `CampaignSetup`.
            disponibles = set(disponibles)
            for noeud in ast.walk(arbre):
                if isinstance(noeud, ast.ImportFrom) and noeud.module and \
                        any(a.name == "*" for a in noeud.names):
                    try:
                        autre = importlib.import_module(noeud.module)
                        disponibles |= set(dir(autre))
                    except Exception:
                        pass
            locaux = set()
            for noeud in ast.walk(arbre):
                if isinstance(noeud, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    locaux.add(noeud.name)
                    for arg in noeud.args.args + noeud.args.kwonlyargs:
                        locaux.add(arg.arg)
                elif isinstance(noeud, ast.Name) and isinstance(noeud.ctx, ast.Store):
                    locaux.add(noeud.id)
                elif isinstance(noeud, ast.alias):
                    locaux.add((noeud.asname or noeud.name).split(".")[0])
                elif isinstance(noeud, ast.ExceptHandler) and noeud.name:
                    locaux.add(noeud.name)
            for noeud in ast.walk(arbre):
                if isinstance(noeud, ast.Call) and isinstance(noeud.func, ast.Name):
                    nom_fn = noeud.func.id
                    if nom_fn not in locaux and nom_fn not in disponibles:
                        trouves.append(
                            f"`{nom_fn}(...)` appele mais defini nulle part : "
                            f"NameError a l'execution")

        # 7. Handlers definis mais jamais reference : capacite morte.
        for noeud in ast.walk(arbre):
            if not (isinstance(noeud, ast.FunctionDef) and noeud.name == "GetAbilities"):
                continue
            for interne in noeud.body:
                if not isinstance(interne, ast.FunctionDef):
                    continue
                # Le nom doit reapparaitre ailleurs que sur sa ligne de `def`.
                usages = len(re.findall(r"\b" + re.escape(interne.name) + r"\b", source))
                if usages <= 1:
                    trouves.append(
                        f"handler `{interne.name}` defini mais jamais passe a une "
                        f"fabrique : code mort")

        if trouves:
            problemes[relatif] = sorted(set(trouves))

resultat = {"fichiers": fichiers, "fichiers_en_faute": len(problemes), "problemes": problemes}
json.dump(resultat, open(REPORT, "w"), indent=1, ensure_ascii=False)

lignes = [f"{fichiers} fichiers analyses, {len(problemes)} en faute"]
for f, ps in sorted(problemes.items()):
    lignes.append(f"  {f}")
    for p in ps:
        lignes.append(f"      {p}")
os.write(vrai_stdout.fileno(), ("\n".join(lignes) + "\n").encode())
os._exit(0 if not problemes else 1)
