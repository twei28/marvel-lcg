"""Construit l'export ZIP de TOUTES les images de cartes (27/10/2026).

Fonction d'administration : le bouton « 📦 Export ZIP cartes » de l'ecran de
preparation (public/js/prepare/lien-admin.js) lance ce script EN TACHE DE FOND
(route `/post_export_cartes_regenerer`, server_get.py), puis sert le fichier
deja pret (`/telecharger_export_cartes`). Il se lance aussi a la main :

    python3 tools/exporter_images_cartes.py                       # tout le catalogue
    python3 tools/exporter_images_cartes.py --packs the_hunger_core
    python3 tools/exporter_images_cartes.py --sans-voile          # en/ et fr/ seulement

Le ZIP (assets/export-cartes/cartes-images.zip) a trois dossiers :

  en/           le scan anglais de chaque carte : celui du jeu (assets/pics,
                textures, assets/cache), sinon telecharge une fois depuis les
                serveurs d'images du moteur (`image_servers` : cerebro puis
                marvelcdb) et range dans assets/cache, comme le fait le moteur.
  fr/           le scan francais OFFICIEL quand il existe (assets/pics-fr,
                importe par tools/importer_scans_fr.py depuis le pack OCTGN FR
                et mc4db). Incomplet PAR NATURE : le fan-made n'a pas de scan FR.
  en_voile_fr/  le scan anglais avec le voile FR du plateau, pour toute carte
                dont le site connait le texte francais. Rendu par le composant
                MEME du plateau (ui-app/src/board/TraductionPosee.tsx) dans un
                Chromium sans ecran : ui-app/outils/export-voile/rendre-voile.mjs.

⚠ LE VOILE DEMANDE NODE, ui-app/node_modules ET PLAYWRIGHT (ui-check). Sans eux
(cas du serveur de production, qui n'a ni Node ni ui-app), le dossier est
rempli depuis le cache des rendus deja faits (assets/export-cartes/voile-cache),
pour les cartes dont le scan n'a pas change ; les autres manquent, et
LISEZMOI.txt le dit.

⚠ UNE SEULE GENERATION A LA FOIS : verrou `generation.lock` (pid dedans). Un
verrou dont le processus est mort est repris.

⚠ RIEN N'EST TELECHARGE DEUX FOIS : un scan recupere est garde dans
assets/cache ; un echec est note dans absents.json et n'est retente qu'apres
ABSENT_RETENTE_JOURS. Une requete par DELAI_TELECHARGEMENT secondes au plus.
"""

import argparse
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
import traceback
import zipfile
from pathlib import Path

MOTEUR = Path(__file__).resolve().parents[1]
RACINE = MOTEUR.parents[1]
UI_APP = RACINE / "ui-app"
RENDU_VOILE = UI_APP / "outils" / "export-voile" / "rendre-voile.mjs"

SORTIE = MOTEUR / "assets" / "export-cartes"
NOM_ZIP = "cartes-images.zip"
VERROU = "generation.lock"
ETAT = "etat.json"
JOURNAL = "journal.txt"

DELAI_TELECHARGEMENT = 1.5      # secondes entre deux requetes aux serveurs d'images
ABSENT_RETENTE_JOURS = 7
EXTENSIONS = (".webp", ".jpg", ".png")   # ordre de Cache.LoadImage
CODE_OFFICIEL = re.compile(r"^\d{5}[a-z]?$")
# Meme filtre que `codeCarteConnu` (ui-app/src/board/marvelcdb.ts) : le plateau ne
# traduit aucune autre carte, l'export non plus.
CODE_TRADUISIBLE = re.compile(r"^(\d{5}[a-z]?|[a-z]{2}\d{3}[a-z]?)$")
ENTETES = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                         "(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


# --------------------------------------------------------------------------- #
# Verrou et etat
# --------------------------------------------------------------------------- #

