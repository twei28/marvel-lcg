"""Assemble le ZIP du kit de creation de HEROS (20/10/2026). Appele par `construire-kit-heros.py`.

Tout vient du depot : rien n'est ecrit a la main ici hors du squelette. Garde-fou final : une recherche de secrets
(cle privee, adresse du serveur, mot de passe) dans TOUT ce qui entre dans le zip ; elle fait echouer la construction.
Les briques communes (classe `Zip`, index de l'API, liste des secrets) sont celles du kit de campagne.
"""
import contextlib
import importlib.util
import io
import os
import re
import shutil
import subprocess
import sys
import tempfile

ICI = os.path.dirname(os.path.abspath(__file__))


def charger(nom, fichier):
    spec = importlib.util.spec_from_file_location(nom, os.path.join(ICI, fichier))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[nom] = mod
    spec.loader.exec_module(mod)
    return mod


ZC = charger("zip_kit_campagne", "zip_kit_campagne.py")

# (dossier dans le zip, pack, deck de depart, officiel, identifiants dont on copie l'image)
MODELES = [
    ("A-officiel-ant-man", "ant", "ant_man", True, ["12001a", "12001b", "12001c", "12002", "12011"]),
    ("B-maison-lockjaw", "lockjaw", "lockjaw", False, ["lj001a", "lj001b", "lj002", "lj003", "lj013", "lj014", "lj015"]),
    ("C-maison-harry-osborn", "harry_osborn", "harry_osborn", False, ["ho001a", "ho001b", "ho002"]),
    ("D-officiel-recent-iron-fist", "iron_fist", "iron_fist", True, ["64001a", "64001b", "64002", "64004"]),
]

COMMUN = {
    "moteur": [
        "src/game/player/element/player_setup.py", "src/game/scene/loader.py", "src/game/scene/replay/hero.py",
        "src/engine/file/manager.py", "src/game/card/factory.py", "src/game/ability/factory/setup.py",
        "src/game/card/face/card_face.py", "src/game/card/face/card_type/identity.py",
        "src/game/card/face/card_type/obligation.py", "src/game/card/face/card_type/minion.py",
        "src/game/puzzle/puzzle.py", "src/cards/pack/__init__.py",
    ],
    "lanceur": [
        "public/js/prepare/catalog.js", "public/js/prepare/auteur.js", "public/js/prepare/variantes.js",
        "public/js/deckbuilder/regles.js",
    ],
    "outils": [
        "tools/verifier_tous_les_decks.py", "tools/substituer_pack.py", "tools/verifier_prefixes.py",
        "tools/verifier_appels_modules.py", "tools/recalculer_checksums.py", "tools/prefixes_fanmade.json",
        "tools/cas/iron_fist.py", "tools/cas/dazzler.py",
    ],
}

ANNEXES = [
    ("docs/reference/KIT-CHATGPT-CREATION.md", "annexes/A-kit-cartes.md"),
    ("docs/reference/RECETTES-MOTEUR.md", "annexes/B-recettes-moteur.md"),
    ("docs/reference/MOTS-CLES-TOUS.md", "annexes/C-mots-cles-tous.md"),
    ("docs/reference/PROCESSUS-CARTE.md", "annexes/D-processus-carte.md"),
    ("docs/reference/PROCESSUS-HEROS.md", "annexes/D-processus-heros.md"),
    ("docs/reference/GUIDE-CREATION-CONTENU.md", "annexes/E-guide-creation-contenu.md"),
    ("docs/kit-campagne-ia/KIT-CAMPAGNE-COMPLET.md", "annexes/L-manuel-campagne-cartes-et-scripts.md"),
    ("docs/packs/iron_fist_cartes.md", "annexes/M-gabarits-iron-fist.md"),
]

QUESTIONS_IRON_FIST = [".planning/iron-fist-officiel/creation-questions.md", ".planning/iron-fist-officiel/lecture-reponses.md"]


def lire(chemin):
    with io.open(chemin, encoding="utf-8", newline="") as f:
        return f.read()


def extraits_harnais(moteur):
    """Du harnais de cas (3 Mo, trop gros pour un zip) : la liste des cles d'`attendu` et le verificateur generique."""
    lignes = lire(os.path.join(moteur, "tools", "test_capacites.py")).replace("\r\n", "\n").split("\n")
    i0 = next(i for i, l in enumerate(lignes) if l.startswith("CLES_ETAT_ATTENDU = {"))
    i1 = next(i for i in range(i0, len(lignes)) if lignes[i].startswith("}"))
    j0 = next(i for i, l in enumerate(lignes) if l.startswith("def etat_attendu("))
    j1 = next((i for i in range(j0 + 1, len(lignes)) if lignes[i].startswith("def ")), len(lignes))
    return ("# Extraits de Fusion/marvel-lcg-src/tools/test_capacites.py (le fichier entier pese 3 Mo et ne vaut que pour Claude).\n"
            "# Ici : (1) les cles que `attendu` peut porter dans un cas qui n'a pas de verificateur propre ;\n"
            "# (2) le verificateur generique `etat_attendu` qui les lit. Une cle absente de la liste fait ECHOUER le cas.\n\n"
            + "\n".join(lignes[i0:i1 + 1]) + "\n\n\n" + "\n".join(lignes[j0:j1]).rstrip() + "\n")


def trouver_image(moteur, cid):
    for ext in ("png", "jpg", "jpeg", "webp"):
        p = os.path.join(moteur, "assets", "pics", "%s.%s" % (cid, ext))
        if os.path.isfile(p):
            return p
    return None


