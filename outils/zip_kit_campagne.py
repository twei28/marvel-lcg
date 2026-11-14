"""Assemble le ZIP du kit de creation de campagne (20/10/2026). Appele par `construire-kit-campagne.py`.

Tout vient du depot : rien n'est ecrit a la main ici hors du squelette. Garde-fou final : une recherche de secrets
(cle privee, adresse du serveur, mot de passe) dans TOUT ce qui entre dans le zip ; elle fait echouer la construction.
"""
import ast
import contextlib
import importlib.util
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

MODELES = [
    # (dossier dans le zip, pack, code, officiel, images d'exemple)
    ("A-officielle-the-mad-titans-shadow", "mts", "mts", True,
     ["assets/pics/21071.jpg", "assets/pics/21074a.jpg", "assets/pics/21183.jpg",
      "assets/textures/sets/21. The Mad Titan's Shadow.webp",
      "public/stories/mts/00-couverture.jpg", "public/stories/mts/00-campagne-regles-1.jpg",
      "public/stories/mts/01-ebony_maw-intro-1.jpg", "public/stories/mts/01-ebony_maw-regles-1.jpg",
      "public/stories/mts/01-ebony_maw-epilogue-1.jpg"]),
    ("B-maison-web-of-deceit", "web_of_deceit", "web_of_deceit", False,
     ["assets/pics/wd001a.jpg", "assets/pics/wd002a.jpg", "assets/pics/wd006.jpg", "assets/pics/wd015.jpg",
      "assets/pics/wd113.jpg", "assets/textures/sets/120. Custom (Web of Deceit).webp",
      "public/stories/web_of_deceit/00-couverture.jpg", "public/stories/web_of_deceit/00-campagne-regles-1.jpg"]),
]

COMMUN = {
    "moteur": [
        "src/game/operate/campaign_logs.py", "src/game/ability/factory/campaign.py", "src/game/ability/factory/expert.py",
        "src/game/ability/factory/setup.py", "src/game/operate/worlds.py", "src/game/operate/store.py",
        "src/game/message/sender/sender_round.py", "src/game/scene/loader.py", "src/game/scene/replay/campaign.py",
        "src/game/world/world.py", "src/game/card/factory.py", "src/cards/pack/__init__.py",
        "src/engine/device/web/server/server_new_game.py", "src/game/puzzle/puzzle.py",
    ],
    "serveur": ["src/engine/device/web/server/server_campagne.py"],
    "ecran": ["public/campagne.html", "public/js/campagne/app.js", "public/js/campagne/api-campagne.js",
              "public/js/campagne/brouillon.js", "public/js/campagne/livre-pages.js", "public/js/campagne/ordre-libre.js",
              "public/css/campagne/campagne.css", "public/js/prepare/launcher.js"],
    "outils": ["tools/verifier_campagnes.py", "tools/test_campagnes.py", "tools/epreuves_campagnes.py",
               "tools/sonde_campagne.py", "tools/pages_livret.py", "tools/livret_fr.py", "tools/verifier_prefixes.py",
               "tools/recalculer_checksums.py", "tools/verifier_desc_mots_cles.py", "tools/importer_web_of_deceit.py",
               "tools/prefixes_fanmade.json"],
}

CAMPAIGN_PY = [("trors", "trors/campaign.py"), ("sm", "sm/campaign.py"), ("mts", "mts/campaign.py"),
               ("mut_gen", "mut_gen/campaign.py"), ("next_evol", "next_evol/campaign.py"),
               ("aoa", "aoa/campaign_setup.py"), ("gmw", "gmw/campaign.py"), ("aos", "aos/campaign.py"),
               ("fne", "fne/campaign.py"), ("hunting_season", "hunting_season/campaign.py"),
               ("skrull_menace", "skrull_menace/campaign.py"), ("web_of_deceit", "web_of_deceit/campaign.py")]

