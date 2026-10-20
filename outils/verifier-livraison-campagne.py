#!/usr/bin/env python3
"""Verifie la FORME d'une livraison de campagne (20/10/2026). Python 3.8+, bibliotheque standard seulement.

    python3 verifier-livraison-campagne.py <dossier livraison> [--reference <dossier reference>] [--officiel]
    python3 verifier-livraison-campagne.py <dossier livraison> --moteur <racine du moteur>
    python3 verifier-livraison-campagne.py --generer-reference <racine du moteur> <dossier sortie>

POURQUOI CET OUTIL
------------------
Il attrape ce qu'une IA (ou un humain) peut corriger SEUL avant de livrer : une cle qui manque, un identifiant en
double, un scenario qui cite une carte absente, un script range dans le mauvais dossier, un script qui renvoie une
liste vide pour une carte qui a une capacite, une cle de carnet qui n'existe nulle part, un mot interdit du
vocabulaire francais, une face 1A qui n'appelle pas `CampaignSetup(niveau)` avec le bon niveau.

IL NE REMPLACE PAS LE JEU. Un script qui passe ce controle peut encore ne rien faire en partie : c'est le travail
des cas de test (`tools/cas`), des epreuves de boucle (`tools/epreuves_campagnes.py`) et d'une vraie partie.
Aucune des erreurs ci-dessous n'est « un avertissement sans importance » : un AVERTISSEMENT est un doute que la
livraison doit expliquer dans `QUESTIONS.md` ou `BESOINS-MOTEUR.md`.

Sortie : une ligne par probleme, `ERREUR` (bloquant, code de retour 1) ou `AVERTISSEMENT`.

La reference (ids existants, traits, compteurs, detecteurs...) est lue dans `reference/` a cote de ce fichier, ou
calculee a partir du moteur avec `--moteur`. `--generer-reference` l'ecrit.
"""
import argparse
import ast
import builtins
import collections
import io
import json
import os
import re
import sys

# --------------------------------------------------------------------------- constantes
TYPES = {"Hero", "AlterEgo", "Ally", "Event", "Upgrade", "Support", "Resource", "Obligation", "PlayerSideScheme",
         "Villain", "Minion", "Treachery", "Attachment", "Environment", "SideScheme", "MainScheme", "Leader",
         "Evidence", "Status", "Insert", "Challenge", "Path", "PlayerMinion"}
OBLIGATOIRES = ("card_id", "type", "name", "subtitle", "desc", "traits", "set_name", "text")
CLES_SCENARIO = ("version", "name", "villain", "expert", "schemes", "set_aside", "encounters", "encounter_sets",
                 "modular_sets")
CLES_CAMPAGNE = {"version", "code", "cle_extension", "nom", "nom_en", "resume", "resume_en", "expert", "scenarios",
                 "victoire_commune", "victoire_commune_expert", "pages_regles", "pages_expert", "pages_intro",
                 "livret_fr", "options_campagne", "marche", "cooperation", "enquete", "bilan", "ordre_libre",
                 "vilains", "pages_vilains"}
CLES_SCENARIO_CAMPAGNE = {"id", "catalogue", "numero", "nom", "nom_fr", "resume", "enjeu", "final", "defaite",
                          "reprise", "defaite_continue", "pages", "victoire", "manigance", "environnement"}
CLES_CHAMP = {"cle", "type", "format", "parJoueur", "obligatoire", "libelle", "aide", "options", "detection",
              "parametres", "condition", "cumulatif", "tirage", "deck", "cases"}
DETECTEURS = {"cartes_en_jeu", "compteur_manigance", "cartes_du_joueur", "joueurs_engages", "cartes_sous_complot",
              "pv_restants", "cartes_en_pile_victoire", "cartes_dans_zone", "compter_trait", "conditions_reputation"}
# La gate `ui-app/src/board/vocabulaire-statuts.test.ts` : ces tournures sont refusees dans un texte francais.
INTERDITS_FR = [(r"Robustesse", "Ténacité (Toughness)"), (r"Inébranlable", "Robuste (Stalwart)"),
                (r"(statut|état) Robuste", "carte d'état Tenace (Tough)"), (r"Résistance\.", "Ténacité / Robuste selon le cas"),
                (r"[ée]tourdi", "Sonné (Stunned)")]
MOTS_CAPACITE = ("<b>Response", "<b>Interrupt", "<b>Action", "<b>Hero", "<b>Alter", "<b>Forced", "<b>When",
                 "<b>Boost", "[star]", "<b>Setup", "<b>Resource")
FAN_ID = re.compile(r"^([a-z]{2})(\d{3})([a-z]?)$")
OFF_ID = re.compile(r"^(\d{5})([a-z]?)$")
BUILTINS = set(dir(builtins))
SANS_ETOILE = re.compile(r"""CardFinder\([^)]*name\s*=\s*['"]\*\s""")


def clean_name(nom):
    """Copie de `FileManager.CleanName` (src/engine/file/manager.py)."""
    return (nom.lstrip("*").strip().lower().replace(" - ", "_").replace(" & ", "_").replace(" ", "_")
            .replace("'", "").replace("-", "_").replace("!", "").replace("?", "").replace("(", "").replace(")", "")
            .replace(".", "").replace(",", "").replace('"', "").replace("&", "_").replace("#", "").replace("/", ""))


