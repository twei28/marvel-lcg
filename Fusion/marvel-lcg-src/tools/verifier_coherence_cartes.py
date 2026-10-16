"""Verifications de coherence sur les DONNEES des cartes et sur leur couverture.

Usage: python3.10 tools/verifier_coherence_cartes.py [rapport.json]

N'a pas besoin du moteur : ne lit que `data/cards.json`, `data/sets_info.json`,
`deck/starter/*.json`, `assets/pics/` et `tools/test_capacites.py`. Se lance
donc en une seconde, contrairement aux autres outils du §8.

Six familles, toutes nees d'un defaut reellement rencontre :

1. COLLISIONS DE NOMS D'IDENTITE entre packs differents. Le pack
   agent_anti_venom a introduit un second « * Flash Thompson », homonyme du
   Venom officiel 20001b : `Puzzle.ChangeForm('Flash Thompson')` est devenu
   ambigu et un cas de test vert est passe au rouge sans que personne ne
   touche a la carte concernee.

2. DESIGNATION PAR NOM dans les cas de test, quand ce nom est porte par
   plusieurs cartes. Le guide l'interdit deja (§8) ; personne ne le verifiait.

3. COUVERTURE des packs custom par les cas de comportement. Sans ce releve,
   « le pack est valide » veut seulement dire « il se charge ».

4. COHERENCE mot-cle imprime / cle `desc`. Un « Toughness. » dans le texte sans
   la cle `Toughness` donne une carte qui ment au joueur, et l'inverse une
   carte qui fait quelque chose que son texte n'annonce pas.

5. IMAGES manquantes pour les packs custom.

6. CAPACITE ANNONCEE SANS AUCUN MODULE (01/09/2026). Une carte dont le texte
   declare une capacite et a laquelle AUCUN fichier ne repond ne fait rien du
   tout : `database.py:220` se contente d'un `ability_cache = []` silencieux,
   et aucun autre outil ne pose cette question — ils supposent tous le module
   deja la.
   ⚠ Deux champs dispensent legitimement de module : `ability_link` (les
   capacites d'une autre carte, database.py:124) et `full_link` (alias
   complet). Ils sont exclus. Leur oubli a produit une fausse alerte de neuf
   cartes le jour meme ou ce crible a ete ecrit.
"""
import sys, os, json, re, collections

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT = sys.argv[1] if len(sys.argv) > 1 else "/tmp/coherence_cartes.json"

cartes = json.load(open(os.path.join(RACINE, "data/cards.json"), encoding="utf-8"))
sets_info = json.load(open(os.path.join(RACINE, "data/sets_info.json"), encoding="utf-8"))
tests = open(os.path.join(RACINE, "tools/test_capacites.py"), encoding="utf-8").read()
images = set()
dossier_pics = os.path.join(RACINE, "assets/pics")
if os.path.isdir(dossier_pics):
    images = {os.path.splitext(n)[0] for n in os.listdir(dossier_pics)}

toutes = []
for pack, liste in cartes.items():
    if pack == "checksum":
        continue
    for c in liste:
        if isinstance(c, dict) and c.get("card_id"):
            toutes.append((pack, c))

rapport = {}

# --- 1. Collisions de noms d'identite entre packs -----------------------------
par_nom = collections.defaultdict(list)
for pack, c in toutes:
    if c.get("type") in ("Hero", "AlterEgo") and c.get("name"):
        par_nom[c["name"]].append((c["card_id"], pack))
collisions = {}
for nom, v in par_nom.items():
    # Deux faces d'une meme identite partagent legitimement leur nom
    # (Ant-Man 12001a/12001c). On ne signale que les identites DISTINCTES.
    identites = {cid[:5] for cid, _ in v}
    if len(identites) > 1:
        collisions[nom] = v
rapport["collisions_noms_identite"] = collisions

# --- 2. Cas de test qui designent une carte par un nom ambigu -----------------
noms_ambigus = collections.defaultdict(list)
for pack, c in toutes:
    if c.get("name"):
        noms_ambigus[c["name"].lstrip("* ").strip()].append(c["card_id"])
designations = set(re.findall(r"Puzzle\.\w+\(\s*'([^']+)'", tests))
par_nom_dans_tests = {}
for d in designations:
    if re.fullmatch(r"[0-9a-z_]+", d):      # deja un card_id
        continue
    homonymes = noms_ambigus.get(d, [])
    if len(homonymes) > 1:
        par_nom_dans_tests[d] = homonymes
