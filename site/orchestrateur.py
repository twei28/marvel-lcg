#!/usr/bin/env python3.10
"""NarwhalChampions — orchestrateur de parties.

Le moteur de jeu est MONO-PARTIE : `tools/config_serveur.py` le dit noir sur
blanc, « une place egale un processus, donc un port et des dossiers a lui ».
Ce service alloue donc UN MOTEUR PAR PARTIE, parmi un nombre fixe
d'emplacements, et le rend a la fin.

⚠ POURQUOI UN SOUS-DOMAINE PAR PARTIE, ET PAS UN CHEMIN.
Le client du jeu utilise des chemins ABSOLUS partout : `/ws`, `/save_deck`,
`/set_choix_siege`, `/app/board.html`, `/get_achievements`... Servir une partie
sous `narwhalchampions.xx/partie3/` casserait chacun de ces appels, qui
repartiraient a la racine du SITE au lieu du moteur de la partie. Avec un
sous-domaine (`p3.narwhalchampions.xx`), l'hote change et les chemins absolus
restent justes : aucune ligne du client a toucher.

⚠ CE SERVICE NE FAIT PAS DE PROXY. Caddy s'en charge, avec des routes
STATIQUES (`p<N>` -> port 2350+N) declarees une fois pour toutes. L'allocation
est dynamique, le routage ne l'est pas : c'est ce qui evite d'avoir a
reconfigurer Caddy en vol, et donc a le deboguer en vol.

Aucune dependance : bibliotheque standard uniquement.
"""
from __future__ import annotations

import hashlib
import html
import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# --------------------------------------------------------------------------
# Reglages. Tout ce qui depend de la machine est ICI.
# --------------------------------------------------------------------------
RACINE_SITE = os.path.dirname(os.path.abspath(__file__))
RACINE_JEU = os.environ.get(
    "RACINE_JEU",
    os.path.join(os.path.dirname(RACINE_SITE), "Fusion", "marvel-lcg-src"))
PYTHON = os.environ.get("PYTHON", os.path.expanduser("~/marvel-work/python/bin/python3.10"))

# Le domaine sert UNIQUEMENT a fabriquer les liens affiches. En local, on
# laisse vide : les liens pointent alors sur 127.0.0.1:<port>.
DOMAINE = os.environ.get("DOMAINE", "")

PORT_SITE = int(os.environ.get("PORT_SITE", "8080"))
PORT_BASE = 2350                      # emplacement N -> port PORT_BASE + N
NB_EMPLACEMENTS = int(os.environ.get("NB_EMPLACEMENTS", "20"))

# Une partie est fauchee quand son moteur est mort, ou passe cette duree.
# ⚠ CE N'EST PAS UNE MESURE D'INACTIVITE : le moteur n'expose rien qui
# permette de savoir si quelqu'un joue encore. C'est un plafond de duree, et
# il est volontairement large. Le bouton « Terminer » reste le moyen propre.
DUREE_MAX_HEURES = float(os.environ.get("DUREE_MAX_HEURES", "8"))
DELAI_DEMARRAGE = 240                 # secondes d'attente avant d'abandonner

# --- Comptes ---------------------------------------------------------------
# Un compte VALIDE est necessaire pour OUVRIR une table. Les trois autres
# joueurs arrivent par leur lien de siege, sans compte : ce lien porte deja sa
# propre cle aleatoire, c'est le moteur qui protege le siege.
#
# ⚠ LE PLAFOND DE COMPTES N'EST PAS LE PLAFOND DE JOUEURS, et les deux se
# reglent separement. `NB_EMPLACEMENTS` (20) borne les parties SIMULTANEES,
# donc 80 joueurs a un instant donne ; `MAX_COMPTES` borne le nombre de
# PERSONNES autorisees a ouvrir une table, tous soirs confondus. Choix de
# l'utilisateur le 05/09/2026 : 20 comptes.
#
# Couche maison plutot que Cloudflare Access : cette derniere s'arrete a 50
# personnes en gratuit et ferait doublon. Ici, aucune dependance —
# `hashlib.scrypt` est dans la bibliotheque standard.
FICHIER_COMPTES = os.environ.get("FICHIER_COMPTES", os.path.join(RACINE_SITE, "comptes.json"))
MAX_COMPTES = int(os.environ.get("MAX_COMPTES", "20"))
ADMIN = os.environ.get("ADMIN", "arnaud").strip().lower()

