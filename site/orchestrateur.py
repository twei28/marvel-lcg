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

import base64
import hashlib
import html
import json
import os
import secrets
import shutil
import signal
import sqlite3
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
# La base remplace le fichier JSON depuis le 05/09/2026 : il fallait pouvoir
# consulter QUI a un compte, avec quelle adresse, et QUAND chacun a joue — ce
# qu'un dictionnaire ecrase a chaque ecriture ne permet pas.
# `sqlite3` est dans la bibliotheque standard : toujours aucune dependance.
BASE = os.environ.get("BASE", os.path.join(RACINE_SITE, "narwhal.db"))
MAX_COMPTES = int(os.environ.get("MAX_COMPTES", "20"))
ADMIN = os.environ.get("ADMIN", "arnaud").strip().lower()
# Inscription LIBRE : quiconque a l'adresse du site peut demander un compte,
# qui reste en attente de validation. La mettre a "0" ferme cette porte : seul
# un LIEN D'INVITATION permet alors de creer un compte.
INSCRIPTION_LIBRE = os.environ.get("INSCRIPTION_LIBRE", "1") != "0"

# Rapports de bug. Les captures d'ecran vont sur DISQUE et non dans la base :
# une image de 400 Ko par rapport ferait grossir narwhal.db sans raison, et un
# fichier se sert directement.
DOSSIER_RAPPORTS = os.environ.get("DOSSIER_RAPPORTS", os.path.join(RACINE_SITE, "rapports"))
# Plafonds. La capture est deja reduite par le navigateur avant l'envoi (voir
# panneau-bug.js) ; ce plafond-ci est la ceinture, pas la bretelle.
MAX_CAPTURE_OCTETS = int(os.environ.get("MAX_CAPTURE_OCTETS", str(4 * 1024 * 1024)))
MAX_JOURNAL_CARACTERES = 400_000
MAX_DESCRIPTION_CARACTERES = 4_000
# Limite de debit, par compte hote. L'adresse est publique et n'importe quel
# invite peut envoyer : sans plafond, une boucle remplirait le disque.
RAPPORTS_PAR_HEURE = int(os.environ.get("RAPPORTS_PAR_HEURE", "12"))
ETATS_RAPPORT = ("nouveau", "en cours", "traite")
# Au-dela de ce delai, un rapport CLASSE « traite » n'a plus rien a apprendre a
# personne et sa capture ne fait que peser. Le plafond de debit est de 12
# rapports par heure ET PAR TABLE, avec une capture jusqu'a 4 Mio : vingt
# tables donnent une borne de l'ordre du gigaoctet par heure, et la sauvegarde
# de nuit multipliait le total par trente en gardant trente archives.
JOURS_RAPPORTS_TRAITES = int(os.environ.get("JOURS_RAPPORTS_TRAITES", "30"))

# Plafond du CORPS d'une requete POST, avant toute lecture.
# ⚠ `Content-Length` EST UNE DECLARATION DU CLIENT, PAS UN FAIT. Sans plafond,
# n'importe qui, sans compte et sans cookie, fait allouer au serveur ce qu'il
# annonce, y compris sur une route qui finira en 404. Le moteur, lui, a le
# sien depuis toujours (`client_max_size=8 Mio`, `web_server.py`) ; c'est le
# site qui n'en avait pas. Meme chiffre pour la meme raison : le plus gros
# envoi legitime est un rapport de bug, capture de 4 Mio encodee en base64
# (+33 %) plus le journal de la partie.
MAX_CORPS_OCTETS = int(os.environ.get("MAX_CORPS_OCTETS", str(8 * 1024 * 1024)))

# Frein sur les tentatives de connexion.
# ⚠ CE N'EST PAS LA DEVINETTE DU MOT DE PASSE QUI INQUIETE, C'EST LA MACHINE.
# `_empreinte` fait du scrypt a n=2^14, soit 16 Mio et plusieurs dizaines de
# millisecondes PAR TENTATIVE, et `ThreadingHTTPServer` cree un fil par requete
# sans plafond. Le cout du hachage, qui protege du vol de la base, devient une
# amplification des qu'on peut le declencher a volonte : un flot de tentatives
# toutes fausses suffit a epuiser un VPS a deux vCPU.
TENTATIVES_CONNEXION = int(os.environ.get("TENTATIVES_CONNEXION", "10"))
FENETRE_CONNEXION = int(os.environ.get("FENETRE_CONNEXION", "900"))

sys.path.insert(0, os.path.join(RACINE_JEU, "tools"))
import config_serveur  # noqa: E402  (dependant de sys.path ci-dessus)


# --------------------------------------------------------------------------
# Etat
# --------------------------------------------------------------------------
class Partie:
    """L'espace de jeu d'UNE personne : son moteur, son port, ses liens.

    ⚠ CE N'EST PAS UNE TABLE JETABLE. L'emplacement appartient au compte, et
    ses dossiers (decks, campagnes, hauts faits, sauvegardes) survivent a
    l'arret du moteur. Ne JAMAIS les effacer au demarrage : c'est tout
    l'interet d'avoir un compte.
    """

    def __init__(self, emplacement: int, code: str, nom: str) -> None:
        self.emplacement = emplacement
        self.port = PORT_BASE + emplacement
        self.code = code
        self.nom = nom
        self.processus: subprocess.Popen | None = None
        self.mot_de_passe = ""
        self.cles_sieges: list[str] = []
        self.debut = time.time()
        # Combien de sieges l'hote veut ouvrir. 1 = il joue seul, et aucun
        # lien d'invitation ne lui est propose.
        # ⚠ Les QUATRE cles existent toujours (voir `lancer_jeu`) : ce nombre
        # ne decide que de ce qu'on AFFICHE. Les sieges non distribues
        # restent verrouilles par une cle que personne n'a.
        self.joueurs = 1
        # Jeton que le MOTEUR presente au site pour parler en son nom (liste
        # des joueurs, tchat). Il ne sort jamais du serveur : le navigateur ne
        # le voit pas, c'est le moteur qui appelle le site en 127.0.0.1.
        self.jeton_site = ""

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
        # ⚠ Borne sur les cles REELLEMENT detenues, pas sur `joueurs` seul :
        # un siege sans cle produirait un lien `key=` vide, c'est-a-dire une
        # place ouverte a qui devine l'adresse.
        for siege in range(min(self.joueurs, len(self.cles_sieges))):
            cle = self.cles_sieges[siege]
            sortie.append({
                "siege": siege,
                "libelle": "Toi" if siege == 0 else f"Invite {siege}",
                "url": f"{base}/claim_seat?p={siege}&key={cle}&to=salon",
            })
        return sortie

    def lien_hote(self) -> str:
        """L'adresse ou l'on DEPOSE le proprietaire du compte.

        `to=prepare` mene a l'ecran « Rassemble tes heros », c'est-a-dire la ou
        il atterrissait autrefois en ouvrant l'adresse du moteur a la main. Le
        `claim_seat` au passage lui pose le cookie du siege 0 : sans lui, le
        moteur ne le reconnaitrait pas comme l'hote et lui refuserait les cles
        d'invitation.
        """
        cle = self.cles_sieges[0] if self.cles_sieges else ""
        return f"{self.base_url()}/claim_seat?p=0&key={cle}&to=prepare"

    def solo(self) -> bool:
        return self.joueurs <= 1

    def vivant(self) -> bool:
        return self.processus is not None and self.processus.poll() is None


PARTIES: dict[str, Partie] = {}          # code -> Partie
EMPLACEMENTS: dict[int, str] = {}        # emplacement -> code
JETONS_SITE: dict[str, str] = {}         # jeton -> pseudo (voir Partie.jeton_site)
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
    # Le bouton « Administration » du jeu n'existe que si cette cle est
    # renseignee, et elle ne l'est que pour l'administrateur : le moteur ne
    # sait rien des comptes du site, c'est ici qu'on le lui dit.
    if partie.code == ADMIN:
        racine = f"https://{DOMAINE}" if DOMAINE else f"http://127.0.0.1:{PORT_SITE}"
        cfg["site_admin_url"] = racine + "/admin"
    # Liste des joueurs et tchat : le MOTEUR interroge le site en local, et le
    # navigateur ne parle qu'a son propre domaine. Sans ce detour il faudrait
    # ouvrir le site aux requetes croisees de p1..p20 et desserrer le SameSite
    # du cookie de session, pour un service qui n'en vaut pas le prix.
    cfg["site_interne"] = f"http://127.0.0.1:{PORT_SITE}"
    cfg["site_jeton"] = partie.jeton_site

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


def _port_libre(port: int) -> bool:
    """Vrai si personne ne tient ce port en ecoute.

    ⚠ ON TESTE LA PRISE, PAS LA REPONSE HTTP, et c'est toute la difference.
    `_moteur_repond` ne voit qu'un moteur qui sert encore des pages ; un
    processus survivant qui tient la prise sans rien servir passerait au
    travers, et c'est precisement celui-la qui fait echouer le demarrage
    suivant sur « Address already in use ».
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as prise:
        prise.settimeout(1)
        try:
            prise.connect(("127.0.0.1", port))
        except OSError:
            return True
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


def jeu_de(pseudo: str):
    """L'espace de jeu ALLUME de cette personne, ou None."""
    return PARTIES.get(pseudo)


