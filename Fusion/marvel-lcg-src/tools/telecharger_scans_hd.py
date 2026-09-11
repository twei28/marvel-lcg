"""Les scans HAUTE DEFINITION des heros et des mechants, pour la scene de l'assistant.

POURQUOI (08/09/2026, « augmenter la resolution de l'image a la selection du
personnage et du mechant »)
---------------------------------------------------------------------------
La scene de l'assistant etire le scan du heros ou du mechant sur un panneau de
plus de 1 000 px. Le scan anglais local n'y fait que 300 px de large : etire
presque quatre fois, il est flou. Les serveurs d'images deja configures dans
launch.json (image_servers) servent les cartes officielles a 715 px.

CE QUE FAIT L'OUTIL
-------------------
Lit data/cards.json, retient les cartes de type Hero, AlterEgo, Villain et
MainScheme dont l'identifiant est OFFICIEL (cinq chiffres et une lettre), et
telecharge dans assets/pics-hd/ celles qui n'y sont pas encore. Le moteur sert
ces fichiers sous /hd/<nom> et retombe sur le scan habituel a defaut
(Cache.LoadImageHD) : l'outil n'est qu'une avance sur ce que le moteur ferait
de lui-meme, carte par carte, a la premiere demande.

⚠ INCREMENTAL et POLI : ce qui est deja la n'est pas redemande, quatre
telechargements a la fois, pas plus. Un echec ne bloque pas les autres.

⚠ TOURNE SUR LE SERVEUR a chaque deploiement (deployer.ps1), apres les
vignettes : les scans HD ne voyagent pas dans l'archive.

    python3 tools/telecharger_scans_hd.py            # telecharge ce qui manque
    python3 tools/telecharger_scans_hd.py --etat     # compte, sans rien telecharger
    python3 tools/telecharger_scans_hd.py --redresser  # n'echange que les faces croisees

⚠ FACES CROISEES (11/09/2026). Les serveurs d'images suivent la lettre
IMPRIMEE au coin de la carte, et sur dix identites (Groot, Rocket, et toute
la vague X-Men) FFG imprime l'alter ego en « 1A » : le scan HD telecharge
sous `a` etait l'alter ego, et la scene montrait Logan pour Wolverine. Apres
chaque telechargement (et seul, avec --redresser), l'outil compare chaque
paire a/b au scan habituel de assets/pics/ et echange les fichiers croises.
Logique dans src/engine/lib/faces_hd.py, partagee avec le moteur ; chargee
par son chemin pour ne pas tirer tout le moteur.
"""
import importlib.util
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor

import requests

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CARTES = os.path.join(RACINE, "data", "cards.json")
REFERENCE = os.path.join(RACINE, "assets", "pics")
FACES_HD = os.path.join(RACINE, "src", "engine", "lib", "faces_hd.py")
LANCEMENT = os.path.join(RACINE, "launch.json")
DESTINATION = os.path.join(RACINE, "assets", "pics-hd")
TYPES = {"Hero", "AlterEgo", "Villain", "MainScheme"}
OFFICIEL = re.compile(r"^\d{5}[a-z]?$")
# En dessous, ce n'est pas un scan HD (marvelcdb rend 300 px en ~40 Ko).
TAILLE_MIN = 60_000
ENTETES = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


def serveurs() -> list[str]:
    try:
        with open(LANCEMENT, encoding="utf-8") as f:
            return list(json.load(f).get("image_servers") or [])
    except (OSError, ValueError):
        return []


def identifiants() -> list[str]:
    with open(CARTES, encoding="utf-8") as f:
        packs = json.load(f)
    vus = set()
    for cartes in packs.values():
        # Certaines entrees de cards.json ne sont pas des listes de cartes
        # (chaines, listes de noms) : on ne retient que les vraies cartes.
        if not isinstance(cartes, list):
            continue
        for carte in cartes:
            if not isinstance(carte, dict) or carte.get("type") not in TYPES:
                continue
            pic = str(carte.get("pic_id") or carte.get("card_id") or "")
            if OFFICIEL.match(pic):
                vus.add(pic)
    return sorted(vus)


def manquants() -> list[str]:
    return [i for i in identifiants() if not os.path.exists(os.path.join(DESTINATION, i + ".jpg"))]


def telecharger(pic: str, sites: list[str]) -> str | None:
    """Rend None si un scan HD a ete garde, sinon la raison."""
    for site in sites:
        url = site.replace("{card_id}", pic).replace("{card_id:U}", pic.upper())
        try:
            r = requests.get(url, headers=ENTETES, timeout=10)
            if r.status_code != 200 or "image/" not in (r.headers.get("Content-Type") or ""):
                continue
            if len(r.content) < TAILLE_MIN:
                continue
            tmp = os.path.join(DESTINATION, pic + ".jpg.tmp")
            with open(tmp, "wb") as f:
                f.write(r.content)
            os.replace(tmp, os.path.join(DESTINATION, pic + ".jpg"))
            return None
        except requests.RequestException as exc:
            derniere = f"{pic} : {exc}"
            continue
    return f"{pic} : aucun serveur ne rend de scan HD"


def redresser_faces_croisees() -> int:
    """Echange les paires a/b croisees dans DESTINATION. Rend le nombre echange."""
    spec = importlib.util.spec_from_file_location("faces_hd", FACES_HD)
    faces_hd = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(faces_hd)
    try:
        echangees = faces_hd.redresser(DESTINATION, REFERENCE, faces_hd.identifiants_heros_de(CARTES))
    except ImportError as exc:
        print(f"faces croisees : non verifiees ({exc})", file=sys.stderr)
        return 0
    for a, b in echangees:
        print(f"  faces croisees redressees : {a} <-> {b}")
    print(f"faces croisees : {len(echangees)} paire(s) redressee(s)")
    return len(echangees)


def main(arguments: list[str]) -> int:
    if "--redresser" in arguments:
        redresser_faces_croisees()
        return 0
    liste = manquants()
    if "--etat" in arguments:
        deja = len(os.listdir(DESTINATION)) if os.path.isdir(DESTINATION) else 0
        print(f"scans HD presents : {deja}   a telecharger : {len(liste)}   dans {DESTINATION}")
        return 0
    sites = serveurs()
    if not sites:
        print("aucun image_servers dans launch.json : rien a telecharger.", file=sys.stderr)
        return 0
    if not liste:
        print("scans HD : rien a faire, tout est la.")
        redresser_faces_croisees()
        return 0
    os.makedirs(DESTINATION, exist_ok=True)
    echecs = []
    faits = 0
    with ThreadPoolExecutor(max_workers=4) as pool:
        for resultat in pool.map(lambda p: telecharger(p, sites), liste):
            faits += 1
            if resultat:
                echecs.append(resultat)
            if faits % 50 == 0:
                print(f"  {faits}/{len(liste)}...", flush=True)
    print(f"scans HD : {faits - len(echecs)} telecharges, {len(echecs)} sans HD, dans {DESTINATION}")
    for e in echecs[:10]:
        print("  ", e, file=sys.stderr)
    redresser_faces_croisees()
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