sys.path.insert(0, os.path.join(RACINE_JEU, "tools"))
import config_serveur  # noqa: E402  (dependant de sys.path ci-dessus)


# --------------------------------------------------------------------------
# Etat
# --------------------------------------------------------------------------
class Partie:
    def __init__(self, emplacement: int, code: str, nom: str) -> None:
        self.emplacement = emplacement
        self.port = PORT_BASE + emplacement
        self.code = code
        self.nom = nom
        self.processus: subprocess.Popen | None = None
        self.mot_de_passe = ""
        self.cles_sieges: list[str] = []
        self.debut = time.time()

    def base_url(self) -> str:
        if DOMAINE:
            return f"https://p{self.emplacement}.{DOMAINE}"
        return f"http://127.0.0.1:{self.port}"

    def liens(self) -> list[dict]:
        """Les liens PERSONNELS, au format exact de `launcher-multi.sh`.

        `claim_seat?p=<0..3>&key=<cle>&to=salon` reserve le siege : personne ne
        peut agir a la place d'un autre. Le siege 0 est l'hote.
        """
        base = self.base_url()
        sortie = []
        for siege in range(4):
            cle = self.cles_sieges[siege] if siege < len(self.cles_sieges) else ""
            sortie.append({
                "siege": siege,
                "libelle": "Hote (joueur 1)" if siege == 0 else f"Joueur {siege + 1}",
                "url": f"{base}/claim_seat?p={siege}&key={cle}&to=salon",
            })
        return sortie

    def vivant(self) -> bool:
        return self.processus is not None and self.processus.poll() is None


PARTIES: dict[str, Partie] = {}          # code -> Partie
EMPLACEMENTS: dict[int, str] = {}        # emplacement -> code
VERROU = threading.Lock()