def lire_json(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return json.load(f)


def lire(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return f.read()


class Rapport:
    def __init__(self):
        self.lignes = []
        self.erreurs = 0
        self.avertissements = 0

    def erreur(self, lieu, texte):
        self.erreurs += 1
        self.lignes.append("ERREUR        %s : %s" % (lieu, texte))

    def avert(self, lieu, texte):
        self.avertissements += 1
        self.lignes.append("AVERTISSEMENT  %s : %s" % (lieu, texte))


# --------------------------------------------------------------------------- reference
def litteraux_python(chemin):
    trouves = set()
    try:
        arbre = ast.parse(lire(chemin))
    except Exception:
        return trouves
    for noeud in ast.walk(arbre):
        if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
            trouves.add(noeud.value)
        elif isinstance(noeud, ast.JoinedStr):
            for part in noeud.values:
                if isinstance(part, ast.Constant) and isinstance(part.value, str):
                    trouves.add(part.value.strip())
    return trouves


def noms_definis(racine):
    """Tous les noms de classes, fonctions et methodes d'un arbre Python (index de l'API)."""
    noms = set()
    for d, ds, fs in os.walk(racine):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f.endswith(".py"):
                try:
                    arbre = ast.parse(lire(os.path.join(d, f)))
                except Exception:
                    continue
                for n in ast.walk(arbre):
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        noms.add(n.name)
                    elif isinstance(n, ast.Assign):
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                noms.add(t.id)
    return noms


def generer_reference(moteur, sortie):
    os.makedirs(sortie, exist_ok=True)
    cartes_json = lire_json(os.path.join(moteur, "data", "cards.json"))
    ids, cles_desc, types = {}, collections.Counter(), collections.Counter()
    classes = set()
    counters_uses = set()
    for pack, liste in cartes_json.items():
        if pack == "checksum":
            continue
        for c in liste:
            if "card_id" in c:
                ids[c["card_id"]] = {"pack": pack, "type": c.get("type"), "set_name": c.get("set_name")}
            for k in (c.get("desc") or {}):
                cles_desc[k] += 1
            for cl in str((c.get("desc") or {}).get("Class", "")).split(";"):
                if cl:
                    classes.add(cl)
            types[c.get("type")] += 1
    perso = os.path.join(moteur, "data", "cards_custom.json")
    if os.path.exists(perso):
        for pack, liste in lire_json(perso).items():
            if isinstance(liste, list):
                for c in liste:
                    if "card_id" in c:
                        ids.setdefault(c["card_id"], {"pack": pack, "type": c.get("type"), "set_name": c.get("set_name")})
    ecrire(sortie, "ids-existants.json", ids)
    ecrire(sortie, "cles-desc.json", sorted(cles_desc))
    ecrire(sortie, "classes.json", sorted(classes))
    ecrire(sortie, "types-de-carte.json", sorted(t for t in types if t))
    sets = sorted(os.path.splitext(f)[0] for f in os.listdir(os.path.join(moteur, "data", "encounter_sets")) if f.endswith(".json"))
    scenarios = sorted(os.path.splitext(f)[0] for f in os.listdir(os.path.join(moteur, "data", "scenarios")) if f.endswith(".json"))
    ecrire(sortie, "sets-existants.json", sets)
    ecrire(sortie, "scenarios-existants.json", scenarios)
    # traits et compteurs : les Literal de card_face.py
    src = lire(os.path.join(moteur, "src", "game", "card", "face", "card_face.py"))
    ecrire(sortie, "traits.json", sorted(set(litteral_liste(src, "TRAITS"))))
    ecrire(sortie, "compteurs.json", sorted(set(litteral_liste(src, "COUNTER"))))
    ecrire(sortie, "jetons.json", sorted(set(litteral_liste(src, "TOKEN"))))
    reg = lire_json(os.path.join(moteur, "tools", "prefixes_fanmade.json"))
    ecrire(sortie, "prefixes-pris.json", reg["prefixes"])
    # cles de carnet connues : litteraux des fichiers communs et de TOUS les campaign.py
    cles = set()
    for rel in ("src/game/operate/campaign_logs.py", "src/game/ability/factory/campaign.py"):
        cles |= litteraux_python(os.path.join(moteur, rel))
    packs = os.path.join(moteur, "src", "cards", "pack")
    for d, ds, fs in os.walk(packs):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f.startswith("campaign") and f.endswith(".py"):
                cles |= litteraux_python(os.path.join(d, f))
    ecrire(sortie, "cles-carnet-connues.json", sorted(c for c in cles if 2 < len(c) < 90))
    # noms d'API : engine + game + core + fonctions de haut niveau des packs
    api = noms_definis(os.path.join(moteur, "src", "game")) | noms_definis(os.path.join(moteur, "src", "core")) \
        | noms_definis(os.path.join(moteur, "src", "engine"))
    # helpers de haut niveau : src/cards/*.py (database, paper...) hors du dossier pack/
    for f in os.listdir(os.path.join(moteur, "src", "cards")):
        if f.endswith(".py"):
            try:
                arbre = ast.parse(lire(os.path.join(moteur, "src", "cards", f)))
            except Exception:
                continue
            for n in ast.walk(arbre):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    api.add(n.name)
    for d, ds, fs in os.walk(packs):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            if f == "__init__.py" or f.startswith("campaign"):
                try:
                    arbre = ast.parse(lire(os.path.join(d, f)))
                except Exception:
                    continue
                for n in arbre.body:
                    if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
                        api.add(n.name)
    ecrire(sortie, "api-names.json", sorted(api))
    ecrire(sortie, "detecteurs.json", sorted(DETECTEURS))
    print("reference ecrite dans %s (%d ids, %d traits, %d compteurs, %d noms d'API)"
          % (sortie, len(ids), len(litteral_liste(src, "TRAITS")), len(litteral_liste(src, "COUNTER")), len(api)))


def litteral_liste(source, nom):
    """Les chaines d'un `NOM = Literal[...]` de card_face.py."""
    m = re.search(r"^\s*%s\s*=\s*Literal\[" % re.escape(nom), source, re.M)
    if not m:
        return []
    depart = m.end()
    prof, i = 1, depart
    while i < len(source) and prof:
        if source[i] == "[":
            prof += 1
        elif source[i] == "]":
            prof -= 1
        i += 1
    corps = source[depart:i - 1]
    corps = re.sub(r"#[^\n]*", "", corps)
    return re.findall(r"""['"]([^'"]+)['"]""", corps)


def ecrire(dossier, nom, valeur):
    with io.open(os.path.join(dossier, nom), "w", encoding="utf-8", newline="") as f:
        json.dump(valeur, f, ensure_ascii=False, indent=1)


class Reference:
    def __init__(self, dossier):
        def charge(nom, defaut):
            chemin = os.path.join(dossier, nom)
            return lire_json(chemin) if os.path.exists(chemin) else defaut
        self.ids = charge("ids-existants.json", {})
        self.cles_desc = set(charge("cles-desc.json", []))
        self.classes = set(charge("classes.json", []))
        self.sets = set(charge("sets-existants.json", []))
        self.scenarios = set(charge("scenarios-existants.json", []))
        self.traits = set(charge("traits.json", []))
        self.compteurs = set(charge("compteurs.json", []))
        self.prefixes = charge("prefixes-pris.json", {})
        self.cles_carnet = set(charge("cles-carnet-connues.json", []))
        self.api = set(charge("api-names.json", []))
        self.detecteurs = set(charge("detecteurs.json", [])) or set(DETECTEURS)
        self.chargee = bool(self.ids)


# --------------------------------------------------------------------------- la livraison
class Livraison:
    def __init__(self, racine, ref, rapport, officiel):
        self.racine = racine
        self.integ = os.path.join(racine, "integration")
        self.ref = ref
        self.r = rapport
        self.officiel = officiel
        self.cartes = {}          # card_id -> carte
        self.packs = {}           # pack -> [cartes]
        self.sets_livres = set()
        self.scenarios_livres = {}
        self.sets_info = {}
        self.campagnes = {}
        self.campaign_py = {}     # pack -> chemin
        self.besoins = ""
        self.prefixe_livre = set()
        self.re_livraison = False

    def chemin(self, *p):
        return os.path.join(self.integ, *p)

    def fichiers(self, sous, ext):
        base = self.chemin(sous)
        if not os.path.isdir(base):
            return []
        sortie = []
        for d, ds, fs in os.walk(base):
            ds[:] = [x for x in ds if x != "__pycache__"]
            for f in fs:
                if f.endswith(ext):
                    sortie.append(os.path.join(d, f))
        return sorted(sortie)

    def rel(self, chemin):
        return os.path.relpath(chemin, self.racine)

    # ---- structure
    def verifier_structure(self):
        r = self.r
        if not os.path.isdir(self.integ):
            r.erreur("livraison", "le dossier `integration/` est introuvable")
            return False
        for nom, grave in (("MANIFESTE.md", True), ("CARNET-CLES.md", True), ("QUESTIONS.md", False),
                           ("BESOINS-MOTEUR.md", False), ("A_FAIRE_CLAUDE.md", False), ("AUTO-VERIFICATION.md", False),
                           ("GABARITS.md", False), ("images.md", False)):
            if not os.path.exists(os.path.join(self.racine, nom)):
                (r.erreur if grave else r.avert)(nom, "fichier de suivi absent de la livraison")
        besoins = os.path.join(self.racine, "BESOINS-MOTEUR.md")
        self.besoins = lire(besoins) if os.path.exists(besoins) else ""
        return True

    # ---- cartes
    def verifier_cartes(self):
        r = self.r
        fragments = self.fichiers("data", ".fragment.json")
        fragments = [f for f in fragments if os.path.basename(f).startswith("cards.")]
        if not fragments:
            r.erreur("data/", "aucun fragment `cards.<pack>.fragment.json`")
            return
        for chemin in fragments:
            lieu = self.rel(chemin)
            try:
                donnees = lire_json(chemin)
            except Exception as e:
                r.erreur(lieu, "JSON invalide : %s" % e)
                continue
            if not isinstance(donnees, dict) or len(donnees) < 1:
                r.erreur(lieu, "attendu un objet {\"<pack>\": [cartes]}")
                continue
            if "checksum" in donnees:
                r.erreur(lieu, "le fragment ne doit pas contenir de `checksum`")
            for pack, liste in donnees.items():
                if pack == "checksum":
                    continue
                if not isinstance(liste, list):
                    r.erreur(lieu, "la valeur du pack %r doit etre une liste" % pack)
                    continue
                self.packs[pack] = liste
                ids_vus = collections.Counter(c.get("card_id") for c in liste)
                for cid, n in ids_vus.items():
                    if n > 1:
                        r.erreur(lieu, "card_id en double dans le fragment : %s (x%d)" % (cid, n))
                triee = [c.get("card_id", "") for c in liste]
                if triee != sorted(triee):
                    r.avert(lieu, "les cartes ne sont pas triees par card_id")
                for c in liste:
                    self.verifier_carte(c, lieu, pack)

    def verifier_carte(self, c, lieu, pack):
        r, ref = self.r, self.ref
        cid = c.get("card_id")
        if not isinstance(cid, str):
            r.erreur(lieu, "une carte n'a pas de `card_id` texte")
            return
        loc = "%s[%s]" % (lieu, cid)
        self.cartes[cid] = c
        if re.match(r"^[a-z][a-z_]*$", cid):
            r.avert(loc, "identifiant special (carte generique du moteur) : controles de forme sautes")
            return
        if "full_link" in c:
            if set(c) - {"card_id", "full_link"}:
                r.erreur(loc, "une carte `full_link` ne porte AUCUNE autre cle que card_id et full_link")
            if c["full_link"] not in ref.ids and c["full_link"] not in self.cartes:
                r.avert(loc, "full_link vers une carte inconnue : %s" % c["full_link"])
            return
        for k in OBLIGATOIRES:
            if k not in c:
                r.erreur(loc, "cle obligatoire absente : %s" % k)
        fan = FAN_ID.match(cid)
        off = OFF_ID.match(cid)
        if not fan and not off:
            r.erreur(loc, "format de card_id invalide (attendu 2 lettres + 3 chiffres + face, ou 5 chiffres + face)")
        if fan and not self.officiel:
            if fan.group(1) not in ref.prefixes and fan.group(1) not in self.prefixe_livre:
                r.erreur(loc, "prefixe %r ni dans le registre existant ni dans ton fragment prefixes" % fan.group(1))
            if not c.get("custom"):
                r.erreur(loc, "contenu fan-made : la cle `custom` (nom de l'auteur) est obligatoire")
        if cid in ref.ids and not self.officiel:
            if ref.ids[cid].get("pack") == pack:
                self.re_livraison = True
            else:
                r.erreur(loc, "ce card_id EXISTE deja dans le jeu (%s) : collision" % ref.ids[cid].get("pack"))
        t = c.get("type")
        if t not in TYPES:
            r.erreur(loc, "type inconnu : %r" % (t,))
        desc = c.get("desc")
        if not isinstance(desc, dict):
            r.erreur(loc, "`desc` doit etre un objet")
            desc = {}
        for k, v in desc.items():
            if not isinstance(v, str):
                r.erreur(loc, "desc.%s doit etre une CHAINE (%r)" % (k, v))
            if ref.cles_desc and k not in ref.cles_desc:
                r.avert(loc, "cle desc inconnue du jeu : %s" % k)
        for cl in str(desc.get("Class", "")).split(";"):
            if cl and ref.classes and cl not in ref.classes:
                r.avert(loc, "desc.Class inconnue : %r" % cl)
        res = str(desc.get("RES", ""))
        if res and not re.match(r"^[RBYG]+$", res):
            r.avert(loc, "desc.RES contient autre chose que R B Y G : %r" % res)
        traits = c.get("traits")
        if not isinstance(traits, list):
            r.erreur(loc, "`traits` doit etre une liste")
        else:
            for tr in traits:
                if tr != str(tr).upper():
                    r.erreur(loc, "trait en MAJUSCULES attendu : %r" % tr)
                elif ref.traits and tr not in ref.traits and tr not in self.besoins:
                    r.avert(loc, "trait %r absent de la liste typee CardFace.TRAITS (non bloquant : aucun controle a "
                                 "l'execution) : a signaler dans BESOINS-MOTEUR.md pour que Claude l'ajoute" % tr)
        uses = desc.get("Uses")
        if isinstance(uses, str) and "," in uses:
            nom_compteur = uses.split(",", 1)[1].strip()
            if ref.compteurs and nom_compteur not in ref.compteurs:
                if nom_compteur in self.besoins:
                    r.avert(loc, "compteur %r absent de la liste du moteur (signale dans BESOINS-MOTEUR.md)" % nom_compteur)
                else:
                    r.erreur(loc, "desc.Uses : le compteur %r n'est PAS dans l'enum COUNTER du moteur : la carte ne "
                                  "se construit pas (assertion). A signaler dans BESOINS-MOTEUR.md." % nom_compteur)
        texte = c.get("text") if isinstance(c.get("text"), str) else ""
        m = re.search(r"Uses \((\d+)[^)]*counters?\)", texte)
        if m and not uses:
            r.erreur(loc, "le texte dit « Uses (%s ... counters) » mais desc.Uses est absent : la carte entre en jeu "
                          "sans compteur et son action reste grisee" % m.group(1))
        if "name" in c and isinstance(c["name"], str) and c["name"].startswith("*") and not c["name"].startswith("* "):
            r.avert(loc, "le prefixe d'unicite est « * » suivi d'une espace")
        if t == "MainScheme" and not re.search(r"[ab]$", cid):
            r.erreur(loc, "un complot principal est une paire a/b : l'identifiant doit finir par a ou b")

    # ---- paires de faces
    def verifier_faces(self):
        for pack, liste in self.packs.items():
            ids = {c.get("card_id") for c in liste}
            for c in liste:
                cid = c.get("card_id", "")
                if c.get("type") == "MainScheme" and cid.endswith("a") and cid[:-1] + "b" not in ids:
                    self.r.erreur(pack + "[" + cid + "]", "complot principal sans sa face B")
                if c.get("type") == "MainScheme" and cid.endswith("b") and cid[:-1] + "a" not in ids:
                    self.r.erreur(pack + "[" + cid + "]", "complot principal sans sa face A")

    # ---- prefixes
    def verifier_prefixes(self):
        for chemin in self.fichiers("tools", ".fragment.json"):
            if not os.path.basename(chemin).startswith("prefixes."):
                continue
            try:
                d = lire_json(chemin)
            except Exception as e:
                self.r.erreur(self.rel(chemin), "JSON invalide : %s" % e)
                continue
            cles = d.get("prefixes", d) if isinstance(d, dict) else {}
            for p, entree in cles.items():
                self.prefixe_livre.add(p)
                if p in self.ref.prefixes:
                    if self.ref.prefixes[p].get("pack") == entree.get("pack"):
                        self.r.avert(self.rel(chemin), "le prefixe %r existe deja pour CE pack : re-livraison d'un pack "
                                                       "deja integre ?" % p)
                    else:
                        self.r.erreur(self.rel(chemin), "le prefixe %r est DEJA pris (%s)" % (p, self.ref.prefixes[p].get("pack")))
                for k in ("pack", "libelle", "cartes", "depuis", "note"):
                    if k not in entree:
                        self.r.avert(self.rel(chemin), "entree %r : cle %r absente" % (p, k))

    # ---- scenarios et sets
    def charger_sets_et_scenarios(self):
        r = self.r
        for chemin in self.fichiers(os.path.join("data", "encounter_sets"), ".json"):
            nom = os.path.splitext(os.path.basename(chemin))[0]
            self.sets_livres.add(nom)
            lieu = self.rel(chemin)
            try:
                d = lire_json(chemin)
            except Exception as e:
                r.erreur(lieu, "JSON invalide : %s" % e)
                continue
            for k in ("version", "name", "encounters"):
                if k not in d:
                    r.erreur(lieu, "cle absente : %s" % k)
            if d.get("version") not in ("0.5.8", "0.5.9"):
                r.erreur(lieu, "`version` doit valoir \"0.5.8\" (ou \"0.5.9\")")
            if isinstance(d.get("name"), str) and d["name"] and d["name"] == d["name"].lower() and not self.officiel:
                r.avert(lieu, "`name` est affiche tel quel au joueur : ecris-le en casse normale (« %s »)" % d["name"].replace("_", " ").title())
            for cid in d.get("encounters", []):
                if not self.carte_connue(cid):
                    r.erreur(lieu, "carte inconnue dans le set : %s" % cid)
            for g in d.get("random_pick", []) or []:
                if not isinstance(g, dict) or "from" not in g or "count" not in g:
                    r.erreur(lieu, "random_pick : chaque groupe est {\"from\": [...], \"count\": n}")
        for chemin in self.fichiers(os.path.join("data", "scenarios"), ".json"):
            nom = os.path.splitext(os.path.basename(chemin))[0]
            try:
                self.scenarios_livres[nom] = lire_json(chemin)
            except Exception as e:
                r.erreur(self.rel(chemin), "JSON invalide : %s" % e)

    def carte_connue(self, cid):
        base = cid
        return base in self.cartes or base in self.ref.ids

    def verifier_scenarios(self):
        r = self.r
        for nom, d in sorted(self.scenarios_livres.items()):
            lieu = "data/scenarios/%s.json" % nom
            est_expert = nom.endswith("_expert")
            for k in CLES_SCENARIO:
                if k not in d:
                    r.erreur(lieu, "cle obligatoire absente : %s" % k)
            inconnues = set(d) - set(CLES_SCENARIO) - {"challenges"}
            if inconnues:
                r.avert(lieu, "cles inattendues : %s" % sorted(inconnues))
            if d.get("version") not in ("0.5.8", "0.5.9"):
                r.erreur(lieu, "`version` doit valoir \"0.5.8\" (ou \"0.5.9\")")
            if bool(d.get("expert")) != est_expert:
                r.erreur(lieu, "`expert` doit valoir %s dans ce fichier" % str(est_expert).lower())
            if not est_expert and nom + "_expert" not in self.scenarios_livres \
                    and nom + "_expert" not in self.ref.scenarios and not self.officiel:
                r.avert(lieu, "pas de variante `%s_expert.json`" % nom)
            for cle in ("villain", "schemes", "set_aside", "encounters"):
                for entree in d.get(cle, []) or []:
                    for cid in str(entree).split(","):
                        if not self.carte_connue(cid.strip()):
                            r.erreur(lieu, "%s : carte inconnue %r" % (cle, cid))
            for entree in d.get("schemes", []) or []:
                if "," not in str(entree):
                    r.erreur(lieu, "schemes : « %s » doit etre une paire « faceA,faceB »" % entree)
            if not d.get("schemes"):
                r.erreur(lieu, "aucun complot principal")
            if not d.get("villain") and not d.get("set_aside"):
                r.avert(lieu, "ni `villain` ni `set_aside` : scenario a plusieurs vilains ? (voir §5.1)")
            for cle in ("encounter_sets", "modular_sets"):
                for s in d.get(cle, []) or []:
                    if s not in self.sets_livres and s not in self.ref.sets:
                        r.erreur(lieu, "%s : le set %r n'existe ni dans ta livraison ni dans le jeu (il se chargerait vide, "
                                       "sans erreur)" % (cle, s))
            if d.get("encounters") and d.get("encounter_sets") and not est_expert:
                pass

    # ---- sets_info
    def verifier_sets_info(self):
        r = self.r
        fr = [f for f in self.fichiers("data", ".fragment.json") if os.path.basename(f).startswith("sets_info.")]
        if not fr:
            r.erreur("data/", "aucun fragment `sets_info.<pack>.fragment.json`")
            return
        for chemin in fr:
            lieu = self.rel(chemin)
            try:
                d = lire_json(chemin)
            except Exception as e:
                r.erreur(lieu, "JSON invalide : %s" % e)
                continue
            for cle, v in d.items():
                if cle == "checksum":
                    r.erreur(lieu, "pas de checksum dans un fragment")
                    continue
                self.sets_info[cle] = v
                if not re.match(r"^(\d+|N|\?)\. ", cle):
                    r.erreur(lieu, "cle %r : forme attendue « N. Nom » (N est attribue par Claude : laisse N)" % cle)
                for k in ("name", "scenarios", "heroes", "encounters", "max_id"):
                    if k not in v:
                        r.erreur(lieu, "entree %r : cle %r absente" % (cle, k))
                for s in v.get("scenarios", []):
                    if s not in self.scenarios_livres and s not in self.ref.scenarios:
                        r.erreur(lieu, "scenario %r : aucun fichier data/scenarios/%s.json" % (s, s))
                    if s.endswith("_expert"):
                        r.erreur(lieu, "scenarios : %r est une variante experte (retire `_expert`)" % s)
                for s in v.get("encounters", []):
                    if s not in self.sets_livres and s not in self.ref.sets:
                        r.erreur(lieu, "encounters : le set %r n'existe pas" % s)
                pack = v.get("name")
                if pack in self.packs:
                    ids = [c.get("card_id", "") for c in self.packs[pack]]
                    def cle_id(x):
                        m = re.search(r"(\d+)([a-z]?)$", x)
                        return (int(m.group(1)), m.group(2)) if m else (0, x)
                    if v.get("max_id") and v["max_id"] not in ids:
                        r.erreur(lieu, "max_id %r n'est pas un card_id du pack" % v.get("max_id"))
                    elif ids and cle_id(v.get("max_id", "")) < max(cle_id(x) for x in ids):
                        r.avert(lieu, "max_id %r est plus petit que le plus grand card_id du pack (%r)"
                                % (v.get("max_id"), max(ids, key=cle_id)))

    # ---- campagnes
    def verifier_campagnes(self):
        r = self.r
        for chemin in self.fichiers(os.path.join("data", "campagnes"), ".json"):
            code = os.path.splitext(os.path.basename(chemin))[0]
            lieu = self.rel(chemin)
            try:
                d = lire_json(chemin)
            except Exception as e:
                r.erreur(lieu, "JSON invalide : %s" % e)
                continue
            self.campagnes[code] = d
            self.verifier_une_campagne(code, d, lieu)

    def verifier_une_campagne(self, code, d, lieu):
        r = self.r
        for k in ("version", "code", "cle_extension", "nom", "nom_en", "resume", "resume_en", "expert", "scenarios",
                  "victoire_commune_expert", "pages_regles"):
            if k not in d:
                r.erreur(lieu, "cle obligatoire absente : %s" % k)
        if d.get("code") != code:
            r.erreur(lieu, "`code` (%r) doit egaler le nom du fichier (%r)" % (d.get("code"), code))
        inconnues = set(d) - CLES_CAMPAGNE
        if inconnues:
            r.avert(lieu, "cles de premier niveau inconnues de l'ecran : %s" % sorted(inconnues))
        cle_ext = d.get("cle_extension", "")
        if cle_ext != "A_FAIRE_CLAUDE":
            ok = any(cle_ext == c or re.sub(r"^(\d+|N|\?)\.", "", cle_ext).strip() == re.sub(r"^(\d+|N|\?)\.", "", c).strip()
                     for c in self.sets_info) if self.sets_info else True
            if not ok:
                r.erreur(lieu, "cle_extension %r ne correspond a AUCUNE cle de ton fragment sets_info (au caractere pres, "
                               "apostrophes comprises)" % cle_ext)
        scenarios = d.get("scenarios") or []
        if not scenarios:
            r.erreur(lieu, "aucun scenario")
        nums = [s.get("numero") for s in scenarios]
        if nums != list(range(1, len(scenarios) + 1)):
            r.erreur(lieu, "`numero` doit valoir 1, 2, 3... dans l'ordre (trouve %s)" % nums)
        finaux = [s.get("id") for s in scenarios if s.get("final")]
        if len(finaux) != 1 or (scenarios and finaux and finaux[0] != scenarios[-1].get("id")) and not d.get("ordre_libre"):
            r.erreur(lieu, "un seul `final: true`, sur le DERNIER scenario (trouve %s)" % finaux)
        ids_info = set()
        for v in self.sets_info.values():
            ids_info |= set(v.get("scenarios", []))
        cles_vues = {}
        for s in scenarios:
            sl = "%s :: scenario %s" % (lieu, s.get("id"))
            for k in ("id", "numero", "nom", "nom_fr", "resume", "enjeu", "pages", "victoire"):
                if k not in s:
                    r.erreur(sl, "cle absente : %s" % k)
            ine = set(s) - CLES_SCENARIO_CAMPAGNE
            if ine:
                r.avert(sl, "cles inconnues de l'ecran : %s" % sorted(ine))
            fichier = s.get("catalogue") or s.get("id")
            if fichier not in self.scenarios_livres and fichier not in self.ref.scenarios:
                r.erreur(sl, "aucun fichier data/scenarios/%s.json" % fichier)
            if ids_info and s.get("id") not in ids_info and fichier not in ids_info:
                r.erreur(sl, "l'id n'est pas dans `scenarios` de sets_info")
            if str(s.get("id", "")).endswith("_expert"):
                r.erreur(sl, "pas de `_expert` dans l'id : l'ecran prend la variante experte tout seul")
            defaite = s.get("defaite")
            if defaite is not None:
                if defaite.get("quand") not in ("partie_perdue", "cle_absente"):
                    r.erreur(sl, "defaite.quand : partie_perdue | cle_absente")
                if defaite.get("quand") == "cle_absente" and not defaite.get("cle"):
                    r.erreur(sl, "defaite cle_absente sans `cle`")
                if not s.get("final"):
                    r.avert(sl, "`defaite` n'a de sens que sur le scenario final")
            for champ in s.get("victoire", []) or []:
                self.verifier_champ(champ, sl, cles_vues)
            for p in (s.get("pages") or {}).values():
                for f in p:
                    if not re.match(r"^[0-9A-Za-z_\-]+\.(jpg|png|webp)$", f):
                        r.erreur(sl, "nom de page de livret invalide : %r" % f)
        for liste in ("victoire_commune", "victoire_commune_expert"):
            for champ in d.get(liste, []) or []:
                self.verifier_champ(champ, "%s :: %s" % (lieu, liste), cles_vues)
        for opt in d.get("options_campagne", []) or []:
            if opt.get("type") not in ("case", "siege"):
                r.erreur(lieu, "options_campagne.%s : type case | siege" % opt.get("cle"))
        for m in (d.get("marche"),):
            if m and not (m.get("cles_cartes") or m.get("cle_cartes")):
                r.avert(lieu, "marche sans `cle_cartes`")
        d["__cles_vues__"] = cles_vues

    def verifier_champ(self, champ, lieu, cles_vues):
        r = self.r
        cle = champ.get("cle")
        loc = "%s :: champ %r" % (lieu, cle)
        for k in ("cle", "type", "libelle", "aide"):
            if k not in champ:
                r.erreur(loc, "cle absente : %s" % k)
        ine = set(champ) - CLES_CHAMP
        if ine:
            r.avert(loc, "cles inconnues du panneau : %s" % sorted(ine))
        if champ.get("type") not in ("auto", "choix"):
            r.erreur(loc, "type : auto | choix")
        if champ.get("format") not in (None, "int", "liste", "liste-joueurs"):
            r.erreur(loc, "format : int | liste | liste-joueurs")
        det = champ.get("detection")
        if det and det not in self.ref.detecteurs:
            r.erreur(loc, "detection %r n'existe pas (champ vide, en silence). Disponibles : %s"
                     % (det, sorted(self.ref.detecteurs)))
        if det and champ.get("type") == "choix":
            r.erreur(loc, "un champ `choix` n'a pas de detection (c'est une decision du joueur)")
        if champ.get("condition") not in (None, "complot_absent"):
            r.erreur(loc, "condition inconnue : %r (le champ serait MASQUE)" % champ.get("condition"))
        if champ.get("deck") is not None:
            if champ["deck"] != "requis":
                r.erreur(loc, "deck : seule la valeur \"requis\" existe")
            if not champ.get("parJoueur"):
                r.erreur(loc, "deck: requis exige parJoueur")
        if champ.get("cumulatif") and champ.get("format") != "int":
            r.erreur(loc, "cumulatif n'a de sens que sur un format int")
        if champ.get("tirage") is not None:
            t = champ["tirage"]
            p = t.get("paliers")
            if not (isinstance(p, list) and p and all(isinstance(x, int) and x > 0 for x in p) and p == sorted(p)):
                r.erreur(loc, "tirage.paliers : liste d'entiers positifs croissants")
            if not champ.get("options"):
                r.erreur(loc, "tirage sans options : rien a tirer")
            if champ.get("type") != "auto":
                r.erreur(loc, "un tirage est releve par le jeu : type auto")
            if t.get("cle_piste") not in cles_vues:
                r.erreur(loc, "tirage.cle_piste %r doit etre declaree AVANT ce champ" % t.get("cle_piste"))
        for cid in champ.get("options", []) or []:
            if not self.carte_connue(cid):
                r.erreur(loc, "option inconnue : %s" % cid)
        if champ.get("obligatoire") and champ.get("type") != "choix":
            r.avert(loc, "`obligatoire` ne bloque que les champs `choix`")
        if cle in cles_vues and cles_vues[cle] != lieu.split(" :: ")[1:2]:
            pass
        cles_vues.setdefault(cle, lieu)

    # ---- campaign.py et branchement
    def verifier_campaign_py(self):
        r = self.r
        for chemin in self.fichiers("src", "campaign.py"):
            pack = chemin.replace("\\", "/").split("/src/cards/pack/")[1].split("/")[0]
            self.campaign_py[pack] = chemin
            lieu = self.rel(chemin)
            try:
                arbre = ast.parse(lire(chemin))
            except SyntaxError as e:
                r.erreur(lieu, "erreur de syntaxe : %s" % e)
                continue
            noms = {n.name for n in arbre.body if isinstance(n, ast.FunctionDef)}
            utilise_campagne = "AbilityFactoryCampaign" in lire(chemin)
            if "CampaignSetup" not in noms and not utilise_campagne:
                r.erreur(lieu, "ni `CampaignSetup(level)` ni aucune capacite `AbilityFactoryCampaign.*` : le carnet ne "
                               "sera jamais applique")
            elif "CampaignSetup" not in noms:
                r.avert(lieu, "pas de fonction `CampaignSetup(level)` : la campagne utilise des fonctions de campagne "
                              "propres (modele Web of Deceit) ; le niveau des faces 1A n'est pas controlable")
        if not self.campaign_py and self.campagnes:
            r.erreur("src/", "une campagne est livree mais aucun `campaign.py` : le carnet est ignore en silence")
        # cles declarees ET connues
        litteraux = set(self.ref.cles_carnet)
        for chemin in self.campaign_py.values():
            litteraux |= litteraux_python(chemin)
        pack_dir = {p: os.path.dirname(c) for p, c in self.campaign_py.items()}
        for p, dossier in pack_dir.items():
            for d, ds, fs in os.walk(dossier):
                ds[:] = [x for x in ds if x != "__pycache__"]
                for f in fs:
                    if f.endswith(".py"):
                        litteraux |= litteraux_python(os.path.join(d, f))
        for code, camp in self.campagnes.items():
            for cle in camp.get("__cles_vues__", {}):
                if cle is None:
                    continue
                if not connue(cle, litteraux):
                    r.erreur("data/campagnes/%s.json" % code,
                             "la cle de carnet %r n'est ECRITE NI LUE nulle part dans ton `campaign.py` ni dans le "
                             "moteur : la recompense disparaitra en silence" % cle)
        # cles ecrites par un collecteur mais non declarees
        for pack, chemin in self.campaign_py.items():
            src = lire(chemin)
            ecrites = set(re.findall(r"""updates\[\s*['"]([^'"]+)['"]\s*\]\s*=""", src))
            declarees = set()
            for camp in self.campagnes.values():
                declarees |= set(k for k in camp.get("__cles_vues__", {}) if k)
            for cle in sorted(ecrites):
                if cle not in declarees and re.sub(r"^Player \d+ ", "", cle) not in declarees:
                    r.avert(self.rel(chemin), "le collecteur ecrit la cle %r mais la description de campagne ne la "
                                              "declare pas : le panneau ne la reportera JAMAIS" % cle)

    def verifier_branchement_1A(self):
        r = self.r
        for code, camp in self.campagnes.items():
            for s in camp.get("scenarios", []):
                fichier = s.get("catalogue") or s.get("id")
                sc = self.scenarios_livres.get(fichier)
                if not sc or not sc.get("schemes"):
                    continue
                face_a = str(sc["schemes"][0]).split(",")[0].strip()
                carte = self.cartes.get(face_a)
                lieu = "scenario %s, face 1A %s" % (s.get("id"), face_a)
                if carte is None:
                    if not self.officiel:
                        r.erreur(lieu, "carte absente de ton fragment")
                    continue
                pack = [p for p, l in self.packs.items() if any(c.get("card_id") == face_a for c in l)]
                pack = pack[0] if pack else None
                script = self.chemin("src", "cards", "pack", pack or "?", clean_name(carte.get("set_name", "")), face_a + ".py")
                if not os.path.exists(script):
                    script2 = self.chemin("src", "cards", "pack", pack or "?", face_a + ".py")
                    script = script2 if os.path.exists(script2) else script
                if not os.path.exists(script):
                    r.erreur(lieu, "aucun script %s : la face 1A doit appeler *CampaignSetup(%s)" % (self.rel(script), s.get("numero")))
                    continue
                texte = lire(script)
                m = re.findall(r"CampaignSetup\(\s*(\d+)", texte)
                importes = set()
                try:
                    arbre_1a = ast.parse(texte)
                    for nd in ast.walk(arbre_1a):
                        if isinstance(nd, ast.ImportFrom) and nd.module and nd.module.endswith(".campaign"):
                            importes |= {al.name for al in nd.names}
                    # seuls comptent les noms importes ET APPELES : un import qui ne sert a rien ne branche rien
                    appeles = {nd.func.id for nd in ast.walk(arbre_1a)
                               if isinstance(nd, ast.Call) and isinstance(nd.func, ast.Name)}
                    importes &= appeles
                except SyntaxError:
                    pass
                collecteur = False
                if pack in self.campaign_py:
                    collecteur = "WriteCampaignLogAtGameOver" in lire(self.campaign_py[pack])
                if m:
                    if int(m[0]) != s.get("numero"):
                        r.erreur(lieu, "CampaignSetup(%s) mais le numero du scenario est %s : les recompenses d'un AUTRE "
                                       "scenario seraient appliquees" % (m[0], s.get("numero")))
                    elif not re.search(r"from\s+cards\.pack\.[A-Za-z0-9_]+\.campaign\s+import", texte):
                        r.erreur(lieu, "import de CampaignSetup depuis cards.pack.<pack>.campaign attendu")
                elif importes:
                    r.avert(lieu, "la face 1A appelle une fonction de campagne propre (%s), pas CampaignSetup(n) : "
                                  "controle que son niveau est bien %s" % (", ".join(sorted(importes)), s.get("numero")))
                elif s.get("numero") == 1 and not collecteur:
                    r.avert(lieu, "pas d'appel de campagne au scenario 1 (acceptable : aucun carnet entrant et aucun "
                                  "collecteur a poser)")
                else:
                    r.erreur(lieu, "la face 1A n'appelle aucune fonction de campagne (*CampaignSetup(%s)) : le carnet est "
                                   "ignore en silence" % s.get("numero"))

    # ---- scripts
    def verifier_scripts(self):
        r = self.r
        marqueurs = 0
        scripts_par_id = {}
        base = self.chemin("src", "cards", "pack")
        if not os.path.isdir(base):
            r.avert("src/", "aucun script livre")
            return
        for pack in sorted(os.listdir(base)):
            dossier_pack = os.path.join(base, pack)
            if not os.path.isdir(dossier_pack) or pack == "__pycache__":
                continue
            if not os.path.exists(os.path.join(dossier_pack, "__init__.py")):
                r.avert(self.rel(dossier_pack), "pas de `__init__.py` a la racine du pack (helpers partages impossibles)")
            for d, ds, fs in os.walk(dossier_pack):
                ds[:] = [x for x in ds if x != "__pycache__"]
                if d != dossier_pack and fs and "__init__.py" not in fs and any(f.endswith(".py") for f in fs):
                    r.erreur(self.rel(d), "dossier de set SANS `__init__.py` : les cartes du set n'auront AUCUNE capacite, "
                                          "sans erreur")
                for f in fs:
                    if not f.endswith(".py"):
                        continue
                    chemin = os.path.join(d, f)
                    lieu = self.rel(chemin)
                    texte = lire(chemin)
                    marqueurs += len(re.findall(r"#\s*A_FAIRE_CLAUDE", texte))
                    try:
                        arbre = ast.parse(texte)
                    except SyntaxError as e:
                        r.erreur(lieu, "erreur de syntaxe : %s" % e)
                        continue
                    self.verifier_un_script(chemin, lieu, texte, arbre, pack, dossier_pack, scripts_par_id)
        self.marqueurs = marqueurs

    def verifier_un_script(self, chemin, lieu, texte, arbre, pack, dossier_pack, scripts_par_id):
        r = self.r
        nom = os.path.basename(chemin)
        if nom in ("__init__.py", "campaign.py") or not re.match(r"^[0-9a-z]+\.py$", nom):
            self.verifier_appels(arbre, texte, lieu, nom)
            return
        cid = nom[:-3]
        carte = self.cartes.get(cid)
        if carte is None:
            if cid in self.ref.ids and self.officiel:
                carte = None
            else:
                r.erreur(lieu, "script pour un card_id absent de ton fragment : %s" % cid)
                return
        else:
            attendu = os.path.relpath(os.path.dirname(chemin), dossier_pack).replace("\\", "/")
            voulu = clean_name(carte.get("set_name", "")) or "."
            # Le moteur cherche `<pack>/<set_nettoye>/<id>.py` PUIS `<pack>/<id>.py` (racine du pack).
            if attendu not in (voulu, "."):
                r.erreur(lieu, "script rangé dans %r mais le set_name %r veut le dossier %r (ou la racine du pack) : "
                               "le script est MUET" % (attendu, carte.get("set_name"), voulu))
        if "GetAbilities" not in {n.name for n in arbre.body if isinstance(n, ast.FunctionDef)}:
            r.erreur(lieu, "pas de fonction GetAbilities()")
        premier = [n for n in arbre.body if isinstance(n, ast.ImportFrom)]
        if not premier or not any(n.names and n.names[0].name == "*" for n in premier):
            r.avert(lieu, "un script de carte commence par `from . import *`")
        if SANS_ETOILE.search(texte):
            r.erreur(lieu, "CardFinder(name=\"* ...\") ne trouve jamais rien : ecris name=\"...\" SANS l'etoile")
        if re.search(r"^\s*print\(", texte, re.M):
            r.avert(lieu, "print() de debug dans un script de carte")
        if re.search(r"\bopen\(|\bimport os\b|\bimport subprocess\b|\bimport socket\b|\bexec\(|\beval\(", texte):
            r.erreur(lieu, "un script de carte ne fait aucune entree-sortie (open/os/subprocess/socket/exec/eval)")
        retours_vides = False
        for n in ast.walk(arbre):
            if isinstance(n, ast.FunctionDef) and n.name == "GetAbilities":
                rets = [x for x in ast.walk(n) if isinstance(x, ast.Return)]
                if not rets or all(isinstance(x.value, ast.List) and not x.value.elts for x in rets):
                    retours_vides = True
        txt = (carte or {}).get("text") if isinstance((carte or {}).get("text"), str) else ""
        commentaires = len([l for l in texte.split("\n") if l.strip().startswith("#")])
        if retours_vides and "A_FAIRE_CLAUDE" not in texte:
            if any(m in txt for m in MOTS_CAPACITE) and commentaires < 2:
                r.erreur(lieu, "GetAbilities() renvoie une liste VIDE sans A_FAIRE_CLAUDE ni commentaire qui explique "
                               "pourquoi, alors que le texte imprime une capacite : une carte vide ne signifie pas une carte "
                               "sans effet")
            elif any(m in txt for m in MOTS_CAPACITE):
                r.avert(lieu, "liste vide justifiee par un commentaire (le moteur fait-il vraiment l'effet ?) : a confirmer par Claude")
            else:
                r.avert(lieu, "script a liste vide : supprime-le si la carte n'a aucune capacite imprimee")
        self.verifier_appels(arbre, texte, lieu, nom)

    def verifier_appels(self, arbre, texte, lieu, nom):
        """Heuristique : un appel CamelCase absent de l'API du moteur, des helpers livres et des builtins."""
        if not self.ref.api:
            return
        if not hasattr(self, "_locaux"):
            self._locaux = set()
            for chemin in self.fichiers("src", ".py"):
                try:
                    a = ast.parse(lire(chemin))
                except SyntaxError:
                    continue
                for n in ast.walk(a):
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                        self._locaux.add(n.name)
                    elif isinstance(n, ast.Assign):
                        for t in n.targets:
                            if isinstance(t, ast.Name):
                                self._locaux.add(t.id)
        locaux = set(self._locaux)
        for n in ast.walk(arbre):
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                for alias in n.names:
                    locaux.add((alias.asname or alias.name).split(".")[0])
        inconnus = set()
        for n in ast.walk(arbre):
            if isinstance(n, ast.Call):
                f = n.func
                nom_appel = f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
                if nom_appel and nom_appel[:1].isupper() and nom_appel not in self.ref.api \
                        and nom_appel not in locaux and nom_appel not in BUILTINS:
                    inconnus.add(nom_appel)
        for nom_appel in sorted(inconnus):
            self.r.avert(lieu, "appel `%s(...)` absent de l'index de l'API du moteur et des helpers livres : fonction "
                               "INVENTEE ? (une fonction inventee ne leve aucune erreur : la carte ne fait rien)" % nom_appel)

    # ---- textes francais
    def verifier_textes_fr(self):
        r = self.r
        fichiers = self.fichiers("textes-fr", ".txt")
        if self.officiel:
            return
        if not fichiers:
            r.erreur("textes-fr/", "aucun fragment de texte francais : les cartes n'auront AUCUN tooltip francais, sans "
                                   "que rien ne le signale")
            return
        presents = {}
        for chemin in fichiers:
            lieu = self.rel(chemin)
            for i, ligne in enumerate(lire(chemin).split("\n"), 1):
                m = re.match(r"""^\s*'([^']+)'\s*:\s*"(.*)",\s*$""", ligne)
                if m:
                    if m.group(1) in presents:
                        r.erreur("%s:%d" % (lieu, i), "entree en double : %s" % m.group(1))
                    presents[m.group(1)] = m.group(2)
                    for motif, bon in INTERDITS_FR:
                        trouve = re.search(motif, m.group(2), re.I if motif.startswith("[ée]") else 0)
                        if trouve:
                            r.erreur("%s:%d" % (lieu, i), "vocabulaire interdit « %s » (utilise %s)" % (trouve.group(0), bon))
                elif ligne.strip() and not ligne.strip().startswith("//"):
                    r.avert("%s:%d" % (lieu, i), "ligne inattendue (attendu : un commentaire ou  'id': \"texte\",)")
        for cid, c in self.cartes.items():
            if "full_link" in c:
                continue
            if cid not in presents:
                r.erreur("textes-fr/", "pas de texte francais pour %s (%s)" % (cid, c.get("name")))
        for cid in presents:
            if cid not in self.cartes:
                r.avert("textes-fr/", "texte pour un card_id absent de ton fragment : %s" % cid)

    # ---- images
    def verifier_images(self):
        chemin = os.path.join(self.racine, "images.md")
        if not os.path.exists(chemin):
            return
        texte = lire(chemin)
        manque = [cid for cid, c in self.cartes.items() if "full_link" not in c and cid not in texte]
        if manque:
            self.r.avert("images.md", "%d card_id absents du tableau (ex. %s)" % (len(manque), ", ".join(manque[:5])))

    # ---- epreuves
    def verifier_epreuves(self):
        r = self.r
        for chemin in self.fichiers("tools", ".fragment.py"):
            if not os.path.basename(chemin).startswith("epreuves."):
                continue
            lieu = self.rel(chemin)
            try:
                arbre = ast.parse(lire(chemin))
            except SyntaxError as e:
                r.erreur(lieu, "erreur de syntaxe : %s" % e)
                continue
            epreuves = []
            for n in ast.walk(arbre):
                if isinstance(n, ast.AugAssign) and isinstance(n.target, ast.Name) and n.target.id == "EPREUVES":
                    try:
                        epreuves = ast.literal_eval(n.value)
                    except Exception:
                        r.erreur(lieu, "`EPREUVES += [...]` doit etre un LITTERAL (dicts, listes, chaines, nombres)")
            if not epreuves:
                r.erreur(lieu, "aucune epreuve trouvee (`EPREUVES += [ ... ]`)")
                continue
            scen_camp = {s["id"] for c in self.campagnes.values() for s in c.get("scenarios", [])}
            couverts = set()
            for e in epreuves:
                for k in ("nom", "scenario", "heros"):
                    if k not in e:
                        r.erreur(lieu, "epreuve sans cle %r" % k)
                if e.get("fin") not in (None, "Win", "Lose"):
                    r.erreur(lieu, "epreuve %r : fin = Win | Lose" % e.get("nom"))
                ce = (e.get("carnet_attendu") or {}).get("scenario")
                if ce:
                    couverts.add(ce)
                    if scen_camp and ce not in scen_camp:
                        r.erreur(lieu, "epreuve %r : carnet_attendu.scenario %r n'est pas l'id d'un scenario de la campagne"
                                 % (e.get("nom"), ce))
                if e.get("scenario") and e["scenario"] not in self.scenarios_livres and e["scenario"] not in self.ref.scenarios:
                    r.erreur(lieu, "epreuve %r : scenario %r inconnu" % (e.get("nom"), e["scenario"]))
            for s in sorted(scen_camp - couverts):
                r.avert(lieu, "aucune epreuve ne verifie l'estampille du carnet sortant du scenario %r "
                              "(`carnet_attendu.scenario`)" % s)

    def verifier_cas(self):
        for chemin in self.fichiers(os.path.join("tools", "cas"), ".py"):
            try:
                ast.parse(lire(chemin))
            except SyntaxError as e:
                self.r.erreur(self.rel(chemin), "erreur de syntaxe : %s" % e)

    # ---- manifeste
    def verifier_manifeste(self):
        chemin = os.path.join(self.racine, "MANIFESTE.md")
        if not os.path.exists(chemin):
            return
        texte = lire(chemin)
        reels = []
        for d, ds, fs in os.walk(self.integ):
            ds[:] = [x for x in ds if x != "__pycache__"]
            for f in fs:
                reels.append(os.path.relpath(os.path.join(d, f), self.integ).replace("\\", "/"))
        non_listes = [f for f in reels if f not in texte]
        if non_listes:
            self.r.avert("MANIFESTE.md", "%d fichier(s) livre(s) non listes (ex. %s)" % (len(non_listes), ", ".join(non_listes[:4])))
        fa = os.path.join(self.racine, "A_FAIRE_CLAUDE.md")
        if os.path.exists(fa) and hasattr(self, "marqueurs"):
            n = len(re.findall(r"A_FAIRE_CLAUDE", lire(fa)))
            if self.marqueurs and n == 0:
                self.r.avert("A_FAIRE_CLAUDE.md", "%d marqueur(s) dans le code mais la liste est vide" % self.marqueurs)

    def verifier_carnet_cles(self):
        chemin = os.path.join(self.racine, "CARNET-CLES.md")
        if not os.path.exists(chemin) or not self.campagnes:
            return
        texte = lire(chemin)
        for code, camp in self.campagnes.items():
            for cle in camp.get("__cles_vues__", {}):
                if cle and cle not in texte:
                    self.r.avert("CARNET-CLES.md", "la cle %r de la description n'a pas de ligne dans la table" % cle)

    def tout(self):
        if not self.verifier_structure():
            return
        self.verifier_prefixes()
        self.verifier_cartes()
        self.verifier_faces()
        self.charger_sets_et_scenarios()
        self.verifier_scenarios()
        self.verifier_sets_info()
        self.verifier_campagnes()
        self.verifier_campaign_py()
        self.verifier_branchement_1A()
        self.verifier_scripts()
        self.verifier_textes_fr()
        self.verifier_images()
        self.verifier_epreuves()
        self.verifier_cas()
        self.verifier_manifeste()
        self.verifier_carnet_cles()


def connue(cle, litteraux):
    """La cle existe-t-elle, ecrite ou COMPOSEE ? (meme regle que tools/verifier_campagnes.py)."""
    nue = re.sub(r"^Player \d+ ", "", cle)
    for k in (cle, nue):
        if k in litteraux:
            return True
        for prefixe in litteraux:
            if prefixe and prefixe.endswith(" ") and k.startswith(prefixe) and k[len(prefixe):] in litteraux:
                return True
    return False


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("livraison", nargs="?")
    ap.add_argument("--reference")
    ap.add_argument("--moteur")
    ap.add_argument("--officiel", action="store_true", help="campagne officielle : ni prefixe, ni custom, ni texte francais")
    ap.add_argument("--generer-reference", nargs=2, metavar=("MOTEUR", "SORTIE"))
    args = ap.parse_args()
    if args.generer_reference:
        generer_reference(*args.generer_reference)
        return 0
    if not args.livraison:
        ap.error("dossier de livraison requis")
    ici = os.path.dirname(os.path.abspath(__file__))
    ref_dir = args.reference or os.path.join(ici, "reference")
    if args.moteur:
        import tempfile
        ref_dir = tempfile.mkdtemp(prefix="reference-")
        generer_reference(args.moteur, ref_dir)
    ref = Reference(ref_dir)
    if not ref.chargee:
        print("ATTENTION : aucune reference trouvee dans %s : les controles contre le jeu existant sont desactives." % ref_dir)
    rapport = Rapport()
    liv = Livraison(os.path.abspath(args.livraison), ref, rapport, args.officiel)
    liv.tout()
    for ligne in rapport.lignes:
        print(ligne)
    print()
    print("%d ERREUR(S), %d AVERTISSEMENT(S)" % (rapport.erreurs, rapport.avertissements))
    return 1 if rapport.erreurs else 0


if __name__ == "__main__":
    sys.exit(main())