rapport["designations_par_nom_ambigu"] = par_nom_dans_tests

# --- 3. Couverture des packs custom ------------------------------------------
packs_custom = set()
for cle, info in sets_info.items():
    if isinstance(info, dict) and re.search(r"custom", cle, re.I):
        packs_custom.add(info.get("name"))
# Deux mesures, parce que l'une flatte et l'autre non :
# - CITEE : l'identifiant apparait quelque part dans un cas. Une carte peut
#   n'y figurer que comme ressource de paiement ou comme decor de mise en
#   place : elle est citee sans etre testee.
# - SUJET : l'identifiant apparait dans le NOM du cas, donc le cas porte
#   vraiment sur elle. C'est la seule mesure honnete, et l'ecart est large
#   (spider_man_rainy passe de 77 % a 50 %).
# Le suffixe de face va de a a z, pas de a a d : Moon Knight est la premiere
# identite a CINQ faces, et mk001e n'etait donc reconnue par aucune de ces
# deux expressions. Son cas existait, le pack affichait quand meme 27/28.
# ⚠ CORRIGE le 01/09/2026 : l'expression ne reconnaissait QUE les identifiants
# officiels a cinq chiffres. Or les packs custom, les seuls que cette mesure
# pretende couvrir, portent un prefixe de DEUX LETTRES suivi de trois chiffres
# (`wd018`, `dd001a`). Aucun n'etait donc reconnu, `total` restait a 0 pour
# chacun, et le tableau de couverture s'affichait VIDE sous son propre titre.
# Une mesure qui ne mesure rien ressemble a une mesure qui ne trouve rien.
ID_CARTE_SEUL = r"(?:\d{5}|[a-z]{2}\d{3})[a-z]?"
ID_CARTE = rf"\b({ID_CARTE_SEUL})\b"
cites = set(re.findall(ID_CARTE, tests))
sujets = set()
for nom_de_cas in re.findall(r'"nom"\s*:\s*(?:\(\s*)?["\']([^"\']+)', tests):
    sujets.update(re.findall(ID_CARTE, nom_de_cas))
# Un pack contient parfois DEUX EXEMPLAIRES de la meme carte, sous deux
# identifiants (Brawn : bw004/bw005, bw006/bw007...). Leurs scripts sont
# identiques a la ligne pres. Ecrire un second cas qui ne differe que par
# l'identifiant n'apprend rien : l'etape 2 du §8 prouve deja que le script se
# construit, et l'etape 5 que ses appels d'API sont bons. Compter ces cartes
# comme non couvertes faisait mentir le taux — Brawn affichait 76 % alors que
# tout son code etait exerce.
#
# On les reconnait mecaniquement : meme code une fois les commentaires et les
# lignes vides retires. Elles sont comptees a part, jamais fondues dans les
# cas dedies, pour qu'on voie toujours la difference.
def _code_normalise(chemin):
    try:
        lignes = open(chemin, encoding="utf-8").read().splitlines()
    except OSError:
        return None
    utiles = [l.rstrip() for l in lignes
              if l.strip() and not l.strip().startswith("#")]
    return "\n".join(utiles) if utiles else None


def _scripts_du_pack(pack):
    """card_id -> code normalise, pour tous les scripts du pack."""
    racine_pack = os.path.join(RACINE, "src", "cards", "pack", pack)
    par_carte = {}
    for dossier, _, fichiers in os.walk(racine_pack):
        for f in fichiers:
            if not f.endswith(".py") or f == "__init__.py":
                continue
            code = _code_normalise(os.path.join(dossier, f))
            if code:
                par_carte[f[:-3]] = code
    return par_carte


