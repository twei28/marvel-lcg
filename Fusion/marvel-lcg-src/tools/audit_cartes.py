"""Audit de COHERENCE des cartes : texte imprime <-> capacites construites.

Ne corrige rien : produit un rapport JSON de discordances a relire par un
humain. Trois familles de verifications :

  1. types d'arguments des appels AbilityFactory (AST) : une chaine passee la
     ou la signature attend une liste (classe du bug Rescue powers="DEF") ;
  2. marqueurs du texte imprime (<b>Response</b>, Interrupt, Action, When
     Revealed, When Defeated, Resource, Setup, Boost) sans capacite du type
     correspondant, et inversement cout d'inclinaison annonce sans
     CostFunc.Exhaust ;
  3. cartes au texte « a capacite » sans aucun script (texte seul), liens
     full_link/ability_link resolus avant de signaler.

Usage: python3.10 audit_cartes.py <game_dir> <port> [rapport.json]
(meme contrat que test_cards.py : ecrit server_addresses dans launch.json du
dossier vise -- utiliser .game-test, jamais le .game du serveur en cours.)
"""
import sys, os, json, re, ast, importlib, inspect, pkgutil, traceback

GAME_DIR = os.path.expanduser(sys.argv[1])
PORT = int(sys.argv[2])
REPORT = sys.argv[3] if len(sys.argv) > 3 else "/tmp/audit_cartes.json"

os.chdir(GAME_DIR); sys.path.insert(0, GAME_DIR)
cfg_path = os.path.join(GAME_DIR, "launch.json")
cfg = json.load(open(cfg_path))
cfg["server_addresses"] = [f"127.0.0.1:{PORT}"]
cfg["check_for_new_version_on_startup"] = False
json.dump(cfg, open(cfg_path, "w"), indent=2)

sys.stdout = open("/tmp/audit_stdout.log", "w", buffering=1)
sys.stderr = sys.stdout

from engine import Engine
ok_init = Engine.Initialize()
print("INIT:", ok_init, flush=True)

from game.ability.factory import AbilityFactory

# ---------------------------------------------------------------- donnees --
def charger_cartes():
    cartes = {}
    origine = {}
    for fichier in ("data/cards.json", "data/cards_custom.json"):
        if not os.path.exists(fichier):
            continue
        d = json.load(open(fichier))
        for groupe, liste in d.items():
            if not isinstance(liste, list):
                continue
            for c in liste:
                if isinstance(c, dict) and isinstance(c.get("card_id"), str):
                    cartes[c["card_id"]] = c
                    origine[c["card_id"]] = (os.path.basename(fichier), groupe)
    return cartes, origine

CARTES, ORIGINE = charger_cartes()

# ------------------------------------------------- signatures des fabriques --
# Annotations BRUTES (chaines) des parametres de chaque fabrique : on y
# detecte 'List[' et les valeurs admises par un eventuel Literal[...].
SIGNATURES = {}
for nom in dir(AbilityFactory):
    fn = getattr(AbilityFactory, nom)
    if not callable(fn) or nom.startswith("_"):
        continue
    try:
        params = inspect.signature(fn).parameters
    except (ValueError, TypeError):
        continue
    annots = {}
    for pnom, p in params.items():
        if p.annotation is inspect.Parameter.empty:
            continue
        annots[pnom] = str(p.annotation)
    SIGNATURES[nom] = annots

def litteraux_admis(annotation: str):
    valeurs = set()
    for bloc in re.findall(r"Literal\[([^\]]*)\]", annotation):
        for v in re.findall(r"['\"]([^'\"]+)['\"]", bloc):
            valeurs.add(v)
    return valeurs

