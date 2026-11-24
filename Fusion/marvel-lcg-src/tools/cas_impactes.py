#!/usr/bin/env python3
"""Quels cas de test rejouer apres CE changement ? (23/10/2026)

La batterie complete de `test_capacites.py` grossit avec chaque carte (8412 cas, environ 1 h 30). Cet outil lit le diff git et en
tire la liste des FILTRES a rejouer, pour ne lancer la batterie complete qu'a la veille d'un deploiement ou apres un changement
trop large. Il ne lance rien par lui-meme tant qu'on ne lui dit pas `--lancer`.

    python3 tools/cas_impactes.py                 # le travail non commite (index + arbre) contre HEAD
    python3 tools/cas_impactes.py --depuis main   # tout ce qui a change depuis `main`
    python3 tools/cas_impactes.py --lancer        # puis joue la selection (`.game-src`, ports 38000+, PARALLELES=4)

Regles (de la plus etroite a la plus large) :

  - `src/cards/pack/<pack>/.../<id>.py`   -> les cas de CETTE carte (filtre = l'identifiant)
  - `src/cards/pack/<pack>/__init__.py` ou un module commun du pack -> tous les cas du pack (les identifiants de ses modules)
  - `tools/cas/<fichier>.py`              -> les cas de ce fichier (filtres = ses prefixes `[xx]`)
  - `data/cards.json`                     -> les cartes dont l'entree a change (filtre = identifiant)
  - `src/game/**`, `src/engine/**`, `src/cards/*.py` (MOTEUR COMMUN) -> les cartes et les fichiers de cas qui UTILISENT les noms
    de fonctions / classes modifies (recherche du mot entier). Trop de cartes (plus de SEUIL_LARGE) ou aucun nom extractible
    (constante, import, decorateur...) : la verdict est BATTERIE COMPLETE.
  - `ui-app/**`, `docs/**`, `public/**`, `.planning/**`... : aucun cas moteur.

Un SUR-ENSEMBLE est sans danger (on rejoue un peu trop) ; un SOUS-ENSEMBLE ne l'est pas : en cas de doute l'outil elargit, jamais
l'inverse. La batterie complete reste la reference (regle de portee du §6bis du GUIDE) : elle est LA validation avant un deploiement.
"""
import argparse
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))          # Fusion/marvel-lcg-src
DEPOT = os.path.dirname(os.path.dirname(RACINE))                              # racine du depot git
SEUIL_LARGE = 400          # plus de cartes touchees que cela : autant jouer la batterie complete
# Noms trop courants pour designer une dependance : s'ils changent, on ne peut pas dire qui les utilise.
NOMS_BANALS = {"__init__", "Get", "Set", "Check", "Send", "Run", "Add", "Remove", "Find", "Cast", "Is", "Update"}


def git(*args):
    r = subprocess.run(["git", "-C", DEPOT, *args], capture_output=True, text=True)
    return r.stdout


def fichiers_changes(depuis):
    """(chemin relatif au depot, ...) des fichiers modifies, ajoutes ou supprimes."""
    if depuis:
        sortie = git("diff", "--name-only", depuis)
    else:
        sortie = git("diff", "--name-only", "HEAD") + git("diff", "--name-only", "--cached")
    return sorted({ligne for ligne in sortie.splitlines() if ligne})


def chemin_moteur(chemin):
    """Retire le prefixe `Fusion/marvel-lcg-src/` : les regles parlent en chemins du moteur."""
    pref = "Fusion/marvel-lcg-src/"
    return chemin[len(pref):] if chemin.startswith(pref) else None


def modules_de_cartes(pack_dir):
    """Identifiants (noms de fichiers sans .py) de tous les modules de cartes sous `src/cards/pack/<pack>/`."""
    ids = set()
    for dossier, _sous, fichiers in os.walk(pack_dir):
        for f in fichiers:
            if f.endswith(".py") and f != "__init__.py":
                ids.add(f[:-3])
    return ids