couverture = {}
for pack in sorted(p for p in packs_custom if p in cartes):
    total, cite, sujet, manquants = 0, 0, 0, []
    scripts = _scripts_du_pack(pack)
    doublons = []
    for c in cartes[pack]:
        cid = c.get("card_id", "")
        # ⚠ le test etait `cid[0].isdigit()`, qui excluait TOUS les packs
        # custom : leur identifiant commence par deux lettres. Voir la note
        # d'ID_CARTE plus haut.
        if not cid or not re.fullmatch(ID_CARTE_SEUL, cid):
            continue
        # Un `full_link` sans `type` n'est pas une carte : c'est un ALIAS vers
        # une carte de base du jeu (gp015 -> 01088). Aucun script, aucun
        # comportement propre, donc rien a tester : le compter au denominateur
        # rendait la couverture du pack artificiellement basse.
        if "full_link" in c and "type" not in c:
            continue
        total += 1
        if cid in cites:
            cite += 1
        if cid in sujets:
            sujet += 1
        else:
            code = scripts.get(cid)
            jumelle = next((autre for autre, c2 in scripts.items()
                            if autre != cid and c2 == code and autre in sujets), None)
            if code and jumelle:
                doublons.append(f"{cid} {c.get('name', '')}".strip() + f" = {jumelle}")
            else:
                manquants.append(f"{cid} {c.get('name', '')}".strip())
    if total:
        exerce = sujet + len(doublons)
        couverture[pack] = {
            "total": total, "cartes_citees": cite, "cartes_sujet_d_un_cas": sujet,
            "cartes_couvertes_par_un_doublon": len(doublons),
            "taux": f"{100 * exerce // total} %",
            "taux_cas_dedies": f"{100 * sujet // total} %",
            "taux_optimiste": f"{100 * cite // total} %",
            "doublons": doublons,
            "sans_cas_dedie": manquants,
        }
rapport["couverture_packs_custom"] = couverture

# --- 4. Coherence mot-cle imprime / cle desc ---------------------------------
# Mots-cles annonces en tete de ligne, suivis d'un point ou d'un chiffre.
MOTS = {
    "Toughness": "Toughness", "Guard": "Guard", "Quickstrike": "Quickstrike",
    "Retaliate": "Retaliate", "Surge": "Surge", "Incite": "Incite",
    "Patrol": "Patrol", "Stalwart": "Stalwart", "Steady": "Steady",
    "Peril": "Peril", "Villainous": "Villainous", "Vulnerable": "Vulnerable",
    "Hinder": "Hinder",
}
incoherences = []
for pack, c in toutes:
    texte = c.get("text") or ""
    desc = c.get("desc") or {}
    for mot, cle in MOTS.items():
        imprime = bool(re.search(r"(?:^|\n)\s*" + mot + r"(?:\s+\d|\.)", texte))
        declare = cle in desc
        if imprime and not declare:
            incoherences.append(
                f"{c['card_id']} ({pack}) : « {mot} » imprime, cle desc `{cle}` absente")
rapport["mot_cle_imprime_sans_cle_desc"] = incoherences

# --- 4 bis. Cartes joueur sans classe d'aspect -------------------------------
# Sans `desc.Class`, `card_classes` reste vide et le moteur PLANTE des que la
# carte est evaluee (`assert self.card_classes != []`). Six cartes etaient dans
# ce cas le 4/8/2026, dont deux d'un pack officiel : la creation de partie de
# Hercule et de Moon Knight etait impossible.
TYPES_JOUEUR = {"Ally", "Event", "Support", "Upgrade", "Resource", "Path"}
sans_classe = []
for pack, c in toutes:
    if c.get("type") in TYPES_JOUEUR and not (c.get("desc") or {}).get("Class"):
        sans_classe.append(f"{c['card_id']} ({pack}) : {c.get('name', '')} — type "
                           f"{c['type']} sans `desc.Class`")
rapport["carte_joueur_sans_classe"] = sans_classe

# --- 4 ter. Obligations sans destinataire ------------------------------------
# Une obligation doit dire A QUI elle est donnee (`desc.GiveTo`), sinon
# `assert self.printed_give_to != None` fait planter le setup.
# On ne signale que les obligations qui figurent dans un DECK DE DEPART : ce
# sont les seules dont le moteur valide les valeurs imprimees au setup. Les
# obligations des sets de rencontre (Zola's Algorithm et consorts) n'ont
# legitimement pas de destinataire.
dans_decks = set()
dossier_decks = os.path.join(RACINE, "deck", "starter")
if os.path.isdir(dossier_decks):
    for nom in os.listdir(dossier_decks):
        if nom.endswith(".json"):
            dans_decks.update(re.findall(r'"(\d{5}[a-z]?)"',
                                         open(os.path.join(dossier_decks, nom),
                                              encoding="utf-8").read()))