def lancer_jeu(pseudo: str, joueurs: int = 1) -> Partie:
    """Allume le moteur de cette personne, sur SON emplacement.

    ⚠ AUCUN EFFACEMENT ICI. `_nettoyer_emplacement` existe toujours, mais
    n'est plus appele au demarrage : il ne sert qu'a une remise a zero
    demandee explicitement. Le premier montage effaçait les dossiers a chaque
    ouverture, ce qui detruisait decks et campagnes entre deux visites.
    """
    joueurs = max(1, min(4, joueurs))
    # ⚠ ACHEVER LE PRECEDENT AVANT DE RECREER. Une partie morte etait
    # simplement ECRASEE dans `PARTIES` : `eteindre_jeu` n'etait jamais appele
    # sur elle, donc `os.killpg` non plus, et les enfants du lanceur
    # survivaient a leur parent en gardant le port. Le nouveau moteur mourait
    # alors sur « Address already in use », l'utilisateur lisait « Le moteur
    # s'est arrete au demarrage », et le cycle se repetait a chaque `/entrer`
    # sans issue automatique. Le faucheur ne voyait rien : il ne juge que
    # `partie.vivant()`.
    # ⚠ HORS DU VERROU : `eteindre_jeu` prend `VERROU`, qui n'est pas
    # reentrant. L'appeler dedans figerait le service.
    deja = PARTIES.get(pseudo)
    if deja is not None and not deja.vivant():
        eteindre_jeu(pseudo)

    with VERROU:
        deja = PARTIES.get(pseudo)
        if deja is not None and deja.vivant():
            deja.joueurs = joueurs
            return deja
        emplacement = emplacement_de(pseudo)
        if emplacement is None:
            raise RuntimeError("Aucun espace de jeu ne t'est attribue.")
        partie = Partie(emplacement, pseudo, f"Jeu de {pseudo}")
        # ⚠ LE MOT DE PASSE DU MOTEUR NE CHANGE PLUS. Il appartient au compte
        # (colonne `mdp_jeu`) : le tirer a chaque allumage perimait le cookie
        # deja pose dans le navigateur des le moindre redemarrage, et laissait
        # son proprietaire devant une demande de mot de passe qu'il ignore.
        partie.mot_de_passe = mot_de_passe_jeu(pseudo)
        # Les cles de SIEGE, elles, changent bien a chaque allumage : un lien
        # d'invitation donne hier ne doit pas rouvrir une place aujourd'hui.
        # QUATRE cles, toujours, meme en solo : un siege sans cle serait un
        # siege ouvert a qui trouve l'adresse.
        partie.cles_sieges = [secrets.token_urlsafe(8) for _ in range(4)]
        partie.joueurs = joueurs
        partie.jeton_site = secrets.token_urlsafe(24)
        JETONS_SITE[partie.jeton_site] = pseudo
        EMPLACEMENTS[emplacement] = pseudo
        PARTIES[pseudo] = partie

    try:
        # ⚠ ET VERIFIER QUE LA PLACE EST VRAIMENT LIBRE. `_moteur_repond`
        # n'etait interroge qu'APRES le `Popen` : le moteur mourait alors sur
        # « Address already in use » et le message ne disait pas pourquoi. On
        # regarde donc avant, et on le dit en toutes lettres, parce que ce
        # cas-la demande un geste a la main.
        if not _port_libre(partie.port):
            raise RuntimeError(
                f"Le port {partie.port} est deja pris par un processus que le "
                f"site ne controle pas. Il faut l'achever a la main "
                f"(sudo fuser -k {partie.port}/tcp) avant de rouvrir cette table.")
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
        eteindre_jeu(pseudo)
        raise


DEMARRAGES: set[str] = set()
ERREURS_DEMARRAGE: dict[str, str] = {}
VERROU_DEMARRAGE = threading.Lock()


def demarrer_en_fond(pseudo: str) -> None:
    """Allume le moteur SANS retenir la requete HTTP.

    ⚠ NE PAS APPELER `lancer_jeu` DEPUIS UNE ROUTE. Le premier allumage peut
    prendre plusieurs minutes : le navigateur abandonnerait bien avant, en ne
    montrant qu'une page blanche. On demarre donc a cote, et la page d'attente
    se rafraichit jusqu'a ce que le moteur reponde.
    """
    with VERROU_DEMARRAGE:
        if pseudo in DEMARRAGES:
            return              # deja en route : ne pas en lancer un second
        DEMARRAGES.add(pseudo)
        ERREURS_DEMARRAGE.pop(pseudo, None)

    def travail() -> None:
        try:
            partie = lancer_jeu(pseudo)
            journal_partie_ouverte(partie, pseudo)
        except Exception as erreur:
            ERREURS_DEMARRAGE[pseudo] = str(erreur)
        finally:
            with VERROU_DEMARRAGE:
                DEMARRAGES.discard(pseudo)

    threading.Thread(target=travail, daemon=True).start()


def eteindre_jeu(code: str) -> bool:
    """Arrete le moteur. ⚠ NE TOUCHE PAS AUX DONNEES : elles appartiennent au
    compte et doivent etre la au prochain allumage."""
    with VERROU:
        partie = PARTIES.pop(code, None)
        if partie is None:
            return False
        EMPLACEMENTS.pop(partie.emplacement, None)
        JETONS_SITE.pop(partie.jeton_site, None)
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
                eteindre_jeu(code)
                journal_partie_fermee(code)


# --------------------------------------------------------------------------
# Comptes
# --------------------------------------------------------------------------
VERROU_COMPTES = threading.Lock()

# Une session dure trois mois. Le but est de ne PLUS retaper son mot de passe
# d'une soiree de jeu a l'autre ; c'est un site prive, a inscription fermee.
DUREE_SESSION_JOURS = 90

SCHEMA = """
CREATE TABLE IF NOT EXISTS comptes (
    pseudo              TEXT PRIMARY KEY,
    email               TEXT UNIQUE,
    sel                 TEXT NOT NULL,
    empreinte           TEXT NOT NULL,
    statut              TEXT NOT NULL DEFAULT 'attente',
    cree                TEXT NOT NULL,
    derniere_connexion  TEXT,
    -- ⚠ L'EMPLACEMENT APPARTIENT AU COMPTE, PAS A LA PARTIE. C'est ce qui
    -- fait qu'on retrouve ses decks, ses campagnes en cours et ses hauts
    -- faits d'une visite a l'autre : le moteur s'arrete, ses dossiers
    -- restent. Consequence assumee : il y a autant de comptes possibles que
    -- d'emplacements.
    -- ⚠ PAS DE `UNIQUE` SUR LA COLONNE : SQLite refuse
    -- `ALTER TABLE ... ADD COLUMN ... UNIQUE` sur une table existante
    -- (« Cannot add a UNIQUE column »), et la migration d'une base deja en
    -- service tombait donc en boucle au demarrage. L'unicite est portee par
    -- l'index partiel ci-dessous, que SQLite accepte dans les deux cas, et
    -- dont la clause WHERE laisse coexister plusieurs comptes sans
    -- emplacement.
    emplacement         INTEGER,
    -- ⚠ MOT DE PASSE DU MOTEUR, ET IL DOIT RESTER STABLE.
    -- Il etait tire au hasard a chaque allumage. Consequence : tout
    -- redemarrage du moteur (mise a jour, plantage, extinction volontaire)
    -- perimait le cookie `session_token` deja pose dans le navigateur, qui
    -- se retrouvait devant une demande de mot de passe QU'IL NE CONNAISSAIT
    -- PAS — le site ne l'affiche nulle part. Il appartient donc au compte,
    -- comme son emplacement. Les cles de SIEGE, elles, continuent de tourner
    -- a chaque allumage : c'est ce qui empeche un lien d'hier de rouvrir une
    -- place aujourd'hui.
    mdp_jeu             TEXT
);
CREATE TABLE IF NOT EXISTS parties (
    code        TEXT PRIMARY KEY,
    nom         TEXT NOT NULL,
    hote        TEXT NOT NULL,
    emplacement INTEGER NOT NULL,
    ouverte_le  TEXT NOT NULL,
    fermee_le   TEXT
);
CREATE INDEX IF NOT EXISTS idx_parties_hote ON parties(hote);
CREATE TABLE IF NOT EXISTS messages (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    pseudo TEXT NOT NULL,
    texte  TEXT NOT NULL,
    quand  TEXT NOT NULL,
    -- NULL = tchat general, lisible par tous les comptes. Un pseudo = message
    -- prive, visible du seul couple expediteur/destinataire.
    destinataire TEXT
);
-- ⚠ LES SESSIONS SONT SUR DISQUE, ET C'EST TOUT L'INTERET.
-- Elles vivaient dans un dictionnaire en memoire : le moindre redemarrage du
-- service — donc chaque deploiement — deconnectait tout le monde, alors que le
-- cookie pose dans le navigateur annonce plusieurs semaines. On retapait son
-- mot de passe sans comprendre pourquoi.
CREATE TABLE IF NOT EXISTS sessions (
    jeton  TEXT PRIMARY KEY,
    pseudo TEXT NOT NULL,
    cree   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_sessions_pseudo ON sessions(pseudo);
CREATE TABLE IF NOT EXISTS invitations (
    jeton       TEXT PRIMARY KEY,
    cree_le     TEXT NOT NULL,
    utilise_par TEXT,
    utilise_le  TEXT
);
-- Rapports de bug. `hote` est le compte proprietaire de la table (celui que
-- designe le jeton de partie) ; `nom` est ce que la personne a tape, et c'est
-- le seul identifiant d'un invite arrive par un lien de siege. Les deux sont
-- gardes : l'un dit ou le bug s'est produit, l'autre a qui repondre.
CREATE TABLE IF NOT EXISTS rapports (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    quand       TEXT NOT NULL,
    hote        TEXT,
    nom         TEXT NOT NULL,
    siege       INTEGER,
    ecran       TEXT,
    description TEXT NOT NULL,
    journal     TEXT,
    capture     TEXT,
    etat        TEXT NOT NULL DEFAULT 'nouveau',
    -- Quand le rapport a ete CLASSE, pas quand il a ete ecrit. La purge se
    -- compte a partir de la, sans quoi un rapport vieux de six mois qu'on
    -- vient tout juste de traiter partirait le lendemain, capture comprise,
    -- avant meme qu'on ait pu s'en reservir.
    traite_le   TEXT
);
CREATE INDEX IF NOT EXISTS idx_rapports_etat ON rapports(etat);
"""


def _cx() -> sqlite3.Connection:
    """Une connexion par appel : `check_same_thread` interdirait le partage
    entre les fils du serveur, et SQLite gere tres bien ce rythme d'ecriture."""
    cx = sqlite3.connect(BASE, timeout=10)
    cx.row_factory = sqlite3.Row
    # WAL : un lecteur ne bloque plus un ecrivain. Sur un site ou l'on consulte
    # la page de validation pendant qu'une partie s'ouvre, ca compte.
    cx.execute("PRAGMA journal_mode=WAL")
    cx.execute("PRAGMA foreign_keys=ON")
    return cx


def initialiser_base() -> None:
    with _cx() as cx:
        cx.executescript(SCHEMA)
        # Reprise des bases anterieures a la colonne `emplacement`.
        colonnes = {r["name"] for r in cx.execute("PRAGMA table_info(comptes)")}
        if "emplacement" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN emplacement INTEGER")
        # ⚠ L'INDEX EST CREE APRES LA COLONNE, ET HORS DU SCHEMA. Place dans
        # `SCHEMA`, `executescript` l'executait AVANT l'ALTER sur une base
        # ancienne, et tombait sur « no such column: emplacement ».
        cx.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_comptes_emplacement"
                   " ON comptes(emplacement) WHERE emplacement IS NOT NULL")
        # Presence : meme precaution que pour `emplacement`, la colonne est
        # ajoutee hors du SCHEMA pour les bases deja en service.
        if "vu_le" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN vu_le TEXT")
        # Meme precaution pour les bases creees avant le tchat prive.
        colonnes_msg = {r["name"] for r in cx.execute("PRAGMA table_info(messages)")}
        if "destinataire" not in colonnes_msg:
            cx.execute("ALTER TABLE messages ADD COLUMN destinataire TEXT")
        if "mdp_jeu" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN mdp_jeu TEXT")
        # Meme precaution pour les bases creees avant la purge des rapports.
        colonnes_rap = {r["name"] for r in cx.execute("PRAGMA table_info(rapports)")}
        if "traite_le" not in colonnes_rap:
            cx.execute("ALTER TABLE rapports ADD COLUMN traite_le TEXT")
    _migrer_depuis_json()
    _attribuer_emplacements_manquants()