# --------------------------------------------------------------------------
# Cycle de vie d'une partie
# --------------------------------------------------------------------------
def _config_partie(emplacement: int, partie: Partie) -> str:
    """Ecrit la configuration du moteur pour cet emplacement.

    ⚠ `config_serveur.construire_config` est le SEUL endroit qui sait quelles
    cles doivent etre separees par place (sauvegardes, historique, decks,
    campagnes, hauts faits...). On l'appelle plutot que de recopier la liste,
    qui divergerait au premier ajout.
    """
    base = json.load(open(os.path.join(RACINE_JEU, "launch.json"), encoding="utf-8"))
    cfg = config_serveur.construire_config(base, emplacement)
    cfg["password"] = partie.mot_de_passe
    cfg["seat_passwords"] = partie.cles_sieges

    # Les chemins de la configuration sont relatifs a `.game/`, pas a la
    # racine : le moteur fait `os.chdir(.game)` avant de les resoudre.
    for relatif in cfg["replay_folders"] + [cfg["deck_folders"][0], cfg["campagne_folder"]]:
        os.makedirs(os.path.normpath(os.path.join(RACINE_JEU, ".game", relatif)), exist_ok=True)

    dossier = os.path.join(RACINE_JEU, ".site")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, f"launch-{emplacement}.json")
    with open(chemin, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return chemin


def _moteur_repond(port: int) -> bool:
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/", timeout=2):
            return True
    except (urllib.error.URLError, OSError):
        return False


def _nettoyer_emplacement(emplacement: int) -> None:
    """Efface les donnees de la partie precedente sur cet emplacement.

    Sans ca, le groupe suivant heriterait des decks, des sauvegardes et des
    hauts faits du precedent. Les dossiers COMMUNS (images, catalogue, decks
    de depart, decks de l'hote) ne sont jamais touches : `construire_config`
    les laisse volontairement partages.
    """
    racine_game = os.path.join(RACINE_JEU, ".game")
    for relatif in (f"../replays/serveur-{emplacement}/",
                    f"../campagnes-serveur-{emplacement}/",
                    f"./deck/serveur-{emplacement}/"):
        chemin = os.path.normpath(os.path.join(racine_game, relatif))
        shutil.rmtree(chemin, ignore_errors=True)
    for relatif in (f"../games_history-serveur-{emplacement}.json",
                    f"../statistics-serveur-{emplacement}.json",
                    f"../achievements-serveur-{emplacement}.json",
                    f"./campaign-log-last-serveur-{emplacement}.json"):
        chemin = os.path.normpath(os.path.join(racine_game, relatif))
        try:
            os.remove(chemin)
        except OSError:
            pass


def creer_partie(nom: str) -> Partie:
    with VERROU:
        libres = [n for n in range(1, NB_EMPLACEMENTS + 1) if n not in EMPLACEMENTS]
        if not libres:
            raise RuntimeError("Toutes les tables sont occupees. Reessaie dans un moment.")
        emplacement = libres[0]
        code = secrets.token_urlsafe(6)
        partie = Partie(emplacement, code, nom or f"Table {emplacement}")
        partie.mot_de_passe = secrets.token_urlsafe(6)
        partie.cles_sieges = [secrets.token_urlsafe(8) for _ in range(4)]
        EMPLACEMENTS[emplacement] = code
        PARTIES[code] = partie

    try:
        _nettoyer_emplacement(emplacement)
        chemin_config = _config_partie(emplacement, partie)
        journal = open(os.path.join(RACINE_JEU, ".site", f"moteur-{emplacement}.log"),
                       "w", encoding="utf-8")
        # PYTHONUNBUFFERED : sans lui Python tamponne des que la sortie n'est
        # plus un terminal, et le journal reste vide au moment ou l'on en a
        # besoin (leçon deja payee dans launcher-multi.sh).
        env = dict(os.environ, PYTHONUNBUFFERED="1")
        partie.processus = subprocess.Popen(
            [PYTHON, "-u", "launcher_fast.py", "--config",
             os.path.relpath(chemin_config, RACINE_JEU), "--no-browser"],
            cwd=RACINE_JEU, stdout=journal, stderr=subprocess.STDOUT, env=env,
            start_new_session=True)

        for _ in range(DELAI_DEMARRAGE):
            if _moteur_repond(partie.port):
                return partie
            if not partie.vivant():
                raise RuntimeError(
                    f"Le moteur s'est arrete au demarrage. Journal : "
                    f".site/moteur-{emplacement}.log")
            time.sleep(1)
        raise RuntimeError("Le moteur n'a pas repondu a temps.")
    except Exception:
        fermer_partie(code)
        raise


def fermer_partie(code: str) -> bool:
    with VERROU:
        partie = PARTIES.pop(code, None)
        if partie is None:
            return False
        EMPLACEMENTS.pop(partie.emplacement, None)
    if partie.processus is not None and partie.processus.poll() is None:
        # `start_new_session` a mis le moteur dans son propre groupe : on tue
        # LE GROUPE, sinon les sous-processus du lanceur survivraient et le
        # port resterait pris.
        try:
            os.killpg(os.getpgid(partie.processus.pid), signal.SIGTERM)
        except OSError:
            partie.processus.terminate()
        try:
            partie.processus.wait(timeout=15)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(partie.processus.pid), signal.SIGKILL)
            except OSError:
                partie.processus.kill()
    return True


def faucheur() -> None:
    """Rend les emplacements dont le moteur est mort ou la partie trop vieille."""
    while True:
        time.sleep(60)
        for code, partie in list(PARTIES.items()):
            trop_vieille = (time.time() - partie.debut) > DUREE_MAX_HEURES * 3600
            if not partie.vivant() or trop_vieille:
                fermer_partie(code)


# --------------------------------------------------------------------------
# Comptes
# --------------------------------------------------------------------------
COMPTES: dict[str, dict] = {}
SESSIONS: dict[str, str] = {}            # jeton -> pseudo
VERROU_COMPTES = threading.Lock()


def charger_comptes() -> None:
    global COMPTES
    try:
        with open(FICHIER_COMPTES, encoding="utf-8") as f:
            COMPTES = json.load(f)
    except (OSError, ValueError):
        COMPTES = {}