sans_destinataire = [f"{c['card_id']} ({pack}) : {c.get('name', '')}"
                     for pack, c in toutes
                     if c.get("type") == "Obligation"
                     and c.get("card_id") in dans_decks
                     and not (c.get("desc") or {}).get("GiveTo")]
rapport["obligation_sans_giveto"] = sans_destinataire

# --- 5. Images manquantes pour les packs custom ------------------------------
sans_image = []
for pack in sorted(p for p in packs_custom if p in cartes):
    for c in cartes[pack]:
        cid = c.get("card_id", "")
        # meme correction que pour la couverture : les packs custom
        # etaient tous exclus par le test sur le premier caractere.
        if cid and re.fullmatch(ID_CARTE_SEUL, cid) and cid not in images:
            sans_image.append(f"{cid} ({pack}) {c.get('name', '')}".strip())
rapport["images_manquantes"] = sans_image

# --- 6. Cartes a capacite ANNONCEE mais SANS AUCUN MODULE --------------------
#
# AJOUTE le 01/09/2026, apres neuf cartes inertes trouvees d'un coup dans
# web_of_deceit (wd018, wd019, wd020, wd021, wd023, wd024, wd078, wd084,
# wd085). Elles etaient dans les decks de rencontre de trois scenarios et ne
# faisaient RIEN.
#
# ⚠ POURQUOI AUCUN OUTIL NE LE VOYAIT. `database.py:220` est muet : quand
# aucun module ne repond, `ability_cache[card_id] = []` et la partie continue.
# Et chaque outil existant pose une question qui suppose le module deja la :
#   * `verifier_noms_modules`   lit le code DES modules presents ;
#   * `verifier_appels_modules` verifie les appels DES modules presents ;
#   * `verifier_cartes_en_jeu`  ne regarde que les attributs du `desc` — il
#     annoncait « les 176 cartes portent ce que leur texte annonce », ce qui
#     etait vrai et trompeur a la fois ;
#   * `sonde_capacites`         compte les capacites trouvees.
# Aucune ne demandait « cette carte devrait-elle avoir un module ? ».
#
# Le crible : on retire les phrases entierement couvertes par une base
# automatique du `desc`, les rappels entre parentheses et l'ambiance en
# italique. Ce qui reste et qui declare une capacite est un manque.
DECLARE = re.compile(
    r"\b(Response|Interrupt|Action|When Revealed|When Defeated|Forced|Special|"
    r"Resource:|Boost:)\b", re.I)
# Un effet CONTINU ne porte aucun de ces mots : wd085 « Reduce the damage… »
# n'a ete attrape que par cette seconde passe.
CONTINU = re.compile(
    r"^(Reduce|Increase|Each|While|Whenever|Players|Cards|The villain|"
    r"Attached|Attacks|Treat|Ignore|Limit)\b", re.I)
# Un mot-cle seul, ou suivi de son rappel entre parentheses, vit dans le desc.
KEYWORD = (r"Surge|Vulnerable|Guard|Patrol|Toughness|Steady|Stalwart|Quickstrike|"
           r"Peril|Permanent|Restricted|Amplify|Overkill|Piercing|Ranged|Elite|"
           r"Retaliate \d+|Hinder \d+\S*|Incite \d+\S*|Victory \d+|Setup|"
           r"Uses \([^)]*\)|Requirement \([^)]*\)|Villainous")
KEYWORD_SEUL = re.compile(rf"^\s*(?:(?:{KEYWORD})[.\s]*)+$", re.I)

modules_par_pack = {}
for pack in sorted(packs_custom):
    racine_pack = os.path.join(RACINE, "src", "cards", "pack", pack)
    trouves = set()
    for dossier, _, fichiers in os.walk(racine_pack):
        for f in fichiers:
            if f.endswith(".py") and f != "__init__.py":
                trouves.add(f[:-3])
    modules_par_pack[pack] = trouves