def _attribuer_emplacements_manquants() -> None:
    """Donne un emplacement aux comptes qui n'en ont pas encore."""
    with _cx() as cx:
        pris = {r["emplacement"] for r in cx.execute(
            "SELECT emplacement FROM comptes WHERE emplacement IS NOT NULL")}
        for c in cx.execute(
                "SELECT pseudo FROM comptes WHERE emplacement IS NULL ORDER BY cree"):
            libre = next((n for n in range(1, NB_EMPLACEMENTS + 1) if n not in pris), None)
            if libre is None:
                print(f"  ⚠ plus d'emplacement libre pour « {c['pseudo']} »")
                break
            cx.execute("UPDATE comptes SET emplacement = ? WHERE pseudo = ?",
                       (libre, c["pseudo"]))
            pris.add(libre)


def mot_de_passe_jeu(pseudo: str) -> str:
    """Le mot de passe que le moteur de CE compte exigera, cree au besoin.

    Stable par construction : voir le commentaire de la colonne `mdp_jeu`.
    """
    with _cx() as cx:
        ligne = cx.execute("SELECT mdp_jeu FROM comptes WHERE pseudo=?",
                           (pseudo,)).fetchone()
        if ligne is not None and ligne["mdp_jeu"]:
            return ligne["mdp_jeu"]
        nouveau = secrets.token_urlsafe(9)
        cx.execute("UPDATE comptes SET mdp_jeu=? WHERE pseudo=?", (nouveau, pseudo))
    return nouveau


def revoquer_mot_de_passe_jeu(pseudo: str) -> None:
    """Perime le laissez-passer du moteur de ce compte.

    ⚠ LE SEUL MOYEN DE FERMER LA PORTE A UN INVITE D'HIER. Le cookie
    `session_token` que le moteur pose pour UN AN est une fonction
    deterministe de `mdp_jeu` (`web_server.py` : `md5(password)`), et c'est le
    seul controle sur le plateau, les decks, le catalogue et le WebSocket. Les
    cles de SIEGE tournent bien a chaque allumage, mais elles ne protegent
    qu'un siege : `allowed_seats` accorde tout siege que personne ne tient, si
    bien qu'un invite revenu seul dans une table vide les obtient tous. Tant
    que `mdp_jeu` ne tourne jamais, son cookie de la semaine derniere ouvre
    encore l'espace de jeu aujourd'hui.

    ⚠ A N'APPELER QU'A L'EXTINCTION VOLONTAIRE. Le faucheur et les plantages
    ne doivent PAS y toucher : une table qui redemarre apres un incident
    remettrait sinon son proprietaire devant une demande de mot de passe que
    le site ne lui affiche nulle part (c'est la regression que `3271e6f` a
    corrigee). Mettre la colonne a NULL suffit : `mot_de_passe_jeu` en tire un
    nouveau au prochain allumage.
    """
    with _cx() as cx:
        cx.execute("UPDATE comptes SET mdp_jeu=NULL WHERE pseudo=?", (pseudo,))


def emplacement_de(pseudo: str):
    ligne = compte(pseudo)
    return ligne["emplacement"] if ligne else None


def _migrer_depuis_json() -> None:
    """Reprend l'ancien `comptes.json` s'il existe et que la base est vide.

    ⚠ SANS CETTE REPRISE, LE PASSAGE A LA BASE EFFACERAIT LES COMPTES DEJA
    VALIDES. Le fichier est conserve tel quel : on ne detruit pas la seule
    trace d'un etat anterieur.
    """
    if not os.path.isfile(FICHIER_COMPTES):
        return
    with _cx() as cx:
        if cx.execute("SELECT COUNT(*) FROM comptes").fetchone()[0]:
            return
        try:
            anciens = json.load(open(FICHIER_COMPTES, encoding="utf-8"))
        except (OSError, ValueError):
            return
        for pseudo, c in anciens.items():
            cx.execute(
                "INSERT OR IGNORE INTO comptes"
                " (pseudo, email, sel, empreinte, statut, cree)"
                " VALUES (?, NULL, ?, ?, ?, ?)",
                (pseudo, c.get("sel", ""), c.get("empreinte", ""),
                 c.get("statut", "attente"), c.get("cree", "")))
        print(f"  base : {len(anciens)} compte(s) repris depuis {FICHIER_COMPTES}")


def _empreinte(mot_de_passe: str, sel: str) -> str:
    """scrypt, de la bibliotheque standard. Aucune dependance a installer."""
    brut = hashlib.scrypt(mot_de_passe.encode("utf-8"), salt=bytes.fromhex(sel),
                          n=2 ** 14, r=8, p=1, dklen=32)
    return brut.hex()


def _maintenant() -> str:
    return time.strftime("%Y-%m-%d %H:%M")


def compte(identifiant: str):
    """Un compte par son PSEUDO OU son EMAIL, au choix de qui se connecte."""
    ident = (identifiant or "").strip().lower()
    if not ident:
        return None
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM comptes WHERE pseudo = ? OR email = ?",
            (ident, ident)).fetchone()


def statut_de(pseudo: str) -> str:
    ligne = compte(pseudo)
    return ligne["statut"] if ligne else ""


def inscrire(pseudo: str, email: str, mot_de_passe: str, jeton: str = "") -> str:
    pseudo = (pseudo or "").strip().lower()
    email = (email or "").strip().lower()
    if not (3 <= len(pseudo) <= 24) or not pseudo.replace("_", "").replace("-", "").isalnum():
        raise ValueError("Pseudo invalide : 3 a 24 caracteres, lettres, chiffres, - et _.")
    # Controle volontairement minimal : on verifie qu'une adresse ressemble a
    # une adresse, pas qu'elle existe. Seule la validation manuelle fait foi.
    if "@" not in email or "." not in email.split("@")[-1] or len(email) < 6:
        raise ValueError("Adresse e-mail invalide.")
    if len(mot_de_passe or "") < 8:
        raise ValueError("Mot de passe trop court : 8 caracteres au minimum.")
    if not INSCRIPTION_LIBRE and not invitation_valide(jeton) and pseudo != ADMIN:
        raise ValueError("Il faut un lien d'invitation pour creer un compte ici.")
    with VERROU_COMPTES, _cx() as cx:
        if cx.execute("SELECT 1 FROM comptes WHERE pseudo = ?", (pseudo,)).fetchone():
            raise ValueError("Ce pseudo est deja pris.")
        if cx.execute("SELECT 1 FROM comptes WHERE email = ?", (email,)).fetchone():
            raise ValueError("Cette adresse est deja utilisee.")
        # ⚠ LE PLAFOND NE COMPTE QUE LES COMPTES VALIDES. Sinon une vague
        # d'inscriptions en attente suffirait a bloquer les vraies demandes.
        valides = cx.execute(
            "SELECT COUNT(*) FROM comptes WHERE statut = 'valide'").fetchone()[0]
        if valides >= MAX_COMPTES and pseudo != ADMIN:
            raise ValueError(f"Le site est complet ({MAX_COMPTES} comptes).")
        # ⚠ LE JETON EST RELU ET CONSOMME DANS LA MEME TRANSACTION que la
        # creation du compte. Le verifier avant puis le consommer apres
        # laisserait deux personnes cliquant en meme temps sur le meme lien
        # creer deux comptes : la fenetre est etroite, elle n'est pas nulle.
        invite = False
        if jeton:
            ligne = cx.execute(
                "SELECT utilise_par FROM invitations WHERE jeton = ?", (jeton,)).fetchone()
            invite = ligne is not None and ligne["utilise_par"] is None
        # Un lien d'invitation VAUT validation : c'est tout son interet.
        # L'administrateur, lui, est valide d'office, sans quoi personne ne
        # pourrait valider le premier compte.
        statut = "valide" if (invite or pseudo == ADMIN) else "attente"
        sel = secrets.token_bytes(16).hex()
        pris = {r["emplacement"] for r in cx.execute(
            "SELECT emplacement FROM comptes WHERE emplacement IS NOT NULL")}
        libre = next((n for n in range(1, NB_EMPLACEMENTS + 1) if n not in pris), None)
        if libre is None:
            raise ValueError("Plus aucun espace de jeu disponible.")
        cx.execute(
            "INSERT INTO comptes"
            " (pseudo, email, sel, empreinte, statut, cree, emplacement)"
            " VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pseudo, email, sel, _empreinte(mot_de_passe, sel), statut,
             _maintenant(), libre))
        if invite:
            cx.execute(
                "UPDATE invitations SET utilise_par = ?, utilise_le = ? WHERE jeton = ?",
                (pseudo, _maintenant(), jeton))
    return pseudo


# Horodatage des tentatives de connexion, par cle. Meme compteur glissant que
# `debit_rapport_ok`, avec un verrou en plus : ici deux fils peuvent tomber sur
# la meme cle en meme temps, et c'est meme le scenario qu'on redoute.
# En memoire : un redemarrage remet les compteurs a zero, ce qui est sans
# consequence : le frein protege d'un flot, pas d'un adversaire patient.
_TENTATIVES: dict[str, list[float]] = {}
_VERROU_TENTATIVES = threading.Lock()


def attente_connexion(cle: str) -> int:
    """Secondes restant a patienter pour cette cle, 0 si la voie est libre.

    Ne compte RIEN : c'est une lecture. Compter ici obligerait a compter aussi
    les tentatives qu'on refuse, et le frein ne se relacherait jamais.
    """
    maintenant = time.time()
    with _VERROU_TENTATIVES:
        recents = [t for t in _TENTATIVES.get(cle, []) if maintenant - t < FENETRE_CONNEXION]
        # ⚠ UNE LECTURE NE CREE RIEN. Ecrire la cle a chaque passage faisait
        # retenir une entree PAR REQUETE, y compris pour celles qu'on refuse :
        # mille requetes freinees, mille cles. Et une fenetre que le temps a
        # videe s'en va, sinon le compteur ne redescendrait jamais.
        if recents:
            _TENTATIVES[cle] = recents
        else:
            _TENTATIVES.pop(cle, None)
        if len(recents) < TENTATIVES_CONNEXION:
            return 0
        return max(1, int(FENETRE_CONNEXION - (maintenant - recents[0])) + 1)


def compter_tentative(cle: str) -> None:
    """Retient une tentative de connexion pour cette cle."""
    with _VERROU_TENTATIVES:
        _TENTATIVES.setdefault(cle, []).append(time.time())


def oublier_tentatives(cle: str) -> None:
    """Efface le compteur : une connexion REUSSIE ne doit pas laisser derriere
    elle un frein que ses propres fautes de frappe ont serre."""
    with _VERROU_TENTATIVES:
        _TENTATIVES.pop(cle, None)