def accepte_aussi_un_scalaire(annotation: str) -> bool:
    """Vrai pour les annotations du genre `X|List[X]|None` : passer un X nu est
    alors parfaitement legal (idiome tres courant du moteur pour les traits et
    les labels). Sans ce filtre, l'audit criait au loup 15 fois."""
    for interieur in re.findall(r"List\[([^\]]*)\]", annotation):
        interieur = interieur.strip()
        if not interieur:
            continue
        reste = annotation.replace("List[" + interieur + "]", "")
        # Comparer les NOMS NUS : le cote scalaire s'ecrit souvent autrement
        # (ForwardRef('CardFace.TRAITS') dans la liste, mais
        # ForwardRef('CardFace.TRAITS|None') a cote).
        trouve = re.search(r"ForwardRef\('([^']+)'\)", interieur)
        noyau = (trouve.group(1) if trouve else interieur).split("|")[0].strip("'\" ")
        if noyau and noyau in reste:
            return True
    return False

def verifier_ast(chemin_module: str):
    """Chaine litterale passee a un parametre annote List[...] -> discordance."""
    problemes = []
    try:
        arbre = ast.parse(open(chemin_module).read())
    except Exception:
        return problemes
    for noeud in ast.walk(arbre):
        if not isinstance(noeud, ast.Call):
            continue
        f = noeud.func
        if not (isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name)
                and f.value.id == "AbilityFactory"):
            continue
        annots = SIGNATURES.get(f.attr)
        if not annots:
            continue
        for kw in noeud.keywords:
            if kw.arg is None or not isinstance(kw.value, ast.Constant):
                continue
            valeur = kw.value.value
            if not isinstance(valeur, str):
                continue
            annotation = annots.get(kw.arg, "")
            if "List[" in annotation and not accepte_aussi_un_scalaire(annotation) \
                    and valeur not in litteraux_admis(annotation):
                problemes.append(
                    f"{f.attr}({kw.arg}='{valeur}') : la signature attend une "
                    f"liste ({annotation}) ; une chaine est iteree lettre a "
                    f"lettre et ne matche jamais")
    return problemes

# ------------------------------------------------------- marqueurs du texte --
MARQUEURS = [
    # (regex dans le texte, nom, predicat sur la liste d'abilities)
    (r"<b>\s*Forced\s+Response\s*</b>|<b>\s*Response\s*</b>", "Response",
     lambda abs_: any(a.flags.is_response for a in abs_)),
    (r"<b>\s*Forced\s+Interrupt\s*</b>|<b>\s*Interrupt\s*</b>", "Interrupt",
     lambda abs_: any(a.flags.is_interrupt for a in abs_)),
    (r"<b>\s*(?:Hero\s+|Alter-Ego\s+)?Action\s*</b>", "Action",
     lambda abs_: any(a.flags.is_action for a in abs_)),
    (r"<b>\s*When\s+Revealed\s*</b>", "When Revealed",
     lambda abs_: any("WhenRevealed" in str(a.type) for a in abs_)),
    (r"<b>\s*When\s+Defeated\s*</b>", "When Defeated",
     lambda abs_: any(a.flags.is_when_defeated for a in abs_)),
    (r"<b>\s*Resource\s*</b>", "Resource",
     lambda abs_: any(str(a.type) == "AbilityType.Resource" or "Resource" in str(a.type) for a in abs_)),
    (r"<b>\s*Setup\s*</b>", "Setup",
     lambda abs_: any("Setup" in str(a.type) for a in abs_)),
    (r"<b>\s*Boost\s*</b>", "Boost",
     lambda abs_: any("Boost" in str(a.type) for a in abs_)),
]
REGEX_MARQUEUR_QUELCONQUE = re.compile(
    "|".join(m[0] for m in MARQUEURS), re.IGNORECASE)

def marqueurs_sans_capacite(texte: str, abilities):
    manquants = []
    for regex, nom, predicat in MARQUEURS:
        if re.search(regex, texte, re.IGNORECASE) and not predicat(abilities):
            manquants.append(nom)
    return manquants

