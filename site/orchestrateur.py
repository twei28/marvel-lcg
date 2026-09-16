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
import urllib.parse
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

# TROIS QUARTS D'HEURE SANS RIEN FAIRE, ET LA TABLE SE FERME (13/09/2026).
#
# Une table allumee tient un port, un processus et sa memoire, sur vingt places.
# Le minuteur des huit heures ne regardait que l'AGE de la table : quelqu'un qui
# ouvrait son jeu le matin et partait travailler l'immobilisait toute la
# journee.
#
# ⚠ ON NE JUGE PAS SUR LE « VU » DU SITE. Il ne bouge qu'a l'ouverture du jeu :
# pendant qu'on joue, le navigateur parle au MOTEUR, pas au site. S'y fier
# aurait ferme la table de quelqu'un en pleine partie au bout de 45 minutes.
# Le signal est la derniere ecriture du JOURNAL DU MOTEUR, que l'orchestrateur
# tient lui-meme (`_ouvrir_journal_moteur`) : le moteur y ecrit a chaque action
# de jeu, et rien du tout quand personne ne joue.
#
# ⚠ ET LA PARTIE EST SAUVEGARDEE AVANT, jamais perdue : voir
# `_sauvegarder_avant_extinction`. A huit heures on pouvait s'en passer, a
# trois quarts d'heure non.
INACTIVITE_MINUTES = float(os.environ.get("INACTIVITE_MINUTES", "45"))
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
# ⚠ « refuse » AJOUTE LE 16/09/2026 avec le suivi des signalements. Il couvre
# « ce n'est pas un bug » comme « je ne le ferai pas », et oblige a ecrire
# pourquoi : un ticket refuse sans un mot est pire qu'un ticket ignore.
ETATS_RAPPORT = ("nouveau", "en cours", "traite", "refuse")
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

    ⚠ ET ON TESTE PAR `bind`, PAS PAR `connect`. Se connecter ne dit que ceci :
    quelqu'un accepte. Un port reserve dont le `listen` n'est pas encore venu,
    ou dont la file d'acceptation deborde, refuse la connexion et se donnait
    donc pour libre, alors que le `Popen` suivant allait mourir dessus. Poser
    la prise, c'est demander a l'OS exactement ce qu'il repondra au moteur.

    SANS `SO_REUSEADDR`, et c'est volontaire : la barriere qui tranche cote
    moteur est `NetLib.IsPortAvailable` (engine/device/manager/web/manager.py),
    qui fait un `bind` nu. Avec l'option, un port laisse en TIME_WAIT par une
    partie qu'on vient d'eteindre se donnait ici pour libre, puis le moteur
    mourait dessus sur son assertion et le joueur lisait « le moteur s'est
    arrete au demarrage ». Poser la prise exactement comme le moteur la posera,
    c'est la seule facon d'obtenir la meme reponse que lui.
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as prise:
        try:
            prise.bind(("127.0.0.1", port))
        except OSError:
            return False
    return True


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


# Combien de journaux d'une meme table on garde, l'actuel non compris.
JOURNAUX_MOTEUR_GARDES = 10


def _ouvrir_journal_moteur(emplacement: int):
    """Ouvre `.site/moteur-N.log` pour un nouveau moteur, SANS ecraser le
    precedent.

    ⚠ ROTATION (11/09/2026). Le journal etait ouvert en "w" : chaque
    rallumage de la table effacait celui de la partie d'avant. Le rapport
    joueur de 08:45 (« mes contres ne retirent pas la menace ») visait une
    table relancee depuis, et son journal, la seule piece a conviction,
    n'existait plus. Ici l'ancien journal est renomme
    `moteur-N-<AAAAMMJJ-HHMMSS>.log` (l'heure de sa cloture, pas de son
    ouverture : c'est elle que l'on connait au moment de le lire), et seuls
    les JOURNAUX_MOTEUR_GARDES plus recents sont conserves. Un journal vide
    n'est pas garde : il ne dit rien.
    """
    dossier = os.path.join(RACINE_JEU, ".site")
    os.makedirs(dossier, exist_ok=True)
    courant = os.path.join(dossier, f"moteur-{emplacement}.log")
    if os.path.exists(courant):
        if os.path.getsize(courant) == 0:
            os.remove(courant)
        else:
            cachet = time.strftime("%Y%m%d-%H%M%S", time.localtime(os.path.getmtime(courant)))
            archive = os.path.join(dossier, f"moteur-{emplacement}-{cachet}.log")
            # Deux clotures dans la meme seconde : on numerote plutot qu'ecraser.
            n = 1
            while os.path.exists(archive):
                n += 1
                archive = os.path.join(dossier, f"moteur-{emplacement}-{cachet}-{n}.log")
            os.replace(courant, archive)
    prefixe = f"moteur-{emplacement}-"
    archives = sorted(f for f in os.listdir(dossier)
                      if f.startswith(prefixe) and f.endswith(".log"))
    for vieux in archives[:-JOURNAUX_MOTEUR_GARDES] if len(archives) > JOURNAUX_MOTEUR_GARDES else []:
        os.remove(os.path.join(dossier, vieux))
    return open(courant, "w", encoding="utf-8")


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
        journal = _ouvrir_journal_moteur(emplacement)
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


# Les joueurs qui ont demande a reprendre leur partie interrompue. Rempli par
# la route /reprendre, vide par `demarrer_en_fond` une fois le chargement
# demande au moteur. En memoire : si le site redemarre entre-temps, le bandeau
# se reproposera, ce qui est le bon repli.
A_REPRENDRE: set[str] = set()


def charger_partie_interrompue(partie: "Partie", pseudo: str) -> bool:
    """Demande au moteur de recharger la partie sauvegardee de ce joueur.

    ⚠ NE LEVE JAMAIS ET NE BLOQUE RIEN. Un chargement qui echoue doit laisser
    la table ouverte sur l'ecran des heros, pas priver quelqu'un de son jeu.
    C'est le cas qui compte : une sauvegarde ecrite par une version anterieure
    du moteur peut etre refusee (`VerifyVersion`), et un deploiement change
    justement de version.

    Rend `True` si le moteur a accepte. Dans tous les cas la partie retenue est
    OUBLIEE : proposer indefiniment une reprise qui echoue serait pire que de
    ne rien proposer.
    """
    attendue = partie_interrompue(pseudo)
    oublier_partie_interrompue(pseudo)
    if not attendue:
        return False
    try:
        # `:-1` = reprendre au DERNIER pas enregistre, comme le bouton
        # « Reprendre » de l'assistant.
        lien = "http://127.0.0.1:%d/debug?/load %s:-1" % (
            partie.port, urllib.parse.quote(attendue["fichier"]))
        with urllib.request.urlopen(lien, timeout=30) as reponse:
            reponse.read()
        return True
    except (urllib.error.URLError, OSError, ValueError) as exc:
        sys.stderr.write("reprise impossible pour %s : %r\n" % (pseudo, exc))
        return False


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
            # ⚠ APRES `lancer_jeu`, QUI ATTEND DEJA QUE LE MOTEUR REPONDE : lui
            # demander de charger avant qu'il ecoute ne donnerait rien.
            if pseudo in A_REPRENDRE:
                A_REPRENDRE.discard(pseudo)
                charger_partie_interrompue(partie, pseudo)
        except Exception as erreur:
            ERREURS_DEMARRAGE[pseudo] = str(erreur)
        finally:
            with VERROU_DEMARRAGE:
                DEMARRAGES.discard(pseudo)

    threading.Thread(target=travail, daemon=True).start()


def _groupe_vivant(groupe: int) -> bool:
    """Reste-t-il quelqu'un dans ce groupe de processus ?

    Le signal 0 n'est pas envoye : il ne sert qu'a demander si la cible
    existe et si l'on aurait le droit de la viser.
    """
    try:
        os.killpg(groupe, 0)
    except OSError:
        return False
    return True


# COMBIEN DE PARTIES TERMINEES ON GARDE, PAR COMPTE (13/09/2026).
#
# Le moteur ecrit desormais un enregistrement complet a la fin de chaque partie
# (`auto_save_after_game_over`, tools/config_serveur.py) : de quoi la revoir pas
# a pas. Sans plafond, le dossier grossirait sans fin. Cinquante, c'est une
# campagne entiere et ses alentours ; mesure faite, un enregistrement pese
# environ 44 Ko, donc 2 Mo par compte et 44 Mo pour les vingt places.
SAUVEGARDES_GARDEES = int(os.environ.get("SAUVEGARDES_GARDEES", "50"))

# ⚠ LES TROIS EMPLACEMENTS DU PLATEAU NE SONT JAMAIS EMPORTES. Ce sont des
# sauvegardes VOULUES, posees a la main sur les boutons Save 1, 2 et 3 : les
# ranger avec les enregistrements automatiques reviendrait a effacer ce que
# quelqu'un a delibérement garde.
EMPLACEMENTS_A_LA_MAIN = {"save_1.json", "save_2.json", "save_3.json"}


def limiter_sauvegardes(emplacement: int) -> int:
    """Ne garde que les `SAUVEGARDES_GARDEES` parties les plus recentes.

    Rend le nombre de fichiers effaces. Ne leve jamais : un menage manque est
    un regret, une exception ici empecherait la table de s'eteindre.
    """
    if SAUVEGARDES_GARDEES <= 0:
        return 0
    dossier = os.path.join(RACINE_JEU, "replays", f"serveur-{emplacement}")
    try:
        fichiers = [f for f in os.listdir(dossier)
                    if f.endswith(".json") and f not in EMPLACEMENTS_A_LA_MAIN]
    except OSError:
        return 0
    if len(fichiers) <= SAUVEGARDES_GARDEES:
        return 0
    # Le plus recent en tete : on garde le dessus de la pile.
    def age(nom):
        try:
            return os.path.getmtime(os.path.join(dossier, nom))
        except OSError:
            return 0.0
    fichiers.sort(key=age, reverse=True)
    efface = 0
    for vieux in fichiers[SAUVEGARDES_GARDEES:]:
        try:
            os.remove(os.path.join(dossier, vieux))
            efface += 1
        except OSError:
            pass
    return efface


def _sauvegarder_avant_extinction(partie: "Partie", cause: str = "", fiche=None) -> None:
    """Demande au moteur d'ecrire sa partie avant qu'on le tue, et RETIENT ou.

    ⚠ NE LEVE JAMAIS, et ne retient pas l'extinction plus que son delai. Une
    sauvegarde manquee est un regret ; une exception ici empecherait la table
    de s'eteindre, donc l'emplacement d'etre rendu.

    Le moteur decide lui-meme s'il y a quelque chose a ecrire : une table ou
    personne n'a quitte l'ecran des heros n'est pas une partie.

    ⚠ ET ON GARDE LE CHEMIN, ce qu'on ne faisait pas : la reponse du moteur le
    contient, on la jetait, et le joueur devait retrouver sa partie tout seul
    dans « Reprendre ». `fiche` est ce que `_fiche_moteur` a deja demande au
    moteur juste avant (scenario, heros, tour) : on la reutilise pour decrire
    la partie au retour, sans le rappeler une seconde fois.
    """
    try:
        if not partie.vivant():
            return
        lien = "http://127.0.0.1:%d/sauver_pour_le_site?jeton=%s" % (
            partie.port, urllib.parse.quote(partie.jeton_site or ""))
        with urllib.request.urlopen(lien, timeout=10) as reponse:
            brut = reponse.read().decode("utf-8", "replace")
        donnees = json.loads(brut) if brut else {}
        fichier = str(donnees.get("fichier") or "")
        if donnees.get("sauve") and fichier:
            retenir_partie_interrompue(partie.code, fichier, cause, fiche or {})
    except (urllib.error.URLError, OSError, ValueError) as exc:
        sys.stderr.write("partie non sauvegardee avant extinction : %r\n" % (exc,))


def retenir_partie_interrompue(pseudo: str, fichier: str, cause: str, fiche: dict) -> None:
    """Note la partie qui attend ce joueur. Remplace la precedente."""
    heros = ", ".join(str(j.get("heros") or j.get("nom") or "")
                      for j in (fiche.get("joueurs") or []) if isinstance(j, dict))
    with _cx() as cx:
        cx.execute(
            "INSERT OR REPLACE INTO parties_interrompues"
            " (pseudo, fichier, quand, cause, version, scenario, heros, tour)"
            " VALUES (?,?,?,?,?,?,?,?)",
            (pseudo, fichier, _maintenant(), cause, str(fiche.get("version") or ""),
             str(fiche.get("scenario") or ""), heros, int(fiche.get("round") or 0)))


def partie_interrompue(pseudo: str):
    """La partie qui attend ce joueur, ou None."""
    with _cx() as cx:
        ligne = cx.execute("SELECT * FROM parties_interrompues WHERE pseudo = ?",
                           (pseudo,)).fetchone()
    return dict(ligne) if ligne else None


def oublier_partie_interrompue(pseudo: str) -> None:
    """Le joueur a repris, ou choisi autre chose : on ne lui reproposera pas."""
    with _cx() as cx:
        cx.execute("DELETE FROM parties_interrompues WHERE pseudo = ?", (pseudo,))


def eteindre_jeu(code: str, cause: str = "extinction") -> bool:
    """Arrete le moteur. ⚠ NE TOUCHE PAS AUX DONNEES : elles appartiennent au
    compte et doivent etre la au prochain allumage.

    `cause` dit POURQUOI la table s'eteint : elle est conservee telle quelle
    dans la trace d'une partie abandonnee (voir `_noter_abandon`).
    """
    with VERROU:
        partie = PARTIES.pop(code, None)
        if partie is None:
            return False
        EMPLACEMENTS.pop(partie.emplacement, None)
        JETONS_SITE.pop(partie.jeton_site, None)
    # ⚠ ICI, ET NULLE PART AILLEURS : c'est la derniere seconde ou l'on peut
    # encore demander au moteur ce qui se jouait. Une ligne plus bas il est
    # mort, et la partie n'aura jamais existe pour personne.
    # (`_noter_abandon` est defini plus bas, avec le reste du suivi : Python
    # resout les globales a l'appel, pas a la lecture du fichier.)
    fiche = _fiche_moteur(partie) if partie.vivant() else {}
    _noter_abandon(partie, cause, fiche)
    # ⚠ ET ON SAUVE AVANT DE TUER. Fermer une table pour cause d'inactivite
    # perdait la partie en cours : a huit heures on pouvait s'en accommoder, a
    # trois quarts d'heure non. Le joueur se la voit proposer a son retour.
    _sauvegarder_avant_extinction(partie, cause, fiche)
    # ⚠ ET LE MENAGE JUSTE APRES, pas avant : la partie qu'on vient d'ecrire
    # doit compter parmi les cinquante gardees.
    try:
        limiter_sauvegardes(partie.emplacement)
    except Exception as souci:
        sys.stderr.write("menage des sauvegardes non fait : %r\n" % (souci,))
    # ⚠ ET LA FERMETURE SE NOTE ICI, PAS CHEZ L'APPELANT. Elle ne l'etait que
    # dans deux des six chemins d'extinction (le faucheur et le bouton
    # « Eteindre ») : ni l'arret du site — donc CHAQUE deploiement — ni le
    # menage de `lancer_jeu` ne l'ecrivaient. Les lignes de ces tables-la
    # restaient « en cours » pour toujours dans la page d'administration, des
    # jours apres que le moteur etait mort (constate le 08/09/2026 : quatre
    # tables ouvertes depuis le 5 septembre encore annoncees en cours).
    # `journal_partie_fermee` ne touche que les lignes encore ouvertes : la
    # rappeler est sans effet.
    journal_partie_fermee(partie.code)
    processus = partie.processus
    if processus is not None:
        # `start_new_session` a mis le moteur dans son propre groupe : on tue
        # LE GROUPE, sinon les sous-processus du lanceur survivraient et le
        # port resterait pris.
        #
        # ⚠ ET ON LE TUE MEME QUAND LE LANCEUR EST DEJA SORTI. C'est meme le
        # seul cas qui arrive : `launcher_fast.py` rend la main, ses enfants
        # tiennent le port. `poll()` n'est alors pas nul, et l'ancien code ne
        # faisait plus rien du tout. Le `pgid` vaut le `pid` du lanceur, que
        # `start_new_session` a fait chef de groupe, et il reste valide tant
        # qu'un membre du groupe vit ; `os.getpgid`, lui, ne repond deja plus.
        # Le risque residuel est celui du numero recycle, contre lequel il n'y
        # a rien a faire ici : le port bloque a coup sur est le mal certain.
        lanceur_vivant = processus.poll() is None
        groupe = processus.pid
        try:
            os.killpg(groupe, signal.SIGTERM)
        except OSError:
            if lanceur_vivant:
                processus.terminate()
        if lanceur_vivant:
            try:
                processus.wait(timeout=15)
            except subprocess.TimeoutExpired:
                pass
        # Les petits-enfants ne sont PAS nos fils : `wait` ne les voit pas. On
        # demande donc au groupe s'il vit encore, avec le signal 0, qui ne fait
        # rien d'autre que poser la question.
        fin = time.time() + 5
        while _groupe_vivant(groupe) and time.time() < fin:
            time.sleep(0.1)
        if _groupe_vivant(groupe):
            try:
                os.killpg(groupe, signal.SIGKILL)
            except OSError:
                pass
        if lanceur_vivant:
            try:
                processus.wait(timeout=5)
            except subprocess.TimeoutExpired:
                processus.kill()
    return True


# Un compte qui expire a deja quatre semaines de retard : le verifier toutes
# les heures est bien assez, et evite de relire toute la table chaque minute.
PERIODE_EXPIRATION_S = 3600