def noms_changes(chemin_depot, depuis):
    """Noms des FONCTIONS (ou classes) dont le corps a change : pour chaque ligne modifiee on remonte, dans le fichier, jusqu'au `def` qui la
    contient. (Les en-tetes de hunk de git donnent la CLASSE englobante, trop large : `Worlds` toucherait tout le moteur.)
    Une ligne hors de toute fonction (constante, import, attribut de classe) rend `None` dans l'ensemble : l'appelant elargit."""
    diff = git("diff", "-U0", *(["HEAD"] if not depuis else [depuis]), "--", chemin_depot)
    try:
        lignes = open(os.path.join(DEPOT, chemin_depot), encoding="utf-8").read().split("\n")
    except OSError:
        return {None}
    noms = set()
    for ligne in diff.splitlines():
        m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", ligne)
        if not m:
            continue
        debut, nombre = int(m.group(1)), int(m.group(2) or "1")
        pour = range(debut, debut + max(nombre, 1))
        for n in pour:
            # Une ligne VIDE (ou un commentaire seul) ajoutee ou retiree ne change aucun comportement : elle ne designe aucune fonction.
            if 0 < n <= len(lignes) and (not lignes[n - 1].strip() or lignes[n - 1].lstrip().startswith("#")):
                continue
            nom = None
            indent_ligne = len(lignes[n - 1]) - len(lignes[n - 1].lstrip()) if 0 < n <= len(lignes) else 0
            for k in range(min(n, len(lignes)) - 1, -1, -1):
                mm = re.match(r"^(\s*)(?:async\s+)?def\s+(\w+)", lignes[k])
                if mm and len(mm.group(1)) < max(indent_ligne, 1) + (1 if k == n - 1 else 0):
                    nom = mm.group(2)
                    break
            noms.add(nom)
    return noms


def utilisateurs(nom):
    """(identifiants de cartes, fichiers de cas) qui contiennent ce nom comme MOT ENTIER."""
    ids, fichiers_cas = set(), set()
    for racine, cible in (("src/cards", ids), ("tools/cas", fichiers_cas)):
        r = subprocess.run(["grep", "-rlw", "--include=*.py", nom, os.path.join(RACINE, racine)], capture_output=True, text=True)
        for chemin in r.stdout.splitlines():
            if cible is ids:
                base = os.path.basename(chemin)[:-3]
                if base == "__init__":
                    ids |= modules_de_cartes(os.path.dirname(chemin))
                else:
                    ids.add(base)
            else:
                fichiers_cas.add(chemin)
    return ids, fichiers_cas


def prefixes_du_fichier_de_cas(chemin):
    """Les prefixes `[xx]` des noms de cas d'un fichier de `tools/cas/` (par defaut leur nom de fichier)."""
    texte = open(chemin, encoding="utf-8").read()
    pref = set(re.findall(r'"\[([a-z0-9_]+)\]\s', texte)) | set(re.findall(r"'\[([a-z0-9_]+)\]\s", texte))
    pref |= set(re.findall(r'^PREFIXE\s*=\s*["\'](\[[a-z0-9_]+\])', texte, re.M))
    return {p if p.startswith("[") else f"[{p}]" for p in pref}


def cartes_modifiees_dans_cards_json(depuis):
    """Identifiants des entrees de `cards.json` ajoutees ou changees (lecture du diff, pas du fichier entier)."""
    diff = git("diff", "-U8", *(["HEAD"] if not depuis else [depuis]), "--", "Fusion/marvel-lcg-src/data/cards.json")
    ids, courant = set(), None
    for ligne in diff.splitlines():
        m = re.search(r'"card_id":\s*"([^"]+)"', ligne)
        if m:
            courant = m.group(1)
        if ligne[:1] in "+-" and not ligne.startswith(("+++", "---")) and '"checksum"' not in ligne:
            if courant:
                ids.add(courant)
    return ids