ANNEXES = [
    ("docs/reference/KIT-CHATGPT-CREATION.md", "annexes/A-kit-cartes.md"),
    ("docs/reference/RECETTES-MOTEUR.md", "annexes/B-recettes-moteur.md"),
    ("docs/reference/MOTS-CLES-TOUS.md", "annexes/C-mots-cles-tous.md"),
    ("docs/reference/PROCESSUS-CARTE.md", "annexes/D-processus-carte.md"),
    ("docs/reference/PROCESSUS-HEROS.md", "annexes/D-processus-heros.md"),
    ("docs/reference/GUIDE-CREATION-CONTENU.md", "annexes/E-guide-creation-contenu.md"),
    ("docs/rapports/CAMPAGNES.md", "annexes/F-campagnes-etat-des-lieux.md"),
    ("docs/superpowers/specs/2026-08-07-mode-campagne-design.md", "annexes/F2-mode-campagne-conception.md"),
    (".planning/todos/2026-08-12-campagne-web-of-deceit.md", "annexes/G-journal-portage-web-of-deceit.md"),
    (".planning/todos/2026-09-19-boucle-de-campagne-dix-boites.md", "annexes/H-boucle-de-campagne-dix-boites.md"),
    (".planning/skrull-menace/CAMPAGNE-MODE.md", "annexes/K-skrull-menace-campagne-mode.md"),
    (".planning/skrull-menace/BRIEF-AGENTS.md", "annexes/K-skrull-menace-brief-agents.md"),
]

SECRETS = [r"178\.105\.", r"cle_narwhal", r"BEGIN [A-Z ]*PRIVATE KEY", r"(?i)api[_-]?key\s*[:=]\s*['\"][A-Za-z0-9]{12,}",
           r"(?i)\"password\"\s*:\s*\"[^\"]{3,}\"", r"(?!noreply@anthropic\.com)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.(com|fr|be|net)\b",
           r"(?i)bearer\s+[A-Za-z0-9._-]{20,}", r"sk-[A-Za-z0-9]{20,}"]


def lire(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return f.read()


class Zip:
    def __init__(self, chemin):
        if os.path.exists(chemin):
            os.remove(chemin)
        self.z = zipfile.ZipFile(chemin, "w", zipfile.ZIP_DEFLATED, compresslevel=6)
        self.noms = set()
        self.texte = []   # (nom, contenu) pour la recherche de secrets

    def ajouter_texte(self, nom, contenu):
        if nom in self.noms:
            return
        self.noms.add(nom)
        self.z.writestr(nom, contenu.encode("utf-8"))
        self.texte.append((nom, contenu))

    def ajouter_fichier(self, source, nom):
        if nom in self.noms or not os.path.isfile(source):
            return False
        self.noms.add(nom)
        ext = os.path.splitext(source)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".webp", ".pdf"):
            self.z.write(source, nom)
        else:
            self.ajouter_texte_apres_lecture(source, nom)
        return True

    def ajouter_texte_apres_lecture(self, source, nom):
        self.noms.discard(nom)
        self.ajouter_texte(nom, lire(source))

    def ajouter_arbre(self, source, prefixe, filtre=None):
        n = 0
        for d, ds, fs in os.walk(source):
            ds[:] = sorted(x for x in ds if x not in ("__pycache__", "node_modules"))
            for f in sorted(fs):
                if f.endswith((".pyc", ".pyo")):
                    continue
                chemin = os.path.join(d, f)
                rel = os.path.relpath(chemin, source).replace("\\", "/")
                if filtre and not filtre(rel):
                    continue
                if self.ajouter_fichier(chemin, prefixe + "/" + rel):
                    n += 1
        return n

    def fermer(self):
        self.z.close()