def secondes_sans_jouer(partie) -> float:
    """Depuis combien de temps ce moteur n'a plus rien fait. -1 si on ne sait pas.

    ⚠ LE SIGNAL EST LE JOURNAL DU MOTEUR, PAS LE « VU » DU SITE. Celui-ci ne
    bouge qu'a l'ouverture du jeu : pendant qu'on joue, le navigateur parle au
    moteur et le site n'entend plus rien. S'y fier aurait ferme la table de
    quelqu'un en pleine partie.

    Le moteur ecrit dans ce journal a chaque action de jeu, et rien du tout
    quand personne ne joue : c'est exactement la mesure qu'on cherche.
    L'orchestrateur ouvre lui-meme ce fichier (`_ouvrir_journal_moteur`), donc
    il existe toujours.

    ⚠ ET ON RENVOIE -1 PLUTOT QUE ZERO quand le fichier manque. Zero se lirait
    « vient de jouer » et la table ne se fermerait jamais ; -1 dit « on ne sait
    pas », et l'appelant s'abstient. Une table qu'on n'arrive pas a juger ne
    doit pas etre fermee au hasard.
    """
    chemin = os.path.join(RACINE_JEU, ".site", f"moteur-{partie.emplacement}.log")
    try:
        return max(0.0, time.time() - os.path.getmtime(chemin))
    except OSError:
        return -1.0


def table_oisive(code: str, partie) -> bool:
    """Cette table doit-elle etre fermee faute d'avoir servi ?

    ⚠ L'ADMINISTRATEUR N'EST JAMAIS FAUCHE POUR INACTIVITE. C'est sa table qui
    sert a regarder ce qui se passe sur le site, souvent sans y jouer : la
    fermer sous son nez serait exactement le contraire du service rendu. Le
    minuteur des huit heures, lui, continue de s'appliquer a tout le monde.

    Fonction a part, et non deux lignes dans le faucheur : c'est la seule
    decision de ce fil qu'on puisse eprouver sans le faire tourner.
    """
    if code == ADMIN or INACTIVITE_MINUTES <= 0:
        return False
    depuis = secondes_sans_jouer(partie)
    # -1 = on ne sait pas. Une table qu'on n'arrive pas a juger ne se ferme pas.
    return depuis >= 0 and depuis > INACTIVITE_MINUTES * 60


def faucheur() -> None:
    """Rend les emplacements dont le moteur est mort, la partie trop vieille ou
    la table abandonnee, et fait expirer les comptes que plus personne n'habite."""
    prochaine_revue = 0.0
    while True:
        time.sleep(60)
        for code, partie in list(PARTIES.items()):
            trop_vieille = (time.time() - partie.debut) > DUREE_MAX_HEURES * 3600
            oisive = table_oisive(code, partie)
            if not partie.vivant() or trop_vieille or oisive:
                if not partie.vivant():
                    cause = "moteur arrete"
                elif trop_vieille:
                    cause = "minuteur"
                else:
                    cause = "inactivite"
                eteindre_jeu(code, cause)
        if time.time() >= prochaine_revue:
            prochaine_revue = time.time() + PERIODE_EXPIRATION_S
            try:
                expirer_comptes_inactifs()
            except Exception as souci:
                # Le faucheur tient AUSSI les tables : une revue des comptes
                # qui echoue ne doit pas emporter le fil avec elle.
                print(f"  ⚠ revue des comptes en echec : {souci}")


# --------------------------------------------------------------------------
# Comptes
# --------------------------------------------------------------------------
VERROU_COMPTES = threading.Lock()

# Une session dure trois mois. Le but est de ne PLUS retaper son mot de passe
# d'une soiree de jeu a l'autre ; c'est un site prive, a inscription fermee.
DUREE_SESSION_JOURS = 90