def _ecrire_comptes() -> None:
    """Ecriture ATOMIQUE : fichier temporaire puis `os.replace`.

    C'est la seule donnee du site qui ne se regenere pas. Une coupure au
    milieu d'un `json.dump` direct laisserait un fichier tronque, donc tous
    les comptes perdus.
    """
    provisoire = FICHIER_COMPTES + ".tmp"
    with open(provisoire, "w", encoding="utf-8") as f:
        json.dump(COMPTES, f, ensure_ascii=False, indent=2)
    os.replace(provisoire, FICHIER_COMPTES)


def _empreinte(mot_de_passe: str, sel: str) -> str:
    """scrypt, de la bibliotheque standard. Aucune dependance a installer."""
    brut = hashlib.scrypt(mot_de_passe.encode("utf-8"), salt=bytes.fromhex(sel),
                          n=2 ** 14, r=8, p=1, dklen=32)
    return brut.hex()


def inscrire(pseudo: str, mot_de_passe: str) -> str:
    pseudo = (pseudo or "").strip().lower()
    if not (3 <= len(pseudo) <= 24) or not pseudo.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Pseudo invalide : 3 a 24 caracteres, lettres, chiffres, - et _.")
    if len(mot_de_passe or "") < 8:
        raise ValueError("Mot de passe trop court : 8 caracteres au minimum.")
    with VERROU_COMPTES:
        if pseudo in COMPTES:
            raise ValueError("Ce pseudo est deja pris.")
        # ⚠ LE PLAFOND NE COMPTE QUE LES COMPTES VALIDES. Sinon une vague
        # d'inscriptions en attente suffirait a bloquer les vraies demandes.
        valides = sum(1 for c in COMPTES.values() if c.get("statut") == "valide")
        if valides >= MAX_COMPTES and pseudo != ADMIN:
            raise ValueError(f"Le site est complet ({MAX_COMPTES} comptes).")
        sel = secrets.token_bytes(16).hex()
        COMPTES[pseudo] = {
            "sel": sel,
            "empreinte": _empreinte(mot_de_passe, sel),
            # Le compte de l'administrateur est valide d'office : sans ca,
            # personne ne pourrait valider le premier compte.
            "statut": "valide" if pseudo == ADMIN else "attente",
            "cree": time.strftime("%Y-%m-%d %H:%M"),
        }
        _ecrire_comptes()
    return pseudo


def verifier(pseudo: str, mot_de_passe: str) -> str:
    pseudo = (pseudo or "").strip().lower()
    with VERROU_COMPTES:
        compte = COMPTES.get(pseudo)
        if compte is None:
            raise ValueError("Pseudo ou mot de passe incorrect.")
        attendu = compte.get("empreinte", "")
        # `compare_digest` : comparaison a temps constant, pour ne pas laisser
        # fuir l'empreinte par le temps de reponse.
        if not secrets.compare_digest(_empreinte(mot_de_passe, compte["sel"]), attendu):
            raise ValueError("Pseudo ou mot de passe incorrect.")
        if compte.get("statut") != "valide":
            raise ValueError("Ton compte attend encore ma validation.")
    return pseudo


def changer_statut(pseudo: str, statut: str) -> None:
    with VERROU_COMPTES:
        if pseudo in COMPTES and statut in ("valide", "attente", "refuse"):
            COMPTES[pseudo]["statut"] = statut
            _ecrire_comptes()
    if statut != "valide":
        for jeton, qui in list(SESSIONS.items()):
            if qui == pseudo:
                SESSIONS.pop(jeton, None)


def ouvrir_session(pseudo: str) -> str:
    jeton = secrets.token_urlsafe(24)
    SESSIONS[jeton] = pseudo
    return jeton