def cle_frein(adresse: str) -> str:
    """La cle a freiner pour cette tentative : l'ADRESSE, et elle seule.

    ⚠ PLUS DE FREIN PAR COMPTE, ET C'EST VOLONTAIRE. Il en existait un, qui
    rendait un 429 des dix tentatives fausses sur un pseudo, d'ou qu'elles
    viennent. Il retournait l'arme : dix requetes lancees depuis dix adresses
    sur le pseudo de quelqu'un lui fermaient SA porte un quart d'heure,
    renouvelable a volonte, avec son bon mot de passe entre les mains. Un
    frein ne doit jamais refuser un mot de passe correct.

    Ce qu'on defend ici, c'est le PROCESSEUR : `_empreinte` fait du scrypt, et
    la limiter par adresse suffit pour ca. Ce que le frein par compte pretendait
    ajouter, l'attaquant reparti sur mille adresses, un delai ne le lui prend
    pas non plus : il envoie en parallele et n'attend pas la reponse, pendant
    que le delai, lui, nous couterait un fil par tentative.

    ⚠ ET LA CLE EST BORNEE. Ce qui entre dans un dictionnaire qui vit aussi
    longtemps que le service ne doit jamais avoir la taille que veut celui qui
    l'envoie.
    """
    return "ip:" + (adresse or "?")[:64]


def delai_lisible(secondes: int) -> str:
    """« 40 secondes », « 3 minutes » : ce qu'on annonce a quelqu'un qui
    attend. Un nombre de secondes a quatre chiffres ne dit rien a personne."""
    if secondes < 90:
        return "%d secondes" % max(1, secondes)
    return "%d minutes" % round(secondes / 60)


def verifier(identifiant: str, mot_de_passe: str) -> str:
    ligne = compte(identifiant)
    if ligne is None:
        raise ValueError("Identifiant ou mot de passe incorrect.")
    # `compare_digest` : comparaison a temps constant, pour ne pas laisser
    # fuir l'empreinte par le temps de reponse.
    if not secrets.compare_digest(_empreinte(mot_de_passe, ligne["sel"]), ligne["empreinte"]):
        raise ValueError("Identifiant ou mot de passe incorrect.")
    if ligne["statut"] != "valide":
        raise ValueError("Ton compte attend encore ma validation.")
    with _cx() as cx:
        cx.execute("UPDATE comptes SET derniere_connexion = ? WHERE pseudo = ?",
                   (_maintenant(), ligne["pseudo"]))
    return ligne["pseudo"]


def changer_statut(pseudo: str, statut: str) -> None:
    if statut not in ("valide", "attente", "refuse"):
        return
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("UPDATE comptes SET statut = ? WHERE pseudo = ?", (statut, pseudo))
    if statut != "valide":
        # Un compte devalide ne doit pas continuer sa session en cours.
        fermer_sessions_de(pseudo)


def liste_comptes():
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM comptes ORDER BY"
            " CASE statut WHEN 'attente' THEN 0 WHEN 'valide' THEN 1 ELSE 2 END,"
            " pseudo").fetchall()


def nb_valides() -> int:
    with _cx() as cx:
        return cx.execute(
            "SELECT COUNT(*) FROM comptes WHERE statut = 'valide'").fetchone()[0]


def journal_partie_ouverte(partie, hote: str) -> None:
    with _cx() as cx:
        cx.execute(
            "INSERT OR REPLACE INTO parties"
            " (code, nom, hote, emplacement, ouverte_le, fermee_le)"
            " VALUES (?, ?, ?, ?, ?, NULL)",
            (partie.code, partie.nom, hote, partie.emplacement, _maintenant()))


def journal_partie_fermee(code: str) -> None:
    with _cx() as cx:
        cx.execute("UPDATE parties SET fermee_le = ? WHERE code = ? AND fermee_le IS NULL",
                   (_maintenant(), code))


def dernieres_parties(combien: int = 25):
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM parties ORDER BY ouverte_le DESC, rowid DESC LIMIT ?",
            (combien,)).fetchall()


def creer_invitation() -> str:
    """Un jeton a USAGE UNIQUE qui vaut validation.

    C'est le chemin normal : celui qui recoit le lien entre directement, sans
    passer par la file d'attente. L'inscription libre reste possible, mais
    elle, elle attend une validation a la main.
    """
    jeton = secrets.token_urlsafe(16)
    with _cx() as cx:
        cx.execute("INSERT INTO invitations (jeton, cree_le) VALUES (?, ?)",
                   (jeton, _maintenant()))
    return jeton


def invitation_valide(jeton: str) -> bool:
    if not jeton:
        return False
    with _cx() as cx:
        ligne = cx.execute(
            "SELECT utilise_par FROM invitations WHERE jeton = ?", (jeton,)).fetchone()
    return ligne is not None and ligne["utilise_par"] is None


def invitations_libres():
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM invitations WHERE utilise_par IS NULL"
            " ORDER BY cree_le DESC").fetchall()


def invitations_utilisees(combien: int = 15):
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM invitations WHERE utilise_par IS NOT NULL"
            " ORDER BY utilise_le DESC LIMIT ?", (combien,)).fetchall()


def supprimer_invitation(jeton: str) -> None:
    with _cx() as cx:
        cx.execute("DELETE FROM invitations WHERE jeton = ? AND utilise_par IS NULL",
                   (jeton,))


# Au-dela de ce delai sans signe de vie, on ne dit plus « en ligne ».
# Le client se signale toutes les 60 s : deux minutes laissent passer un
# battement manque sans faire clignoter la liste.
DELAI_PRESENCE = 120


def toucher_presence(pseudo: str) -> None:
    with _cx() as cx:
        cx.execute("UPDATE comptes SET vu_le=? WHERE pseudo=?", (_maintenant(), pseudo))


def _secondes_depuis(quand):
    """Secondes ecoulees depuis cet horodatage, ou None s'il est illisible."""
    from datetime import datetime
    try:
        return (datetime.now() - datetime.fromisoformat(quand)).total_seconds()
    except (TypeError, ValueError):
        return None


def _il_y_a(quand: str) -> str:
    """« a l'instant », « il y a 3 min », « il y a 2 h », « il y a 4 j »."""
    ecart = _secondes_depuis(quand)
    if ecart is None:
        return ""
    if ecart < 90:
        return "a l'instant"
    if ecart < 5400:
        return "il y a %d min" % round(ecart / 60)
    if ecart < 172800:
        return "il y a %d h" % round(ecart / 3600)
    return "il y a %d j" % round(ecart / 86400)


def presence():
    """Qui est la, et dans quel etat.

    Trois etats, et non deux : savoir que quelqu'un est deja EN PARTIE evite
    de l'inviter pour rien. « En ligne » vient de la derniere fois qu'il s'est
    signale ; « en partie » vient du moteur reellement allume, qui est un fait
    et non une declaration.
    """
    sortie = []
    for ligne in liste_comptes():
        if ligne["statut"] != "valide":
            continue
        pseudo = ligne["pseudo"]
        partie = PARTIES.get(pseudo)
        vu = ligne["vu_le"] if "vu_le" in ligne.keys() else None
        ecart = _secondes_depuis(vu) if vu else None
        if partie is not None and partie.vivant():
            etat, detail = "partie", "en partie"
        elif ecart is not None and ecart < DELAI_PRESENCE:
            etat, detail = "ligne", "en ligne"
        elif vu:
            etat, detail = "absent", "vu " + _il_y_a(vu)
        else:
            etat, detail = "absent", "jamais venu"
        sortie.append({"pseudo": pseudo, "etat": etat, "detail": detail})
    return sortie


# On ne garde pas l'historique complet : un tchat de salon sert a se retrouver,
# pas a archiver. Au-dela, les plus anciens partent.
MESSAGES_GARDES = 200
# Les conversations privees sont plus nombreuses et plus lentes a defiler :
# une seule generale se partage entre tous, les privees se multiplient.
PRIVES_GARDES = 500
TAILLE_MESSAGE = 500


# --------------------------------------------------------------------------
# Rapports de bug
# --------------------------------------------------------------------------

# Horodatage des derniers envois, par compte hote. En memoire : un redemarrage
# remet les compteurs a zero, ce qui est sans consequence — la limite protege
# d'une boucle, pas d'un adversaire patient.
_ENVOIS_RAPPORTS: dict[str, list[float]] = {}


def debit_rapport_ok(hote: str) -> bool:
    """Vrai si `hote` peut encore envoyer un rapport dans l'heure qui court."""
    maintenant = time.time()
    recents = [t for t in _ENVOIS_RAPPORTS.get(hote, []) if maintenant - t < 3600]
    _ENVOIS_RAPPORTS[hote] = recents
    if len(recents) >= RAPPORTS_PAR_HEURE:
        return False
    recents.append(maintenant)
    return True


def enregistrer_rapport(hote: str, champs: dict) -> int:
    """Range un rapport et rend son numero. La capture part sur disque.

    Rien n'est refuse pour cause de champ trop long : on TRONQUE. Un rapport
    ampute vaut mieux qu'un rapport perdu, et la personne qui l'envoie n'a
    aucun moyen de savoir ce qui passe.
    """
    nom = " ".join(str(champs.get("nom") or "").split())[:80] or "anonyme"
    description = str(champs.get("description") or "").strip()[:MAX_DESCRIPTION_CARACTERES]
    journal = str(champs.get("journal") or "")[:MAX_JOURNAL_CARACTERES]
    ecran = " ".join(str(champs.get("ecran") or "").split())[:120]
    try:
        siege = int(champs.get("siege") or 0)
    except (TypeError, ValueError):
        siege = 0

    capture = None
    brut = champs.get("capture") or ""
    if brut:
        capture = _ecrire_capture(brut)

    with _cx() as cx:
        cur = cx.execute(
            "INSERT INTO rapports (quand, hote, nom, siege, ecran, description,"
            " journal, capture, etat) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'nouveau')",
            (_maintenant(), hote, nom, siege, ecran, description, journal, capture))
        return int(cur.lastrowid or 0)


def _ecrire_capture(donnee: str) -> str | None:
    """Decode une capture « data:image/... ;base64,... » vers un fichier.

    Rend le nom du fichier, ou None si l'image est illisible ou trop lourde.
    On ne fait CONFIANCE A RIEN de ce qui arrive : ni au type annonce, ni a la
    taille. Le type est deduit des premiers octets, pas de l'etiquette.
    """
    try:
        entete, _, corps = donnee.partition(",")
        if "base64" not in entete or not corps:
            return None
        image = base64.b64decode(corps, validate=True)
    except Exception:
        return None
    if not image or len(image) > MAX_CAPTURE_OCTETS:
        return None
    # Signature du fichier, jamais l'etiquette annoncee : c'est elle qui decide
    # de l'extension, donc du type que le navigateur se verra servir.
    if image[1:4] == b"PNG":
        ext = "png"
    elif image[:2] == bytes((0xFF, 0xD8)):
        ext = "jpg"
    elif image[:4] == b"RIFF" and image[8:12] == b"WEBP":
        ext = "webp"
    else:
        return None
    os.makedirs(DOSSIER_RAPPORTS, exist_ok=True)
    nom = secrets.token_hex(16) + "." + ext
    with open(os.path.join(DOSSIER_RAPPORTS, nom), "wb") as f:
        f.write(image)
    return nom


def liste_rapports(limite: int = 60) -> list[dict]:
    with _cx() as cx:
        return [dict(r) for r in cx.execute(
            "SELECT * FROM rapports ORDER BY id DESC LIMIT ?", (limite,))]