# QUATRE SEMAINES SANS VENIR, ET LA PLACE RETOURNE AU POT (13/09/2026).
#
# Il n'y a que `MAX_COMPTES` places, et une place n'est pas qu'une ligne en
# base : c'est un EMPLACEMENT, avec ses decks, ses campagnes en cours et ses
# hauts faits. Quelqu'un qui ne revient pas immobilise tout cela.
#
# ⚠ LE COMPTE N'EST PAS SUPPRIME, IL EXPIRE. Son statut passe a `expire` : sa
# session se ferme, sa table s'eteint, il ne compte plus dans le quota. Mais sa
# ligne reste, ET SON EMPLACEMENT AUSSI : ses decks et ses campagnes l'attendent
# tant que personne n'a pris sa place. Il recontacte l'administrateur, qui le
# revalide d'un clic, et il retrouve tout.
#
# ⚠ ET SI QUELQU'UN PREND SA PLACE, elle est effacee a ce moment-la, pas avant
# (voir `_attribuer_emplacements_manquants`). Sans cet effacement, le nouveau
# venu heriterait des decks et des campagnes du precedent.
EXPIRATION_JOURS = int(os.environ.get("EXPIRATION_JOURS", "28"))

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
-- Liens de reinitialisation de mot de passe (08/09/2026). Un lien par
-- demande, cree par l'administrateur depuis /admin, a usage unique, valable
-- 24 heures. Le site n'envoie pas de courrier : c'est l'administrateur qui
-- transmet le lien a la personne, comme pour une invitation.
CREATE TABLE IF NOT EXISTS reinitialisations (
    jeton      TEXT PRIMARY KEY,
    pseudo     TEXT NOT NULL,
    cree_le    TEXT NOT NULL,
    utilise_le TEXT
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
-- Le FIL d'un ticket (16/09/2026). Un rapport de bug envoye par le TITULAIRE
-- d'un compte (siege 0) devient un ticket : on peut lui repondre, il peut
-- repondre a son tour.
--
-- ⚠ `auteur` vaut « admin » ou « joueur », JAMAIS un pseudo. Le proprietaire
-- du ticket est deja connu par `rapports.hote` ; stocker un pseudo ici
-- ouvrirait deux sources de verite sur « a qui appartient ce fil ».
--
-- ⚠ `lu_le` est celui du DESTINATAIRE : un message d'admin est lu par le
-- joueur, et reciproquement. C'est lui qui allume et eteint la pastille.
CREATE TABLE IF NOT EXISTS rapports_messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    rapport_id INTEGER NOT NULL,
    auteur     TEXT NOT NULL,
    texte      TEXT NOT NULL,
    quand      TEXT NOT NULL,
    lu_le      TEXT
);
CREATE INDEX IF NOT EXISTS idx_rapports_messages ON rapports_messages(rapport_id);
-- ⚠ LES PARTIES QUITTEES EN COURS DE ROUTE N'EXISTENT NULLE PART AILLEURS.
-- Le journal du moteur (`games_history-serveur-N.json`) n'est ecrit qu'a la
-- FIN declaree par le moteur (victoire, defaite, elimination). Une partie
-- qu'on abandonne restait donc visible dans « En cours » tant que la table
-- brulait, puis disparaissait sans laisser une ligne. On prend sa photo juste
-- avant d'eteindre la table (`_noter_abandon`), et elle rejoint la liste des
-- parties terminees avec la mention « abandonnee ».
-- L'ANNONCE EN COURS, et il n'y en a qu'une. Ajoutee le 13/09/2026 pour un
-- besoin precis : prevenir les joueurs qu'un deploiement approche. Le
-- deploiement fait `systemctl restart narwhal`, l'orchestrateur emporte ses
-- moteurs, et TOUTE PARTIE EN COURS EST PERDUE. Sans preavis, la personne
-- decouvre l'ardoise vide sans comprendre. Avec, elle a le temps d'appuyer sur
-- le bouton Save du plateau.
--
-- ⚠ `jusqu_a` est un INSTANT UNIX, pas une date lisible comme le reste de la
-- base. Le navigateur en fait un decompte qui descend tout seul ; une chaine a
-- la minute l'obligerait a deviner le fuseau du serveur.
--
-- Une SEULE ligne est gardee : poser une annonce efface la precedente. Il n'y
-- a rien a archiver, une annonce perimee n'interesse plus personne.
CREATE TABLE IF NOT EXISTS annonces (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    texte   TEXT NOT NULL,
    jusqu_a INTEGER NOT NULL,
    pose_le TEXT NOT NULL
);
-- LA PARTIE INTERROMPUE QUI ATTEND SON JOUEUR (13/09/2026).
--
-- Chaque extinction de table ecrit la partie en cours dans les sauvegardes
-- (`_sauvegarder_avant_extinction`). Jusqu'ici l'orchestrateur JETAIT la
-- reponse du moteur, qui contient pourtant le chemin du fichier : le joueur
-- devait retrouver sa partie tout seul dans « Reprendre ». On la retient donc,
-- pour la lui proposer a son retour.
--
-- ⚠ UNE SEULE LIGNE PAR JOUEUR : une nouvelle interruption remplace la
-- precedente. Proposer la partie d'avant-hier quand celle d'hier existe n'a
-- aucun sens, et empiler serait une liste que personne ne trie.
--
-- ⚠ ET ON GARDE LA VERSION DU MOTEUR qui l'a ecrite. Un deploiement change
-- souvent cette version, et le moteur casse net sur une sauvegarde plus
-- ancienne que sa version minimale supportee (`VerifyVersion`, engine/lib) :
-- c'est ce qui permet de le dire au joueur plutot que de lui montrer une
-- erreur.
CREATE TABLE IF NOT EXISTS parties_interrompues (
    pseudo    TEXT PRIMARY KEY,
    fichier   TEXT NOT NULL,
    quand     TEXT NOT NULL,
    cause     TEXT,
    version   TEXT,
    scenario  TEXT,
    heros     TEXT,
    tour      INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS abandons (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    quand       TEXT NOT NULL,
    joueur      TEXT NOT NULL,
    emplacement INTEGER NOT NULL,
    mechant     TEXT,
    expert      INTEGER NOT NULL DEFAULT 0,
    tour        INTEGER NOT NULL DEFAULT 0,
    heros       TEXT,
    vilains     TEXT,
    manigances  TEXT,
    cause       TEXT
);
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
        # ⚠ CE QUE CHACUN A DEJA LU, et c'est tout ce qui manquait pour poser
        # une pastille : l'identifiant du dernier message prive qu'il a vu
        # passer. Sans lui, on ne sait pas distinguer « un message t'attend »
        # de « tu l'as deja lu », et la pastille resterait allumee pour
        # toujours. Ajoutee hors du SCHEMA comme les autres, pour les bases
        # deja en service.
        if "dernier_message_vu" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN dernier_message_vu INTEGER")
        # Meme precaution pour les bases creees avant la purge des rapports.
        colonnes_rap = {r["name"] for r in cx.execute("PRAGMA table_info(rapports)")}
        if "traite_le" not in colonnes_rap:
            cx.execute("ALTER TABLE rapports ADD COLUMN traite_le TEXT")
    _migrer_depuis_json()
    _attribuer_emplacements_manquants()


def _prendre_un_emplacement(cx, pour: str = "") -> int:
    """Une place libre, quitte a la reprendre a un compte EXPIRE. -1 si aucune.

    ⚠ C'EST ICI QUE L'EXPIRATION SERT A QUELQUE CHOSE. Sans ce recyclage, un
    compte expire garderait sa place pour toujours : le quota se libererait
    sur le papier, mais la vingtieme personne s'entendrait quand meme repondre
    « Plus aucun espace de jeu disponible ».

    ⚠ ET L'EFFACEMENT SE FAIT ICI, AU MOMENT DE DONNER LA PLACE, jamais avant.
    C'est ce qui permet a un compte expire de retrouver ses decks et ses
    campagnes s'il revient a temps, et ce qui empeche le nouveau venu
    d'heriter de ceux du precedent. `lancer_jeu` n'efface plus rien : si on ne
    le faisait pas ici, personne ne le ferait.

    On reprend au plus anciennement inactif : celui qui a le moins de chances
    de revenir.
    """
    pris = {r["emplacement"] for r in cx.execute(
        "SELECT emplacement FROM comptes WHERE emplacement IS NOT NULL")}
    libre = next((n for n in range(1, NB_EMPLACEMENTS + 1) if n not in pris), None)
    if libre is not None:
        return libre
    recyclable = cx.execute(
        "SELECT pseudo, emplacement FROM comptes"
        " WHERE statut = 'expire' AND emplacement IS NOT NULL"
        " ORDER BY MAX(COALESCE(vu_le, ''), COALESCE(derniere_connexion, ''),"
        "              COALESCE(cree, '')) LIMIT 1").fetchone()
    if recyclable is None:
        return -1
    cx.execute("UPDATE comptes SET emplacement = NULL WHERE pseudo = ?",
               (recyclable["pseudo"],))
    _nettoyer_emplacement(recyclable["emplacement"])
    print(f"  place {recyclable['emplacement']} reprise a « {recyclable['pseudo']} »"
          f" (compte expire){' pour « %s »' % pour if pour else ''}")
    return recyclable["emplacement"]


def _attribuer_emplacements_manquants() -> None:
    """Donne un emplacement aux comptes qui n'en ont pas encore.

    ⚠ QUAND IL N'Y A PLUS DE PLACE NEUVE, ON RECYCLE CELLE D'UN COMPTE EXPIRE,
    le plus anciennement inactif d'abord. C'est ce qui donne tout son sens a
    l'expiration : sans ce recyclage, un compte expire garderait son
    emplacement pour toujours et la place ne serait rendue que sur le papier.

    ⚠ ET ON EFFACE L'EMPLACEMENT AU MOMENT DE LE DONNER, jamais avant. C'est
    ce qui permet a un compte expire de retrouver ses decks et ses campagnes
    s'il revient a temps, et ce qui empeche le nouveau venu d'heriter de ceux
    du precedent. `lancer_jeu` n'efface plus rien depuis longtemps : si on ne
    le faisait pas ici, personne ne le ferait.
    """
    with _cx() as cx:
        # ⚠ ON LIT LA LISTE D'ABORD. `_prendre_un_emplacement` ecrit dans la
        # meme table : parcourir un curseur ouvert dessus reviendrait a se lire
        # en train de s'ecrire.
        sans_place = [r["pseudo"] for r in cx.execute(
            "SELECT pseudo FROM comptes WHERE emplacement IS NULL ORDER BY cree")]
        for pseudo in sans_place:
            libre = _prendre_un_emplacement(cx, pseudo)
            if libre < 0:
                print(f"  ⚠ plus d'emplacement libre pour « {pseudo} »")
                break
            cx.execute("UPDATE comptes SET emplacement = ? WHERE pseudo = ?",
                       (libre, pseudo))


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


# ===========================================================================
# LE TEMPS : LE SERVEUR ENVOIE UN INSTANT, LE NAVIGATEUR ECRIT L'HEURE.
#
# AJOUT du 14/09/2026, apres ce constat de l'utilisateur : « il faudra que tout
# le jeu soit a l'heure locale du joueur, moi il est sept heures vingt six ».
# Le serveur repondait 05:26 : il tourne en `Etc/UTC` (verifie le 14/09/2026
# par `timedatectl`), Bruxelles est a UTC+2 l'ete. Deux heures d'ecart sur tout
# ce que le site affichait.
#
# ⚠ ON NE MET PAS LE SERVEUR A L'HEURE DE BRUXELLES. Ce serait juste pour une
# seule personne. Un joueur a Montreal verrait alors six heures d'ecart au lieu
# de deux, et personne ne s'en apercevrait avant qu'il le dise.
#
# ⚠ LE SERVEUR NE FORMATE PLUS AUCUNE HEURE DESTINEE A UN HUMAIN. Il n'a aucun
# moyen de connaitre le fuseau de qui regarde : seul le navigateur le sait. Le
# serveur envoie donc un INSTANT (secondes depuis l'epoque, sans fuseau, le
# meme partout sur Terre) et le navigateur le met en toutes lettres, avec
# `toLocaleString`. Voir `_horodate` et `SCRIPT_HEURE_LOCALE`.
#
# ⚠ LES HORODATAGES STOCKES SONT EN UTC, ET LE RESTENT. Ils sont ecrits en
# clair (« 2026-09-14 05:26 ») depuis l'origine, sans fuseau, par un serveur
# qui a toujours ete en UTC. On les relit donc comme de l'UTC, explicitement.
# `time.strftime` sans argument suivait le fuseau du serveur : si celui-ci
# changeait un jour, les anciennes lignes deviendraient fausses en silence et
# les nouvelles seraient decalees. `time.gmtime()` ferme la porte.
# ===========================================================================

def _maintenant() -> str:
    """L'instant present, en UTC, au format stocke en base.

    ⚠ `time.gmtime()` et pas l'heure locale du serveur : voir l'avertissement
    ci-dessus. Ne jamais montrer cette chaine telle quelle a un humain.
    """
    return time.strftime("%Y-%m-%d %H:%M", time.gmtime())


def _epoque_de(horodatage) -> float | None:
    """Un horodatage stocke -> secondes depuis l'epoque, ou None s'il est illisible.

    ⚠ `calendar.timegm` et pas `time.mktime` : le premier lit un temps UTC, le
    second le lit dans le fuseau du serveur. Sur un serveur en UTC les deux
    donnent la meme chose ; le jour ou il changerait de fuseau, seul le premier
    resterait juste.
    """
    import calendar
    texte = str(horodatage or "").strip()
    # ⚠ DEUX FORMES, ET C'EST VOULU. `_maintenant` ecrit a la minute
    # (« 2026-09-14 05:26 »), mais d'anciennes lignes portent les secondes
    # (« 2026-09-14 05:26:31 »), ecrites ailleurs par `isoformat`. Le premier
    # jet ne lisait que la forme courte et rendait None sur les autres : une
    # visite d'il y a trois heures redevenait « jamais vu ». Attrape par
    # `site/test_parcours.py` le 14/09/2026.
    for forme in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
        try:
            return calendar.timegm(time.strptime(texte, forme))
        except (TypeError, ValueError):
            continue
    return None


def _horodate(horodatage, secours: str = "") -> str:
    """Une date, pour le HTML : un instant que le navigateur mettra a l'heure.

    Rend `<time data-ts="...">…</time>`. Le texte a l'interieur est la chaine
    UTC brute : c'est ce que verra quelqu'un dont le navigateur n'execute pas
    JavaScript, et c'est mieux que rien. `SCRIPT_HEURE_LOCALE` la remplace par
    l'heure du lecteur des que la page est chargee.
    """
    epoque = _epoque_de(horodatage)
    texte = html.escape(str(horodatage or secours))
    if epoque is None:
        return texte
    return '<time data-ts="%d">%s</time>' % (int(epoque), texte)


# Mis dans chaque page qui montre des dates. ⚠ Il ne DEVINE rien : il ne touche
# qu'aux elements qui portent `data-ts`, pose par `_horodate`. Une date ecrite
# en dur ailleurs reste en UTC, et c'est voulu : mieux vaut qu'elle se voie.
SCRIPT_HEURE_LOCALE = """
<script>
(function () {
  function langue() {
    try { return navigator.language || "fr-FR"; } catch (e) { return "fr-FR"; }
  }
  function mettreALHeure(racine) {
    var noeuds = (racine || document).querySelectorAll("time[data-ts]");
    for (var i = 0; i < noeuds.length; i++) {
      var n = noeuds[i];
      var ts = Number(n.getAttribute("data-ts"));
      if (!isFinite(ts) || ts <= 0) continue;
      var d = new Date(ts * 1000);
      try {
        n.textContent = d.toLocaleString(langue(), {
          day: "2-digit", month: "2-digit", year: "numeric",
          hour: "2-digit", minute: "2-digit"
        });
        n.setAttribute("datetime", d.toISOString());
        n.title = "heure de votre appareil";
      } catch (e) { /* navigateur sans Intl : la chaine UTC reste lisible */ }
    }
  }
  mettreALHeure(document);
  // Les parties de page redessinees apres coup (suivi, tchat) portent leurs
  // propres `data-ts` : on repasse derriere elles.
  window.mettreALHeureLocale = mettreALHeure;
  document.addEventListener("DOMContentLoaded", function () { mettreALHeure(document); });
})();
</script>
"""


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
        # Quitte a reprendre la place d'un compte expire : c'est tout l'objet
        # de l'expiration. Voir `_prendre_un_emplacement`.
        libre = _prendre_un_emplacement(cx, pseudo)
        if libre < 0:
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
    if ligne["statut"] == "expire":
        # ⚠ ON DIT POURQUOI, ET QUOI FAIRE. « Ton compte attend ma validation »
        # aurait envoye quelqu'un attendre indefiniment quelque chose qui ne
        # viendra pas : personne ne sait, cote site, qu'il est revenu.
        raise ValueError(
            "Ton compte a expire : plus de %d jours sans venir, et la place est "
            "retournee au pot. Ecris-moi, je te la rends." % EXPIRATION_JOURS)
    if ligne["statut"] != "valide":
        raise ValueError("Ton compte attend encore ma validation.")
    with _cx() as cx:
        cx.execute("UPDATE comptes SET derniere_connexion = ? WHERE pseudo = ?",
                   (_maintenant(), ligne["pseudo"]))
    return ligne["pseudo"]


def changer_statut(pseudo: str, statut: str) -> None:
    if statut not in ("valide", "attente", "refuse", "expire"):
        return
    # Remettre en service un compte expire dont la place a ete recyclee : il
    # lui en faut une nouvelle, sinon il se connecte dans le vide.
    rendre_une_place = (statut == "valide" and emplacement_de(pseudo) is None)
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("UPDATE comptes SET statut = ? WHERE pseudo = ?", (statut, pseudo))
    if statut != "valide":
        # Un compte devalide ne doit pas continuer sa session en cours.
        fermer_sessions_de(pseudo)
    elif rendre_une_place:
        _attribuer_emplacements_manquants()


def derniere_activite(ligne) -> str:
    """Le dernier signe de vie de ce compte, quel qu'il soit.

    ⚠ TROIS SOURCES, ET IL EN FAUT TROIS. `derniere_connexion` ne bouge qu'a
    la saisie du mot de passe, or une session dure quatre-vingt-dix jours :
    quelqu'un qui joue tous les soirs sans jamais retaper son mot de passe
    aurait l'air absent depuis des mois. `vu_le` est touche a chaque `/entrer`,
    c'est-a-dire chaque fois qu'on ouvre son jeu, et c'est le vrai signal. Et
    `cree` rattrape le compte tout neuf qui n'a encore rien fait.
    """
    return max(ligne["vu_le"] or "", ligne["derniere_connexion"] or "",
               ligne["cree"] or "")


def _visite_lisible(ligne) -> str:
    """« 2026-09-13 10:04 (il y a 3 j) », ou « jamais ».

    ⚠ ON N'AFFICHE PLUS `derniere_connexion` SEULE, et c'etait trompeur : une
    session dure quatre-vingt-dix jours, donc quelqu'un qui joue tous les soirs
    sans retaper son mot de passe y apparaissait absent depuis des mois. C'est
    aussi ce chiffre-la qui decide de l'expiration : la page doit montrer celui
    qui compte. Voir `derniere_activite`.
    """
    quand = derniere_activite(ligne)
    if not quand:
        return "jamais"
    depuis = _il_y_a(quand)
    return "%s (%s)" % (quand, depuis) if depuis else quand


def expirer_comptes_inactifs() -> list:
    """Fait expirer les comptes sans signe de vie depuis EXPIRATION_JOURS.

    Rend la liste des pseudos expires. Voir le commentaire de
    `EXPIRATION_JOURS` : le compte n'est pas supprime, sa place retourne au pot
    et ses donnees l'attendent tant que personne ne la prend.

    ⚠ L'ADMINISTRATEUR N'EXPIRE JAMAIS. C'est lui qui remet les autres en
    service : s'il se verrouillait dehors, plus personne ne pourrait rentrer.
    """
    seuil = EXPIRATION_JOURS * 86400
    expires = []
    for c in liste_comptes():
        if c["statut"] != "valide" or c["pseudo"] == ADMIN:
            continue
        ecart = _secondes_depuis(derniere_activite(c))
        if ecart is None or ecart < seuil:
            continue
        expires.append(c["pseudo"])
    for pseudo in expires:
        # La table d'abord : un compte expire ne doit pas garder un moteur
        # allume, qui tient un port et de la memoire pour personne.
        if pseudo in PARTIES:
            eteindre_jeu(pseudo, "compte expire")
        changer_statut(pseudo, "expire")
        print(f"  compte « {pseudo} » expire : {EXPIRATION_JOURS} jours sans venir")
    return expires


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


def fermer_parties_orphelines() -> int:
    """Au demarrage, AUCUNE table ne survit au site : `PARTIES` vit en memoire
    et les moteurs sont morts avec le processus precedent. Une ligne encore
    « ouverte » en base est donc une orpheline, et sans ce menage elle le
    reste indefiniment — c'est ce qui affichait « en cours » sur des tables
    eteintes depuis des jours.

    ⚠ L'HEURE ECRITE EST CELLE DU DEMARRAGE, pas celle de la vraie fermeture,
    qu'on ne peut plus connaitre. C'est le moment ou l'on SAIT que la table
    n'est plus la, et c'est tout ce que la ligne pretend dire.
    """
    with _cx() as cx:
        return cx.execute("UPDATE parties SET fermee_le = ? WHERE fermee_le IS NULL",
                          (_maintenant(),)).rowcount


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


REINITIALISATION_DUREE = 24 * 3600   # secondes


def creer_reinitialisation(pseudo: str) -> str:
    """Un lien a USAGE UNIQUE pour choisir un nouveau mot de passe.

    Demande du 08/09/2026 : un nouvel inscrit n'arrivait pas a se connecter et
    se demandait s'il avait fait une erreur dans son mot de passe. Le site
    n'envoie pas de courrier : l'administrateur cree le lien depuis /admin et
    le transmet lui-meme, comme une invitation. Leve ValueError si le compte
    n'existe pas."""
    pseudo = (pseudo or "").strip().lower()
    with _cx() as cx:
        if not cx.execute("SELECT 1 FROM comptes WHERE pseudo = ?", (pseudo,)).fetchone():
            raise ValueError("Compte inconnu : %s" % pseudo)
        jeton = secrets.token_urlsafe(16)
        cx.execute("INSERT INTO reinitialisations (jeton, pseudo, cree_le) VALUES (?, ?, ?)",
                   (jeton, pseudo, _maintenant()))
    return jeton


def _age_secondes(horodatage: str) -> float:
    """⚠ Passe par `_epoque_de`, donc lit l'horodatage comme de l'UTC. Avec
    `time.mktime`, un serveur qui changerait de fuseau aurait fait expirer les
    liens de reinitialisation avec plusieurs heures d'avance ou de retard."""
    epoque = _epoque_de(horodatage)
    return float("inf") if epoque is None else time.time() - epoque


def reinitialisation_valide(jeton: str) -> str | None:
    """Le pseudo que ce lien autorise a changer de mot de passe, ou None s'il
    est inconnu, deja utilise ou vieux de plus de 24 heures."""
    if not jeton:
        return None
    with _cx() as cx:
        l = cx.execute("SELECT pseudo, cree_le, utilise_le FROM reinitialisations WHERE jeton = ?",
                       (jeton,)).fetchone()
    if l is None or l["utilise_le"] is not None:
        return None
    if _age_secondes(l["cree_le"]) > REINITIALISATION_DUREE:
        return None
    return l["pseudo"]


def reinitialiser_mot_de_passe(jeton: str, mot_de_passe: str) -> str:
    """Pose le nouveau mot de passe, consomme le lien, ferme les sessions
    ouvertes du compte (un mot de passe change parce qu'on a un doute : les
    sessions d'avant ne doivent pas survivre). Rend le pseudo."""
    if len(mot_de_passe or "") < 8:
        raise ValueError("Mot de passe trop court : 8 caracteres au minimum.")
    with _cx() as cx:
        l = cx.execute("SELECT pseudo, cree_le, utilise_le FROM reinitialisations WHERE jeton = ?",
                       (jeton or "",)).fetchone()
        # ⚠ Relu et consomme dans la MEME transaction, comme une invitation :
        # deux envois du formulaire ne doivent pas poser deux mots de passe.
        if l is None or l["utilise_le"] is not None or _age_secondes(l["cree_le"]) > REINITIALISATION_DUREE:
            raise ValueError("Ce lien n'est plus valable. Demande un nouveau lien a l'administrateur.")
        sel = secrets.token_bytes(16).hex()
        cx.execute("UPDATE comptes SET sel = ?, empreinte = ? WHERE pseudo = ?",
                   (sel, _empreinte(mot_de_passe, sel), l["pseudo"]))
        cx.execute("UPDATE reinitialisations SET utilise_le = ? WHERE jeton = ?",
                   (_maintenant(), jeton))
        cx.execute("DELETE FROM sessions WHERE pseudo = ?", (l["pseudo"],))
    return l["pseudo"]


def reinitialisations_ouvertes():
    """Les liens encore valables, pour la page d'administration."""
    with _cx() as cx:
        lignes = cx.execute("SELECT jeton, pseudo, cree_le FROM reinitialisations"
                            " WHERE utilise_le IS NULL ORDER BY cree_le DESC").fetchall()
    return [dict(l) for l in lignes if _age_secondes(l["cree_le"]) <= REINITIALISATION_DUREE]


def supprimer_reinitialisation(jeton: str) -> None:
    with _cx() as cx:
        cx.execute("DELETE FROM reinitialisations WHERE jeton = ?", (jeton,))


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
    """Secondes ecoulees depuis cet horodatage, ou None s'il est illisible.

    ⚠ Meme correction que `_age_secondes` le 14/09/2026 : `datetime.now()`
    contre un `fromisoformat` sans fuseau melangeait l'heure du serveur et une
    date UTC. Les « il y a 3 min » du suivi etaient donc faux de deux heures
    des que le serveur n'etait pas en UTC.
    """
    epoque = _epoque_de(quand)
    return None if epoque is None else time.time() - epoque


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


# ---------------------------------------------------------------------------
# LE SUIVI DES SIGNALEMENTS (16/09/2026)
#
# Demande : « quand je corrige ou que je reponds, j'aimerais qu'une petite
# modale s'ouvre pour voir ma reponse, voire developper tout un truc de
# tickets ». Cadre par la spec du meme jour.
#
# ⚠ LE TICKET EST RESERVE AU SIEGE 0, ET CE N'EST PAS UN CHOIX DE CONFORT.
# Une table appartient a un compte ; les autres sieges sont des invites, meme
# quand la personne a un compte ailleurs. `hote` dit de quelle TABLE vient le
# rapport, PAS qui l'ecrit. Le siege 0 est le seul dont on sache le compte.
# Un rapport d'invite reste donc un rapport : lu, traite, sans fil — et le
# formulaire le dit honnetement a celui qui l'envoie.
# ---------------------------------------------------------------------------
def _est_un_ticket(r: dict) -> bool:
    """Ce rapport a-t-il un proprietaire connu ?"""
    return bool(r.get("hote")) and int(r.get("siege") or 0) == 0


def ticket_de(numero: int) -> dict | None:
    """Le rapport ET son fil, ou None si ce n'est pas un ticket."""
    with _cx() as cx:
        r = cx.execute("SELECT * FROM rapports WHERE id = ?", (numero,)).fetchone()
        if r is None:
            return None
        rapport = dict(r)
        if not _est_un_ticket(rapport):
            return None
        rapport["messages"] = [dict(m) for m in cx.execute(
            "SELECT * FROM rapports_messages WHERE rapport_id = ? ORDER BY id",
            (numero,))]
        return rapport


def ecrire_message(numero: int, auteur: str, texte: str) -> bool:
    """Ajoute un message au fil. Rend False si le ticket n'existe pas.

    Le texte est TRONQUE plutot que refuse, comme la description d'un rapport :
    un message ampute vaut mieux qu'un message perdu.
    """
    qui = "admin" if auteur == "admin" else "joueur"
    propre = str(texte or "").strip()[:MAX_DESCRIPTION_CARACTERES]
    if not propre:
        return False
    with _cx() as cx:
        r = cx.execute("SELECT hote, siege FROM rapports WHERE id = ?",
                       (numero,)).fetchone()
        if r is None or not _est_un_ticket(dict(r)):
            return False
        cx.execute("INSERT INTO rapports_messages (rapport_id, auteur, texte, quand)"
                   " VALUES (?, ?, ?, ?)", (numero, qui, propre, _maintenant()))
    return True


def tickets_de(pseudo: str) -> list[dict]:
    """Les tickets de CE compte, du plus recent au plus ancien, fils compris."""
    if not pseudo:
        return []
    with _cx() as cx:
        lignes = [dict(r) for r in cx.execute(
            "SELECT * FROM rapports WHERE hote = ? AND siege = 0 ORDER BY id DESC",
            (pseudo,))]
        for rapport in lignes:
            rapport["messages"] = [dict(m) for m in cx.execute(
                "SELECT * FROM rapports_messages WHERE rapport_id = ? ORDER BY id",
                (rapport["id"],))]
    return lignes


def marquer_ticket_lu(numero: int, par: str) -> None:
    """Le destinataire a ouvert le fil : ses messages non lus ne le sont plus.

    ⚠ ON MARQUE CEUX DE L'AUTRE. Le joueur qui ouvre son ticket lit les
    messages de l'admin, jamais les siens : marquer les siens eteindrait la
    pastille de l'admin sans qu'il ait rien vu.
    """
    ecrits_par = "joueur" if par == "admin" else "admin"
    with _cx() as cx:
        cx.execute("UPDATE rapports_messages SET lu_le = ?"
                   " WHERE rapport_id = ? AND auteur = ? AND lu_le IS NULL",
                   (_maintenant(), numero, ecrits_par))


def reponses_non_lues(pseudo: str) -> int:
    """Combien de reponses attendent ce compte, tous ses tickets confondus."""
    if not pseudo:
        return 0
    with _cx() as cx:
        r = cx.execute(
            "SELECT COUNT(*) AS n FROM rapports_messages m"
            " JOIN rapports r ON r.id = m.rapport_id"
            " WHERE r.hote = ? AND r.siege = 0"
            " AND m.auteur = 'admin' AND m.lu_le IS NULL", (pseudo,)).fetchone()
        return int(r["n"] if r else 0)


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
    """Allege les rapports classes « traite » depuis plus de `jours` : la
    CAPTURE part, le rapport et son fil restent.

    ⚠ CHANGE LE 16/09/2026, AVEC LE SUIVI DES SIGNALEMENTS. La purge effacait
    la ligne entiere. Un rapport est devenu un TICKET que son auteur consulte :
    effacer la ligne viderait sa page « Mes signalements » un mois apres, avec
    la reponse qu'on lui a faite. Or ce qui pesait n'a jamais ete le texte,
    c'est l'image — jusqu'a 4 Mio par rapport, 12 rapports par heure et par
    table, et trente archives de sauvegarde par-dessus.

    On efface donc l'image et on met `capture` a NULL dans le meme geste : la
    base ne renvoie jamais vers un fichier absent.

    ⚠ ET DANS CET ORDRE : LA BASE, LA VALIDATION, PUIS LE DISQUE. Effacer un
    fichier au milieu d'une transaction, c'est promettre au disque ce que la
    base peut encore annuler.

    Rend le nombre de rapports alleges.
    """
    from datetime import datetime, timedelta
    if jours < 0:
        return 0
    # Meme format que `_maintenant()` : la comparaison de chaines suffit, ces
    # horodatages se trient dans l'ordre alphabetique comme dans le temps.
    # ⚠ `utcnow`, pas `now` : la borne doit etre dans le meme fuseau que les
    # lignes comparees, sans quoi la purge efface deux heures trop tot ou deux
    # heures trop tard (corrige le 14/09/2026).
    limite = (datetime.utcnow() - timedelta(days=jours)).strftime("%Y-%m-%d %H:%M")
    with _cx() as cx:
        # ⚠ TOLERER UNE BASE PAS ENCORE MIGREE. Cette fonction est appelee par
        # la purge hebdomadaire, dans un AUTRE processus que le service : lui
        # faire lancer la migration ferait deux `ALTER TABLE` concurrents pour
        # rien. Sans la colonne, on retombe sur la date d'envoi.
        colonnes = {r["name"] for r in cx.execute("PRAGMA table_info(rapports)")}
        # ⚠ LES DEUX REQUETES SONT ECRITES EN TOUTES LETTRES. Composer un nom
        # de colonne avec un « % » n'etait pas exploitable ici, le code
        # choisissant lui-meme les deux valeurs possibles ; mais l'invariant
        # « aucun % dans une chaine SQL » se verifie d'un coup d'oeil, et une
        # exception, meme sure, oblige a les relire toutes.
        # ⚠ `capture IS NOT NULL` : ON N'ALLEGE QUE CE QUI PESE ENCORE. Depuis
        # que la ligne reste, un rapport deja allege serait repris a chaque
        # passage de la purge, qui annoncerait indefiniment le meme travail.
        if "traite_le" in colonnes:
            lignes = cx.execute(
                "SELECT id, capture FROM rapports WHERE etat = 'traite'"
                " AND capture IS NOT NULL"
                " AND COALESCE(traite_le, quand) < ?", (limite,)).fetchall()
        else:
            lignes = cx.execute(
                "SELECT id, capture FROM rapports WHERE etat = 'traite'"
                " AND capture IS NOT NULL AND quand < ?", (limite,)).fetchall()
        for r in lignes:
            cx.execute("UPDATE rapports SET capture = NULL WHERE id = ?", (r["id"],))

    # La transaction est validee : la base ne renvoie plus vers ces images, on
    # peut donc les effacer sans risquer de laisser un rapport pointer dans le
    # vide si quelque chose echoue ici.
    for r in lignes:
        if not r["capture"]:
            continue
        chemin = os.path.join(DOSSIER_RAPPORTS, os.path.basename(r["capture"]))
        try:
            os.remove(chemin)
        except FileNotFoundError:
            pass                      # deja parti : c'est le resultat voulu
        except OSError as erreur:
            # ⚠ NE PAS AVALER CELLE-CI. Une capture restee seule sur le disque
            # n'apparait sur aucune page : sans cette ligne, personne ne
            # l'apprend jamais, et le dossier grossit en silence.
            print("purge : capture non effacee %s (%s)" % (chemin, erreur),
                  file=sys.stderr)
    return len(lignes)


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


# --------------------------------------------------------------------------
# L'annonce en cours
# --------------------------------------------------------------------------
# AJOUT du 13/09/2026. Une seule annonce a la fois, avec une heure de fin.
# Elle est relayee aux moteurs par `/api/annonce`, et de la au plateau et a
# l'assistant de preparation. Voir le commentaire de la table `annonces`.

# Un preavis ne se pose pas pour la semaine prochaine : au-dela, c'est une
# erreur de frappe, pas une intention.
ANNONCE_MINUTES_MAX = 180

# La phrase par defaut, ECRITE POUR UN JOUEUR. Elle dit ce qui va se passer et
# ce qu'il faut faire, dans cet ordre. Le decompte est ajoute par le client,
# qui seul sait combien de minutes il reste au moment ou il dessine.
ANNONCE_DEPLOIEMENT = ("Mise a jour du jeu en approche : les parties en cours "
                       "seront interrompues. Sauvegarde la tienne avec le "
                       "bouton Save du plateau.")


def poser_annonce(minutes: int, texte: str = "") -> dict:
    """Pose l'annonce et rend ce qu'un client en verra.

    `minutes` est une DUREE a partir de maintenant, jamais une heure : c'est
    ainsi qu'on y pense (« dans dix minutes »), et ca evite de se tromper de
    fuseau. Le texte est libre ; vide, il prend la phrase de preavis.
    """
    minutes = max(1, min(ANNONCE_MINUTES_MAX, int(minutes)))
    texte = (texte or "").strip() or ANNONCE_DEPLOIEMENT
    jusqu_a = int(time.time()) + minutes * 60
    with _cx() as cx:
        cx.execute("DELETE FROM annonces")
        cx.execute("INSERT INTO annonces (texte, jusqu_a, pose_le) VALUES (?,?,?)",
                   (texte[:400], jusqu_a, _maintenant()))
    return {"texte": texte[:400], "jusqu_a": jusqu_a}



def retirer_annonce() -> None:
    """Annule l'annonce. Un deploiement qui glisse ne doit pas laisser un
    decompte mensonger tourner devant les joueurs."""
    with _cx() as cx:
        cx.execute("DELETE FROM annonces")


def annonce_courante() -> dict | None:
    """L'annonce encore valable, ou None.

    ⚠ ON NE RECOPIE PAS `jusqu_a` TEL QUEL AU CLIENT. Le navigateur d'un
    joueur n'est pas a l'heure du serveur, parfois a plusieurs minutes pres :
    un instant absolu lui ferait afficher un decompte faux, voire negatif. On
    envoie donc les SECONDES QUI RESTENT, qui ne dependent d'aucune horloge
    commune.
    """
    with _cx() as cx:
        ligne = cx.execute("SELECT texte, jusqu_a FROM annonces"
                           " ORDER BY id DESC LIMIT 1").fetchone()
    if ligne is None:
        return None
    restant = int(ligne["jusqu_a"]) - int(time.time())
    if restant <= 0:
        return None                 # perimee : elle s'efface d'elle-meme
    return {"texte": ligne["texte"], "secondes": restant}


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
    # `quand` reste le « HH:MM » du serveur (les anciens clients le lisent
    # tel quel) ; `quand_ts` est l'instant, que le navigateur met a l'heure de
    # CELUI QUI LIT. Le serveur vit en UTC, le joueur en Belgique : le
    # « HH:MM » nu s'affichait deux heures en retard.
    #
    # ⚠ 14/09/2026 : `quand_ts` se calculait par `time.time() - _secondes_depuis(...)`,
    # un aller-retour qui repassait par l'horloge courante et rendait un
    # resultat legerement different a chaque appel. `_epoque_de` lit la date une
    # fois pour toutes, et la lit explicitement comme de l'UTC.
    return [{"id": l["id"], "pseudo": l["pseudo"], "texte": l["texte"],
             "quand": l["quand"][11:16], "quand_ts": _epoque_de(l["quand"])}
            for l in lignes]


def messages_non_lus(moi: str) -> dict:
    """Ce qui attend cette personne : combien, et de qui.

    ⚠ SEULS LES MESSAGES RECUS COMPTENT. Les siens portent des identifiants
    plus grands que le dernier qu'il a lu, forcement : les compter lui aurait
    montre une pastille pour ses propres mots.
    """
    moi = (moi or "").strip().lower()
    if not moi:
        return {"nouveaux": 0, "de": [], "tickets": 0}
    with _cx() as cx:
        ligne = cx.execute("SELECT dernier_message_vu FROM comptes WHERE pseudo=?",
                           (moi,)).fetchone()
        vu = int((ligne["dernier_message_vu"] if ligne else 0) or 0)
        lignes = cx.execute(
            "SELECT pseudo, COUNT(*) AS combien FROM messages"
            " WHERE destinataire = ? AND id > ? GROUP BY pseudo",
            (moi, vu)).fetchall()
    # ⚠ LES REPONSES DE TICKETS VOYAGENT PAR CETTE MEME ROUTE (16/09/2026), et
    # c'est ce qui evite de toucher au moteur : `get_messages_prives` recopie
    # ce que le site lui donne, sans rien connaitre du contenu. Aucun
    # redemarrage de serveur pour cette partie du chantier.
    #
    # ⚠ ET LA RESERVE DE SIEGE TOMBE JUSTE. Le moteur ne relaie cette route
    # qu'au siege 0 (« un invite n'a pas a savoir qu'il a recu un message ») :
    # c'est exactement le seul siege qui puisse avoir un ticket.
    return {"nouveaux": sum(int(l["combien"]) for l in lignes),
            "de": [l["pseudo"] for l in lignes],
            "tickets": reponses_non_lues(moi)}


def marquer_messages_lus(moi: str) -> None:
    """Eteint la pastille : tout ce qui existe aujourd'hui est considere lu."""
    moi = (moi or "").strip().lower()
    if not moi:
        return
    with _cx() as cx:
        dernier = cx.execute("SELECT MAX(id) AS m FROM messages").fetchone()
        cx.execute("UPDATE comptes SET dernier_message_vu = ? WHERE pseudo = ?",
                   (int((dernier["m"] if dernier else 0) or 0), moi))


def conversation(moi: str, avec: str, combien: int = 40) -> list:
    """Les derniers messages echanges entre deux comptes, le plus ancien en tete."""
    moi = (moi or "").strip().lower()
    avec = (avec or "").strip().lower()
    if not moi or not avec:
        return []
    with _cx() as cx:
        lignes = cx.execute(
            "SELECT id, pseudo, texte, quand FROM messages"
            " WHERE (pseudo=? AND destinataire=?) OR (pseudo=? AND destinataire=?)"
            " ORDER BY id DESC LIMIT ?", (moi, avec, avec, moi, combien)).fetchall()
    return [dict(l) for l in reversed(lignes)]


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
{tete_appli}
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
  .barre .pastille {{ background:#f85149; color:#0e1116; border-radius:1rem;
                     padding:.05rem .45rem; font-size:.8rem; }}
  /* Le FIL d'un signalement (16/09/2026) : ma reponse et la sienne, distinguees
     par leur bord. Meme forme que dans /admin, pour que la meme conversation se
     lise pareil des deux cotes. */
  .fil {{ display:grid; gap:.4rem; margin:.4rem 0 .6rem; }}
  .fil .msg {{ margin:0; padding:.45rem .6rem; border-radius:.4rem;
              background:#0b0f14; border-left:3px solid #30363d; font-size:.9rem; }}
  .fil .msg.de-lui {{ border-left-color:#1f6feb; }}
  .fil .msg.de-moi {{ border-left-color:#f0b429; }}
  .repondre {{ display:flex; gap:.4rem; align-items:flex-start; }}
  .repondre textarea {{ flex:1; font:inherit; background:#0b0f14; color:inherit;
                       border:1px solid #30363d; border-radius:.4rem;
                       padding:.4rem .6rem; resize:vertical; }}
  .repondre button {{ width:auto; }}
  .avert {{ border:1px solid #9e6a03; background:#1d1a0e; color:#e3b341;
           border-radius:.5rem; padding:.7rem .9rem; margin-bottom:1.5rem; font-size:.9rem; }}
  footer {{ margin-top:2.5rem; color:#6e7681; font-size:.85rem; }}
</style>
<main>
  <h1>NarwhalChampions</h1>
  <p class="sous">{sous}</p>
  {barre}
  {corps}
  {bouton_appli}
  <footer>Ton espace de jeu est a toi : tes decks, tes campagnes en cours et
  tes hauts faits t'y attendent d'une fois sur l'autre. Eteindre le jeu
  n'efface rien. Tes invites, eux, rejoignent ta partie par leur lien sans
  avoir besoin d'un compte. Extinction automatique au bout de {heures} h
  d'allumage.</footer>
</main>
"""

def _barre(pseudo: str) -> str:
    admin = (' &middot; <a href="/admin">Administration</a>'
             ' &middot; <a href="/suivi">Suivi des parties</a>') if pseudo == ADMIN else ""
    # ⚠ L'ENTREE EST LA POUR TOUT LE MONDE, le compteur seulement quand une
    # reponse attend. Une page « Mes signalements » qu'on ne trouve qu'une fois
    # prevenu n'existe pas vraiment.
    attente = reponses_non_lues(pseudo)
    signalements = (' &middot; <a href="/signalements">Mes signalements</a>'
                    + (' <span class="pastille">(%d)</span>' % attente if attente else ""))
    return ('<div class="barre"><span>Connecte : <strong>%s</strong>%s%s</span>'
            '<a href="/deconnexion">Se deconnecter</a></div>'
            % (html.escape(pseudo), signalements, admin))


def page_reprise(pseudo: str, attendue: dict) -> bytes:
    """« Ta partie t'attend » : reprendre, ou commencer autre chose.

    ⚠ ON PROPOSE, ON NE FORCE PAS (decision de l'utilisateur, 13/09/2026).
    Quelqu'un qui revient le lendemain ne veut pas forcement reprendre la
    partie de la veille, et une reprise automatique lui enleve le choix.

    ⚠ ET LA PAGE DIT D'OU VIENT LA COUPURE. « Ta table s'est fermee » sans
    raison laisse croire a un plantage ; le motif est deja traduit pour la page
    de suivi (`CAUSES_ABANDON`), on le reutilise.
    """
    quoi = " · ".join(x for x in (attendue.get("scenario"), attendue.get("heros")) if x)
    tour = int(attendue.get("tour") or 0)
    if tour:
        quoi += (" · " if quoi else "") + "round %d" % tour
    motif = CAUSES_ABANDON.get(attendue.get("cause") or "", attendue.get("cause") or "")
    corps = ('<div class="table">'
             '<div class="entete"><strong>Ta partie t\'attend</strong>'
             '<span class="mdp">%s</span></div>'
             '<p class="mdp">Interrompue le %s%s. Elle a ete sauvegardee : '
             'tu peux la reprendre la ou tu l\'avais laissee.</p>'
             '<div class="choix" style="margin-top:1rem">'
             '<form method="get" action="/reprendre">'
             '<button type="submit"><b>Reprendre cette partie</b>'
             '<em>On recharge la sauvegarde et on te remet au plateau.</em>'
             '</button></form>'
             '<form method="get" action="/nouvelle-partie">'
             '<button type="submit" class="calme"><b>Commencer autre chose</b>'
             '<em>La sauvegarde reste dans « Reprendre », sur l\'ecran de '
             'preparation.</em></button></form>'
             '</div></div>'
             % (html.escape(quoi), _horodate(attendue.get("quand") or ""),
                (", " + html.escape(motif)) if motif else ""))
    return PAGE.format(tete="", sous="Tu etais en pleine partie.",
                       barre=_barre(pseudo), corps=corps,
                       heures=int(DUREE_MAX_HEURES)).encode("utf-8")


ETIQUETTES_TICKET = {
    "nouveau": "Recu",
    "en cours": "En cours",
    "traite": "Corrige",
    "refuse": "Refuse",
}


def page_signalements(pseudo: str) -> bytes:
    """« Mes signalements » : ses bugs, leur etat, et la conversation.

    ⚠ IL NE VOIT QUE LES SIENS. `tickets_de` filtre sur le compte ET sur le
    siege 0 : un rapport envoye depuis la table de quelqu'un d'autre ne lui
    appartient pas, meme s'il l'a ecrit de sa main.

    ⚠ TOUT CE QUI VIENT D'UN JOUEUR PASSE PAR `html.escape`, ici comme dans
    /admin : la description, le nom et le fil sont ecrits a la main.
    """
    tickets = tickets_de(pseudo)
    if not tickets:
        corps = ('<div class="table"><div class="entete">'
                 '<strong>Aucun signalement</strong></div>'
                 '<p class="mdp">Quand un bug te gene en partie, le bouton '
                 '« Signaler un bug » l\'envoie avec ta capture d\'ecran et le '
                 'journal de la partie. Tu retrouveras ici ma reponse.</p></div>')
        return PAGE.format(tete="", sous="Rien a suivre pour l\'instant.",
                           barre=_barre(pseudo), corps=corps,
                           heures=int(DUREE_MAX_HEURES)).encode("utf-8")

    corps = ""
    for r in tickets:
        etat = r["etat"] or "nouveau"
        fil = ""
        for m in r.get("messages") or []:
            fil += ('<p class="msg %s"><b>%s</b> <span class="mdp">%s</span><br>%s</p>'
                    % ("de-lui" if m["auteur"] == "admin" else "de-moi",
                       "Reponse" if m["auteur"] == "admin" else "Moi",
                       _horodate(m["quand"] or ""),
                       html.escape(m["texte"] or "").replace("\n", "<br>")))
        if not fil:
            fil = '<p class="mdp">Pas encore de reponse.</p>'
        capture = ('<p><a href="/admin/capture?id=%d" target="_blank" rel="noopener">'
                   'Voir la capture</a></p>' % r["id"]) if r["capture"] else ""
        corps += ('<div class="table">'
                  '<div class="entete"><strong>%s</strong>'
                  '<span class="mdp">%s &middot; %s</span></div>'
                  '<div class="fil">%s</div>%s'
                  '<form method="post" action="/signalements" class="repondre">'
                  '<input type="hidden" name="id" value="%d">'
                  '<textarea name="texte" rows="2" placeholder="Ajouter quelque chose"></textarea>'
                  '<button type="submit">Envoyer</button></form>'
                  '</div>'
                  % (html.escape((r["description"] or "")[:160]),
                     ETIQUETTES_TICKET.get(etat, etat),
                     _horodate(r["quand"] or ""), fil, capture, r["id"]))
    return PAGE.format(tete="", sous="Ce que tu as signale, et ma reponse.",
                       barre=_barre(pseudo), corps=corps,
                       heures=int(DUREE_MAX_HEURES)).encode("utf-8")


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
{tete_appli}
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
  {bouton_appli}
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
  .etat.refuse {{ color:#9aa7b4; border-color:#9aa7b4; }}
  /* Le FIL d'un ticket (16/09/2026) : ce que j'ai repondu, ce que le joueur a
     repondu. Les deux camps se distinguent par leur bord, pas par un alignement
     a droite : une conversation a deux voix, pas une messagerie. */
  .fil {{ margin:.6rem 0; display:grid; gap:.4rem; }}
  .fil .msg {{ margin:0; padding:.45rem .6rem; border-radius:.4rem;
              background:#0b0f14; border-left:3px solid #30363d; font-size:.88rem; }}
  .fil .msg.de-moi {{ border-left-color:#1f6feb; }}
  .fil .msg.de-lui {{ border-left-color:#f0b429; }}
  .fil .msg b {{ font-size:.8rem; }}
  .repondre {{ display:flex; gap:.4rem; align-items:flex-start; margin-top:.2rem; }}
  .repondre textarea {{ flex:1; font:inherit; background:#0b0f14; color:inherit;
                       border:1px solid #30363d; border-radius:.4rem; padding:.4rem .6rem;
                       resize:vertical; }}
  .pastille {{ font-size:.8rem; vertical-align:middle; background:#f85149;
              color:#0e1116; border-radius:1rem; padding:.05rem .5rem; }}
  /* Les sections repliees (12/09/2026, demande de l'utilisateur : « je dois
     defiler trop longtemps ») : un titre qu'on ouvre, avec le compte. */
  .section {{ margin-top:2rem; }}
  .section > summary {{ cursor:pointer; list-style:none; display:flex; gap:.6rem;
                        align-items:baseline; }}
  .section > summary::-webkit-details-marker {{ display:none; }}
  .section > summary h1 {{ margin:0; }}
  .section > summary::before {{ content:"▸"; color:#9aa7b4; font-size:1.1rem; }}
  .section[open] > summary::before {{ content:"▾"; }}
  .section .compte {{ color:#9aa7b4; font-weight:normal; font-size:.85rem; }}
  .groupe {{ margin:.6rem 0; }}
  .groupe > summary {{ cursor:pointer; color:#c9d1d9; font-size:.9rem; padding:.3rem 0; }}
  .msg {{ border-left:3px solid #30363d; padding:.3rem .6rem; margin:.35rem 0;
         font-size:.9rem; }}
  .msg.moi {{ border-color:#1f6feb; }}
  .msg.lui {{ border-color:#3fb950; }}
  .msg .meta {{ color:#6e7681; font-size:.75rem; }}
</style>
{styles_suivi}
<main>
  <!-- L'ANNONCE EST EN TETE, ET C'EST VOULU. On vient ici pour la poser quand
       le deploiement est deja lance dans l'autre fenetre : elle doit tomber
       sous la main, pas au bout d'un defilement. -->
  <h1>Annonce aux joueurs</h1>
  <p class="sous">{annonce_etat}</p>
  <form method="post" action="/admin" style="margin-bottom:2rem">
    <input type="hidden" name="action" value="annonce">
    <label style="color:#9aa7b4;font-size:.9rem">Dans
      <input name="minutes" type="number" min="1" max="{annonce_max}" value="10"
             style="width:4.5rem;font:inherit;background:#161b22;color:inherit;
                    border:1px solid #30363d;border-radius:.4rem;padding:.3rem .5rem">
      minutes</label>
    <input name="texte" type="text" maxlength="400" placeholder="Message (vide = preavis de mise a jour)"
           style="width:100%;box-sizing:border-box;margin:.5rem 0;font:inherit;
                  background:#161b22;color:inherit;border:1px solid #30363d;
                  border-radius:.4rem;padding:.4rem .6rem">
    <button class="oui" type="submit">Prevenir</button>
  </form>
  {annonce_annuler}

  <h1>Comptes</h1>
  <p class="sous">{valides} valide(s) sur {max}. {regle_expiration}
  <a href="/">Retour au site</a></p>
  <table>
    <tr><th>Pseudo</th><th>Adresse</th><th>Demande le</th><th>Derniere visite</th>
        <th>Statut</th><th></th></tr>
    {lignes}
  </table>
  <details class="section">
  <summary><h1>Invitations</h1> <span class="compte">{nb_invitations}</span></summary>
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
  </details>

  <details class="section"{ouvrir_reinit}>
  <summary><h1>Mots de passe oublies</h1> <span class="compte">{nb_reinit}</span></summary>
  <p class="sous">Le bouton « Mot de passe » d'un compte cree un lien a usage
  unique, valable 24 heures. Transmets-le a la personne : elle y choisit son
  nouveau mot de passe, et ses anciennes sessions sont fermees.</p>
  <table>
    <tr><th>Compte</th><th>Lien</th><th>Cree le</th><th></th></tr>
    {reinitialisations}
  </table>
  </details>

  <details class="section"{ouvrir_rapports}>
  <summary><h1>Rapports de bug {pastille}</h1> <span class="compte">{nb_rapports}</span></summary>
  <p class="sous">Les 60 derniers, le plus recent en haut, ranges par etat.
  Deplie pour voir la capture et le journal de la partie.</p>
  {rapports}
  </details>

  <details class="section"{ouvrir_salon}>
  <summary><h1>Joueurs {pastille_salon}</h1> <span class="compte">{nb_en_ligne}</span></summary>
  <p class="sous">Qui est la, et de quoi on se parle. Un message part tout de
  suite : la personne voit une pastille dans son jeu, et te repond de la.</p>
  {salon}
  </details>

  <h1 style="margin-top:2.5rem">Parties <small id="maj" style="color:#9aa7b4;font-weight:normal;font-size:.8rem">chargement…</small></h1>
  <p class="sous">Qui joue en ce moment, et les {suivi_max} dernieres parties
  finies : heros, deck, aspect, mechant, rounds et resultat. Les abandons sont
  en orange. Rafraichi tout seul toutes les 30 s. La meme chose, a epingler sur
  le telephone : <a href="/suivi">page de suivi</a>.</p>
  {suivi}

  <details class="rapport" style="margin-top:1.5rem">
    <summary><span class="quoi">Journal technique des tables</span>
    <span class="meta">allumage et extinction des 25 dernieres</span></summary>
    <div style="padding:0 .8rem .8rem">
      <table>
        <tr><th>Table</th><th>Hote</th><th>Ouverte le</th><th>Fermee le</th></tr>
        {parties}
      </table>
    </div>
  </details>
</main>
"""



# --------------------------------------------------------------------------
# Suivi des parties (page /suivi, reservee a l'administrateur)
# --------------------------------------------------------------------------
# AJOUT du 08/09/2026. Une page pour le telephone, a epingler sur l'ecran
# d'accueil : qui joue en ce moment (heros, mechant, round, depuis quand) et
# les dernieres parties terminees (heros, aspect, mechant, rounds, resultat).
#
# Deux sources, aucune nouvelle table :
#   - les tables ALLUMEES (`PARTIES`) : chaque moteur repond a
#     `/get_partie_en_cours?jeton=<jeton_site>` sur 127.0.0.1 (route ajoutee
#     dans server_get.py le meme jour) ;
#   - les journaux `games_history-serveur-<N>.json` que chaque moteur ecrit a
#     la fin d'une partie (game/rule/statistics.py), un par emplacement, lus
#     ici et fusionnes. L'emplacement donne le compte (`comptes.emplacement`).
#
# ⚠ RESERVEE A L'ADMINISTRATEUR, comme /admin : la page nomme les joueurs.

SUIVI_TERMINEES_MAX = 40
SUIVI_DELAI_MOTEUR = 1.5   # secondes, par moteur interroge


def _fiche_moteur(partie: "Partie") -> dict:
    """La fiche de la partie en cours sur ce moteur, ou {} s'il ne repond pas."""
    try:
        lien = "http://127.0.0.1:%d/get_partie_en_cours?jeton=%s" % (
            partie.port, urllib.parse.quote(partie.jeton_site or ""))
        with urllib.request.urlopen(lien, timeout=SUIVI_DELAI_MOTEUR) as reponse:
            fiche = json.loads(reponse.read().decode("utf-8"))
        return fiche if isinstance(fiche, dict) else {}
    except (urllib.error.URLError, OSError, ValueError):
        return {}


def _pseudos_par_emplacement() -> dict:
    with _cx() as cx:
        lignes = cx.execute(
            "SELECT pseudo, emplacement FROM comptes WHERE emplacement IS NOT NULL").fetchall()
    return {int(l["emplacement"]): l["pseudo"] for l in lignes}


def _depuis(secondes: float) -> str:
    secondes = max(0, int(secondes))
    if secondes < 90:
        return "a l'instant"
    if secondes < 5400:
        return "depuis %d min" % round(secondes / 60)
    if secondes < 172800:
        return "depuis %d h" % round(secondes / 3600)
    return "depuis %d j" % round(secondes / 86400)


def _il_y_a_horodatage(quand: float) -> str:
    ecart = max(0, time.time() - float(quand))
    if ecart < 90:
        return "a l'instant"
    if ecart < 5400:
        return "il y a %d min" % round(ecart / 60)
    if ecart < 172800:
        return "il y a %d h" % round(ecart / 3600)
    return "il y a %d j" % round(ecart / 86400)


CAUSES_ABANDON = {
    "extinction": "table \u00e9teinte par le joueur",
    "minuteur": "table ferm\u00e9e apr\u00e8s %d h" % int(DUREE_MAX_HEURES),
    "inactivite": "table ferm\u00e9e apr\u00e8s %d min sans jouer" % int(INACTIVITE_MINUTES),
    "moteur arrete": "moteur arr\u00eat\u00e9",
    "arret du site": "red\u00e9marrage du site",
}


def _noter_abandon(partie: "Partie", cause: str, fiche: dict | None = None) -> None:
    """La photo d'une partie qu'on eteint alors qu'elle etait EN COURS.

    ⚠ NE LEVE JAMAIS. Une trace manquee est un regret ; une exception ici
    empecherait la table de s'eteindre, donc l'emplacement d'etre rendu.

    Deux garde-fous avant d'ecrire : le moteur doit etre vivant (sinon
    `_fiche_moteur` attendrait son delai pour rien) et la partie doit avoir
    commence (une table allumee ou l'on n'a jamais quitte l'ecran des heros
    n'est pas une partie abandonnee, c'est une table qu'on ferme).
    """
    try:
        if not partie.vivant():
            return
        # ⚠ UNE SEULE INTERROGATION DU MOTEUR. `eteindre_jeu` a deja demande sa
        # fiche pour la sauvegarde : la redemander ici doublait le delai de
        # chaque extinction, sur un moteur qu'on s'apprete a tuer.
        if fiche is None:
            fiche = _fiche_moteur(partie)
        if not fiche.get("en_cours"):
            return
        with _cx() as cx:
            cx.execute(
                "INSERT INTO abandons (quand, joueur, emplacement, mechant, expert,"
                " tour, heros, vilains, manigances, cause) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (_maintenant(), partie.code, partie.emplacement,
                 str(fiche.get("scenario") or ""),
                 1 if fiche.get("expert") else 0,
                 int(fiche.get("round") or 0),
                 json.dumps(fiche.get("joueurs") or [], ensure_ascii=False),
                 json.dumps(fiche.get("vilains") or [], ensure_ascii=False),
                 json.dumps(fiche.get("manigances") or [], ensure_ascii=False),
                 cause))
    except Exception as exc:
        sys.stderr.write("trace d'abandon non ecrite : %r\n" % (exc,))


def _detail_abandon(vilains: list, manigances: list) -> str:
    """« PV 9/14 · stade 2 · menace 3 », comme sur une carte « en cours »."""
    bouts = []
    if vilains:
        vilain = vilains[0]
        if vilain.get("pv_max"):
            bouts.append("PV %s/%s" % (vilain.get("pv"), vilain.get("pv_max")))
        if vilain.get("stage"):
            bouts.append("stade %s" % vilain.get("stage"))
    if manigances:
        bouts.append("menace %s" % (manigances[0].get("menace") or 0))
    return " \u00b7 ".join(bouts)


def parties_abandonnees(limite: int = SUIVI_TERMINEES_MAX) -> list:
    """Les parties quittees en cours de route, au format des parties finies."""
    try:
        with _cx() as cx:
            lignes = cx.execute("SELECT * FROM abandons ORDER BY id DESC LIMIT ?",
                                (limite,)).fetchall()
    except sqlite3.Error:
        return []
    sortie = []
    for ligne in lignes:
        try:
            joueurs = json.loads(ligne["heros"] or "[]")
            vilains = json.loads(ligne["vilains"] or "[]")
            manigances = json.loads(ligne["manigances"] or "[]")
        except (TypeError, ValueError):
            joueurs, vilains, manigances = [], [], []
        ecart = _secondes_depuis(ligne["quand"])
        sortie.append({
            "quand": time.time() - ecart if ecart is not None else 0.0,
            "il_y_a": _il_y_a(ligne["quand"]),
            "joueur": ligne["joueur"] or "",
            "emplacement": ligne["emplacement"],
            # Meme forme que le journal, plus la forme et les PV : au moment de
            # la photo, ils sont connus, et c'est tout l'interet de la trace.
            "heros": [{"nom": str(j.get("heros") or "").lstrip("* "),
                       "card_id": str(j.get("card_id") or ""),
                       "deck": str(j.get("deck") or ""),
                       "aspects": [],
                       "forme": str(j.get("forme") or ""),
                       "pv": j.get("pv"), "pv_max": j.get("pv_max")}
                      for j in joueurs if isinstance(j, dict)],
            "mechant": ligne["mechant"] or "",
            "expert": bool(ligne["expert"]),
            "etat": "abandon",
            "victoire": False,
            "raison": CAUSES_ABANDON.get(ligne["cause"], ligne["cause"] or ""),
            "rounds": int(ligne["tour"] or 0),
            "detail": _detail_abandon(vilains, manigances),
        })
    return sortie


def parties_terminees(limite: int = SUIVI_TERMINEES_MAX) -> list:
    """Les dernieres parties FINIES, abandons compris, tous emplacements
    confondus. Deux sources qui ne se recouvrent jamais : le journal du moteur
    (fin declaree) et la table `abandons` (fin subie)."""
    proprietaires = _pseudos_par_emplacement()
    sortie = []
    for emplacement in range(1, NB_EMPLACEMENTS + 1):
        chemin = os.path.join(RACINE_JEU, "games_history-serveur-%d.json" % emplacement)
        if not os.path.isfile(chemin):
            continue
        try:
            with open(chemin, encoding="utf-8") as f:
                journal = json.load(f)
        except (OSError, ValueError):
            continue
        if not isinstance(journal, list):
            continue
        for entree in journal:
            if not isinstance(entree, dict):
                continue
            heros = []
            for h in entree.get("heroes") or []:
                if isinstance(h, dict):
                    heros.append({
                        "nom": str(h.get("name") or "").lstrip("* "),
                        "card_id": str(h.get("card_id") or ""),
                        "deck": str(h.get("deck") or ""),
                        "aspects": [str(a) for a in (h.get("aspects") or [])],
                    })
            quand = float(entree.get("time") or 0)
            sortie.append({
                "quand": quand,
                "il_y_a": _il_y_a_horodatage(quand) if quand else "",
                "joueur": proprietaires.get(emplacement, ""),
                "emplacement": emplacement,
                "heros": heros,
                "mechant": str(entree.get("scenario") or ""),
                "expert": bool(entree.get("expert")),
                "etat": "victoire" if entree.get("won") else "defaite",
                "victoire": bool(entree.get("won")),
                "raison": str(entree.get("reason") or ""),
                "rounds": int(entree.get("rounds") or 0),
                "detail": "",
            })
    sortie += parties_abandonnees(limite)
    sortie.sort(key=lambda e: e["quand"], reverse=True)
    return sortie[:limite]


def parties_en_cours() -> list:
    """Les tables allumees, avec la fiche du moteur quand il repond."""
    with VERROU:
        vivantes = [p for p in PARTIES.values() if p.vivant()]
    sortie = []
    maintenant = time.time()
    for partie in vivantes:
        fiche = _fiche_moteur(partie)
        sortie.append({
            "joueur": partie.code,
            "emplacement": partie.emplacement,
            "allumee_depuis": _depuis(maintenant - partie.debut),
            "sieges": partie.joueurs,
            "en_cours": bool(fiche.get("en_cours")),
            "round": int(fiche.get("round") or 0),
            "mechant": str(fiche.get("scenario") or ""),
            "expert": bool(fiche.get("expert")),
            "joueurs": fiche.get("joueurs") or [],
            "vilains": fiche.get("vilains") or [],
            "manigances": fiche.get("manigances") or [],
            "moteur_repond": bool(fiche),
        })
    sortie.sort(key=lambda e: (not e["en_cours"], e["emplacement"]))
    return sortie


def etat_suivi() -> dict:
    return {"maintenant": int(time.time()),
            "en_cours": parties_en_cours(),
            "terminees": parties_terminees()}


# --------------------------------------------------------------------------
# Le bloc de suivi, PARTAGE par /suivi et par /admin
# --------------------------------------------------------------------------
# ⚠ UN SEUL RENDU POUR DEUX PAGES (08/09/2026, demande de l'utilisateur : « je
# veux que le suivi soit dans /admin »). Le meme balisage, le meme script et
# les memes styles servent la page a epingler sur le telephone et la section
# « Parties » de l'administration. Dupliquer le rendu, c'etait se condamner a
# corriger deux fois chaque ligne.
#
# ⚠ LES STYLES DU BLOC SONT PREFIXES PAR `#suivi`. Sans cela, la regle `h2` du
# suivi (petites capitales grises) repeindrait les titres de /admin, et sa
# regle `.carte` mordrait sur les blocs de rapport de bug.
#
# ⚠ ET ILS PASSENT PAR UN ARGUMENT DE `.format`, jamais par le gabarit :
# PAGE_ADMIN est une chaine `.format`, ou chaque accolade de CSS ou de
# JavaScript devrait etre doublee. Injecte en argument, le bloc reste lisible
# et personne n'a a y penser.

SUIVI_STYLE_BLOC = """<style>
  #suivi h2 { font-size:.8rem; text-transform:uppercase; letter-spacing:.08em; color:#9aa7b4; margin:1.2rem 0 .5rem; }
  #suivi .carte { border:1px solid #30363d; border-radius:.7rem; padding:.7rem .85rem; margin-bottom:.55rem; background:#161b22; }
  #suivi .carte.live { border-color:#238636; box-shadow: inset 3px 0 0 #238636; }
  #suivi .carte.abandon { box-shadow: inset 3px 0 0 #9e6a03; }
  #suivi .carte.attente { border-color:#30363d; opacity:.75; }
  #suivi .ligne { display:flex; justify-content:space-between; gap:.6rem; align-items:baseline; }
  #suivi .qui { font-weight:600; }
  #suivi .quand { color:#9aa7b4; font-size:.8rem; white-space:nowrap; }
  #suivi .heros { font-size:1.05rem; margin:.15rem 0; }
  #suivi .heros .aspect { font-size:.75rem; padding:.05rem .4rem; border-radius:.3rem; margin-left:.3rem; vertical-align:middle; background:#30363d; }
  /* Le nom du deck : discret, il accompagne le heros sans lui voler la ligne. */
  #suivi .heros .deck { color:#8b949e; font-size:.78rem; margin-left:.4rem; }
  #suivi .aspect.Aggression { background:#8b1e1e; } #suivi .aspect.Justice { background:#8a6d00; color:#fff; }
  #suivi .aspect.Leadership { background:#1f4e8c; } #suivi .aspect.Protection { background:#1e6b3a; }
  #suivi .aspect.Pool { background:#6b1e8c; } #suivi .aspect.Determination { background:#5a2d8c; }
  #suivi .contre { color:#c9d1d9; }
  #suivi .contre b { color:#e6edf3; }
  #suivi .bas { display:flex; gap:.9rem; flex-wrap:wrap; color:#9aa7b4; font-size:.85rem; margin-top:.25rem; }
  /* Les boutons « Regarder », un par siege. Discrets : la liste sert d'abord a
     LIRE ce qui se passe ; on ne clique que quand on veut voir de pres. */
  #suivi .regards { display:flex; gap:.4rem; flex-wrap:wrap; margin-left:auto; }
  #suivi a.regarder { color:#58a6ff; text-decoration:none; border:1px solid #30363d;
                      border-radius:.4rem; padding:.1rem .5rem; font-size:.8rem; }
  #suivi a.regarder:hover { border-color:#58a6ff; background:#1f6feb22; }
  #suivi .res { font-weight:700; }
  #suivi .res.v { color:#3fb950; } #suivi .res.d { color:#f85149; } #suivi .res.a { color:#d29922; }
  #suivi .pv { font-variant-numeric: tabular-nums; }
  #suivi .vide { color:#9aa7b4; font-style:italic; }
  #suivi details.groupe { margin:.4rem 0; }
  #suivi details.groupe > summary { cursor:pointer; color:#c9d1d9; font-size:.9rem; padding:.35rem 0; }
  #suivi .erreur { border:1px solid #f85149; background:#1d1113; color:#ff7b72; padding:.6rem .8rem; border-radius:.5rem; }
</style>"""

# Le balisage, sans titre : chaque page pose le sien, avec le `#maj` que le
# script remplit (l'heure du dernier rafraichissement).
SUIVI_CORPS = """<div id="suivi">
<div id="erreur" class="erreur" hidden></div>
<h2>En cours</h2>
<div id="encours"><p class="vide">…</p></div>
<h2>Terminées</h2>
<div id="terminees"><p class="vide">…</p></div>
</div>"""

SUIVI_SCRIPT = """<script>
(function () {
  var ECHAP = function (t) { return String(t == null ? "" : t).replace(/[&<>"']/g, function (c) {
    return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]; }); };
  function aspects(liste) {
    return (liste || []).map(function (a) {
      var cls = String(a).replace(/[^A-Za-z]/g, "");
      return '<span class="aspect ' + cls + '">' + ECHAP(a) + '</span>';
    }).join("");
  }
  function carteEnCours(p) {
    var joueurs = p.joueurs || [];
    var vil = (p.vilains || [])[0];
    var men = (p.manigances || [])[0];
    var titre = '<div class="ligne"><span class="qui">' + ECHAP(p.joueur) + (p.sieges > 1 ? ' · ' + p.sieges + ' sièges' : '') + '</span>'
              + '<span class="quand">' + ECHAP(p.allumee_depuis) + '</span></div>';
    if (!p.en_cours) {
      var etat = p.moteur_repond ? "table allumée, pas de partie en cours" : "moteur muet";
      return '<div class="carte attente">' + titre + '<div class="contre">' + etat + '</div></div>';
    }
    var h = joueurs.map(function (j) {
      var deck = j.deck ? ' <span class="deck">' + ECHAP(j.deck) + '</span>' : '';
      return '<div class="heros">' + ECHAP(j.heros) + (j.forme === "AlterEgo" ? ' <small>(alter ego)</small>' : '')
           + deck + ' <span class="pv">' + j.pv + '/' + j.pv_max + '</span>' + (j.elimine ? ' ✝' : '') + '</div>';
    }).join("");
    var contre = '<div class="contre">contre <b>' + ECHAP(p.mechant) + '</b>' + (p.expert ? ' (expert)' : '')
               + (vil ? ' · PV ' + vil.pv + '/' + vil.pv_max + (vil.stage ? ' · stade ' + ECHAP(vil.stage) : '') : '')
               + (men ? ' · menace ' + men.menace : '') + '</div>';
    // ⚠ REGARDER LA PARTIE, UN BOUTON PAR SIEGE (15/09/2026). L'utilisateur
    // voulait « le plateau, en vrai, comme si j'y etais », et pouvoir changer
    // de siege. Un bouton par siege ouvert est la facon la plus directe : on
    // arrive DIRECTEMENT par les yeux de celui qu'on a choisi.
    //
    // Le lien passe par /regarder, jamais par l'adresse du moteur : elle seule
    // connait le mot de passe de la table, et elle est refusee a tout autre
    // que l'administrateur.
    var regarder = '';
    for (var i = 0; i < Math.max(1, p.sieges || 1); i++) {
      var nom = joueurs[i] && joueurs[i].heros ? joueurs[i].heros : ('Joueur ' + (i + 1));
      regarder += '<a class="regarder" target="_blank" rel="noopener" href="/regarder?joueur='
                + encodeURIComponent(p.joueur) + '&p=' + i + '">Regarder · ' + ECHAP(nom) + '</a>';
    }
    var bas = '<div class="bas"><span>round <b>' + p.round + '</b></span>'
            + '<span class="regards">' + regarder + '</span></div>';
    return '<div class="carte live">' + titre + h + contre + bas + '</div>';
  }
  function ligneHeros(x) {
    // Les PV et la forme ne sont connus que des parties ABANDONNEES (photo
    // prise en cours de jeu) : absents, ils ne s'affichent pas.
    var forme = x.forme === "AlterEgo" ? ' <small>(alter ego)</small>' : '';
    var pv = x.pv_max ? ' <span class="pv">' + x.pv + '/' + x.pv_max + '</span>' : '';
    // Le nom du DECK, demande des l'origine et longtemps absent de l'affichage
    // alors que les deux sources le portaient deja (08/09/2026).
    var deck = x.deck ? ' <span class="deck">' + ECHAP(x.deck) + '</span>' : '';
    return '<div class="heros">' + ECHAP(x.nom) + forme + aspects(x.aspects) + deck + pv + '</div>';
  }
  function carteTerminee(p) {
    var abandon = p.etat === "abandon";
    var h = (p.heros || []).map(ligneHeros).join("") || '<div class="heros">?</div>';
    var titre = '<div class="ligne"><span class="qui">' + ECHAP(p.joueur || ("table " + p.emplacement)) + '</span>'
              + '<span class="quand">' + ECHAP(p.il_y_a) + '</span></div>';
    var contre = '<div class="contre">contre <b>' + ECHAP(p.mechant) + '</b>' + (p.expert ? ' (expert)' : '')
               + (p.detail ? ' · ' + ECHAP(p.detail) : '') + '</div>';
    var res = abandon ? '<span class="res a">Abandonnée</span>'
            : p.etat === "victoire" ? '<span class="res v">Victoire</span>'
            : '<span class="res d">Défaite</span>';
    var tours = abandon ? ('au round ' + p.rounds)
              : (p.rounds + ' round' + (p.rounds > 1 ? 's' : ''));
    var bas = '<div class="bas">' + res + '<span>' + tours + '</span>'
            + '<span>' + ECHAP(p.raison) + '</span></div>';
    return '<div class="carte' + (abandon ? ' abandon' : '') + '">' + titre + h + contre + bas + '</div>';
  }
  function rendre(etat) {
    var ec = document.getElementById("encours"), te = document.getElementById("terminees");
    ec.innerHTML = (etat.en_cours || []).length ? etat.en_cours.map(carteEnCours).join("") : '<p class="vide">Personne ne joue en ce moment.</p>';
    // Trois groupes replies (12/09/2026, « je dois defiler trop longtemps ») :
    // gagnees, perdues, abandonnees, chacun avec son compte.
    var finies = etat.terminees || [];
    var groupes = [["Gagnées", finies.filter(function (p) { return p.etat === "victoire"; })],
                   ["Perdues", finies.filter(function (p) { return p.etat !== "victoire" && p.etat !== "abandon"; })],
                   ["Abandonnées", finies.filter(function (p) { return p.etat === "abandon"; })]];
    te.innerHTML = finies.length
      ? groupes.filter(function (g) { return g[1].length; }).map(function (g) {
          return '<details class="groupe"><summary>' + g[0] + ' (' + g[1].length + ')</summary>'
               + g[1].map(carteTerminee).join("") + '</details>';
        }).join("")
      : '<p class="vide">Aucune partie terminée.</p>';
    var d = new Date((etat.maintenant || Date.now() / 1000) * 1000);
    document.getElementById("maj").textContent = "à " + d.toLocaleTimeString("fr-FR", {hour: "2-digit", minute: "2-digit"});
  }
  function charger() {
    fetch("/api/suivi", {credentials: "same-origin", cache: "no-store"}).then(function (r) {
      if (r.status === 403) { location.href = "/"; return null; }
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function (etat) {
      if (!etat) return;
      document.getElementById("erreur").hidden = true;
      rendre(etat);
    }).catch(function (e) {
      var err = document.getElementById("erreur");
      err.textContent = "Le site ne répond pas : " + e.message;
      err.hidden = false;
    });
  }
  charger();
  setInterval(charger, 30000);
  document.addEventListener("visibilitychange", function () { if (!document.hidden) charger(); });
})();
</script>"""

PAGE_SUIVI = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#0e1116">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="/suivi.webmanifest">
<link rel="icon" href="/suivi-192.png">
<link rel="apple-touch-icon" href="/suivi-192.png">
<title>Suivi des parties</title>
<style>
  :root { color-scheme: dark; }
  * { box-sizing: border-box; }
  body { margin:0; font:15px/1.4 system-ui,sans-serif; background:#0e1116; color:#e6edf3;
         padding: max(.8rem, env(safe-area-inset-top)) .8rem 2rem; }
  h1 { font-size:1.15rem; margin:.2rem 0 .8rem; display:flex; justify-content:space-between; align-items:baseline; }
  h1 small { color:#9aa7b4; font-weight:normal; font-size:.8rem; }
  .pied { color:#6e7681; font-size:.75rem; margin-top:1.5rem; text-align:center; }
  .pied a { color:#9aa7b4; }
</style>
""" + SUIVI_STYLE_BLOC + """
<h1>Parties <small id="maj">chargement…</small></h1>
""" + SUIVI_CORPS + """
<p class="pied">Rafraîchie toutes les 30 s · <a href="/suivi">recharger</a> · <a href="/admin">administration</a></p>
""" + SUIVI_SCRIPT + """
"""

MANIFESTE_SUIVI = json.dumps({
    "name": "Suivi des parties NarwhalChampions",
    "short_name": "Parties",
    "start_url": "/suivi",
    "scope": "/",
    "display": "standalone",
    "background_color": "#0e1116",
    "theme_color": "#0e1116",
    "icons": [
        {"src": "/suivi-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/suivi-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"},
    ],
}, ensure_ascii=False).encode("utf-8")


# L'APPLI INSTALLABLE (13/09/2026, premiere des idees marvelsimulator).
#
# « Ajouter a l'ecran d'accueil » depuis le navigateur du telephone : une icone,
# un plein ecran sans barre d'adresse, rien a publier sur un store. Trois pieces
# suffisent : ce manifeste, deux icones, et un service worker.
#
# ⚠ INSTALLEE SUR LE SITE, PAS SUR LA TABLE (decision de l'utilisateur). Une
# appli est liee a UNE adresse ; la table d'un compte est sur p<N>.<domaine>,
# qui ne repond pas quand elle est eteinte. `/entrer` allume la table au besoin
# et y envoie : ca marche toujours. Contrepartie assumee : une fois sur la
# table, le navigateur garde une fine barre d'adresse, l'appli ayant change de
# domaine.
#
# ⚠ LE SERVICE WORKER NE MET RIEN EN CACHE. Le navigateur en exige un pour
# proposer l'installation, et c'est son seul role ici : ce site se bat deja
# contre les caches perimes (cookie de version), un worker qui servirait un
# vieux JS apres un deploiement serait exactement le defaut qu'on a chasse.
MANIFESTE_APPLI = json.dumps({
    "name": "NarwhalChampions",
    "short_name": "Narwhal",
    # ⚠ « EN LIGNE » EST DANS LA DESCRIPTION, ET C'EST VOLONTAIRE. Android la
    # montre dans la boite d'installation. Une icone sur l'ecran d'accueil
    # promet implicitement le hors ligne ; ici c'est impossible par
    # construction, le moteur tourne sur le serveur et chaque action passe
    # par lui. Mieux vaut le dire avant l'installation qu'apres.
    "description": "Marvel Champions entre amis. Raccourci vers le jeu : une connexion est necessaire pour jouer, rien ne fonctionne hors ligne.",
    "start_url": "/entrer",
    "scope": "/",
    "display": "standalone",
    "orientation": "any",
    "background_color": "#0e1116",
    "theme_color": "#0e1116",
    "lang": "fr",
    "icons": [
        {"src": "/app-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/app-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "/app-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"},
    ],
}, ensure_ascii=False).encode("utf-8")

# L'ECRAN « PAS DE CONNEXION » (13/09/2026).
#
# Sans lui, ouvrir l'appli sans reseau donne la page d'erreur du navigateur, qui
# ne dit rien du jeu. Celle-ci dit ce qui se passe, pourquoi, et propose de
# reessayer. Elle est volontairement AUTONOME : aucune feuille de style, aucune
# image, aucun script externe. Tout ce qu'elle reclamerait serait justement ce
# qu'on ne peut pas aller chercher.
PAGE_HORS_LIGNE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pas de connexion - NarwhalChampions</title>
<style>
  :root { color-scheme: dark; }
  body { margin:0; min-height:100vh; display:flex; align-items:center; justify-content:center;
         font:16px/1.6 system-ui,sans-serif; background:#0e1116; color:#e6edf3; padding:2rem 1.2rem; }
  main { max-width:26rem; text-align:center; }
  h1 { font-size:1.4rem; margin:0 0 .6rem; }
  p { color:#9aa7b4; margin:0 0 1.4rem; }
  button { font:inherit; background:#1f6feb; color:#fff; border:0; border-radius:.5rem;
           padding:.7rem 1.4rem; cursor:pointer; }
</style>
<main>
  <h1>Pas de connexion</h1>
  <p>NarwhalChampions a besoin du reseau pour tourner : la partie se joue sur
  le serveur, pas sur ton telephone. Reconnecte-toi et reessaie.</p>
  <button onclick="location.replace('/entrer')">Reessayer</button>
</main>
""".encode("utf-8")

SERVICE_WORKER = """// NarwhalChampions : un service worker qui ne fait RIEN, et c'est voulu.
// Le navigateur en exige un pour proposer « Ajouter a l'ecran d'accueil ».
// ⚠ IL NE MET EN CACHE QU'UNE SEULE PAGE, ET JAMAIS LE JEU. Ce site se bat
// contre le cache perime : un worker qui servirait un vieux JS apres un
// deploiement serait le defaut qu'on a chasse. La seule chose gardee ici est
// l'ecran « Pas de connexion », qui n'est JAMAIS servi quand le reseau repond.
//
// Deux verrous, et il faut les deux :
//   - on n'intercepte que les NAVIGATIONS (request.mode === 'navigate') : ni JS,
//     ni CSS, ni image, ni appel d'API ne passent par ici ;
//   - on va TOUJOURS au reseau d'abord, et on ne rend la page de secours que
//     si le reseau echoue. Une reponse du serveur, meme une erreur, gagne.
const SECOURS = '/hors-ligne.html';
const BOITE = 'narwhal-secours-v1';

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(BOITE).then((c) => c.add(SECOURS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
  // Les boites d'une version precedente partent : rien de ce qu'elles
  // contiennent ne doit survivre a une mise a jour.
  e.waitUntil(caches.keys()
    .then((noms) => Promise.all(noms.filter((n) => n !== BOITE).map((n) => caches.delete(n))))
    .then(() => self.clients.claim()));
});
self.addEventListener('fetch', (e) => {
  if (e.request.mode !== 'navigate') return;
  e.respondWith(fetch(e.request).catch(() => caches.match(SECOURS)));
});
""".encode("utf-8")

# Les lignes a poser dans <head> de chaque page publique.
TETE_APPLI = ('<link rel="manifest" href="/manifest.webmanifest">'
              '<meta name="theme-color" content="#0e1116">'
              # L'onglet prend le narval DETOURE (fond transparent) ; l'icone
              # d'accueil, elle, est pleine, bord a bord, comme les stores le
              # demandent.
              '<link rel="icon" type="image/png" href="/favicon.png">'
              '<link rel="apple-touch-icon" href="/app-192.png">'
              '<meta name="apple-mobile-web-app-capable" content="yes">'
              '<script>if("serviceWorker"in navigator)navigator.serviceWorker.register("/sw.js").catch(function(){});</script>')
# LE BOUTON « INSTALLER L'APPLICATION » (13/09/2026, demande de l'utilisateur :
# « un vrai bouton qu'on peut installer sous Android »).
#
# Sous Android, Chrome previent la page quand l'installation est possible
# (`beforeinstallprompt`). On retient l'evenement, on montre le bouton, et un
# clic ouvre la boite d'installation native. Sans ce bouton, le geste restait
# cache dans le menu du navigateur. Sur iPhone il n'y a pas d'evenement : on
# affiche a la place le chemin a suivre, Partager puis « Sur l'ecran
# d'accueil ». Une fois installee, l'appli tourne en plein ecran et le bouton
# n'a plus lieu d'etre : on le tait.
BOUTON_APPLI = (
    '<div id="appli-installer" hidden style="margin:1.2rem 0 0;padding:.8rem .9rem;'
    'border:1px solid #30363d;border-radius:.5rem;background:#161b22;font-size:.9rem">'
    '<button id="appli-bouton" type="button" style="width:100%;font:inherit;background:#238636;'
    'color:#fff;border:0;border-radius:.5rem;padding:.7rem;cursor:pointer">'
    'Installer l\'application sur ce telephone</button>'
    '<p id="appli-ios" hidden style="margin:.4rem 0 0;color:#9aa7b4">Sur iPhone : bouton Partager, '
    'puis « Sur l\'ecran d\'accueil ».</p>'
    # ⚠ DIT AVANT L'INSTALLATION, pas apres. Une icone sur l'ecran d'accueil
    # laisse croire au hors ligne ; le jeu tourne sur le serveur, il n'y a
    # rien a jouer sans connexion.
    '<p style="margin:.5rem 0 0;color:#9aa7b4;font-size:.85rem">C\'est un raccourci '
    'vers le jeu, pas une version hors ligne : il faut une connexion pour jouer.</p>'
    '</div>'
    '<script>(function(){'
    'var bloc=document.getElementById("appli-installer"),bouton=document.getElementById("appli-bouton"),'
    'ios=document.getElementById("appli-ios"),retenu=null;'
    'if(window.matchMedia("(display-mode: standalone)").matches||navigator.standalone===true)return;'
    'window.addEventListener("beforeinstallprompt",function(e){e.preventDefault();retenu=e;bloc.hidden=false;});'
    'bouton.addEventListener("click",function(){if(!retenu)return;retenu.prompt();'
    'retenu.userChoice.then(function(){retenu=null;bloc.hidden=true;});});'
    'window.addEventListener("appinstalled",function(){bloc.hidden=true;});'
    'if(/iPhone|iPad|iPod/.test(navigator.userAgent)){bouton.hidden=true;ios.hidden=false;bloc.hidden=false;}'
    '})();</script>')

# ⚠ POSEE UNE FOIS, ICI, ET NON PAR UN ARGUMENT DE `.format`. Les gabarits sont
# formates a six endroits differents ; une cle oubliee a l'un d'eux faisait
# tomber le serveur sur cette page (KeyError, connexion fermee sans reponse),
# constate au premier passage du test de parcours. Les accolades des gabarits
# sont doublees (`{{ }}`) sauf les cles : on substitue la notre avant tout
# `.format`, et elle n'existe plus pour lui.
# ⚠ ET LES ACCOLADES DU SCRIPT SONT DOUBLEES : `catch(function(){})` contient
# un `{}` que `.format` prendrait pour un champ positionnel (IndexError, vu au
# premier essai). Doublees, elles redeviennent des accolades pour lui.
_TETE_POUR_FORMAT = TETE_APPLI.replace("{", "{{").replace("}", "}}")
_BOUTON_POUR_FORMAT = BOUTON_APPLI.replace("{", "{{").replace("}", "}}")
PAGE = PAGE.replace("{tete_appli}", _TETE_POUR_FORMAT).replace("{bouton_appli}", _BOUTON_POUR_FORMAT)
PAGE_FORMULAIRE = PAGE_FORMULAIRE.replace("{tete_appli}", _TETE_POUR_FORMAT).replace("{bouton_appli}", _BOUTON_POUR_FORMAT)

# L'heure locale, ajoutee aux deux pages qui montrent des dates ABSOLUES.
#
# ⚠ MEME PIEGE QUE CI-DESSUS, ET LA MEME PARADE : le script est plein
# d'accolades, `.format` y verrait des champs positionnels. On les double.
#
# ⚠ `PAGE_SUIVI` N'EN A PAS BESOIN, ET CE N'EST PAS UN OUBLI. Elle n'affiche
# que des durees (« il y a 3 min », « allumee depuis 2 h »), qui ne dependent
# d'aucun fuseau. Un premier jet l'incluait quand meme : le `replace` ne
# trouvait aucun `</main>` (cette page n'en a pas) et ne faisait donc RIEN, en
# silence. Une ligne qui ne sert a rien et qui en a l'air est pire que pas de
# ligne : elle ferait croire le probleme traite ailleurs.
_HEURE_POUR_FORMAT = SCRIPT_HEURE_LOCALE.replace("{", "{{").replace("}", "}}")


def _avec_heure_locale(gabarit: str, nom: str) -> str:
    """Colle le script avant la fin du gabarit. ⚠ LEVE si la balise manque :
    un `replace` muet laisserait la page en UTC sans que personne le voie."""
    if "</main>" not in gabarit:
        raise RuntimeError(f"{nom} n'a pas de </main> : le script d'heure locale ne peut pas y entrer")
    return gabarit.replace("</main>", "</main>" + _HEURE_POUR_FORMAT, 1)


PAGE = _avec_heure_locale(PAGE, "PAGE")
PAGE_ADMIN = _avec_heure_locale(PAGE_ADMIN, "PAGE_ADMIN")


def _icone_appli(nom: str) -> bytes | None:
    if nom not in ("app-192.png", "app-512.png", "favicon.png"):
        return None
    try:
        with open(os.path.join(RACINE_SITE, "static", nom), "rb") as f:
            return f.read()
    except OSError:
        return None


def _icone_suivi(nom: str) -> bytes | None:
    if nom not in ("suivi-192.png", "suivi-512.png"):
        return None
    try:
        with open(os.path.join(RACINE_SITE, "static", nom), "rb") as f:
            return f.read()
    except OSError:
        return None


class Handler(BaseHTTPRequestHandler):

    @property
    def chemin(self) -> str:
        """Le chemin demande, SANS la chaine de requete.

        ⚠ `self.path` LA CONTIENT, ET C'EST LE PIEGE. Un formulaire
        `<form method="get" action="/reprendre">` sans champ envoie
        « /reprendre? », avec le point d'interrogation : compare a
        « /reprendre », l'egalite est fausse et le site repond « Introuvable ».

        Defaut constate EN PRODUCTION le 14/09/2026 sur le bouton « Reprendre »
        de la page de reprise : il n'a JAMAIS pu marcher depuis sa livraison, et
        aucune erreur ne le signalait — une route qui ne correspond a rien tombe
        simplement dans le `else` final. Les 33 comparaisons de ce fichier
        portaient toutes sur `self.path`.

        Toute route se compare desormais a `self.chemin`. Un test le fait
        respecter (`site/test_routes_chemin.py`).
        """
        return urllib.parse.urlparse(self.path).path

    @property
    def parametres(self) -> dict:
        """La chaine de requete, decoupee. Pendant de `chemin`.

        Rendue au format de `parse_qs` (une LISTE par cle) : une route qui
        attend une seule valeur prend le premier element, et personne ne se fait
        surprendre par un parametre repete.
        """
        return urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

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

        ⚠ ET CE QUI TIENT ICI, C'EST QUE PERSONNE D'AUTRE QUE CADDY NE PARLE AU
        SERVICE. On ne verifie pas le pair, on ne le pourrait pas : derriere le
        proxy, il est toujours 127.0.0.1. La surete vient d'ailleurs, et de deux
        choses seulement : `main` ecoute sur `127.0.0.1` et non sur `0.0.0.0`,
        et le pare-feu de la machine n'ouvre que 80 et 443. Le jour ou l'une des
        deux tombe, n'importe qui choisit son adresse d'un en-tete et le frein
        de `/connexion` ne freine plus rien.
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
        80 vers lui de lui-meme. Mais le meme fichier tourne en local sur
        `http://127.0.0.1:8080`, sans proxy devant : `Secure` en dur y ferait
        jeter le cookie par le navigateur, et la connexion tournerait en rond
        sans rien dire.

        ⚠ ET `DOMAINE` NE VAUT PAS PREUVE. Il l'a valu, et c'etait un piege :
        sur le serveur meme, `curl http://127.0.0.1:8080` ou un coup d'oeil au
        service sans passer par Caddy recevaient un cookie que le navigateur
        jette, pour la seule raison qu'une variable d'environnement est
        renseignee. Seul `X-Forwarded-Proto: https` dit quelque chose de la
        requete en cours, et c'est Caddy qui l'ecrit.

        ⚠ LA FALSIFICATION NE RAPPORTE RIEN ICI. Un client qui mentirait sur
        `X-Forwarded-Proto` ne ferait que durcir SON PROPRE cookie, ou le
        rendre inutilisable pour lui seul. Rien a y gagner.
        """
        if (self.headers.get("X-Forwarded-Proto") or "").strip().lower() == "https":
            return "; Secure"
        return ""

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
                  'Pas encore de compte ? <a href="/inscription">En demander un</a>.'
                  ' Mot de passe oublie ? Demande un lien de reinitialisation a l\'administrateur.'
                  # ⚠ LA REGLE EST ANNONCEE, PAS SUBIE. Le site ne sait pas
                  # envoyer de courriel : personne ne peut etre prevenu de son
                  # expiration. La seule facon honnete de la faire accepter est
                  # de l'ecrire la ou tout le monde passe.
                  ' Les places sont comptees : %d jours sans venir et la tienne'
                  ' retourne au pot. Ecris-moi, je te la rends.' % EXPIRATION_JOURS),
        ).encode("utf-8")

    def _formulaire_reinitialisation(self, jeton: str, erreur: str = "") -> bytes:
        """Le formulaire du nouveau mot de passe, sur le gabarit commun."""
        return PAGE_FORMULAIRE.format(
            titre="Nouveau mot de passe",
            action="/reinitialisation", bouton="Enregistrer", auto="new-password",
            champs='<input type="hidden" name="r" value="%s">' % html.escape(jeton),
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            pied="Huit caracteres au minimum. Tes sessions ouvertes seront fermees."
                 ' <a href="/connexion">Se connecter</a>.',
        ).encode("utf-8")

    def _servir_capture(self) -> None:
        """L'image d'un rapport, designee par le NUMERO du rapport.

        Le nom du fichier vient de la base, jamais de l'adresse : c'est ce qui
        rend la traversee de dossier impossible ici.
        """
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
                actions += ('<form method="post" action="/admin">'
                            '<input type="hidden" name="action" value="reinitialiser">'
                            '<input type="hidden" name="pseudo" value="%s">'
                            '<button type="submit" title="Creer un lien pour choisir un nouveau mot de passe">'
                            'Mot de passe</button></form>' % html.escape(c["pseudo"]))
            lignes.append(
                "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                    html.escape(c["pseudo"]), html.escape(c["email"] or "—"),
                    html.escape(c["cree"] or ""),
                    html.escape(_visite_lisible(c)),
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
                       % (html.escape(lien), _horodate(i["cree_le"]),
                          html.escape(i["jeton"])))
        for i in invitations_utilisees():
            inv.append("<tr><td>—</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
                _horodate(i["cree_le"]), html.escape(i["utilise_par"] or ""),
                html.escape(i["utilise_le"] or "")))
        if not inv:
            inv.append('<tr><td colspan="4">Aucune invitation. '
                       'Cree-en une ci-dessus.</td></tr>')
        reinit = []
        for r in reinitialisations_ouvertes():
            lien = "%s/reinitialisation?r=%s" % (base, r["jeton"])
            reinit.append('<tr><td>%s</td><td><code>%s</code></td><td>%s</td>'
                          '<td><form method="post" action="/admin">'
                          '<input type="hidden" name="action" value="reinit_annuler">'
                          '<input type="hidden" name="jeton" value="%s">'
                          '<button class="non" type="submit">Annuler</button></form></td></tr>'
                          % (html.escape(r["pseudo"]), html.escape(lien),
                             _horodate(r["cree_le"]), html.escape(r["jeton"])))
        if not reinit:
            reinit.append('<tr><td colspan="4">Aucun lien en cours. Le bouton '
                          '« Mot de passe » d\'un compte en cree un.</td></tr>')
        tous_rapports = liste_rapports()
        rapports = ""
        for etat_r, libelle_r in (("nouveau", "Nouveaux"), ("en cours", "En cours"), ("traite", "Traites")):
            groupe = [r for r in tous_rapports if (r["etat"] or "nouveau") == etat_r]
            if not groupe:
                continue
            rapports += ('<details class="groupe"%s><summary>%s (%d)</summary>%s</details>'
                         % (" open" if etat_r == "nouveau" else "", libelle_r, len(groupe),
                            "".join(self._bloc_rapport(r) for r in groupe)))
        if not rapports:
            rapports = '<p class="sous">Aucun rapport. Bonne nouvelle.</p>'
        # L'annonce : son etat en une phrase, et le bouton d'annulation qui
        # n'existe que s'il y a quelque chose a annuler.
        en_cours = annonce_courante()
        if en_cours is None:
            annonce_etat = ("Aucune annonce. Le message apparait en haut du "
                            "plateau et de l'assistant, avec le decompte, "
                            "chez tous les joueurs connectes.")
            annonce_annuler = ""
        else:
            annonce_etat = ('Annonce en cours, encore %d minute(s) : « %s »'
                            % (max(1, round(en_cours["secondes"] / 60)),
                               html.escape(en_cours["texte"])))
            # ⚠ UN FORMULAIRE A PART, PAS UN SECOND BOUTON. Dans le
            # formulaire ci-dessus, le champ cache `action` part en premier et
            # `_champs` ne garde que la premiere valeur : le bouton d'annulation
            # aurait repose une annonce au lieu de l'effacer.
            annonce_annuler = ('<form method="post" action="/admin"'
                               ' style="margin:-1.5rem 0 2rem">'
                               '<input type="hidden" name="action" value="annonce_annuler">'
                               '<button class="non" type="submit">Annuler l\'annonce</button>'
                               '</form>')
        # Le panneau des joueurs : un bloc par personne, avec sa conversation
        # et de quoi repondre. ⚠ ON MONTRE TOUT LE MONDE, pas seulement ceux
        # qui sont en ligne : ecrire a quelqu'un d'absent est justement l'usage
        # le plus courant, il lira en revenant.
        qui = presence()
        nb_en_ligne = sum(1 for p in qui if p["etat"] in ("ligne", "partie"))
        attente_salon = messages_non_lus(ADMIN)
        pastille_salon = ('<span class="pastille">%d nouveau%s</span>'
                          % (attente_salon["nouveaux"],
                             "x" if attente_salon["nouveaux"] > 1 else "")
                          ) if attente_salon["nouveaux"] else ""
        salon = ""
        for personne in qui:
            if personne["pseudo"] == ADMIN:
                continue
            echange = conversation(ADMIN, personne["pseudo"])
            lignes_msg = "".join(
                '<div class="msg %s"><b>%s</b> <span class="meta">%s</span><br>%s</div>'
                % ("moi" if m["pseudo"] == ADMIN else "lui",
                   html.escape(m["pseudo"]), _horodate(m["quand"]),
                   html.escape(m["texte"]).replace("\n", "<br>"))
                for m in echange) or '<p class="sous">Rien encore.</p>'
            nouveau = personne["pseudo"] in attente_salon["de"]
            salon += (
                '<details class="rapport"%s><summary>'
                '<span class="quoi"><b>%s</b> %s</span>'
                '<span class="meta">%s</span></summary>'
                '<div class="corps">%s'
                '<form method="post" action="/admin" style="display:flex;gap:.5rem;margin-top:.6rem">'
                '<input type="hidden" name="action" value="message">'
                '<input type="hidden" name="a" value="%s">'
                '<input name="texte" maxlength="%d" placeholder="Ecrire a %s" required'
                ' style="flex:1;font:inherit;background:#161b22;color:inherit;'
                'border:1px solid #30363d;border-radius:.4rem;padding:.4rem .6rem">'
                '<button class="oui" type="submit">Envoyer</button>'
                '</form></div></details>'
                % (" open" if nouveau else "",
                   html.escape(personne["pseudo"]),
                   '<span class="pastille">nouveau</span>' if nouveau else "",
                   html.escape(personne["detail"]),
                   lignes_msg, html.escape(personne["pseudo"]),
                   TAILLE_MESSAGE, html.escape(personne["pseudo"])))
        if not salon:
            salon = '<p class="sous">Aucun compte valide a qui ecrire.</p>'
        nb_invitations = len(invitations_libres()) + len(invitations_utilisees())
        nb_reinit = len(reinitialisations_ouvertes())
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
        # ⚠ Le bloc de suivi et ses styles passent en ARGUMENTS, jamais dans
        # le gabarit : PAGE_ADMIN est une chaine `.format`, ou chaque accolade
        # de CSS ou de JavaScript devrait etre doublee.
        return PAGE_ADMIN.format(valides=nb_valides(), max=MAX_COMPTES,
                                 lignes="".join(lignes),
                                 invitations="".join(inv),
                                 reinitialisations="".join(reinit),
                                 rapports=rapports, pastille=pastille,
                                 salon=salon, nb_en_ligne=nb_en_ligne,
                                 pastille_salon=pastille_salon,
                                 ouvrir_salon=" open" if attente_salon["nouveaux"] else "",
                                 regle_expiration=(
                                     "Sans visite pendant %d jours, un compte passe"
                                     " en « expire » : sa place retourne au pot, ses"
                                     " decks et ses campagnes l'attendent tant que"
                                     " personne ne la prend. « Valider » le remet en"
                                     " service." % EXPIRATION_JOURS),
                                 annonce_etat=annonce_etat,
                                 annonce_annuler=annonce_annuler,
                                 annonce_max=ANNONCE_MINUTES_MAX,
                                 nb_rapports=len(tous_rapports),
                                 nb_invitations=nb_invitations, nb_reinit=nb_reinit,
                                 # Une section s'ouvre d'elle-meme quand elle
                                 # attend quelque chose de l'administrateur.
                                 ouvrir_rapports=" open" if nouveaux else "",
                                 ouvrir_reinit=" open" if nb_reinit else "",
                                 parties=parties,
                                 suivi_max=SUIVI_TERMINEES_MAX,
                                 styles_suivi=SUIVI_STYLE_BLOC,
                                 suivi=SUIVI_CORPS + SUIVI_SCRIPT).encode("utf-8")

    @staticmethod
    def _bloc_rapport(r: dict) -> str:
        """Un rapport replie. TOUT ce qui vient du rapport passe par
        html.escape : la description, le nom et le journal sont ecrits par
        n'importe qui, y compris par un invite qu'on ne connait pas."""
        etat = r["etat"] or "nouveau"
        classe = {"nouveau": "nouveau", "en cours": "encours", "traite": "traite",
                  "refuse": "refuse"}.get(etat, "nouveau")
        boutons = ""
        for cible, libelle in (("en cours", "Prendre"), ("traite", "Classer"),
                               ("refuse", "Refuser")):
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

        # ⚠ LE FIL N'EXISTE QUE POUR UN TICKET. Un rapport d'invite n'a pas de
        # proprietaire connu (voir `_est_un_ticket`) : lui offrir un champ de
        # reponse promettrait une reponse qui n'atteindrait personne. On le dit
        # plutot que de faire semblant.
        if _est_un_ticket(r):
            ticket = ticket_de(r["id"]) or {}
            fil = ""
            for m in ticket.get("messages") or []:
                fil += ('<p class="msg %s"><b>%s</b> <span class="sous">%s</span><br>%s</p>'
                        % ("de-moi" if m["auteur"] == "admin" else "de-lui",
                           "Moi" if m["auteur"] == "admin" else html.escape(r["nom"] or "Le joueur"),
                           _horodate(m["quand"] or ""),
                           html.escape(m["texte"] or "").replace("\n", "<br>")))
            if not fil:
                fil = '<p class="sous">Aucun echange pour l\'instant.</p>'
            fil += ('<form method="post" action="/admin" class="repondre">'
                    '<input type="hidden" name="action" value="rapport_repondre">'
                    '<input type="hidden" name="id" value="%d">'
                    '<textarea name="texte" rows="2" placeholder="Repondre a %s"></textarea>'
                    '<button type="submit">Repondre</button></form>'
                    % (r["id"], html.escape(r["hote"] or "")))
        else:
            fil = ('<p class="sous">Rapport envoye depuis un siege invite : on ne '
                   'sait pas a quel compte il appartient, il n\'y a donc pas de fil.</p>')

        return ('<details class="rapport">'
                '<summary><span class="etat %s">%s</span>'
                '<span class="quoi">%s</span>'
                '<span class="meta">%s &middot; %s &middot; %s</span></summary>'
                '<div class="corps"><p>%s</p>%s%s<div class="fil">%s</div><p>%s</p></div></details>'
                % (classe, html.escape(etat),
                   html.escape((r["description"] or "")[:110]),
                   html.escape(r["nom"] or "?"), html.escape(ou),
                   _horodate(r["quand"] or ""),
                   html.escape(r["description"] or "").replace("\n", "<br>"),
                   image, journal, fil, boutons))

    def do_GET(self):
        pseudo = self._session()
        if self.chemin in ("/", "/index.html"):
            # ⚠ LE SITE N'EST QU'UNE PORTE. Qui est connecte n'a rien a faire
            # ici : il veut son jeu, pas une page d'accueil. Qui ne l'est pas
            # voit le formulaire tout de suite, sans page intermediaire.
            if pseudo:
                self._rediriger("/entrer")
            else:
                self._repondre(200, self._formulaire("connexion"))
        elif self.chemin in ("/entrer", "/reprendre", "/nouvelle-partie"):
            if not pseudo:
                self._rediriger("/")
                return
            # ⚠ « Commencer autre chose » OUBLIE la partie, il ne la charge pas :
            # sans cela le bandeau revenait a chaque visite, et le joueur devait
            # le refuser indefiniment.
            if self.chemin == "/nouvelle-partie":
                oublier_partie_interrompue(pseudo)
                self._rediriger("/entrer")
                return
            # Le joueur a dit oui : on note qu'il faut charger sa partie des que
            # son moteur repond. `demarrer_en_fond` peut prendre une dizaine de
            # secondes, on ne bloque pas la reponse pour autant.
            if self.chemin == "/reprendre":
                A_REPRENDRE.add(pseudo)
            toucher_presence(pseudo)
            partie = jeu_de(pseudo)
            # ⚠ LA QUESTION NE SE POSE QUE TABLE ETEINTE. Une partie
            # interrompue n'existe que parce que la table a ete tuee ; si le
            # moteur tourne deja, il n'y a rien a reprendre et rien a demander.
            if self.chemin == "/entrer" and (partie is None or not partie.vivant()):
                attendue = partie_interrompue(pseudo)
                if attendue:
                    self._repondre(200, page_reprise(pseudo, attendue))
                    return
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
        elif self.chemin == "/arret":
            if not pseudo:
                self._rediriger("/")
                return
            self._repondre(200, page_arret(pseudo))
        elif self.chemin == "/signalements":
            # ⚠ SESSION OBLIGATOIRE : la page nomme des bugs et montre des
            # captures d'ecran de partie. Un visiteur sans compte n'a rien a y
            # voir, et `tickets_de("")` rendrait de toute facon une liste vide.
            if not pseudo:
                self._rediriger("/")
                return
            # Ouvrir la page vaut lecture : les reponses cessent d'attendre.
            for _t in tickets_de(pseudo):
                marquer_ticket_lu(_t["id"], "joueur")
            self._repondre(200, page_signalements(pseudo))
        elif self.chemin.startswith("/inscription"):
            requete = urllib.parse.urlparse(self.path)
            jeton = urllib.parse.parse_qs(requete.query).get("i", [""])[0]
            if not INSCRIPTION_LIBRE and not invitation_valide(jeton):
                self._repondre(403, self._formulaire(
                    "inscription", "Il faut un lien d'invitation pour creer un compte ici."))
                return
            self._repondre(200, self._formulaire("inscription", jeton=jeton))
        elif self.chemin == "/connexion":
            self._repondre(200, self._formulaire("connexion"))
        elif self.chemin == "/deconnexion":
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
                             "nc_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0"
                             + self._secure())
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.chemin.startswith("/reinitialisation"):
            jeton = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("r", [""])[0]
            if reinitialisation_valide(jeton) is None:
                self._repondre(410, self._formulaire_reinitialisation(
                    "", "Ce lien n'est plus valable. Demande un nouveau lien a l'administrateur."))
                return
            self._repondre(200, self._formulaire_reinitialisation(jeton))
        elif self.chemin == "/admin":
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._repondre(200, self._page_admin())
        elif self.chemin == "/suivi":
            # La page de suivi nomme les joueurs : reservee a l'administrateur,
            # comme /admin. Un visiteur non connecte est envoye au formulaire.
            if not pseudo:
                self._rediriger("/")
                return
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._repondre(200, PAGE_SUIVI.encode("utf-8"))
        elif self.chemin == "/regarder":
            # ⚠ REGARDER UNE PARTIE EN COURS, SANS Y TOUCHER (15/09/2026).
            #
            # Demande de l'utilisateur : « c'est possible d'ajouter un truc qui
            # me permet de voir en live les parties que les gens jouent
            # actuellement ? ». Reponses au cadrage : le plateau en vrai, toutes
            # les mains visibles, LUI SEUL, et « regarder seulement, rien de
            # cliquable ».
            #
            # Cette route ne rend rien elle-meme : elle FABRIQUE le lien que
            # personne d'autre ne peut fabriquer, parce qu'elle seule connait le
            # mot de passe de la table (`comptes.mdp_jeu`). Le moteur, de son
            # cote, ouvre la lecture sans distribuer de siege (`/spectateur`).
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            vise = (self.parametres.get("joueur") or [""])[0].strip().lower()
            try:
                siege = int((self.parametres.get("p") or ["0"])[0])
            except ValueError:
                siege = 0
            partie = jeu_de(vise)
            if partie is None or not partie.vivant():
                # La table s'est eteinte entre l'affichage de la liste et le
                # clic : on le DIT, plutot que d'envoyer sur une adresse morte.
                self._rediriger("/suivi?disparue=" + urllib.parse.quote(vise))
                return
            if siege < 0 or siege > 3:
                siege = 0
            cle = urllib.parse.quote(partie.mot_de_passe)
            self._rediriger(f"{partie.base_url()}/spectateur?p={siege}&key={cle}")
        elif self.chemin == "/api/suivi":
            if pseudo != ADMIN:
                self._repondre(403, b'{"error":"admin"}', "application/json; charset=utf-8")
                return
            corps = json.dumps(etat_suivi(), ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
        elif self.chemin == "/manifest.webmanifest":
            self._repondre(200, MANIFESTE_APPLI, "application/manifest+json; charset=utf-8")
        elif self.chemin == "/hors-ligne.html":
            self._repondre(200, PAGE_HORS_LIGNE, "text/html; charset=utf-8")
        elif self.chemin == "/sw.js":
            # ⚠ SANS CACHE HTTP non plus : un worker mis en cache par le
            # navigateur survivrait a sa propre mise a jour.
            self._repondre(200, SERVICE_WORKER, "application/javascript; charset=utf-8")
        elif self.chemin in ("/app-192.png", "/app-512.png", "/favicon.png", "/favicon.ico"):
            # /favicon.ico : les navigateurs le demandent d'office, on leur
            # rend le meme narval plutot qu'un 404 a chaque page.
            image = _icone_appli("favicon.png" if self.chemin == "/favicon.ico" else self.chemin[1:])
            if image is None:
                self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")
                return
            self._repondre(200, image, "image/png")
        elif self.chemin == "/suivi.webmanifest":
            # Public : le manifeste ne contient que des libelles, et le
            # navigateur le demande SANS cookie.
            self._repondre(200, MANIFESTE_SUIVI, "application/manifest+json; charset=utf-8")
        elif self.chemin in ("/suivi-192.png", "/suivi-512.png"):
            image = _icone_suivi(self.chemin[1:])
            if image is None:
                self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")
                return
            self._repondre(200, image, "image/png")
        elif self.chemin.startswith("/admin/capture"):
            # La capture d'un rapport, reservee a l'administrateur comme la
            # page qui l'affiche. On ne sert JAMAIS le nom de fichier venu de
            # l'adresse : on lit celui que la base associe au numero demande,
            # sans quoi n'importe quel chemin sortirait du dossier.
            if pseudo != ADMIN:
                self._repondre(403, b"Reserve a l'administrateur.", "text/plain; charset=utf-8")
                return
            self._servir_capture()
        elif self.chemin == "/etat":
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

        if self.chemin == "/signalements":
            # ⚠ LE JOUEUR NE REPOND QUE SUR SES PROPRES TICKETS. On ne se fie
            # pas au numero envoye : on le cherche dans SES tickets. Sans cette
            # verification, n'importe quel compte connecte pourrait ecrire dans
            # le fil d'un autre en changeant un champ cache.
            if not pseudo:
                self._rediriger("/")
                return
            champs = self._champs()
            try:
                numero = int(champs.get("id", "0"))
            except ValueError:
                numero = 0
            if numero and any(x["id"] == numero for x in tickets_de(pseudo)):
                ecrire_message(numero, "joueur", champs.get("texte", ""))
            self._rediriger("/signalements")
            return

        if self.chemin == "/inscription":
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

        elif self.chemin == "/reinitialisation":
            champs = self._champs()
            try:
                qui = reinitialiser_mot_de_passe(champs.get("r", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire_reinitialisation(champs.get("r", ""), str(erreur)))
                return
            self._repondre(200, PAGE_FORMULAIRE.format(
                titre="Mot de passe enregistre", action="/connexion", bouton="Entrer",
                auto="current-password", erreur="",
                champs='<label>Pseudo ou adresse e-mail<input name="pseudo" '
                       'autocomplete="username" value="%s" required></label>' % html.escape(qui),
                pied="Ton nouveau mot de passe est en place : connecte-toi.").encode("utf-8"))

        elif self.chemin == "/connexion":
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

        elif self.chemin == "/admin":
            # Le controle passe AVANT la lecture du corps : un inconnu n'a pas
            # a faire allouer un octet sur une route qui va le refuser.
            if pseudo != ADMIN:
                self._raccrocher()
                self._repondre(403, b"Reserve a l'administrateur.",
                               "text/plain; charset=utf-8")
                return
            champs = self._champs()
            action = champs.get("action", "")
            if action == "annonce":
                try:
                    minutes = int(champs.get("minutes", "10") or "10")
                except ValueError:
                    minutes = 10
                poser_annonce(minutes, champs.get("texte", ""))
            elif action == "annonce_annuler":
                retirer_annonce()
            elif action == "message":
                # ⚠ ON MARQUE LU EN MEME TEMPS QU'ON REPOND : repondre, c'est
                # avoir lu. Sans cela, la pastille de l'administrateur restait
                # allumee sur une conversation qu'il venait de traiter.
                dire(ADMIN, champs.get("texte", ""), champs.get("a", ""))
                marquer_messages_lus(ADMIN)
            elif action == "messages_lus":
                marquer_messages_lus(ADMIN)
            elif action == "inviter":
                creer_invitation()
            elif action == "annuler":
                supprimer_invitation(champs.get("jeton", ""))
            elif action == "reinitialiser":
                try:
                    creer_reinitialisation(champs.get("pseudo", ""))
                except ValueError:
                    pass          # compte inconnu : rien a creer, la page se reaffiche
            elif action == "reinit_annuler":
                supprimer_reinitialisation(champs.get("jeton", ""))
            elif action in ("rapport", "rapport_supprimer", "rapport_repondre"):
                try:
                    numero = int(champs.get("id", "0"))
                except ValueError:
                    numero = 0
                if numero:
                    if action == "rapport":
                        changer_etat_rapport(numero, champs.get("etat", ""))
                    elif action == "rapport_repondre":
                        # ⚠ REPONDRE VAUT LECTURE. L'administrateur qui ecrit a
                        # forcement lu ce qui precede : sans ce marquage, sa
                        # propre pastille resterait allumee sur un fil qu'il
                        # vient de traiter.
                        if ecrire_message(numero, "admin", champs.get("texte", "")):
                            marquer_ticket_lu(numero, "admin")
                    else:
                        supprimer_rapport(numero)
            else:
                changer_statut(champs.get("pseudo", "").strip().lower(),
                               champs.get("statut", ""))
            self._rediriger("/admin")

        elif self.chemin in ("/api/vue", "/api/dire", "/api/bug", "/api/annonce",
                           "/api/prives", "/api/prives_lus"):
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
            if self.chemin == "/api/bug":
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
            if self.chemin == "/api/prives":
                # ⚠ PAS DE `toucher_presence` ICI. C'est une horloge qui
                # tourne, pas un geste du joueur : la compter comme une
                # presence ferait apparaitre « en ligne » quelqu'un qui a
                # laisse un onglet ouvert. Meme raison que pour l'annonce.
                self._repondre(200, json.dumps(messages_non_lus(qui),
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/prives_lus":
                marquer_messages_lus(qui)
                self._repondre(200, b'{"ok":true}',
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/annonce":
                # ⚠ AUCUNE RESERVE DE SIEGE, ET AUCUN SIGNE DE VIE NON PLUS.
                # Un preavis d'extinction concerne tout le monde a la table,
                # invite compris : c'est meme lui qui n'a aucun autre moyen
                # d'etre prevenu. Et ce n'est pas un geste du joueur, juste une
                # horloge qui tourne : la compter comme une presence ferait
                # apparaitre « en ligne » quelqu'un qui a laisse un onglet
                # ouvert.
                self._repondre(200, json.dumps(annonce_courante() or {},
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/dire":
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

        elif self.chemin == "/eteindre":
            # Aucun champ a lire ici : le bouton n'envoie rien, et le pseudo
            # vient du cookie. On ne touche donc pas au corps du tout.
            if not pseudo:
                self._raccrocher()
                self._rediriger("/")
                return
            self._raccrocher()
            # ⚠ ON COUPE LES ACCES D'ABORD, ON ETEINT ENSUITE, ET L'ORDRE EST
            # TOUT. C'est le seul geste du site qui soit VOLONTAIRE : la
            # personne dit qu'elle a fini. On perime donc le laissez-passer du
            # moteur, sans quoi les invites de la soiree gardent un cookie
            # valable un an. Ni le faucheur ni un plantage ne passent par ici :
            # une table qui redemarre toute seule ne doit pas laisser son
            # proprietaire dehors.
            #
            # Et si l'on revoquait APRES, `eteindre_jeu` tenant la main jusqu'a
            # quinze secondes, le `meta refresh` de la page d'attente aurait
            # tout le temps de rappeler `/entrer` : un moteur repartait avec
            # l'ANCIEN mot de passe et la revocation le manquait.
            revoquer_mot_de_passe_jeu(pseudo)
            # On n'eteint QUE son propre jeu : le code est le pseudo.
            eteindre_jeu(pseudo)
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
    orphelines = fermer_parties_orphelines()
    if orphelines:
        print(f"  {orphelines} table(s) laissee(s) ouverte(s) par la session precedente : fermees.")
    if compte(ADMIN) is None:
        print(f"  ⚠ Aucun compte administrateur « {ADMIN} » : cree-le sur /inscription,")
        print("    il sera valide d'office.")
    threading.Thread(target=faucheur, daemon=True).start()
    serveur = ThreadingHTTPServer(("127.0.0.1", PORT_SITE), Handler)

    def arreter(*_):
        print("\nFermeture de toutes les tables...")
        for code in list(PARTIES):
            eteindre_jeu(code, "arret du site")
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
            eteindre_jeu(code, "arret du site")
    return 0


def purge_en_ligne_de_commande(arguments: list) -> int:
    """`orchestrateur.py purger-rapports [jours]`, pour `deploiement/purge.sh`.

    ⚠ LA PURGE NE PASSE PAS PAR LE SHELL POUR LA BASE. Effacer les fichiers
    avec `find` et laisser les lignes derriere donnerait une page
    d'administration qui renvoie vers des captures disparues. L'orchestrateur
    est le seul qui sache faire les deux d'un coup : le script l'appelle plutot
    que de recopier la regle.

    ⚠ ET DEPUIS LE 16/09/2026 ELLE ALLEGE, ELLE N'EFFACE PLUS : un rapport est
    devenu un ticket que son auteur consulte, seule la capture part. Le compte
    rendu le dit, sans quoi le journal de la purge annoncerait des suppressions
    qui n'ont pas lieu.
    """
    try:
        jours = int(arguments[0]) if arguments else JOURS_RAPPORTS_TRAITES
    except ValueError:
        print(f"Nombre de jours invalide : {arguments[0]}", file=sys.stderr)
        return 2
    if not os.path.isfile(BASE):
        print(f"  (base absente, rien a purger) {BASE}")
        return 0
    alleges = purger_rapports_traites(jours)
    print(f"  rapports traites depuis plus de {jours} jours : "
          f"{alleges} allege(s), capture retiree, fil conserve")
    return 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "purger-rapports":
        sys.exit(purge_en_ligne_de_commande(sys.argv[2:]))
    sys.exit(main())