def index_api(moteur):
    """L'index de l'API du moteur : chaque classe et fonction, ses arguments, la premiere ligne de son commentaire."""
    sortie = ["# Index de l'API du moteur (genere le 20/10/2026 par `outils/zip_kit_campagne.py`)", "",
              "Chaque classe et chaque fonction des dossiers `src/game`, `src/engine`, `src/core` et des helpers de "
              "`src/cards`, avec ses arguments (sans `self`) et la premiere ligne de son commentaire. **C'est la "
              "reference pour ne rien inventer** : un nom qui n'est pas ici n'existe pas pour une carte.", ""]
    total = 0
    racines = [("game", os.path.join(moteur, "src", "game")), ("engine", os.path.join(moteur, "src", "engine")),
               ("core", os.path.join(moteur, "src", "core"))]
    fichiers = []
    for nom, racine in racines:
        for d, ds, fs in os.walk(racine):
            ds[:] = sorted(x for x in ds if x != "__pycache__")
            for f in sorted(fs):
                if f.endswith(".py"):
                    fichiers.append(os.path.join(d, f))
    for f in sorted(os.listdir(os.path.join(moteur, "src", "cards"))):
        if f.endswith(".py"):
            fichiers.append(os.path.join(moteur, "src", "cards", f))
    fichiers.append(os.path.join(moteur, "src", "cards", "pack", "__init__.py"))
    for chemin in fichiers:
        try:
            arbre = ast.parse(lire(chemin))
        except Exception:
            continue
        rel = os.path.relpath(chemin, os.path.join(moteur, "src")).replace("\\", "/")
        lignes = []

        def signature(fn):
            a = fn.args
            morceaux = []
            nb_def = len(a.defaults)
            pos = [x for x in a.args if x.arg not in ("self", "cls")]
            for i, x in enumerate(pos):
                idx_def = i - (len(a.args) - nb_def) + (len(a.args) - len(pos))
                morceaux.append(x.arg)
            if a.vararg:
                morceaux.append("*" + a.vararg.arg)
            for x in a.kwonlyargs:
                morceaux.append(x.arg + "=")
            if a.kwarg:
                morceaux.append("**" + a.kwarg.arg)
            return "(" + ", ".join(morceaux) + ")"

        def doc(n):
            d = ast.get_docstring(n) or ""
            d = d.strip().split("\n")[0].strip()
            return (" — " + d[:150]) if d else ""

        def parcourir(corps, niveau, dans_classe):
            for n in corps:
                if isinstance(n, ast.ClassDef):
                    lignes.append("%s- **class `%s`**%s" % ("  " * niveau, n.name, doc(n)))
                    parcourir(n.body, niveau + 1, True)
                elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if n.name.startswith("_") and not n.name.startswith("__init__"):
                        continue
                    if n.name == "__init__":
                        continue
                    lignes.append("%s- `%s%s`%s" % ("  " * niveau, n.name, signature(n), doc(n)))

        parcourir(arbre.body, 0, False)
        if lignes:
            sortie.append("## `%s`" % rel)
            sortie.extend(lignes)
            sortie.append("")
            total += len(lignes)
    sortie.insert(3, "%d entrees." % total)
    return "\n".join(sortie)