# --------------------------------------------------------------------------
# Site
# --------------------------------------------------------------------------
PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NarwhalChampions</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; background:#0e1116; color:#e6edf3;
         display:flex; justify-content:center; padding:2rem 1rem; }}
  main {{ width:100%; max-width:44rem; }}
  h1 {{ font-size:1.9rem; margin:0 0 .25rem; letter-spacing:-.02em; }}
  p.sous {{ color:#9aa7b4; margin:0 0 2rem; }}
  form {{ display:flex; gap:.5rem; margin-bottom:2rem; }}
  input, button {{ font:inherit; border-radius:.5rem; border:1px solid #30363d; padding:.6rem .9rem; }}
  input {{ flex:1; background:#161b22; color:inherit; }}
  button {{ background:#1f6feb; color:#fff; border-color:#1f6feb; cursor:pointer; }}
  button:hover {{ background:#388bfd; }}
  button.rouge {{ background:transparent; color:#f85149; border-color:#f85149; padding:.35rem .7rem; font-size:.85rem; }}
  .table {{ border:1px solid #30363d; border-radius:.6rem; padding:1rem 1.1rem; margin-bottom:1rem; background:#161b22; }}
  .entete {{ display:flex; justify-content:space-between; align-items:center; gap:1rem; margin-bottom:.7rem; }}
  .entete strong {{ font-size:1.05rem; }}
  .mdp {{ color:#9aa7b4; font-size:.9rem; }}
  .mdp code {{ background:#0e1116; padding:.15rem .4rem; border-radius:.3rem; color:#e6edf3; }}
  ul {{ list-style:none; margin:0; padding:0; }}
  li {{ display:flex; align-items:center; gap:.6rem; padding:.3rem 0; }}
  li span {{ min-width:8.5rem; color:#9aa7b4; font-size:.9rem; }}
  li a {{ color:#58a6ff; word-break:break-all; font-size:.9rem; }}
  .vide {{ color:#9aa7b4; }}
  .barre {{ display:flex; justify-content:space-between; align-items:center;
           gap:1rem; margin-bottom:1.5rem; color:#9aa7b4; font-size:.9rem; }}
  .barre a {{ color:#58a6ff; }}
  .avert {{ border:1px solid #9e6a03; background:#1d1a0e; color:#e3b341;
           border-radius:.5rem; padding:.7rem .9rem; margin-bottom:1.5rem; font-size:.9rem; }}
  footer {{ margin-top:2.5rem; color:#6e7681; font-size:.85rem; }}
</style>
<main>
  <h1>NarwhalChampions</h1>
  <p class="sous">{libres} table(s) libre(s) sur {total}. Une table accueille jusqu'a 4 joueurs.</p>
  {barre}
  {ouvrir}
  {tables}
  <footer>Un compte n'est necessaire que pour OUVRIR une table. Tes invites
  arrivent par leur lien de siege, sans rien creer. Chaque lien reserve un
  siege : personne ne peut jouer a la place d'un autre. Une table se ferme
  quand on clique sur Terminer, ou automatiquement au bout de {heures} h.</footer>
</main>
"""

GABARIT_TABLE = """<div class="table">
  <div class="entete">
    <strong>{nom}</strong>
    <form method="post" action="/fermer" style="margin:0">
      <input type="hidden" name="code" value="{code}">
      <button class="rouge" type="submit">Terminer</button>
    </form>
  </div>
  <p class="mdp">Mot de passe d'entree : <code>{mdp}</code></p>
  <ul>{liens}</ul>
</div>"""


def rendre_page(pseudo=None, message="") -> bytes:
    if pseudo:
        admin = ' &middot; <a href="/admin">Validations</a>' if pseudo == ADMIN else ""
        barre = ('<div class="barre"><span>Connecte : <strong>%s</strong>%s</span>'
                 '<a href="/deconnexion">Se deconnecter</a></div>'
                 % (html.escape(pseudo), admin))
        ouvrir = ('<form method="post" action="/partie">'
                  '<input name="nom" placeholder="Nom de la table (facultatif)" maxlength="40">'
                  '<button type="submit">Ouvrir une table</button></form>')
    else:
        barre = ('<div class="barre"><span>Il faut un compte pour ouvrir une table.</span>'
                 '<span><a href="/connexion">Se connecter</a> &middot; '
                 '<a href="/inscription">Creer un compte</a></span></div>')
        ouvrir = ""
    if message:
        barre = '<div class="avert">%s</div>%s' % (html.escape(message), barre)
    with VERROU:
        parties = sorted(PARTIES.values(), key=lambda p: p.emplacement)
        libres = NB_EMPLACEMENTS - len(EMPLACEMENTS)
    if parties:
        blocs = []
        for p in parties:
            liens = "".join(
                '<li><span>{}</span><a href="{}">{}</a></li>'.format(
                    html.escape(l["libelle"]), html.escape(l["url"]), html.escape(l["url"]))
                for l in p.liens())
            blocs.append(GABARIT_TABLE.format(
                nom=html.escape(p.nom), code=html.escape(p.code),
                mdp=html.escape(p.mot_de_passe), liens=liens))
        tables = "".join(blocs)
    else:
        tables = '<p class="vide">Aucune table ouverte pour le moment.</p>'
    return PAGE.format(libres=libres, total=NB_EMPLACEMENTS, tables=tables,
                       barre=barre, ouvrir=ouvrir,
                       heures=int(DUREE_MAX_HEURES)).encode("utf-8")


PAGE_FORMULAIRE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titre} — NarwhalChampions</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; background:#0e1116; color:#e6edf3;
         display:flex; justify-content:center; padding:3rem 1rem; }}
  main {{ width:100%; max-width:24rem; }}
  h1 {{ font-size:1.4rem; margin:0 0 1.5rem; }}
  label {{ display:block; margin-bottom:1rem; font-size:.9rem; color:#9aa7b4; }}
  input {{ width:100%; box-sizing:border-box; font:inherit; margin-top:.3rem;
          background:#161b22; color:inherit; border:1px solid #30363d;
          border-radius:.5rem; padding:.6rem .9rem; }}
  button {{ width:100%; font:inherit; background:#1f6feb; color:#fff; border:0;
           border-radius:.5rem; padding:.7rem; cursor:pointer; }}
  .erreur {{ border:1px solid #f85149; background:#1d1113; color:#ff7b72;
            border-radius:.5rem; padding:.7rem .9rem; margin-bottom:1.2rem; font-size:.9rem; }}
  p {{ color:#9aa7b4; font-size:.9rem; }} a {{ color:#58a6ff; }}
</style>
<main>
  <h1>{titre}</h1>
  {erreur}
  <form method="post" action="{action}">
    <label>Pseudo<input name="pseudo" autocomplete="username" required></label>
    <label>Mot de passe<input name="mdp" type="password" autocomplete="{auto}" required></label>
    <button type="submit">{bouton}</button>
  </form>
  <p>{pied}</p>
</main>
"""

PAGE_ADMIN = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Validations — NarwhalChampions</title>
<style>
  :root {{ color-scheme: dark; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; background:#0e1116; color:#e6edf3;
         display:flex; justify-content:center; padding:2rem 1rem; }}
  main {{ width:100%; max-width:40rem; }}
  h1 {{ font-size:1.4rem; margin:0 0 .3rem; }}
  p.sous {{ color:#9aa7b4; margin:0 0 2rem; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ text-align:left; padding:.6rem .4rem; border-bottom:1px solid #21262d; }}
  th {{ color:#9aa7b4; font-weight:500; font-size:.85rem; }}
  button {{ font:inherit; font-size:.85rem; border-radius:.4rem; padding:.3rem .7rem;
           cursor:pointer; border:1px solid #30363d; background:transparent; color:inherit; }}
  button.oui {{ border-color:#238636; color:#3fb950; }}
  button.non {{ border-color:#f85149; color:#f85149; }}
  form {{ display:inline; margin-right:.3rem; }}
  a {{ color:#58a6ff; }}
</style>
<main>
  <h1>Validations</h1>
  <p class="sous">{valides} compte(s) valide(s) sur {max}. <a href="/">Retour au site</a></p>
  <table>
    <tr><th>Pseudo</th><th>Cree le</th><th>Statut</th><th></th></tr>
    {lignes}
  </table>
</main>
"""


class Handler(BaseHTTPRequestHandler):
    server_version = "NarwhalChampions"

    def log_message(self, fmt, *args):  # journal plus sobre
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    def _repondre(self, code: int, corps: bytes, type_mime="text/html; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", type_mime)
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)

    def _rediriger(self, vers="/"):
        self.send_response(303)
        self.send_header("Location", vers)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _session(self):
        """Le pseudo connecte, ou None.

        ⚠ Les sessions vivent EN MEMOIRE : un redemarrage du service les perd
        et chacun se reconnecte. C'est assume — la seule donnee qui doit
        survivre est le fichier des comptes, qui, lui, est ecrit sur disque.
        """
        brut = self.headers.get("Cookie") or ""
        for morceau in brut.split(";"):
            nom, _, valeur = morceau.strip().partition("=")
            if nom == "nc_session":
                pseudo = SESSIONS.get(valeur)
                # Un compte devalide en cours de route ne doit plus passer.
                if pseudo and COMPTES.get(pseudo, {}).get("statut") == "valide":
                    return pseudo
        return None

    def _champs(self) -> dict:
        import urllib.parse
        taille = int(self.headers.get("Content-Length") or 0)
        brut = self.rfile.read(taille).decode("utf-8", "replace")
        return {k: v[0] for k, v in urllib.parse.parse_qs(brut).items()}

    def _formulaire(self, quoi: str, erreur: str = "") -> bytes:
        inscription = quoi == "inscription"
        return PAGE_FORMULAIRE.format(
            titre="Creer un compte" if inscription else "Se connecter",
            action="/inscription" if inscription else "/connexion",
            bouton="Demander un compte" if inscription else "Entrer",
            auto="new-password" if inscription else "current-password",
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            pied=('Ton compte devra etre valide a la main avant de servir. '
                  'Deja un compte ? <a href="/connexion">Se connecter</a>.'
                  if inscription else
                  'Pas encore de compte ? <a href="/inscription">En demander un</a>.'),
        ).encode("utf-8")

    def _page_admin(self) -> bytes:
        with VERROU_COMPTES:
            comptes = sorted(COMPTES.items())
            valides = sum(1 for c in COMPTES.values() if c.get("statut") == "valide")
        lignes = []
        for pseudo, compte in comptes:
            statut = compte.get("statut", "attente")
            actions = ""
            if pseudo != ADMIN:
                for cible, classe, libelle in (("valide", "oui", "Valider"),
                                               ("refuse", "non", "Refuser")):
                    if statut != cible:
                        actions += ('<form method="post" action="/admin">'
                                    '<input type="hidden" name="pseudo" value="%s">'
                                    '<input type="hidden" name="statut" value="%s">'
                                    '<button class="%s" type="submit">%s</button></form>'
                                    % (html.escape(pseudo), cible, classe, libelle))
            lignes.append("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                html.escape(pseudo), html.escape(compte.get("cree", "")),
                html.escape(statut), actions))
        return PAGE_ADMIN.format(valides=valides, max=MAX_COMPTES,
                                 lignes="".join(lignes)).encode("utf-8")

    def do_GET(self):
        pseudo = self._session()
        if self.path in ("/", "/index.html"):
            self._repondre(200, rendre_page(pseudo))
        elif self.path == "/inscription":
            self._repondre(200, self._formulaire("inscription"))
        elif self.path == "/connexion":
            self._repondre(200, self._formulaire("connexion"))
        elif self.path == "/deconnexion":
            brut = self.headers.get("Cookie") or ""
            for morceau in brut.split(";"):
                nom, _, valeur = morceau.strip().partition("=")
                if nom == "nc_session":
                    SESSIONS.pop(valeur, None)
            self.send_response(303)
            self.send_header("Location", "/")
            self.send_header("Set-Cookie", "nc_session=; Max-Age=0; Path=/")
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/admin":
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._repondre(200, self._page_admin())
        elif self.path == "/etat":
            with VERROU:
                etat = {"libres": NB_EMPLACEMENTS - len(EMPLACEMENTS),
                        "total": NB_EMPLACEMENTS,
                        "tables": [{"code": p.code, "nom": p.nom,
                                    "emplacement": p.emplacement,
                                    "vivant": p.vivant()} for p in PARTIES.values()]}
            self._repondre(200, json.dumps(etat, ensure_ascii=False).encode("utf-8"),
                           "application/json; charset=utf-8")
        else:
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")

    def do_POST(self):
        champs = self._champs()
        pseudo = self._session()

        if self.path == "/inscription":
            try:
                inscrire(champs.get("pseudo", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire("inscription", str(erreur)))
                return
            self._repondre(200, PAGE_FORMULAIRE.format(
                titre="Demande enregistree", action="/connexion", bouton="Entrer",
                auto="current-password", erreur="",
                pied="Ton compte attend une validation manuelle. Reviens une fois "
                     "qu'elle est faite.").encode("utf-8"))

        elif self.path == "/connexion":
            try:
                qui = verifier(champs.get("pseudo", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire("connexion", str(erreur)))
                return
            jeton = ouvrir_session(qui)
            self.send_response(303)
            self.send_header("Location", "/")
            # HttpOnly : le cookie n'est pas lisible en JavaScript.
            # SameSite=Lax : il ne part pas sur une requete venue d'un autre site.
            self.send_header("Set-Cookie",
                             f"nc_session={jeton}; HttpOnly; SameSite=Lax; Path=/; Max-Age=604800")
            self.send_header("Content-Length", "0")
            self.end_headers()

        elif self.path == "/admin":
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            changer_statut(champs.get("pseudo", "").strip().lower(),
                           champs.get("statut", ""))
            self._rediriger("/admin")

        elif self.path == "/partie":
            # ⚠ LE COMPTE N'EST EXIGE QUE POUR OUVRIR UNE TABLE. Les invites
            # arrivent par leur lien de siege, qui porte sa propre cle : c'est
            # le moteur qui protege le siege, pas ce service.
            if not pseudo:
                self._repondre(403, rendre_page(None, "Il faut un compte valide pour ouvrir une table."))
                return
            try:
                creer_partie(champs.get("nom", "").strip() or f"Table de {pseudo}")
            except Exception as erreur:
                self._repondre(503, rendre_page(pseudo, str(erreur)))
                return
            self._rediriger("/")

        elif self.path == "/fermer":
            if not pseudo:
                self._repondre(403, rendre_page(None, "Connecte-toi pour fermer une table."))
                return
            fermer_partie(champs.get("code", ""))
            self._rediriger("/")

        else:
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")


def main() -> int:
    if not os.path.isfile(os.path.join(RACINE_JEU, "launch.json")):
        print(f"Racine du jeu introuvable : {RACINE_JEU}", file=sys.stderr)
        return 1
    if not os.access(PYTHON, os.X_OK):
        print(f"Python du moteur introuvable ou non executable : {PYTHON}", file=sys.stderr)
        return 1

    charger_comptes()
    if ADMIN not in COMPTES:
        print(f"  ⚠ Aucun compte administrateur « {ADMIN} » : cree-le sur /inscription,")
        print("    il sera valide d'office.")
    threading.Thread(target=faucheur, daemon=True).start()
    serveur = ThreadingHTTPServer(("127.0.0.1", PORT_SITE), Handler)

    def arreter(*_):
        print("\nFermeture de toutes les tables...")
        for code in list(PARTIES):
            fermer_partie(code)
        serveur.shutdown()

    signal.signal(signal.SIGINT, lambda *_: threading.Thread(target=arreter).start())
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=arreter).start())

    print(f"NarwhalChampions sur http://127.0.0.1:{PORT_SITE}")
    print(f"  moteur      : {RACINE_JEU}")
    print(f"  emplacements: {NB_EMPLACEMENTS} (ports {PORT_BASE + 1} a {PORT_BASE + NB_EMPLACEMENTS})")
    print(f"  domaine     : {DOMAINE or '(local, liens en 127.0.0.1)'}")
    print(f"  comptes     : {sum(1 for c in COMPTES.values() if c.get('statut') == 'valide')}"
          f"/{MAX_COMPTES} valides, admin « {ADMIN} »")
    try:
        serveur.serve_forever()
    finally:
        for code in list(PARTIES):
            fermer_partie(code)
    return 0


if __name__ == "__main__":
    sys.exit(main())