def processus_vivant(pid) -> bool:
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def lire_verrou(dossier: Path):
    """Le contenu du verrou s'il est TENU (processus vivant), sinon None."""
    chemin = dossier / VERROU
    try:
        info = json.loads(chemin.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except Exception:
        info = {}
    if processus_vivant(info.get("pid")):
        return info
    return None


def prendre_verrou(dossier: Path, info: dict) -> bool:
    """Cree le verrou atomiquement. Faux s'il est tenu par un processus vivant."""
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / VERROU
    for _ in range(2):
        try:
            fd = os.open(str(chemin), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            if lire_verrou(dossier) is not None:
                return False
            # Verrou orphelin (processus mort) : on le reprend.
            try:
                chemin.unlink()
            except FileNotFoundError:
                pass
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(info, f)
        return True
    return False


def ecrire_json_atomique(chemin: Path, donnees) -> None:
    provisoire = chemin.with_suffix(chemin.suffix + ".tmp")
    provisoire.write_text(json.dumps(donnees, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(provisoire, chemin)


class Etat:
    """etat.json, lu par la route d'etat pour l'ecran de l'administrateur."""

    def __init__(self, dossier: Path, packs):
        self.chemin = dossier / ETAT
        self.donnees = {
            "en_cours": True,
            "pid": os.getpid(),
            "debut": time.time(),
            "fin": None,
            "packs": packs or None,
            "phase": "catalogue",
            "fait": 0,
            "total": 0,
            "message": "Lecture du catalogue",
            "resultat": None,
            "erreur": None,
        }
        self._dernier = 0.0
        self.ecrire(force=True)

    def ecrire(self, force=False, **champs):
        self.donnees.update(champs)
        maintenant = time.time()
        if force or maintenant - self._dernier >= 1.0:
            self._dernier = maintenant
            ecrire_json_atomique(self.chemin, self.donnees)


# --------------------------------------------------------------------------- #
# Catalogue
# --------------------------------------------------------------------------- #

def lire_config(chemin: Path) -> dict:
    try:
        return json.loads(chemin.read_text(encoding="utf-8"))
    except Exception:
        return {}


def charger_catalogue(fichiers, packs_voulus):
    """Toutes les cartes connues du jeu, une fois chacune, dans l'ordre des fichiers.

    Memes fichiers que /get_cards_json (cards.json, puis les fichiers custom).
    Une carte presente deux fois garde sa premiere fiche, comme la fusion du
    plateau ; `pack` est la cle de paquet du fichier (« the_hunger_core »).
    """
    cartes = {}
    for chemin in fichiers:
        donnees = json.loads(Path(chemin).read_text(encoding="utf-8"))
        for pack, liste in donnees.items():
            if not isinstance(liste, list):
                continue
            if packs_voulus and pack not in packs_voulus:
                continue
            for fiche in liste:
                code = str(fiche.get("card_id") or "").strip()
                if not code or code in cartes:
                    continue
                cartes[code] = {
                    "code": code,
                    "pack": pack,
                    "nom": fiche.get("name") or "",
                    "type": fiche.get("type") or "",
                    "pic_id": fiche.get("pic_id") or "",
                    "full_link": fiche.get("full_link") or "",
                }
    return cartes


def chercher_fichier(dossiers, nom: str):
    for dossier in dossiers:
        for ext in EXTENSIONS:
            chemin = Path(dossier) / f"{nom}{ext}"
            if chemin.is_file():
                return chemin
    return None


def noms_candidats(carte):
    """Le fichier de la carte d'abord, puis l'image qu'elle emprunte (pic_id, reimpression)."""
    noms = [carte["code"]]
    for autre in (carte["pic_id"], carte["full_link"]):
        if autre and autre not in noms:
            noms.append(autre)
    return noms


# --------------------------------------------------------------------------- #
# Telechargements (scans anglais absents du disque)
# --------------------------------------------------------------------------- #

class Telechargeur:
    def __init__(self, serveurs, cache: Path, absents_fichier: Path, journal):
        self.serveurs = list(serveurs)
        self.cache = cache
        self.absents_fichier = absents_fichier
        self.journal = journal
        try:
            self.absents = json.loads(absents_fichier.read_text(encoding="utf-8"))
        except Exception:
            self.absents = {}
        self._derniere = 0.0
        self.faits = 0
        self.echecs = 0

    def _attendre(self):
        reste = DELAI_TELECHARGEMENT - (time.time() - self._derniere)
        if reste > 0:
            time.sleep(reste)
        self._derniere = time.time()

    def recuperer(self, code: str):
        """Le chemin du scan telecharge (range dans assets/cache), ou None."""
        if not self.serveurs or not CODE_OFFICIEL.match(code):
            return None
        vu = self.absents.get(code)
        if vu and time.time() - vu < ABSENT_RETENTE_JOURS * 86400:
            return None
        import requests
        for site in self.serveurs:
            url = site.replace("{card_id}", code).replace("{card_id:U}", code.upper())
            self._attendre()
            try:
                reponse = requests.get(url, headers=ENTETES, timeout=10)
            except Exception as e:  # reseau coupe, delai : on passe au serveur suivant
                self.journal(f"telechargement {code} : {url} : {e}")
                continue
            type_contenu = reponse.headers.get("Content-Type") or ""
            if reponse.status_code != 200 or "image/" not in type_contenu:
                continue
            ext = "png" if "png" in type_contenu else "webp" if "webp" in type_contenu else "jpg"
            self.cache.mkdir(parents=True, exist_ok=True)
            chemin = self.cache / f"{code}.{ext}"
            chemin.write_bytes(reponse.content)
            self.faits += 1
            self.absents.pop(code, None)
            self.journal(f"telecharge {code} depuis {url}")
            return chemin
        self.echecs += 1
        self.absents[code] = time.time()
        return None

    def sauver(self):
        ecrire_json_atomique(self.absents_fichier, self.absents)


# --------------------------------------------------------------------------- #
# Voile FR
# --------------------------------------------------------------------------- #

def est_complot(type_carte: str) -> bool:
    """Meme regle que coteDuTexte(typeDeBoite(type)) du plateau : ces cartes se lisent couchees."""
    return type_carte == "MainScheme" or type_carte.endswith("SideScheme")


def image_orientee(chemin: Path, complot: bool, dossier_orientes: Path):
    """Le scan tel que le plateau le montre : (chemin, largeur, hauteur).

    Le serveur redresse tout scan paysage en portrait (ImageLib.TryRotateImage :
    EXIF, puis rotation de 90° anti-horaire) ; le plateau couche ensuite un
    complot de 90° dans le sens horaire. On fait les memes rotations ici, et on
    ne recopie le fichier que s'il change.
    """
    from PIL import Image, ImageOps
    with Image.open(chemin) as brute:
        orientation = brute.getexif().get(0x0112, 1)
        image = ImageOps.exif_transpose(brute) if orientation != 1 else brute.copy()
    rotation = 0
    largeur, hauteur = image.size
    if largeur > hauteur:
        rotation += 90
    if complot:
        rotation -= 90
    if rotation:
        image = image.rotate(rotation, expand=True)
    if orientation == 1 and rotation == 0:
        return chemin, image.size[0], image.size[1]
    dossier_orientes.mkdir(parents=True, exist_ok=True)
    sortie = dossier_orientes / f"{chemin.stem}-{'paysage' if complot else 'portrait'}.png"
    image.convert("RGB").save(sortie, "PNG")
    return sortie, image.size[0], image.size[1]


def node_disponible():
    node = shutil.which("node")
    if not node or not RENDU_VOILE.is_file() or not (UI_APP / "node_modules" / "vite").is_dir():
        return None
    return node


def rendre_voiles(travaux, dossier: Path, catalogues, paralleles, etat: Etat, journal):
    """Lance rendre-voile.mjs ; rend son resume (dict) ou None si Node manque."""
    node = node_disponible()
    if not node:
        journal("voile : Node, ui-app ou rendre-voile.mjs absent ; seul le cache des rendus sert")
        return None
    fichier_travail = dossier / "voile-travail.json"
    ecrire_json_atomique(fichier_travail, {
        "cache": str(dossier / "voile-cache"),
        "public": str(MOTEUR / "public"),
        "catalogues": [str(Path(c).resolve()) for c in catalogues],
        "paralleles": paralleles,
        "cartes": travaux,
    })
    resume = None
    etat.ecrire(force=True, phase="voile", fait=0, total=len(travaux), message="Rendu du voile FR")
    processus = subprocess.Popen([node, str(RENDU_VOILE), str(fichier_travail)], cwd=str(UI_APP),
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
    for ligne in processus.stdout:
        ligne = ligne.rstrip("\n")
        if ligne.startswith("PROGRES "):
            fait, _, total = ligne[8:].partition("/")
            etat.ecrire(fait=int(fait), total=int(total))
        elif ligne.startswith("FIN "):
            resume = json.loads(ligne[4:])
        elif ligne.strip():
            journal(f"voile : {ligne}")
    processus.wait()
    if processus.returncode != 0:
        journal(f"voile : rendre-voile.mjs s'est arrete avec le code {processus.returncode}")
    return resume


def sha1_fichier(chemin: Path) -> str:
    h = hashlib.sha1()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# --------------------------------------------------------------------------- #
# Generation
# --------------------------------------------------------------------------- #

def generer(args, etat: Etat, journal):
    config = lire_config(Path(args.config)) if args.config else {}
    os.chdir(MOTEUR)
    catalogues = args.catalogue or (
        [config.get("cards_json_file") or "./data/cards.json"]
        + list(config.get("cards_json_custom_files") or [])
        + ([config["cards_json_custom_file"]] if config.get("cards_json_custom_file") else [])
    )
    serveurs = args.serveur_images if args.serveur_images is not None else list(config.get("image_servers") or [])
    if args.sans_telechargement:
        serveurs = []
    packs = set(p.strip() for p in (args.packs or "").split(",") if p.strip())

    cartes = charger_catalogue(catalogues, packs)
    if packs and not cartes:
        raise SystemExit(f"aucune carte pour les paquets {sorted(packs)}")
    journal(f"catalogue : {len(cartes)} cartes ({', '.join(catalogues)})")

    dossiers_en = [MOTEUR / "assets" / "pics", MOTEUR / "assets" / "textures", MOTEUR / "assets" / "cache"]
    dossier_fr = [MOTEUR / "assets" / "pics-fr"]
    telechargeur = Telechargeur(serveurs, MOTEUR / "assets" / "cache", SORTIE / "absents.json", journal)

    # 1. Les scans anglais et francais, telechargement des manquants compris.
    etat.ecrire(force=True, phase="scans", fait=0, total=len(cartes), message="Recherche des scans")
    for i, carte in enumerate(cartes.values(), 1):
        en = None
        for nom in noms_candidats(carte):
            en = chercher_fichier(dossiers_en, nom)
            if en:
                break
        if en is None:
            for nom in noms_candidats(carte):
                en = telechargeur.recuperer(nom)
                if en:
                    break
        carte["en"] = en
        fr = None
        for nom in noms_candidats(carte):
            fr = chercher_fichier(dossier_fr, f"fr_{nom}")
            if fr:
                break
        carte["fr"] = fr
        etat.ecrire(fait=i, message=f"Recherche des scans ({telechargeur.faits} telecharges)")
    telechargeur.sauver()

    # 2. Le voile FR.
    dossier_orientes = SORTIE / "scans-orientes"
    travaux = []
    if not args.sans_voile:
        etat.ecrire(force=True, phase="voile-preparation", fait=0, total=len(cartes), message="Preparation du voile FR")
        for i, carte in enumerate(cartes.values(), 1):
            etat.ecrire(fait=i)
            if not carte["en"] or not CODE_TRADUISIBLE.match(carte["code"]):
                continue
            try:
                chemin, largeur, hauteur = image_orientee(carte["en"], est_complot(carte["type"]), dossier_orientes)
            except Exception as e:
                journal(f"voile : scan illisible {carte['code']} ({carte['en']}) : {e}")
                continue
            carte["voile_source"] = chemin
            travaux.append({"code": carte["code"], "image": str(chemin), "largeur": largeur,
                            "hauteur": hauteur, "type": carte["type"]})
    resume_voile = rendre_voiles(travaux, SORTIE, catalogues, args.paralleles, etat, journal) if travaux else None
    try:
        index_voile = json.loads((SORTIE / "voile-cache" / "index.json").read_text(encoding="utf-8"))
    except Exception:
        index_voile = {}

    # 3. Le ZIP, ecrit a cote puis mis en place d'un coup : le telechargement en
    #    cours d'un ancien ZIP n'est jamais coupe par la generation suivante.
    etat.ecrire(force=True, phase="zip", fait=0, total=len(cartes), message="Ecriture du ZIP")
    provisoire = SORTIE / (NOM_ZIP + ".tmp")
    compte = {"en": 0, "fr": 0, "en_voile_fr": 0, "sans_en": 0}
    manifeste = {}
    cache_voile = SORTIE / "voile-cache"
    with zipfile.ZipFile(provisoire, "w", compression=zipfile.ZIP_STORED, allowZip64=True) as archive:
        # Les trois dossiers existent toujours, meme vides (fr/ d'un paquet fan-made).
        for dossier_zip in ("en/", "fr/", "en_voile_fr/"):
            archive.writestr(zipfile.ZipInfo(dossier_zip), b"")
        for i, carte in enumerate(cartes.values(), 1):
            etat.ecrire(fait=i)
            ligne = {"pack": carte["pack"], "nom": carte["nom"], "type": carte["type"]}
            if carte["en"]:
                archive.write(carte["en"], f"en/{carte['code']}{carte['en'].suffix.lower()}")
                ligne["en"] = str(carte["en"].relative_to(MOTEUR))
                compte["en"] += 1
            else:
                compte["sans_en"] += 1
            if carte["fr"]:
                archive.write(carte["fr"], f"fr/{carte['code']}{carte['fr'].suffix.lower()}")
                ligne["fr"] = str(carte["fr"].relative_to(MOTEUR))
                compte["fr"] += 1
            entree = index_voile.get(carte["code"])
            source = carte.get("voile_source")
            if entree and entree.get("fichier") and source and entree.get("image_sha") == sha1_fichier(source):
                rendu = cache_voile / entree["fichier"]
                if rendu.is_file():
                    archive.write(rendu, f"en_voile_fr/{carte['code']}.jpg")
                    ligne["en_voile_fr"] = True
                    compte["en_voile_fr"] += 1
            elif entree and not entree.get("fichier"):
                ligne["en_voile_fr"] = f"non pose ({entree.get('raison')})"
            manifeste[carte["code"]] = ligne
        resultat = {
            "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            "packs": sorted(packs) or "tout le catalogue",
            "cartes": len(cartes),
            "en": compte["en"],
            "sans_en": compte["sans_en"],
            "fr": compte["fr"],
            "en_voile_fr": compte["en_voile_fr"],
            "telecharges": telechargeur.faits,
            "telechargements_echoues": telechargeur.echecs,
            "voile": resume_voile if resume_voile else (
                "non rendu : Node/ui-app absents, rendus repris du cache" if travaux else "desactive"),
        }
        archive.writestr("LISEZMOI.txt", lisezmoi(resultat), compress_type=zipfile.ZIP_DEFLATED)
        archive.writestr("manifeste.json", json.dumps({"resume": resultat, "cartes": manifeste},
                                                      ensure_ascii=False, indent=1),
                         compress_type=zipfile.ZIP_DEFLATED)
    os.replace(provisoire, SORTIE / NOM_ZIP)
    shutil.rmtree(dossier_orientes, ignore_errors=True)
    return resultat


def lisezmoi(r) -> str:
    voile = r["voile"]
    if isinstance(voile, dict):
        voile = (f"{voile.get('rendues', 0)} rendus, {voile.get('gardees', 0)} repris du cache, "
                 f"{voile.get('nonPosees', 0)} cartes dont la zone de texte n'est pas reconnue "
                 f"(le plateau montre alors le francais sous la carte), {voile.get('erreurs', 0)} erreurs")
    return (
        "Export des images de cartes - Narwhal Champions\n"
        f"Genere le {r['date']} ; perimetre : {r['packs'] if isinstance(r['packs'], str) else ', '.join(r['packs'])}\n\n"
        f"en/           {r['en']} scans anglais ({r['sans_en']} cartes sans aucun scan)\n"
        f"fr/           {r['fr']} scans francais officiels. Incomplet par nature : le contenu\n"
        "              fan-made et les cartes jamais traduites n'en ont pas.\n"
        f"en_voile_fr/  {r['en_voile_fr']} scans anglais avec le voile FR du plateau\n"
        f"              ({voile}).\n\n"
        "Les fichiers portent le code de la carte (card_id). manifeste.json donne, pour\n"
        "chaque carte, son paquet, son nom, son type et la source de chaque image.\n"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--packs", help="paquets a exporter (cles de cards.json, separees par des virgules)")
    parser.add_argument("--config", default=str(MOTEUR / "launch.json"),
                        help="configuration du moteur (catalogues, image_servers)")
    parser.add_argument("--catalogue", action="append", help="fichier de cartes (repetable) ; remplace la config")
    parser.add_argument("--serveur-images", action="append", help="modele d'URL (repetable) ; remplace la config")
    parser.add_argument("--sans-telechargement", action="store_true",
                        help="ne rien telecharger (aucun serveur d'images configure)")
    parser.add_argument("--sans-voile", action="store_true", help="ne pas rendre le dossier en_voile_fr/")
    parser.add_argument("--paralleles", type=int, default=3, help="pages Chromium en parallele pour le voile")
    parser.add_argument("--verrou-pris", action="store_true",
                        help="le verrou a deja ete pris par le serveur (lancement depuis le site)")
    args = parser.parse_args()

    SORTIE.mkdir(parents=True, exist_ok=True)
    if args.verrou_pris:
        ecrire_json_atomique(SORTIE / VERROU, {"pid": os.getpid(), "debut": time.time(), "packs": args.packs})
    elif not prendre_verrou(SORTIE, {"pid": os.getpid(), "debut": time.time(), "packs": args.packs}):
        print("Une generation est deja en cours (generation.lock).", file=sys.stderr)
        return 2
    try:
        os.nice(10)   # les parties en cours passent avant
    except Exception:
        pass

    journal_f = open(SORTIE / JOURNAL, "w", encoding="utf-8")

    def journal(message):
        ligne = f"{time.strftime('%H:%M:%S')} {message}"
        print(ligne, flush=True)
        journal_f.write(ligne + "\n")
        journal_f.flush()

    etat = Etat(SORTIE, args.packs)
    code = 0
    try:
        resultat = generer(args, etat, journal)
        journal(f"termine : {json.dumps(resultat, ensure_ascii=False)}")
        etat.ecrire(force=True, en_cours=False, fin=time.time(), phase="termine", message="Termine",
                    resultat=resultat)
    except BaseException as e:   # noqa: BLE001 -- l'etat doit dire l'echec, quel qu'il soit
        journal("ECHEC\n" + traceback.format_exc())
        etat.ecrire(force=True, en_cours=False, fin=time.time(), phase="echec", message="Echec",
                    erreur=f"{type(e).__name__}: {e}")
        code = 1
    finally:
        journal_f.close()
        try:
            (SORTIE / VERROU).unlink()
        except FileNotFoundError:
            pass
        try:
            (SORTIE / (NOM_ZIP + ".tmp")).unlink()
        except FileNotFoundError:
            pass
    return code


if __name__ == "__main__":
    sys.exit(main())