def charger(nom, chemin):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def construire(racine, kit, zip_path):
    moteur = os.path.join(racine, "Fusion", "marvel-lcg-src")
    outils = os.path.join(racine, "outils")
    tmp = tempfile.mkdtemp(prefix="kit-campagne-")
    z = Zip(zip_path)
    base = "KIT-CAMPAGNE-IA/"

    # --- 1. le manuel et ses annexes de tete
    z.ajouter_texte(base + "LISEZ-MOI.md", lire(os.path.join(kit, "LISEZ-MOI.md")))
    z.ajouter_texte(base + "KIT-CAMPAGNE-COMPLET.md", lire(os.path.join(kit, "KIT-CAMPAGNE-COMPLET.md")))
    liste = lire(os.path.join(kit, "parties", "03-liste-des-fichiers.md")).lstrip("-\n ")
    z.ajouter_texte(base + "LISTE-DES-FICHIERS.md", "# La liste maitresse des fichiers d'une campagne\n\n" + liste)

    # --- 2. le verificateur et sa reference
    z.ajouter_fichier(os.path.join(outils, "verifier-livraison-campagne.py"), base + "verifier-livraison-campagne.py")
    ref = os.path.join(tmp, "reference")
    r = subprocess.run([sys.executable, os.path.join(outils, "verifier-livraison-campagne.py"), "--generer-reference", moteur, ref],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("reference : " + r.stderr)
    for f in sorted(os.listdir(ref)):
        z.ajouter_fichier(os.path.join(ref, f), base + "reference/" + f)

    # --- 3. les modeles (livraisons reconstituees)
    liv = charger("livraison_depuis_le_depot", os.path.join(outils, "livraison-depuis-le-depot.py"))
    for dossier, pack, code, officiel, images in MODELES:
        sortie = os.path.join(tmp, "liv-" + pack)
        with contextlib.redirect_stdout(io.StringIO()):
            liv.construire(pack, code, sortie, officiel)
        n = z.ajouter_arbre(sortie, base + "modeles/" + dossier + "/livraison")
        for rel in images:
            src = os.path.join(moteur, *rel.split("/"))
            z.ajouter_fichier(src, base + "modeles/" + dossier + "/images-exemples/" + rel.replace("/", "__"))
        manifeste = []
        for sous in ("assets/pics", "public/stories/" + code):
            d = os.path.join(moteur, *sous.split("/"))
            if os.path.isdir(d):
                if sous == "assets/pics":
                    continue
                for f in sorted(os.listdir(d)):
                    manifeste.append("%s/%s (%d Ko)" % (sous, f, os.path.getsize(os.path.join(d, f)) // 1024))
        z.ajouter_texte(base + "modeles/" + dossier + "/README.md",
                        "# Modele %s\n\nLivraison reconstituee depuis le depot (`outils/livraison-depuis-le-depot.py`) : %d fichiers "
                        "sous `livraison/`. Les fichiers de suivi (`MANIFESTE.md`, `CARNET-CLES.md`, `images.md`...) sont "
                        "GENERES : ils montrent la forme attendue, ils ne sont pas relus par un humain.\n\n"
                        "`images-exemples/` : quelques vraies images (nom = chemin du depot, `/` remplace par `__`) pour fixer les formats.\n\n"
                        "## Pages de livret de cette campagne dans le depot (`public/stories/%s/`)\n\n%s\n"
                        % (dossier, n, code, "\n".join("- " + m for m in manifeste) or "(aucune)"))

    # --- 4. la vraie livraison d'une autre IA (Hunting Season)
    hs = os.path.join(racine, ".planning", "hunting-season")
    pref = base + "modeles/C-livraison-exemple-hunting-season/"
    for f in ("LIRE_D_ABORD.md", "PROMPT_POUR_CLAUDE.md", "SPECIFICATIONS.md", "POINTS_OUVERTS.md", "VERIFICATION.json"):
        z.ajouter_fichier(os.path.join(hs, f), pref + f)
    z.ajouter_arbre(os.path.join(hs, "integration"), pref + "integration")
    for f in ("campaign_log_contract.json", "campaign_rules.py", "card_manifest.json", "booklet_extracted.txt"):
        z.ajouter_fichier(os.path.join(hs, "reference", f), pref + "reference/" + f)

    # --- 5. les douze campaign.py
    lignes = ["# Les douze `campaign.py` du jeu", "", "| Campagne | Fichier | Lignes |", "|---|---|---|"]
    for pack, rel in CAMPAIGN_PY:
        src = os.path.join(moteur, "src", "cards", "pack", *rel.split("/"))
        if z.ajouter_fichier(src, base + "modeles/D-patrons-de-campaign-py/%s/%s" % (pack, os.path.basename(rel))):
            lignes.append("| %s | `src/cards/pack/%s` | %d |" % (pack, rel, lire(src).count("\n") + 1))
    z.ajouter_texte(base + "modeles/D-patrons-de-campaign-py/README.md", "\n".join(lignes) + "\n\nVoir le §13.4 du manuel : ce que chacun apprend.\n")

    # --- 6. les fichiers communs
    for groupe, fichiers in COMMUN.items():
        for rel in fichiers:
            src = os.path.join(moteur, *rel.split("/"))
            z.ajouter_fichier(src, base + "commun/%s/%s" % (groupe, rel))
    plateau = os.path.join(racine, "ui-app", "src", "board", "campagne")
    z.ajouter_arbre(plateau, base + "commun/plateau/ui-app/src/board/campagne", filtre=lambda r: ".test." not in r)

    # --- 7. les annexes
    for src, dest in ANNEXES:
        chemin = os.path.join(racine, *src.split("/"))
        if os.path.isfile(chemin):
            # les liens de session d'un autre outil n'ont rien a faire dans un kit destine a une autre IA
            texte = re.sub(r"[^\n]*Claude-Session:[^\n]*\n?", "", lire(chemin))
            z.ajouter_texte(base + dest, texte)
    z.ajouter_arbre(os.path.join(racine, "docs", "reference", "mots-cles"), base + "annexes/C-mots-cles")
    z.ajouter_arbre(os.path.join(racine, ".planning", "codebase"), base + "annexes/J2-carte-du-code-juillet")
    z.ajouter_texte(base + "annexes/I-index-api-moteur.md", index_api(moteur))
    z.ajouter_fichier(os.path.join(kit, "ARCHITECTURE-ET-CODE.md"), base + "annexes/J-architecture-et-code.md")

    # --- 8. garde-fou : aucun secret dans ce qu'on donne a une autre IA
    trouves = []
    for nom, contenu in z.texte:
        if nom.endswith(("reference/prefixes-pris.json",)):
            continue
        for motif in SECRETS:
            m = re.search(motif, contenu)
            if m:
                trouves.append("%s : %s" % (nom, m.group(0)[:60]))
    z.fermer()
    shutil.rmtree(tmp, ignore_errors=True)
    if trouves:
        print("ATTENTION : motifs de secret trouves (le zip est ecrit mais NE DOIT PAS etre donne tel quel) :")
        for t in trouves[:40]:
            print("  ", t)
        raise SystemExit(1)
    taille = os.path.getsize(zip_path)
    print("%s : %d fichiers, %.1f Mo (aucun secret detecte)" % (zip_path, len(z.noms), taille / 1e6))