def construire(racine, kit, zip_path):
    moteur = os.path.join(racine, "Fusion", "marvel-lcg-src")
    outils = os.path.join(racine, "outils")
    tmp = tempfile.mkdtemp(prefix="kit-heros-")
    z = ZC.Zip(zip_path)
    base = "KIT-HEROS-IA/"

    # --- 1. le manuel et ses annexes de tete
    z.ajouter_texte(base + "LISEZ-MOI.md", lire(os.path.join(kit, "LISEZ-MOI.md")))
    z.ajouter_texte(base + "KIT-HEROS-COMPLET.md", lire(os.path.join(kit, "KIT-HEROS-COMPLET.md")))
    liste = lire(os.path.join(kit, "parties", "03-liste-des-fichiers.md")).lstrip("-\n ")
    z.ajouter_texte(base + "LISTE-DES-FICHIERS.md", "# La liste maitresse des fichiers d'un heros\n\n" + liste)

    # --- 2. le verificateur (il charge celui des campagnes a cote de lui) et sa reference
    z.ajouter_fichier(os.path.join(outils, "verifier-livraison-heros.py"), base + "verifier-livraison-heros.py")
    z.ajouter_fichier(os.path.join(outils, "verifier-livraison-campagne.py"), base + "verifier-livraison-campagne.py")
    ref = os.path.join(tmp, "reference")
    r = subprocess.run([sys.executable, os.path.join(outils, "verifier-livraison-heros.py"), "--generer-reference", moteur, ref],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("reference : " + r.stderr)
    for f in sorted(os.listdir(ref)):
        z.ajouter_fichier(os.path.join(ref, f), base + "reference/" + f)

    # --- 3. les modeles (livraisons reconstituees)
    liv = charger("livraison_heros_depuis_le_depot", "livraison-heros-depuis-le-depot.py")
    for dossier, pack, deck, officiel, images in MODELES:
        sortie = os.path.join(tmp, "liv-" + pack)
        with contextlib.redirect_stdout(io.StringIO()):
            liv.construire(pack, deck, sortie, officiel)
        n = z.ajouter_arbre(sortie, base + "modeles/" + dossier + "/livraison")
        vues = []
        for cid in images:
            src = trouver_image(moteur, cid)
            if src:
                z.ajouter_fichier(src, base + "modeles/" + dossier + "/images-exemples/" + os.path.basename(src))
                vues.append(os.path.basename(src))
        z.ajouter_texte(base + "modeles/" + dossier + "/README.md",
                        "# Modele %s\n\nLivraison reconstituee depuis le depot (`outils/livraison-heros-depuis-le-depot.py`) : %d fichiers "
                        "sous `livraison/`. Les fichiers de suivi (`MANIFESTE.md`, `images.md`...) sont GENERES : ils montrent la forme "
                        "attendue, ils ne sont pas relus par un humain.\n\n`images-exemples/` : quelques vraies images de cartes "
                        "(%s) pour fixer les formats (taille, orientation).\n\nVerification de cette livraison : "
                        "`python3 ../../verifier-livraison-heros.py livraison%s`.\n"
                        % (dossier, n, ", ".join(vues) or "aucune", " --officiel" if officiel else ""))
    pref = base + "modeles/E-questions-iron-fist/"
    for rel in QUESTIONS_IRON_FIST:
        z.ajouter_fichier(os.path.join(racine, *rel.split("/")), pref + os.path.basename(rel))
    z.ajouter_texte(pref + "README.md", "# Questions et decisions reelles : Iron Fist\n\n`creation-questions.md` : une question ouverte, "
                    "dans le format du chapitre 9.4 du manuel.\n`lecture-reponses.md` : les cinq decisions de l'utilisateur, prises une a "
                    "une, avec l'image de la carte. C'est la forme exacte de `QUESTIONS.md` une fois tranchee.\n")

    # --- 4. les fichiers communs
    for groupe, fichiers in COMMUN.items():
        for rel in fichiers:
            src = os.path.join(moteur, *rel.split("/"))
            z.ajouter_fichier(src, base + "commun/%s/%s" % (groupe, rel))
    z.ajouter_texte(base + "commun/outils/test_capacites.extraits.py", extraits_harnais(moteur))
    for nom in ("heros-info.js", "repliques-heros.js"):
        texte = lire(os.path.join(moteur, "public", "js", "prepare", nom)).replace("\r\n", "\n")
        z.ajouter_texte(base + "commun/lanceur/public/js/prepare/%s.entete.txt" % nom,
                        "// Les 70 premieres lignes de %s (le fichier entier est un registre partage : tu n'y livres qu'un fragment).\n\n%s\n"
                        % (nom, "\n".join(texte.split("\n")[:70])))

    # --- 5. les annexes
    for src, dest in ANNEXES:
        chemin = os.path.join(racine, *src.split("/"))
        if os.path.isfile(chemin):
            texte = re.sub(r"[^\n]*Claude-Session:[^\n]*\n?", "", lire(chemin))
            z.ajouter_texte(base + dest, texte)
    z.ajouter_arbre(os.path.join(racine, "docs", "reference", "mots-cles"), base + "annexes/C-mots-cles")
    z.ajouter_texte(base + "annexes/I-index-api-moteur.md", ZC.index_api(moteur))
    z.ajouter_fichier(os.path.join(racine, "docs", "kit-campagne-ia", "ARCHITECTURE-ET-CODE.md"), base + "annexes/J-architecture-et-code.md")

    # --- 6. garde-fou : aucun secret dans ce qu'on donne a une autre IA
    trouves = []
    for nom, contenu in z.texte:
        if nom.endswith(("reference/prefixes-pris.json",)):
            continue
        for motif in ZC.SECRETS:
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
