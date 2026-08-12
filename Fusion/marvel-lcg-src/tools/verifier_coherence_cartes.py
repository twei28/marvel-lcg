"""Verifications de coherence sur les DONNEES des cartes et sur leur couverture.

Usage: python3.10 tools/verifier_coherence_cartes.py [rapport.json]

N'a pas besoin du moteur : ne lit que `data/cards.json`, `data/sets_info.json`,
`deck/starter/*.json`, `assets/pics/` et `tools/test_capacites.py`. Se lance
donc en une seconde, contrairement aux autres outils du §8.

Quatre familles, toutes nees d'un defaut reellement rencontre le 4/8/2026 :

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
cites = set(re.findall(r"\b(\d{5}[a-z]?)\b", tests))
sujets = set()
for nom_de_cas in re.findall(r'"nom"\s*:\s*(?:\(\s*)?["\']([^"\']+)', tests):
    sujets.update(re.findall(r"\b(\d{5}[a-z]?)\b", nom_de_cas))
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
        if not cid or not cid[0].isdigit():
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
TYPES_JOUEUR = {"Ally", "Event", "Support", "Upgrade", "Resource"}
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
        if cid and cid[0].isdigit() and cid not in images:
            sans_image.append(f"{cid} ({pack}) {c.get('name', '')}".strip())
rapport["images_manquantes"] = sans_image

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
probleme = bool(par_nom_dans_tests or incoherences or sans_image)
sys.exit(1 if probleme else 0)