sans_module = []
for pack, c in toutes:
    if pack not in packs_custom:
        continue
    cid = c.get("card_id", "")
    if not cid or not c.get("type"):
        continue
    mods = modules_par_pack.get(pack, set())
    # Une face porte parfois le module de son identite (wd077a / wd077).
    if cid in mods or cid.rstrip("abcde") in mods:
        continue
    # ⚠ CORRECTIF DU MEME JOUR, apres une FAUSSE ALERTE de neuf cartes.
    # `ability_link` fait charger les capacites d'une AUTRE carte
    # (database.py:124) : la carte n'a pas de module a elle, et c'est voulu.
    # Web of Deceit reimprime neuf modulaires officiels sous des identifiants
    # `wd`, chacun renvoyant a son jumeau — wd085 -> 50159, wd020 -> 02041...
    # Sans cette exclusion, le crible les declarait toutes inertes. Elles
    # fonctionnaient parfaitement.
    # `full_link` va plus loin encore : la carte entiere est un alias.
    if c.get("ability_link") or c.get("full_link"):
        continue
    texte = c.get("text") or ""
    texte = re.sub(r"<i>.*?</i>", " ", texte, flags=re.S)   # ambiance
    texte = re.sub(r"<[^>]+>", "", texte)
    texte = re.sub(r"\([^)]*\)", "", texte)                 # rappels de regles
    restes = []
    for ligne in texte.split("\n"):
        ligne = ligne.strip()
        if not ligne or KEYWORD_SEUL.match(ligne):
            continue
        if DECLARE.search(ligne) or CONTINU.match(ligne):
            restes.append(ligne)
    if restes:
        sans_module.append({
            "card_id": cid, "pack": pack, "type": c.get("type"),
            "nom": c.get("name", ""), "texte": restes,
        })
rapport["capacite_annoncee_sans_module"] = sans_module

json.dump(rapport, open(REPORT, "w"), indent=1, ensure_ascii=False)

lignes = []
lignes.append(f"collisions de noms d'identite entre packs : {len(collisions)}")
for nom, v in sorted(collisions.items()):
    lignes.append(f"    {nom} -> {v}")
lignes.append(f"designations par nom ambigu dans les tests : {len(par_nom_dans_tests)}")
for nom, v in sorted(par_nom_dans_tests.items()):
    lignes.append(f"    {nom!r} -> {v}")
lignes.append(f"mots-cles imprimes sans cle desc : {len(incoherences)}")
for i in incoherences[:20]:
    lignes.append(f"    {i}")
lignes.append(f"cartes joueur sans classe d'aspect : {len(sans_classe)}")
for i in sans_classe:
    lignes.append(f"    {i}")
lignes.append(f"obligations sans destinataire : {len(sans_destinataire)}")
for i in sans_destinataire:
    lignes.append(f"    {i}")
lignes.append(f"images manquantes (packs custom) : {len(sans_image)}")
for i in sans_image[:20]:
    lignes.append(f"    {i}")
lignes.append(f"capacite annoncee SANS AUCUN module : {len(sans_module)}")
for i in sans_module:
    lignes.append(f"    {i['card_id']} ({i['pack']}) {i['type']} {i['nom']}")
    for t in i["texte"]:
        lignes.append(f"        {t[:96]}")
lignes.append("couverture des packs custom (cas DEDIE + doublon de code, puis simplement citees) :")
for pack, info in sorted(couverture.items(), key=lambda kv: int(kv[1]["taux"].rstrip(" %"))):
    # Les doublons sont affiches A PART, jamais fondus dans les cas dedies :
    # « 20+6/26 » se lit d'un coup d'oeil, « 26/26 » masquerait le fait que six
    # cartes n'ont pas de cas a elles.
    d = info["cartes_couvertes_par_un_doublon"]
    compte = (f"{info['cartes_sujet_d_un_cas']}+{d}/{info['total']}" if d
              else f"{info['cartes_sujet_d_un_cas']}/{info['total']}")
    lignes.append(f"    {pack:24s} {compte:>9s} "
                  f"{info['taux']:>5s}   (citees : {info['taux_optimiste']})")
print("\n".join(lignes))

# Les collisions de noms ne sont PAS une faute : deux personnages distincts
# peuvent legitimement partager un nom de heros (Black Panther T'Challa et
# Shuri). C'est un releve « a connaitre », qui explique pourquoi on ne designe
# jamais une carte par son nom. Les trois autres familles, elles, sont des
# defauts a corriger.
probleme = bool(par_nom_dans_tests or incoherences or sans_image or sans_module)
sys.exit(1 if probleme else 0)