def cout_exhaust_manquant(texte: str, nom_carte: str, abilities):
    """'Exhaust <cette carte>' avant la fleche -> un CostFunc.Exhaust attendu."""
    nom_nu = re.sub(r"^\*\s*", "", nom_carte or "")
    for segment in re.findall(r"</b>[^<]*?:?([^<]*?)(?:→|-&gt;|->)", texte):
        if "exhaust" not in segment.lower():
            continue
        if nom_nu and nom_nu.lower() not in segment.lower() \
                and "this card" not in segment.lower():
            continue
        a_exhaust = any(
            type(cf).__name__.startswith("Exhaust")
            for a in abilities for cf in getattr(a, "cost_funcs", []))
        if not a_exhaust:
            return True
    return False

# ------------------------------------------------------------------- audit --
import cards.pack as P

modules_par_carte = {}
erreurs_modules = {}
for mi in pkgutil.walk_packages(P.__path__, P.__name__ + "."):
    basename = mi.name.rsplit(".", 1)[-1]
    try:
        m = importlib.import_module(mi.name)
    except Exception:
        erreurs_modules[mi.name] = traceback.format_exc(limit=1).splitlines()[-1]
        continue
    if hasattr(m, "GetAbilities"):
        modules_par_carte.setdefault(basename, []).append(m)

rapport = {
    "types_arguments": {},     # card_id -> [problemes]  (quasi certains)
    "marqueur_sans_capacite": {},  # card_id -> {manquants, texte}
    "exhaust_sans_cout": {},   # card_id -> texte
    "texte_seul": {},          # card_id -> texte (marqueur mais aucun script)
    "construction_impossible": {},  # card_id/module -> erreur
    "stats": {},
}

def resoudre_lien(carte):
    vus = set()
    while True:
        lien = carte.get("full_link") or carte.get("ability_link")
        if not lien or lien in vus or lien not in CARTES:
            return carte
        vus.add(lien)
        carte = CARTES[lien]

nb_scriptees = 0
for card_id, carte in CARTES.items():
    texte = str(carte.get("text") or "")
    nom = str(carte.get("name") or "")
    cible = resoudre_lien(carte)
    modules = modules_par_carte.get(str(cible.get("card_id")), [])

    if modules:
        nb_scriptees += 1
        abilities = []
        for m in modules:
            try:
                abilities += list(m.GetAbilities())
            except Exception:
                rapport["construction_impossible"][card_id] = \
                    traceback.format_exc(limit=1).splitlines()[-1]
            problemes = verifier_ast(m.__file__)
            if problemes:
                rapport["types_arguments"][card_id] = problemes
        if abilities and texte:
            manquants = marqueurs_sans_capacite(texte, abilities)
            if manquants:
                rapport["marqueur_sans_capacite"][card_id] = {
                    "nom": nom, "manquants": manquants, "texte": texte[:220]}
            if cout_exhaust_manquant(texte, nom, abilities):
                rapport["exhaust_sans_cout"][card_id] = texte[:220]
    else:
        if texte and REGEX_MARQUEUR_QUELCONQUE.search(texte):
            rapport["texte_seul"][card_id] = {"nom": nom, "texte": texte[:220]}

for cle in ("types_arguments", "marqueur_sans_capacite", "exhaust_sans_cout",
            "texte_seul", "construction_impossible"):
    rapport["stats"][cle] = len(rapport[cle])
rapport["stats"]["cartes"] = len(CARTES)
rapport["stats"]["cartes_scriptees"] = nb_scriptees
rapport["stats"]["modules_en_erreur"] = len(erreurs_modules)
rapport["erreurs_modules"] = erreurs_modules
rapport["origine"] = {cid: ORIGINE.get(cid) for cle in (
    "types_arguments", "marqueur_sans_capacite", "exhaust_sans_cout",
    "texte_seul", "construction_impossible") for cid in rapport[cle]}

json.dump(rapport, open(REPORT, "w"), indent=1, ensure_ascii=False)
print("STATS:", json.dumps(rapport["stats"]), flush=True)
os._exit(0)