def selectionner(depuis):
    """-> (filtres: set[str], complete: bool, raisons: list[str])"""
    filtres, raisons, complete = set(), [], False
    for chemin in fichiers_changes(depuis):
        rel = chemin_moteur(chemin)
        if rel is None:
            continue
        if rel.startswith("src/cards/pack/"):
            parts = rel.split("/")
            if len(parts) >= 4 and parts[-1] != "__init__.py" and parts[-1].endswith(".py"):
                filtres.add(parts[-1][:-3])
                raisons.append(f"{rel} -> carte {parts[-1][:-3]}")
            elif len(parts) >= 4:
                pack_dir = os.path.join(RACINE, *parts[:4])
                ids = modules_de_cartes(pack_dir)
                filtres |= ids
                raisons.append(f"{rel} (commun au pack) -> {len(ids)} cartes de {parts[3]}")
        elif rel.startswith("tools/cas/") and rel.endswith(".py"):
            pref = prefixes_du_fichier_de_cas(os.path.join(RACINE, rel))
            if pref:
                filtres |= pref
                raisons.append(f"{rel} -> prefixes {sorted(pref)}")
            else:
                complete = True
                raisons.append(f"{rel} : prefixes introuvables -> BATTERIE COMPLETE")
        elif rel == "data/cards.json":
            ids = cartes_modifiees_dans_cards_json(depuis)
            filtres |= ids
            raisons.append(f"data/cards.json -> {len(ids)} entrees changees")
        elif rel.startswith(("src/game/", "src/engine/", "src/core/")) or re.match(r"src/cards/[^/]+\.py$", rel):
            noms = noms_changes(chemin, depuis)
            if None in noms:
                complete = True
                raisons.append(f"{rel} : une modification hors de toute fonction (constante, import...) -> BATTERIE COMPLETE")
                continue
            if not noms:
                complete = True
                raisons.append(f"{rel} : aucun nom de fonction extractible -> BATTERIE COMPLETE")
                continue
            banals = noms & NOMS_BANALS
            if banals:
                complete = True
                raisons.append(f"{rel} : nom trop courant {sorted(banals)} -> BATTERIE COMPLETE")
                continue
            ids_tous, fichiers_tous = set(), set()
            for nom in sorted(noms):
                ids, fichiers = utilisateurs(nom)
                ids_tous |= ids
                fichiers_tous |= fichiers
            if len(ids_tous) > SEUIL_LARGE:
                complete = True
                raisons.append(f"{rel} : {len(ids_tous)} cartes touchees (> {SEUIL_LARGE}) -> BATTERIE COMPLETE")
                continue
            filtres |= ids_tous
            for f in fichiers_tous:
                filtres |= prefixes_du_fichier_de_cas(f)
            raisons.append(f"{rel} : {sorted(noms)} -> {len(ids_tous)} cartes, {len(fichiers_tous)} fichiers de cas")
        # tout le reste (interface, docs, donnees non cartes) : aucun cas moteur
    return filtres, complete, raisons


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--depuis", default="", help="reference git (defaut : le travail non commite contre HEAD)")
    ap.add_argument("--lancer", action="store_true", help="joue la selection (sinon, affiche seulement)")
    ap.add_argument("--port", type=int, default=38000)
    a = ap.parse_args()

    filtres, complete, raisons = selectionner(a.depuis)
    for r in raisons:
        print("  ·", r)
    if complete:
        print("\n=> BATTERIE COMPLETE : python3.10 tools/test_capacites.py .game-src <port> <rapport>")
        return 2
    if not filtres:
        print("\n=> Aucun cas moteur a rejouer (le changement ne touche ni cartes, ni moteur, ni cas).")
        return 0
    liste = sorted(filtres)
    print(f"\n=> {len(liste)} filtres a rejouer : {', '.join(liste[:12])}{' ...' if len(liste) > 12 else ''}")
    if not a.lancer:
        print("   (ajouter --lancer pour les jouer ; le filtre `a|b|c` est accepte par test_capacites.py)")
        return 0
    env = dict(os.environ, PARALLELES=os.environ.get("PARALLELES", "4"), CAS_PREFIX="imp_")
    rapport = "/tmp/cas_impactes_rapport.json"
    python = os.environ.get("PYTHON") or os.path.expanduser("~/.marvel-venv/bin/python")   # le moteur exige Python 3.10 (pas celui du systeme)
    cmd = [python, os.path.join(RACINE, "tools", "test_capacites.py"), ".game-src", str(a.port), rapport, "|".join(liste)]
    return subprocess.call(cmd, cwd=RACINE, env=env)


if __name__ == "__main__":
    sys.exit(main())