def nb_rapports_nouveaux() -> int:
    with _cx() as cx:
        r = cx.execute("SELECT COUNT(*) AS n FROM rapports WHERE etat = 'nouveau'").fetchone()
    return int(r["n"] if r else 0)


def changer_etat_rapport(numero: int, etat: str) -> None:
    if etat not in ETATS_RAPPORT:
        return
    # `traite_le` est pose au classement et efface si l'on rouvre : c'est de
    # cette date que part le compte a rebours de la purge, jamais de celle de
    # l'envoi. Un vieux rapport qu'on vient de traiter garde ses trente jours.
    quand = _maintenant() if etat == "traite" else None
    with _cx() as cx:
        cx.execute("UPDATE rapports SET etat = ?, traite_le = ? WHERE id = ?",
                   (etat, quand, numero))


def purger_rapports_traites(jours: int = JOURS_RAPPORTS_TRAITES) -> int:
    """Efface les rapports classes « traite » depuis plus de `jours`.

    ⚠ LA CAPTURE ET LA LIGNE PARTENT ENSEMBLE. Effacer l'image seule
    laisserait la base renvoyer vers un fichier absent ; effacer la ligne seule
    laisserait l'image grossir le disque sans que rien n'y renvoie plus. C'est
    la meme regle que `supprimer_rapport`, appliquee en gros.

    Rend le nombre de rapports effaces.
    """
    from datetime import datetime, timedelta
    if jours < 0:
        return 0
    # Meme format que `_maintenant()` : la comparaison de chaines suffit, ces
    # horodatages se trient dans l'ordre alphabetique comme dans le temps.
    limite = (datetime.now() - timedelta(days=jours)).strftime("%Y-%m-%d %H:%M")
    efface = 0
    with _cx() as cx:
        # ⚠ TOLERER UNE BASE PAS ENCORE MIGREE. Cette fonction est appelee par
        # la purge hebdomadaire, dans un AUTRE processus que le service : lui
        # faire lancer la migration ferait deux `ALTER TABLE` concurrents pour
        # rien. Sans la colonne, on retombe sur la date d'envoi.
        colonnes = {r["name"] for r in cx.execute("PRAGMA table_info(rapports)")}
        champ = "COALESCE(traite_le, quand)" if "traite_le" in colonnes else "quand"
        lignes = cx.execute(
            "SELECT id, capture FROM rapports WHERE etat = 'traite'"
            " AND %s < ?" % champ, (limite,)).fetchall()
        for r in lignes:
            if r["capture"]:
                try:
                    os.remove(os.path.join(DOSSIER_RAPPORTS, os.path.basename(r["capture"])))
                except OSError:
                    pass
            cx.execute("DELETE FROM rapports WHERE id = ?", (r["id"],))
            efface += 1
    return efface


def supprimer_rapport(numero: int) -> None:
    """Efface le rapport ET sa capture : laisser l'image seule sur le disque
    ferait grossir le dossier sans que rien n'y renvoie plus."""
    with _cx() as cx:
        r = cx.execute("SELECT capture FROM rapports WHERE id = ?", (numero,)).fetchone()
        if r and r["capture"]:
            try:
                os.remove(os.path.join(DOSSIER_RAPPORTS, r["capture"]))
            except OSError:
                pass
        cx.execute("DELETE FROM rapports WHERE id = ?", (numero,))


def dire(pseudo: str, texte: str, destinataire: str = "") -> None:
    """Ecrit un message. `destinataire` vide = tchat general."""
    texte = " ".join(str(texte or "").split())[:TAILLE_MESSAGE]
    if not texte:
        return
    a = (destinataire or "").strip().lower() or None
    # ⚠ On n'ecrit un message prive que vers un compte QUI EXISTE. Sans ce
    # controle, une faute de frappe ecrirait dans une conversation que
    # personne ne lira jamais, sans que l'expediteur s'en doute.
    if a is not None and compte(a) is None:
        return
    with _cx() as cx:
        cx.execute("INSERT INTO messages (pseudo, texte, quand, destinataire)"
                   " VALUES (?,?,?,?)", (pseudo, texte, _maintenant(), a))
        # ⚠ DEUX PURGES SEPAREES. Une seule, globale, aurait laisse une
        # conversation generale animee effacer les messages prives de tout le
        # monde : ils partagent la meme table, pas le meme usage.
        cx.execute("DELETE FROM messages WHERE destinataire IS NULL AND id NOT IN"
                   " (SELECT id FROM messages WHERE destinataire IS NULL"
                   "  ORDER BY id DESC LIMIT ?)", (MESSAGES_GARDES,))
        cx.execute("DELETE FROM messages WHERE destinataire IS NOT NULL AND id NOT IN"
                   " (SELECT id FROM messages WHERE destinataire IS NOT NULL"
                   "  ORDER BY id DESC LIMIT ?)", (PRIVES_GARDES,))


def messages_depuis(depuis: int = 0, moi: str = "", avec: str = ""):
    """Les messages d'UNE conversation, apres `depuis`.

    Sans `avec`, c'est le tchat general. Avec, c'est la conversation privee
    entre `moi` et `avec`, dans les deux sens.
    """
    avec = (avec or "").strip().lower()
    with _cx() as cx:
        if not avec:
            lignes = cx.execute(
                "SELECT id, pseudo, texte, quand FROM messages"
                " WHERE destinataire IS NULL AND id > ?"
                " ORDER BY id LIMIT ?", (depuis, MESSAGES_GARDES)).fetchall()
        else:
            lignes = cx.execute(
                "SELECT id, pseudo, texte, quand FROM messages WHERE id > ?"
                " AND ((pseudo=? AND destinataire=?) OR (pseudo=? AND destinataire=?))"
                " ORDER BY id LIMIT ?",
                (depuis, moi, avec, avec, moi, MESSAGES_GARDES)).fetchall()
    return [{"id": l["id"], "pseudo": l["pseudo"], "texte": l["texte"],
             "quand": l["quand"][11:16]} for l in lignes]


def derniers_prives(moi: str) -> dict:
    """Pour chaque correspondant, l'identifiant du dernier message echange.

    Le client le compare a ce qu'il a deja affiche pour signaler d'une pastille
    les conversations ou quelque chose est arrive. Sans cela, un message prive
    resterait invisible tant qu'on n'ouvre pas la bonne conversation.
    """
    with _cx() as cx:
        lignes = cx.execute(
            "SELECT CASE WHEN pseudo=? THEN destinataire ELSE pseudo END AS qui,"
            "       MAX(id) AS dernier FROM messages"
            " WHERE destinataire IS NOT NULL AND (pseudo=? OR destinataire=?)"
            " GROUP BY qui", (moi, moi, moi)).fetchall()
    return {l["qui"]: l["dernier"] for l in lignes if l["qui"]}


def ouvrir_session(pseudo: str) -> str:
    jeton = secrets.token_urlsafe(24)
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("INSERT INTO sessions (jeton, pseudo, cree) VALUES (?, ?, ?)",
                   (jeton, pseudo, _maintenant()))
    return jeton


def pseudo_de_session(jeton: str) -> str | None:
    """Le pseudo derriere un jeton, ou None s'il ne vaut plus rien.

    Trois raisons de refuser : jeton inconnu, session trop vieille, compte qui
    n'est plus valide. Le statut est relu EN BASE a chaque fois — devalider un
    compte doit couper sa session en cours, pas seulement ses connexions
    futures.
    """
    from datetime import datetime, timedelta
    if not jeton:
        return None
    with _cx() as cx:
        ligne = cx.execute("SELECT pseudo, cree FROM sessions WHERE jeton = ?",
                           (jeton,)).fetchone()
    if not ligne:
        return None
    try:
        nee = datetime.fromisoformat(ligne["cree"])
    except (TypeError, ValueError):
        nee = None
    if nee is not None and datetime.now() - nee > timedelta(days=DUREE_SESSION_JOURS):
        fermer_session(jeton)
        return None
    pseudo = ligne["pseudo"]
    return pseudo if statut_de(pseudo) == "valide" else None


def fermer_session(jeton: str) -> None:
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("DELETE FROM sessions WHERE jeton = ?", (jeton,))


def fermer_sessions_de(pseudo: str) -> None:
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("DELETE FROM sessions WHERE pseudo = ?", (pseudo,))


# --------------------------------------------------------------------------
# Site
# --------------------------------------------------------------------------
PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{tete}
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
  .choix {{ display:grid; gap:.75rem; margin-bottom:1.5rem; }}
  .choix form {{ display:block; margin:0; }}
  .choix button {{ width:100%; text-align:left; padding:.9rem 1.1rem; }}
  .choix b {{ display:block; font-size:1rem; font-weight:600; }}
  .choix em {{ display:block; font-size:.85rem; font-style:normal; opacity:.75; margin-top:.2rem; }}
  button.calme {{ background:#161b22; color:#e6edf3; border-color:#30363d; }}
  button.calme:hover {{ background:#1c232c; }}
  .places {{ display:flex; gap:.6rem; flex-wrap:wrap; align-items:center; margin:0 0 1.5rem; }}
  .places form {{ display:inline; margin:0; }}
  .places button {{ min-width:5.5rem; }}
  .places span {{ color:#9aa7b4; font-size:.9rem; }}
  .apres {{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center;
           margin-top:1rem; padding-top:.9rem; border-top:1px solid #21262d; }}
  .apres form {{ display:inline; margin:0; }}
  .apres span {{ color:#9aa7b4; font-size:.85rem; }}
  .apres button {{ background:transparent; color:#9aa7b4; border-color:#30363d;
                  font-size:.85rem; padding:.25rem .7rem; min-width:0; }}
  .apres button:hover {{ background:#1c232c; color:#e6edf3; }}
  .apres button[disabled] {{ border-color:#1f6feb; color:#58a6ff; cursor:default; }}
  a.retour {{ color:#58a6ff; font-size:.9rem; }}
  .barre {{ display:flex; justify-content:space-between; align-items:center;
           gap:1rem; margin-bottom:1.5rem; color:#9aa7b4; font-size:.9rem; }}
  .barre a {{ color:#58a6ff; }}
  .avert {{ border:1px solid #9e6a03; background:#1d1a0e; color:#e3b341;
           border-radius:.5rem; padding:.7rem .9rem; margin-bottom:1.5rem; font-size:.9rem; }}
  footer {{ margin-top:2.5rem; color:#6e7681; font-size:.85rem; }}
</style>
<main>
  <h1>NarwhalChampions</h1>
  <p class="sous">{sous}</p>
  {barre}
  {corps}
  <footer>Ton espace de jeu est a toi : tes decks, tes campagnes en cours et
  tes hauts faits t'y attendent d'une fois sur l'autre. Eteindre le jeu
  n'efface rien. Tes invites, eux, rejoignent ta partie par leur lien sans
  avoir besoin d'un compte. Extinction automatique au bout de {heures} h
  d'allumage.</footer>
</main>
"""

def _barre(pseudo: str) -> str:
    admin = ' &middot; <a href="/admin">Administration</a>' if pseudo == ADMIN else ""
    return ('<div class="barre"><span>Connecte : <strong>%s</strong>%s</span>'
            '<a href="/deconnexion">Se deconnecter</a></div>'
            % (html.escape(pseudo), admin))


def page_attente(pseudo: str) -> bytes:
    """Le seul ecran du site entre la connexion et le jeu.

    Il ne s'affiche que le temps que le moteur reponde, puis la balise
    `refresh` renvoie sur `/entrer`, qui redirige vers le jeu. En regime
    normal (moteur deja allume) personne ne voit jamais cette page.
    """
    erreur = ERREURS_DEMARRAGE.get(pseudo, "")
    if erreur:
        tete = ""
        sous = "Quelque chose a coince."
        corps = ('<div class="table">'
                 '<div class="entete"><strong>Ton jeu n\'a pas demarre</strong></div>'
                 '<p class="mdp">%s</p>'
                 '<form method="get" action="/entrer" style="margin-top:1rem">'
                 '<button type="submit">Reessayer</button></form></div>'
                 % html.escape(erreur))
    else:
        tete = '<meta http-equiv="refresh" content="3;url=/entrer">'
        sous = "Un instant."
        corps = ('<div class="table">'
                 '<div class="entete"><strong>Ton jeu demarre</strong></div>'
                 '<p class="mdp">Le premier allumage prend une minute ou deux. '
                 'Cette page bascule toute seule des que c\'est pret.</p></div>')
    return PAGE.format(tete=tete, sous=sous, barre=_barre(pseudo), corps=corps,
                       heures=int(DUREE_MAX_HEURES)).encode("utf-8")


def page_arret(pseudo: str) -> bytes:
    corps = ('<div class="table">'
             '<div class="entete"><strong>Ton jeu est eteint</strong></div>'
             '<p class="mdp">Rien n\'est perdu : tes decks, tes campagnes et tes '
             'hauts faits t\'attendent au prochain allumage.</p>'
             '<p class="mdp">Eteindre ferme aussi la porte aux invites de la '
             'partie precedente : leur lien et leur navigateur ne rouvrent plus '
             'ta table. Toi, tu rentres par ce bouton, comme d\'habitude.</p>'
             '<form method="get" action="/entrer" style="margin-top:1rem">'
             '<button type="submit">Rallumer mon jeu</button></form></div>')
    return PAGE.format(tete="", sous="A tout de suite.", barre=_barre(pseudo),
                       corps=corps, heures=int(DUREE_MAX_HEURES)).encode("utf-8")


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
    {champs}
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
  code {{ background:#161b22; padding:.2rem .45rem; border-radius:.3rem;
         font-size:.8rem; word-break:break-all; }}
  form {{ display:inline; margin-right:.3rem; }}
  a {{ color:#58a6ff; }}
  .rapport {{ border:1px solid #21262d; border-radius:.5rem; margin-bottom:.6rem;
             background:#11161d; }}
  .rapport[open] {{ border-color:#30363d; }}
  .rapport > summary {{ cursor:pointer; padding:.6rem .8rem; list-style:none;
                       display:flex; gap:.6rem; align-items:baseline; flex-wrap:wrap; }}
  .rapport > summary::-webkit-details-marker {{ display:none; }}
  .rapport .quoi {{ flex:1; min-width:12rem; }}
  .rapport .meta {{ color:#9aa7b4; font-size:.8rem; }}
  .rapport .corps {{ padding:0 .8rem .8rem; }}
  .rapport pre {{ background:#0b0f14; border:1px solid #21262d; border-radius:.4rem;
                 padding:.6rem; max-height:22rem; overflow:auto; font-size:.78rem;
                 white-space:pre-wrap; word-break:break-word; }}
  .rapport img {{ max-width:100%; border:1px solid #30363d; border-radius:.4rem; }}
  .etat {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.04em;
          border-radius:.3rem; padding:.1rem .45rem; border:1px solid; }}
  .etat.nouveau {{ color:#f0b429; border-color:#f0b429; }}
  .etat.encours {{ color:#58a6ff; border-color:#58a6ff; }}
  .etat.traite {{ color:#3fb950; border-color:#3fb950; }}
  .pastille {{ font-size:.8rem; vertical-align:middle; background:#f85149;
              color:#0e1116; border-radius:1rem; padding:.05rem .5rem; }}
</style>
<main>
  <h1>Comptes</h1>
  <p class="sous">{valides} valide(s) sur {max}. <a href="/">Retour au site</a></p>
  <table>
    <tr><th>Pseudo</th><th>Adresse</th><th>Demande le</th><th>Derniere connexion</th>
        <th>Statut</th><th></th></tr>
    {lignes}
  </table>
  <h1 style="margin-top:2.5rem">Invitations</h1>
  <p class="sous">Un lien vaut une place, une seule fois. Celui qui le recoit
  entre directement, sans passer par la file d'attente.</p>
  <form method="post" action="/admin" style="margin-bottom:1rem">
    <input type="hidden" name="action" value="inviter">
    <button class="oui" type="submit">Creer un lien d'invitation</button>
  </form>
  <table>
    <tr><th>Lien</th><th>Cree le</th><th>Utilise par</th><th></th></tr>
    {invitations}
  </table>

  <h1 style="margin-top:2.5rem">Rapports de bug {pastille}</h1>
  <p class="sous">Les 60 derniers, le plus recent en haut. Deplie pour voir la
  capture et le journal de la partie.</p>
  {rapports}

  <h1 style="margin-top:2.5rem">Parties</h1>
  <p class="sous">Les 25 dernieres, la plus recente en haut.</p>
  <table>
    <tr><th>Table</th><th>Hote</th><th>Ouverte le</th><th>Fermee le</th></tr>
    {parties}
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

        Les sessions sont EN BASE (table `sessions`) : elles survivent aux
        redemarrages du service, sans quoi chaque deploiement redemandait le
        mot de passe a tout le monde.
        """
        brut = self.headers.get("Cookie") or ""
        for morceau in brut.split(";"):
            nom, _, valeur = morceau.strip().partition("=")
            if nom == "nc_session":
                pseudo = pseudo_de_session(valeur)
                if pseudo:
                    return pseudo
        return None

    def _taille_corps(self) -> int:
        """Le `Content-Length` annonce, ou -1 s'il est illisible ou trop gros.

        ⚠ ON JUGE L'ANNONCE, PAS LE CORPS, ET C'EST LE POINT. Lire d'abord
        pour mesurer ensuite revient a faire exactement ce qu'on veut eviter :
        allouer ce qu'un inconnu declare.
        """
        try:
            taille = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            return -1
        if taille < 0 or taille > MAX_CORPS_OCTETS:
            return -1
        return taille

    def _corps_refuse(self) -> None:
        """Repond 413 et RACCROCHE. Les octets annonces n'ont pas ete lus : ils
        seraient sinon relus comme la requete suivante sur la meme connexion."""
        self.close_connection = True
        self._repondre(413, b"Requete trop volumineuse.", "text/plain; charset=utf-8")

    def _raccrocher(self) -> None:
        """A appeler AVANT de repondre sans avoir lu le corps. Ses octets sont
        toujours dans la prise : gardee ouverte, la connexion les relirait
        comme s'ils etaient la requete suivante."""
        self.close_connection = True

    def _champs(self) -> dict:
        """Les champs du formulaire. Le corps est deja plafonne : `do_POST`
        refuse au-dela de `MAX_CORPS_OCTETS` avant d'arriver ici."""
        import urllib.parse
        taille = max(0, self._taille_corps())
        brut = self.rfile.read(taille).decode("utf-8", "replace")
        return {k: v[0] for k, v in urllib.parse.parse_qs(brut).items()}

    def _adresse_client(self) -> str:
        """L'adresse du visiteur, telle que Caddy la rapporte.

        ⚠ ON PREND LA DERNIERE VALEUR DE `X-Forwarded-For`, PAS LA PREMIERE.
        Caddy AJOUTE au bout de la liste l'adresse du pair qu'il voit ; tout ce
        qui precede a ete ecrit par le client et se falsifie librement. Prendre
        la premiere donnerait un frein qu'il suffit de contourner en changeant
        un en-tete.
        """
        relais = (self.headers.get("X-Forwarded-For") or "").strip()
        if relais:
            return relais.split(",")[-1].strip()
        return self.client_address[0] if self.client_address else "?"

    def _secure(self) -> str:
        """« ; Secure » quand la requete est arrivee par HTTPS, sinon rien.

        ⚠ POURQUOI PAS EN DUR. Le site EST servi en HTTPS seulement : le
        `Caddyfile` declare ses deux blocs par leur nom d'hote, sans schema et
        sans `auto_https off`, ce qui fait que Caddy sert le 443 et redirige le
        80 vers lui de lui-meme. En production l'attribut est donc toujours
        pose. Mais le meme fichier tourne en local sur `http://127.0.0.1:8080`,
        sans proxy devant : `Secure` en dur y ferait jeter le cookie par le
        navigateur, et la connexion tournerait en rond sans rien dire.

        ⚠ ET LA FALSIFICATION NE RAPPORTE RIEN ICI. Un client qui mentirait sur
        `X-Forwarded-Proto` ne ferait que durcir SON PROPRE cookie, ou le
        rendre inutilisable pour lui seul. Rien a y gagner.
        """
        if (self.headers.get("X-Forwarded-Proto") or "").strip().lower() == "https":
            return "; Secure"
        return "; Secure" if DOMAINE else ""

    def _formulaire(self, quoi: str, erreur: str = "", jeton: str = "") -> bytes:
        inscription = quoi == "inscription"
        champs = ('<input type="hidden" name="i" value="%s">'
                  '<label>Pseudo<input name="pseudo" autocomplete="username" required></label>'
                  '<label>Adresse e-mail<input name="email" type="email" '
                  'autocomplete="email" required></label>'
                  % html.escape(jeton)) if inscription else (
                  '<label>Pseudo ou adresse e-mail<input name="pseudo" '
                  'autocomplete="username" required></label>')
        return PAGE_FORMULAIRE.format(
            titre="Creer un compte" if inscription else "Se connecter",
            action="/inscription" if inscription else "/connexion",
            bouton="Demander un compte" if inscription else "Entrer",
            auto="new-password" if inscription else "current-password",
            champs=champs,
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            pied=(('Tu es invite : ton compte sera actif tout de suite.'
                   if invitation_valide(jeton) else
                   'Ton compte devra etre valide a la main avant de servir.')
                  + ' Deja un compte ? <a href="/connexion">Se connecter</a>.'
                  if inscription else
                  'Pas encore de compte ? <a href="/inscription">En demander un</a>.'),
        ).encode("utf-8")

    def _servir_capture(self) -> None:
        """L'image d'un rapport, designee par le NUMERO du rapport.

        Le nom du fichier vient de la base, jamais de l'adresse : c'est ce qui
        rend la traversee de dossier impossible ici.
        """
        import urllib.parse
        requete = urllib.parse.urlparse(self.path).query
        try:
            numero = int(urllib.parse.parse_qs(requete).get("id", ["0"])[0])
        except ValueError:
            numero = 0
        nom = None
        if numero:
            with _cx() as cx:
                r = cx.execute("SELECT capture FROM rapports WHERE id = ?",
                               (numero,)).fetchone()
            nom = r["capture"] if r else None
        if not nom:
            self._repondre(404, b"Aucune capture.", "text/plain; charset=utf-8")
            return
        chemin = os.path.join(DOSSIER_RAPPORTS, os.path.basename(nom))
        try:
            with open(chemin, "rb") as f:
                image = f.read()
        except OSError:
            self._repondre(404, b"Capture introuvable.", "text/plain; charset=utf-8")
            return
        types = {"png": "image/png", "jpg": "image/jpeg", "webp": "image/webp"}
        mime = types.get(nom.rsplit(".", 1)[-1].lower(), "application/octet-stream")
        self._repondre(200, image, mime)

    def _page_admin(self) -> bytes:
        lignes = []
        for c in liste_comptes():
            statut = c["statut"]
            actions = ""
            if c["pseudo"] != ADMIN:
                for cible, classe, libelle in (("valide", "oui", "Valider"),
                                               ("refuse", "non", "Refuser")):
                    if statut != cible:
                        actions += ('<form method="post" action="/admin">'
                                    '<input type="hidden" name="pseudo" value="%s">'
                                    '<input type="hidden" name="statut" value="%s">'
                                    '<button class="%s" type="submit">%s</button></form>'
                                    % (html.escape(c["pseudo"]), cible, classe, libelle))
            lignes.append(
                "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    html.escape(c["pseudo"]), html.escape(c["email"] or "—"),
                    html.escape(c["cree"] or ""),
                    html.escape(c["derniere_connexion"] or "jamais"),
                    html.escape(statut), actions))
        base = ("https://%s" % DOMAINE) if DOMAINE else "http://127.0.0.1:%d" % PORT_SITE
        inv = []
        for i in invitations_libres():
            lien = "%s/inscription?i=%s" % (base, i["jeton"])
            inv.append('<tr><td><code>%s</code></td><td>%s</td><td>—</td>'
                       '<td><form method="post" action="/admin">'
                       '<input type="hidden" name="action" value="annuler">'
                       '<input type="hidden" name="jeton" value="%s">'
                       '<button class="non" type="submit">Annuler</button></form></td></tr>'
                       % (html.escape(lien), html.escape(i["cree_le"]),
                          html.escape(i["jeton"])))
        for i in invitations_utilisees():
            inv.append("<tr><td>—</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                html.escape(i["cree_le"]), html.escape(i["utilise_par"] or ""),
                html.escape(i["utilise_le"] or "")))
        if not inv:
            inv.append('<tr><td colspan="4">Aucune invitation. '
                       'Cree-en une ci-dessus.</td></tr>')
        rapports = "".join(self._bloc_rapport(r) for r in liste_rapports())
        if not rapports:
            rapports = '<p class="sous">Aucun rapport. Bonne nouvelle.</p>'
        nouveaux = nb_rapports_nouveaux()
        pastille = ('<span class="pastille">%d nouveau%s</span>'
                    % (nouveaux, "x" if nouveaux > 1 else "")) if nouveaux else ""
        parties = "".join(
            "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                html.escape(p["nom"]), html.escape(p["hote"]),
                html.escape(p["ouverte_le"]),
                html.escape(p["fermee_le"] or "en cours"))
            for p in dernieres_parties())
        if not parties:
            parties = '<tr><td colspan="4">Aucune partie pour le moment.</td></tr>'
        return PAGE_ADMIN.format(valides=nb_valides(), max=MAX_COMPTES,
                                 lignes="".join(lignes),
                                 invitations="".join(inv),
                                 rapports=rapports, pastille=pastille,
                                 parties=parties).encode("utf-8")

    @staticmethod
    def _bloc_rapport(r: dict) -> str:
        """Un rapport replie. TOUT ce qui vient du rapport passe par
        html.escape : la description, le nom et le journal sont ecrits par
        n'importe qui, y compris par un invite qu'on ne connait pas."""
        etat = r["etat"] or "nouveau"
        classe = {"nouveau": "nouveau", "en cours": "encours", "traite": "traite"}.get(etat, "nouveau")
        boutons = ""
        for cible, libelle in (("en cours", "Prendre"), ("traite", "Classer")):
            if etat != cible:
                boutons += ('<form method="post" action="/admin">'
                            '<input type="hidden" name="action" value="rapport">'
                            '<input type="hidden" name="id" value="%d">'
                            '<input type="hidden" name="etat" value="%s">'
                            '<button type="submit">%s</button></form>'
                            % (r["id"], html.escape(cible), libelle))
        boutons += ('<form method="post" action="/admin">'
                    '<input type="hidden" name="action" value="rapport_supprimer">'
                    '<input type="hidden" name="id" value="%d">'
                    '<button class="non" type="submit">Supprimer</button></form>' % r["id"])
        image = ('<p><a href="/admin/capture?id=%d" target="_blank" rel="noopener">'
                 '<img src="/admin/capture?id=%d" alt="capture"></a></p>'
                 % (r["id"], r["id"])) if r["capture"] else "<p class=\"sous\">Aucune capture.</p>"
        if r["journal"]:
            journal = ('<details><summary class="sous">Journal de la partie</summary>'
                       '<pre>%s</pre></details>' % html.escape(r["journal"]))
        else:
            journal = '<p class="sous">Aucun journal (rapport envoye hors partie).</p>'
        ou = r["ecran"] or "?"
        if r["siege"]:
            ou += " · siege %d" % r["siege"]
        return ('<details class="rapport">'
                '<summary><span class="etat %s">%s</span>'
                '<span class="quoi">%s</span>'
                '<span class="meta">%s &middot; %s &middot; %s</span></summary>'
                '<div class="corps"><p>%s</p>%s%s<p>%s</p></div></details>'
                % (classe, html.escape(etat),
                   html.escape((r["description"] or "")[:110]),
                   html.escape(r["nom"] or "?"), html.escape(ou),
                   html.escape(r["quand"] or ""),
                   html.escape(r["description"] or "").replace("\n", "<br>"),
                   image, journal, boutons))

    def do_GET(self):
        pseudo = self._session()
        if self.path in ("/", "/index.html"):
            # ⚠ LE SITE N'EST QU'UNE PORTE. Qui est connecte n'a rien a faire
            # ici : il veut son jeu, pas une page d'accueil. Qui ne l'est pas
            # voit le formulaire tout de suite, sans page intermediaire.
            if pseudo:
                self._rediriger("/entrer")
            else:
                self._repondre(200, self._formulaire("connexion"))
        elif self.path == "/entrer":
            if not pseudo:
                self._rediriger("/")
                return
            toucher_presence(pseudo)
            partie = jeu_de(pseudo)
            if partie is not None and partie.vivant() and _moteur_repond(partie.port):
                # Redirection vers un AUTRE hote (p<N>.domaine) : c'est voulu,
                # le client du jeu utilise des chemins absolus et ne supporte
                # pas d'etre servi sous un prefixe (voir l'en-tete du fichier).
                self.send_response(303)
                self.send_header("Location", partie.lien_hote())
                self.send_header("Content-Length", "0")
                self.end_headers()
                return
            demarrer_en_fond(pseudo)
            self._repondre(200, page_attente(pseudo))
        elif self.path == "/arret":
            if not pseudo:
                self._rediriger("/")
                return
            self._repondre(200, page_arret(pseudo))
        elif self.path.startswith("/inscription"):
            import urllib.parse
            requete = urllib.parse.urlparse(self.path)
            jeton = urllib.parse.parse_qs(requete.query).get("i", [""])[0]
            if not INSCRIPTION_LIBRE and not invitation_valide(jeton):
                self._repondre(403, self._formulaire(
                    "inscription", "Il faut un lien d'invitation pour creer un compte ici."))
                return
            self._repondre(200, self._formulaire("inscription", jeton=jeton))
        elif self.path == "/connexion":
            self._repondre(200, self._formulaire("connexion"))
        elif self.path == "/deconnexion":
            brut = self.headers.get("Cookie") or ""
            for morceau in brut.split(";"):
                nom, _, valeur = morceau.strip().partition("=")
                if nom == "nc_session":
                    fermer_session(valeur)
            self.send_response(303)
            self.send_header("Location", "/")
            # Les memes attributs qu'a la pose : un cookie efface doit
            # ressembler a celui qu'il remplace, sans quoi certains navigateurs
            # gardent l'ancien a cote.
            self.send_header("Set-Cookie",
                             "nc_session=; Max-Age=0; Path=/" + self._secure())
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.path == "/admin":
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._repondre(200, self._page_admin())
        elif self.path.startswith("/admin/capture"):
            # La capture d'un rapport, reservee a l'administrateur comme la
            # page qui l'affiche. On ne sert JAMAIS le nom de fichier venu de
            # l'adresse : on lit celui que la base associe au numero demande,
            # sans quoi n'importe quel chemin sortirait du dossier.
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._servir_capture()
        elif self.path == "/etat":
            # ⚠ LES NOMS NE SORTENT PAS SANS COMPTE. `code` EST le pseudo
            # (`lancer_jeu` : `Partie(emplacement, pseudo, ...)`) et
            # `emplacement` donne le sous-domaine : servis a un visiteur
            # anonyme, ils composaient la liste nominative des personnes en
            # train de jouer et l'adresse de leur table. Le COMPTEUR, lui, ne
            # nomme personne et reste public : il ne dit que « c'est plein ».
            with VERROU:
                etat = {"libres": NB_EMPLACEMENTS - len(EMPLACEMENTS),
                        "total": NB_EMPLACEMENTS,
                        "occupes": len(EMPLACEMENTS)}
                if pseudo:
                    etat["jeux"] = [{"code": p.code, "nom": p.nom,
                                     "emplacement": p.emplacement,
                                     "vivant": p.vivant()} for p in PARTIES.values()]
                else:
                    etat["jeux"] = []
            self._repondre(200, json.dumps(etat, ensure_ascii=False).encode("utf-8"),
                           "application/json; charset=utf-8")
        else:
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")

    def do_POST(self):
        # ⚠ L'ORDRE DE CES TROIS LIGNES EST LE CORRECTIF. On plafonne le corps
        # AVANT de le lire, et on identifie qui parle AVANT de le lire aussi.
        # Le code precedent lisait `Content-Length` octets en premier, sans
        # plafond et sans savoir qui envoyait : de quoi faire allouer ce qu'on
        # declare, sans compte ni cookie, y compris sur une route qui finira
        # en 404. Chaque branche appelle `_champs()` elle-meme, et seulement
        # apres avoir verifie ce qu'elle pouvait verifier.
        if self._taille_corps() < 0:
            self._corps_refuse()
            return
        pseudo = self._session()

        if self.path == "/inscription":
            champs = self._champs()
            try:
                jeton = champs.get("i", "")
                invite = invitation_valide(jeton)
                inscrire(champs.get("pseudo", ""), champs.get("email", ""),
                         champs.get("mdp", ""), jeton)
            except ValueError as erreur:
                self._repondre(400, self._formulaire(
                    "inscription", str(erreur), champs.get("i", "")))
                return
            self._repondre(200, PAGE_FORMULAIRE.format(
                titre="Demande enregistree", action="/connexion", bouton="Entrer",
                auto="current-password", erreur="",
                champs='<label>Pseudo ou adresse e-mail<input name="pseudo" '
                       'autocomplete="username" required></label>',
                pied=("Ton compte est actif : connecte-toi." if invite else
                      "Ton compte attend une validation manuelle. Reviens une fois "
                      "qu'elle est faite.")).encode("utf-8"))

        elif self.path == "/connexion":
            champs = self._champs()
            cle = cle_frein(self._adresse_client())
            # ⚠ ON LIT LE COMPTEUR AVANT DE L'INCREMENTER. Compter au fil de la
            # lecture ferait qu'une adresse deja bloquee continuerait de charger
            # son propre compteur, et le frein ne se relacherait jamais.
            reste = attente_connexion(cle)
            if reste:
                self._repondre(429, self._formulaire(
                    "connexion", "Trop de tentatives. Reessaie dans %s."
                                 % delai_lisible(reste)))
                return
            compter_tentative(cle)
            try:
                qui = verifier(champs.get("pseudo", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire("connexion", str(erreur)))
                return
            # Reussite : on relache le frein, pour que ses propres fautes de
            # frappe ne poursuivent pas quelqu'un qui a fini par entrer.
            oublier_tentatives(cle)
            jeton = ouvrir_session(qui)
            # Sans ceci, « en ligne » n'apparaitrait presque jamais : la
            # presence n'etait rafraichie que par le MOTEUR, donc uniquement
            # pendant qu'une partie tourne. On la touche des l'entree sur le
            # site, ce qui couvre le moment ou le moteur demarre encore.
            toucher_presence(qui)
            self.send_response(303)
            self.send_header("Location", "/entrer")
            # HttpOnly : le cookie n'est pas lisible en JavaScript.
            # SameSite=Lax : il ne part pas sur une requete venue d'un autre site.
            # Secure : il ne part pas en clair. Sans lui, une premiere visite
            # tapee en `http://` envoyait le cookie sur le reseau avant meme que
            # Caddy n'ait eu le temps de rediriger vers HTTPS.
            self.send_header("Set-Cookie",
                             f"nc_session={jeton}; HttpOnly; SameSite=Lax; Path=/;"
                             f" Max-Age={DUREE_SESSION_JOURS * 86400}"
                             + self._secure())
            self.send_header("Content-Length", "0")
            self.end_headers()

        elif self.path == "/admin":
            # Le controle passe AVANT la lecture du corps : un inconnu n'a pas
            # a faire allouer un octet sur une route qui va le refuser.
            if pseudo != ADMIN:
                self._raccrocher()
                self._repondre(403, b"Reserve a l'administrateur.",
                               "text/plain; charset=utf-8")
                return
            champs = self._champs()
            action = champs.get("action", "")
            if action == "inviter":
                creer_invitation()
            elif action == "annuler":
                supprimer_invitation(champs.get("jeton", ""))
            elif action in ("rapport", "rapport_supprimer"):
                try:
                    numero = int(champs.get("id", "0"))
                except ValueError:
                    numero = 0
                if numero:
                    if action == "rapport":
                        changer_etat_rapport(numero, champs.get("etat", ""))
                    else:
                        supprimer_rapport(numero)
            else:
                changer_statut(champs.get("pseudo", "").strip().lower(),
                               champs.get("statut", ""))
            self._rediriger("/admin")

        elif self.path in ("/api/vue", "/api/dire", "/api/bug"):
            # ⚠ CES ROUTES NE SONT PAS POUR LE NAVIGATEUR. Elles sont appelees
            # par le MOTEUR, en 127.0.0.1, et s'authentifient par le jeton de
            # partie plutot que par le cookie de session : le navigateur est sur
            # p<N>.<domaine> et son cookie de site ne voyagerait pas jusqu'ici.
            # Le jeton dit de quel compte il s'agit ; il meurt avec la partie.
            #
            # Ces trois routes-ci lisent le corps AVANT de savoir qui parle, et
            # il n'y a pas moyen de faire autrement : leur laissez-passer est
            # dans le corps, pas dans un cookie. C'est justement pour elles que
            # `MAX_CORPS_OCTETS` existe, deja verifie en tete de `do_POST`.
            champs = self._champs()
            qui = JETONS_SITE.get(champs.get("jeton", ""))
            if not qui:
                self._repondre(403, b'{"error":"jeton inconnu"}',
                               "application/json; charset=utf-8")
                return
            if self.path == "/api/bug":
                # ⚠ N'IMPORTE QUI PEUT ARRIVER ICI. Le jeton dit de quelle
                # TABLE vient le rapport, pas qui l'ecrit : un invite entre par
                # un lien de siege et n'a pas de compte. D'ou le plafond de
                # debit, compte par table, et les troncatures dans
                # enregistrer_rapport().
                if not debit_rapport_ok(qui):
                    self._repondre(429, b'{"error":"trop de rapports, reessaie plus tard"}',
                                   "application/json; charset=utf-8")
                    return
                if not str(champs.get("description") or "").strip():
                    self._repondre(400, b'{"error":"description vide"}',
                                   "application/json; charset=utf-8")
                    return
                numero = enregistrer_rapport(qui, champs)
                self._repondre(200, json.dumps({"ok": True, "numero": numero}).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.path == "/api/dire":
                dire(qui, champs.get("texte", ""), champs.get("a", ""))
                self._repondre(200, b'{"ok":true}',
                               "application/json; charset=utf-8")
                return
            # Toute consultation vaut signe de vie : c'est ce qui fait
            # apparaitre « en ligne » sans demander au joueur de le declarer.
            toucher_presence(qui)
            try:
                depuis = int(champs.get("depuis", "0") or "0")
            except ValueError:
                depuis = 0
            avec = champs.get("avec", "")
            messages = messages_depuis(depuis, qui, avec)
            corps = {
                "pseudo": qui,
                "joueurs": presence(),
                "messages": messages,
                "dernier": messages[-1]["id"] if messages else depuis,
                # Dernier message echange avec chacun : le client s'en sert pour
                # signaler d'une pastille les conversations ou il s'est passe
                # quelque chose, sans avoir a les ouvrir une par une.
                "prives": derniers_prives(qui),
            }
            self._repondre(200, json.dumps(corps, ensure_ascii=False).encode("utf-8"),
                           "application/json; charset=utf-8")

        elif self.path == "/eteindre":
            # Aucun champ a lire ici : le bouton n'envoie rien, et le pseudo
            # vient du cookie. On ne touche donc pas au corps du tout.
            if not pseudo:
                self._raccrocher()
                self._rediriger("/")
                return
            self._raccrocher()
            # On n'eteint QUE son propre jeu : le code est le pseudo.
            if eteindre_jeu(pseudo):
                journal_partie_fermee(pseudo)
            # ⚠ ET ON COUPE LES ACCES, ICI SEULEMENT. C'est le seul geste du
            # site qui soit VOLONTAIRE : la personne dit qu'elle a fini. On en
            # profite pour perimer le laissez-passer du moteur, sans quoi les
            # invites de la soiree gardent un cookie valable un an. Ni le
            # faucheur ni un plantage ne passent par ici : une table qui
            # redemarre toute seule ne doit pas laisser son proprietaire
            # dehors.
            revoquer_mot_de_passe_jeu(pseudo)
            # Vers /arret et surtout PAS vers / : cette derniere rallumerait
            # aussitot ce qu'on vient d'eteindre.
            self._rediriger("/arret")

        else:
            # ⚠ ON NE LIT PAS LE CORPS D'UNE ROUTE QUI N'EXISTE PAS. C'etait le
            # pire des cas : faire allouer plusieurs mega-octets pour rendre un
            # 404 de onze caracteres.
            self._raccrocher()
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")


def main() -> int:
    if not os.path.isfile(os.path.join(RACINE_JEU, "launch.json")):
        print(f"Racine du jeu introuvable : {RACINE_JEU}", file=sys.stderr)
        return 1
    if not os.access(PYTHON, os.X_OK):
        print(f"Python du moteur introuvable ou non executable : {PYTHON}", file=sys.stderr)
        return 1

    initialiser_base()
    if compte(ADMIN) is None:
        print(f"  ⚠ Aucun compte administrateur « {ADMIN} » : cree-le sur /inscription,")
        print("    il sera valide d'office.")
    threading.Thread(target=faucheur, daemon=True).start()
    serveur = ThreadingHTTPServer(("127.0.0.1", PORT_SITE), Handler)

    def arreter(*_):
        print("\nFermeture de toutes les tables...")
        for code in list(PARTIES):
            eteindre_jeu(code)
        serveur.shutdown()

    signal.signal(signal.SIGINT, lambda *_: threading.Thread(target=arreter).start())
    signal.signal(signal.SIGTERM, lambda *_: threading.Thread(target=arreter).start())

    print(f"NarwhalChampions sur http://127.0.0.1:{PORT_SITE}")
    print(f"  moteur      : {RACINE_JEU}")
    print(f"  emplacements: {NB_EMPLACEMENTS} (ports {PORT_BASE + 1} a {PORT_BASE + NB_EMPLACEMENTS})")
    print(f"  domaine     : {DOMAINE or '(local, liens en 127.0.0.1)'}")
    print(f"  base        : {BASE}")
    print(f"  comptes     : {nb_valides()}/{MAX_COMPTES} valides, admin « {ADMIN} »")
    try:
        serveur.serve_forever()
    finally:
        for code in list(PARTIES):
            eteindre_jeu(code)
    return 0


def purge_en_ligne_de_commande(arguments: list) -> int:
    """`orchestrateur.py purger-rapports [jours]`, pour `deploiement/purge.sh`.

    ⚠ LA PURGE NE PASSE PAS PAR LE SHELL POUR LA BASE. Effacer les fichiers
    avec `find` et laisser les lignes derriere donnerait une page
    d'administration qui renvoie vers des captures disparues. L'orchestrateur
    est le seul qui sache faire les deux d'un coup : le script l'appelle plutot
    que de recopier la regle.
    """
    try:
        jours = int(arguments[0]) if arguments else JOURS_RAPPORTS_TRAITES
    except ValueError:
        print(f"Nombre de jours invalide : {arguments[0]}", file=sys.stderr)
        return 2
    if not os.path.isfile(BASE):
        print(f"  (base absente, rien a purger) {BASE}")
        return 0
    efface = purger_rapports_traites(jours)
    print(f"  rapports traites depuis plus de {jours} jours : {efface} efface(s)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "purger-rapports":
        sys.exit(purge_en_ligne_de_commande(sys.argv[2:]))
    sys.exit(main())
