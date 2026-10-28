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
import re
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

# L'ID CLIENT de l'application Discord (panneau developpeur -> OAuth2), pour
# `/activite` (voir DISCORD.md). Public par nature (il part dans le HTML
# servi au navigateur) : PAS un secret, contrairement a un jeton d'API. Vide =
# l'activite Discord est desactivee (`/activite` repond 404), le reste du
# site est INCHANGE.
DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID", "")

PORT_SITE = int(os.environ.get("PORT_SITE", "8080"))
PORT_BASE = 2350                      # emplacement N -> port PORT_BASE + N
NB_EMPLACEMENTS = int(os.environ.get("NB_EMPLACEMENTS", "30"))

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
# trente minutes non.
#
# ⚠ 45 -> 30 MINUTES LE 16/09/2026, en cherchant a tenir plus de joueurs sur la
# meme machine. Une table coute 221 Mo et la machine en a 3,8 Go : ce qui
# limite, c'est le nombre de tables ALLUMEES EN MEME TEMPS, pas le nombre de
# comptes. Trente minutes sans la moindre action, c'est quelqu'un parti manger
# ou qui a ferme son onglet ; il retrouvera sa partie dans « Reprendre », et sa
# table se rallume en quelques secondes.
#
# ⚠ CE REGLAGE N'AVAIT AUCUN EFFET APRES UN DEPLOIEMENT, et c'est corrige le
# meme jour : mes journaux de moteur partaient dans l'archive et ecrasaient
# ceux du serveur, donc `secondes_sans_jouer` lisait la date du deploiement.
# Voir l'exclusion de `.site` dans `deploiement/deployer.ps1`.
INACTIVITE_MINUTES = float(os.environ.get("INACTIVITE_MINUTES", "30"))
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
# Les SAUVEGARDES DU CODE (08/10/2026) : un zip par deploiement (tout le projet
# sans les images, historique compris), pose par deploiement/deployer-tout.sh,
# les 5 derniers gardes. HORS de site/ : le deploiement vide ce dossier.
DOSSIER_SAUVEGARDES_CODE = os.environ.get(
    "DOSSIER_SAUVEGARDES_CODE", os.path.join(os.path.dirname(RACINE_SITE), "sauvegardes-code"))


# Les IMAGES du jeu (scans, vignettes, HD, sons, documents), servies d'un bloc a
# l'administrateur pour reconstruire un poste a partir d'une sauvegarde du code.
DOSSIER_ASSETS = os.environ.get(
    "DOSSIER_ASSETS", os.path.join(os.path.dirname(RACINE_SITE), "Fusion", "marvel-lcg-src", "assets"))


# Les PROJETS DU CREATEUR DE CARTES (fichiers JSON, un dossier par compte).
# HORS de site/ : le deploiement vide ce dossier (sauf base et rapports).
DOSSIER_CREATEUR = os.environ.get(
    "DOSSIER_CREATEUR", os.path.join(os.path.dirname(RACINE_SITE), "donnees-createur"))
# Un projet porte des images en data URL : 25 Mo au plus, par PUT.
MAX_PROJET_OCTETS = int(os.environ.get("MAX_PROJET_OCTETS", str(25 * 1024 * 1024)))
# Quota par compte (projets + historique des versions).
QUOTA_CREATEUR_OCTETS = int(os.environ.get("QUOTA_CREATEUR_OCTETS", str(500 * 1024 * 1024)))
# La page et ses fichiers statiques sont ceux du jeu (public/).
DOSSIER_PUBLIC_JEU = os.environ.get("DOSSIER_PUBLIC_JEU", os.path.join(RACINE_JEU, "public"))

DOSSIER_PARTIES_JOUEURS = os.environ.get(
    "DOSSIER_PARTIES_JOUEURS", os.path.join(os.path.dirname(RACINE_SITE), "parties-joueurs"))


def parties_des_joueurs(dossier: str = "") -> dict[str, list[str]]:
    """{pseudo: [fichiers .marvelreplay, le plus recent en tete]}, joueurs tries."""
    dossier = dossier or DOSSIER_PARTIES_JOUEURS
    resultat: dict[str, list[str]] = {}
    try:
        pseudos = sorted(os.listdir(dossier))
    except OSError:
        return resultat
    for pseudo in pseudos:
        try:
            noms = os.listdir(os.path.join(dossier, pseudo))
        except OSError:
            continue
        parties = sorted((n for n in noms if n.endswith(".marvelreplay")), reverse=True)
        if parties:
            resultat[pseudo] = parties
    return resultat


def sauvegardes_du_code(dossier: str = "") -> list[str]:
    """Les zips de sauvegarde, le plus recent en tete (le nom porte la date)."""
    dossier = dossier or DOSSIER_SAUVEGARDES_CODE
    try:
        noms = os.listdir(dossier)
    except OSError:
        return []
    return sorted((n for n in noms if n.startswith("code-") and n.endswith(".zip")), reverse=True)
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
# ⚠ UN ETAT SANS GROUPE EST UN RAPPORT INVISIBLE. L'ecran d'administration
# classait les rapports par une liste ECRITE EN DUR ; en ajoutant « refuse »
# le 16/09/2026 sans toucher a cette liste, un rapport refuse disparaissait de
# la page — le bouton existait, on cliquait, et le rapport s'evanouissait.
# Les libelles vivent donc ici, a cote des etats, et l'ecran les DERIVE.
LIBELLES_ETAT_RAPPORT = {
    "nouveau": "Nouveaux",
    "en cours": "En cours",
    "traite": "Traités",
    "refuse": "Refusés",
}
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
import config_serveur
import langue as lang
import createur_cartes
import narval as narval_du_moment  # noqa: E402  (dependant de sys.path ci-dessus)


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
        # La V2 mobile reste privee pendant sa construction. Le site est le
        # seul endroit qui connait le compte ; le moteur, lui, ne connait que
        # la cle du siege. On lui transmet donc une destination distincte
        # uniquement pour le compte d'essai. La route `/claim_seat` verifiera
        # ensuite la cle du siege 0 avant de poser le temoin V2.
        destination = "prepare-v2" if self.code.strip().lower() == "arnaud" else "prepare"
        return f"{self.base_url()}/claim_seat?p=0&key={cle}&to={destination}"

    def solo(self) -> bool:
        return self.joueurs <= 1

    def vivant(self) -> bool:
        return self.processus is not None and self.processus.poll() is None


PARTIES: dict[str, Partie] = {}          # code -> Partie
EMPLACEMENTS: dict[int, str] = {}        # emplacement -> code
JETONS_SITE: dict[str, str] = {}         # jeton -> pseudo (voir Partie.jeton_site)
VERROU = threading.Lock()

# --------------------------------------------------------------------------
# Activité Discord : une table par salon vocal (demande de l'utilisateur,
# 28/09/2026 -- « jouer depuis Discord »).
# --------------------------------------------------------------------------
# instance_id (fourni par le SDK Discord embarque, un par lancement d'une
# activite dans un salon vocal) -> pseudo de l'hote qui a ouvert cette
# activite EN PREMIER. Purement en memoire, comme `PARTIES` : une activite ne
# survit pas un redemarrage du site, et c'est le bon repli -- elle redemande
# simplement qui en est l'hote a la prochaine ouverture.
INSTANCES_DISCORD: dict[str, str] = {}


def role_activite_discord(instance_id: str, pseudo: str | None) -> tuple[str, str | None]:
    """Decide qui est CE visiteur pour CETTE activite Discord.

    Rend (role, hote) ou role vaut :
      - "connexion_requise" : personne n'a encore ouvert cette activite, et ce
        visiteur n'est pas connecte -- il doit se connecter AVANT de pouvoir
        devenir l'hote (jamais d'inscription proposee dans ce parcours,
        recapitulatif valide avec l'utilisateur).
      - "hote" : il vient de le devenir (premiere ouverture, deja connecte),
        ou il l'etait deja (reouverture de SA propre activite). `hote` porte
        alors son propre pseudo.
      - "participant" : quelqu'un d'autre est deja hote de cette activite.
        `hote` porte le pseudo de cette autre personne.

    Atomique : deux visiteurs qui ouvrent la MEME activite au meme instant ne
    peuvent jamais devenir hote tous les deux (verifier-puis-creer sous
    `VERROU`, meme discipline que `lancer_jeu`).
    """
    deja = INSTANCES_DISCORD.get(instance_id)
    if deja is None:
        if not pseudo:
            return "connexion_requise", None
        with VERROU:
            deja = INSTANCES_DISCORD.get(instance_id)
            if deja is None:
                INSTANCES_DISCORD[instance_id] = pseudo
                # Nouvel hote, nouvelle table : les sieges repartent de zero.
                SIEGES_DISCORD.pop(instance_id, None)
                deja = pseudo
    return ("hote" if deja == pseudo else "participant"), deja


# Par activite Discord : numero de siege -> qui l'occupe (pseudo, ou jeton
# d'invite anonyme). En memoire, comme `INSTANCES_DISCORD`.
SIEGES_DISCORD: dict[str, dict[int, str]] = {}


def siege_activite_discord(instance_id: str, identite: str, sieges: list[dict]) -> dict | None:
    """Le siege de CE participant a CETTE activite.

    Le sien s'il en a deja un (il revient apres une deconnexion ou un
    rechargement), sinon le premier libre, sinon None (table complete).
    `sieges` : les liens de siege invites de la table (`Partie.liens()` sans
    le siege 0). Sous `VERROU` : deux participants qui arrivent ensemble ne
    recoivent jamais le meme siege.

    ⚠ AVANT (28/09/2026), TOUT LE MONDE RECEVAIT LE SIEGE 1 : le second
    invite aurait pris la place du premier. Le moteur ne sait pas qui tient un
    siege avant le debut de la partie, c'est donc ici que l'on tient le compte.
    """
    with VERROU:
        pris = SIEGES_DISCORD.setdefault(instance_id, {})
        for numero, qui in pris.items():
            if qui == identite:
                for s in sieges:
                    if s["siege"] == numero:
                        return s
        for s in sieges:
            if s["siege"] not in pris:
                pris[s["siege"]] = identite
                return s
    return None


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
    racine = f"https://{DOMAINE}" if DOMAINE else f"http://127.0.0.1:{PORT_SITE}"
    # L'adresse PUBLIQUE du site, pour tout le monde (19/09/2026) : le jeu est
    # servi depuis `pN.<domaine>`, donc un lien relatif vers une page du site
    # tombe sur le moteur. Le bouton « Mes signalements » de l'ecran de
    # preparation en a besoin, et il n'a rien d'un privilege.
    cfg["site_url"] = racine
    if partie.code == ADMIN:
        cfg["site_admin_url"] = racine + "/admin"
    # Essai « Nouvelle phase du mechant » (10/10/2026) : reserve aux comptes
    # coches dans /admin. Toute la table le voit, invites compris.
    if essai_phase_de(partie.code):
        cfg["essai_phase_mechant"] = True
    # Liste des joueurs et tchat : le MOTEUR interroge le site en local, et le
    # navigateur ne parle qu'a son propre domaine. Sans ce detour il faudrait
    # ouvrir le site aux requetes croisees de p1..p20 et desserrer le SameSite
    # du cookie de session, pour un service qui n'en vaut pas le prix.
    cfg["site_interne"] = f"http://127.0.0.1:{PORT_SITE}"
    cfg["site_jeton"] = partie.jeton_site
    # Les parties TERMINEES de l'hote, rangees par le moteur pour l'administrateur
    # (engine/enregistrement.py, 08/10/2026).
    cfg["pseudo_hote"] = partie.code
    cfg["parties_joueurs_dossier"] = DOSSIER_PARTIES_JOUEURS

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
    """Efface les donnees de la partie précédente sur cet emplacement.

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
        raise RuntimeError("Le moteur n'a pas répondu à temps.")
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

# ⚠⚠ COURSE CORRIGEE (23/09/2026, signale par l'utilisateur : « on fait
# resume et on arrive sur la page de choix de style de partie »). `lancer_jeu`
# ATTEND DEJA que le moteur reponde avant de rendre la main -- donc des que
# `demarrer_en_fond` en ressort, `/pret` (interroge par la page d'attente
# toutes les 1,5 s, DANS UNE AUTRE REQUETE) voit le port repondre et redirige
# aussitot le joueur vers la table, AVANT que `charger_partie_interrompue`
# (appelee juste apres, dans le MEME fil de fond) n'ait eu le temps d'envoyer
# le rechargement de la sauvegarde au moteur. Le joueur atterrit donc sur
# l'ecran par defaut du moteur -- le choix de heros et de scenario -- une
# ou deux secondes avant que sa partie ne soit effectivement rechargee, sans
# que rien ne rafraichisse la page pour lui. Rempli juste avant l'appel a
# `charger_partie_interrompue`, vide juste apres (succes ou echec) : `/pret`
# doit rester « pas encore » tant que ce chargement est en cours.
REPRISE_EN_COURS: set[str] = set()


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
        # ⚠ `/debug` EXIGE DEUX COOKIES, PAS SEULEMENT LE MOT DE PASSE
        # (25/09/2026, signale en jeu : « Reprendre cette partie » retombait
        # toujours sur l'écran de preparation). `session_token` ET
        # `app_version` (IsAuthenticate/IsVersionMatch, web_server.py) : sans
        # eux, le moteur repond un simple 200 + page d'authentification —
        # PAS une erreur — et la commande /load n'est jamais executee.
        # `urllib.request.urlopen` nu, sans cookie, laissait donc cet echec
        # totalement silencieux.
        #
        # `session_token` = md5(mot de passe) est deterministe (meme formule
        # que `IsAuthenticate`, cote moteur). `app_version`, lui, ne l'est
        # PAS depuis ce processus : c'est le moteur qui le calcule
        # (`Ver.ui_version_str`, buildvers a build), donc on le lui demande
        # d'abord via `/get_version`, route deliberement SANS authentification
        # (c'est le bootstrap qui pose ce cookie chez un vrai navigateur).
        jeton_session = hashlib.md5(partie.mot_de_passe.encode()).hexdigest()
        lien_version = "http://127.0.0.1:%d/get_version" % partie.port
        with urllib.request.urlopen(lien_version, timeout=10) as reponse:
            app_version = reponse.read().decode("utf-8", "replace").strip()
        cookies = f"session_token={jeton_session}; app_version={app_version}"
        # `:-1` = reprendre au DERNIER pas enregistre, comme le bouton
        # « Reprendre » de l'assistant.
        #
        # ⚠ TOUTE LA COMMANDE PASSE PAR `quote()`, PAS SEULEMENT LE FICHIER
        # (25/09/2026, trouve APRES le correctif des cookies ci-dessus : le
        # bouton retombait toujours sur l'écran de preparation). L'espace
        # entre « /load » et le chemin restait litteral dans l'URL — Python
        # 3.10 le refuse net : `http.client.InvalidURL: URL can't contain
        # control characters ... (found at least ' ')`. Cette exception
        # N'EST PAS un `URLError`/`OSError`/`ValueError` : le `except`
        # ci-dessous ne l'attrapait jamais, elle remontait crue jusqu'au
        # thread de fond (`demarrer_en_fond`), qui l'avalait dans
        # `ERREURS_DEMARRAGE` sans que rien ne le dise au joueur. Verifie en
        # direct contre le moteur reel : 200 + corps = la commande telle
        # quelle une fois `quote()` sur l'ensemble, plus d'exception.
        commande = f"/load {attendue['fichier']}:-1"
        lien = "http://127.0.0.1:%d/debug?%s" % (partie.port, urllib.parse.quote(commande, safe="/:"))
        requete = urllib.request.Request(lien, headers={"Cookie": cookies})
        with urllib.request.urlopen(requete, timeout=30) as reponse:
            reponse.read()
        # ⚠ `/debug` NE FAIT QUE POSER LA COMMANDE EN FILE
        # (`console.SetCommand`), IL NE L'EXECUTE PAS AVANT DE REPONDRE
        # (`handle_debug_command`, server_sync.py) : verifie en direct
        # contre le moteur reel, la reponse HTTP revient en ~5 ms et
        # `/get_partie_en_cours` dit encore `en_cours: false` juste apres.
        # Sans cette attente, `charger_partie_interrompue` rend `True` avant
        # que la partie ne soit reellement chargee -- exactement « LA COURSE
        # DU 24/09/2026 » documentee plus haut dans ce fichier
        # (`REPRISE_EN_COURS`), mais un cran plus loin : cette fois la
        # course n'est plus entre deux REQUETES separees, mais entre CETTE
        # requete et le fil de jeu interne du moteur qui la traite.
        lien_etat = "http://127.0.0.1:%d/get_partie_en_cours?jeton=%s" % (
            partie.port, urllib.parse.quote(partie.jeton_site or ""))
        for _ in range(30):
            with urllib.request.urlopen(lien_etat, timeout=5) as reponse:
                etat = json.loads(reponse.read())
            if etat.get("en_cours"):
                return True
            time.sleep(0.3)
        sys.stderr.write("reprise impossible pour %s : chargement jamais confirme\n" % pseudo)
        return False
    except (urllib.error.URLError, OSError, ValueError) as exc:
        sys.stderr.write("reprise impossible pour %s : %r\n" % (pseudo, exc))
        return False


def demarrer_en_fond(pseudo: str, joueurs: int = 1) -> None:
    """Allume le moteur SANS retenir la requete HTTP.

    ⚠ NE PAS APPELER `lancer_jeu` DEPUIS UNE ROUTE. Le premier allumage peut
    prendre plusieurs minutes : le navigateur abandonnerait bien avant, en ne
    montrant qu'une page blanche. On demarre donc a cote, et la page d'attente
    se rafraichit jusqu'a ce que le moteur reponde.

    `joueurs` : nombre de sieges a ouvrir des l'allumage (voir `lancer_jeu`).
    Sert a l'hote d'une activite Discord, qui doit pouvoir inviter d'autres
    personnes du salon vocal des le depart, sans passer par `/reprendre`.
    """
    with VERROU_DEMARRAGE:
        if pseudo in DEMARRAGES:
            return              # deja en route : ne pas en lancer un second
        DEMARRAGES.add(pseudo)
        ERREURS_DEMARRAGE.pop(pseudo, None)

    def travail() -> None:
        try:
            partie = lancer_jeu(pseudo, joueurs)
            journal_partie_ouverte(partie, pseudo)
            # ⚠ APRES `lancer_jeu`, QUI ATTEND DEJA QUE LE MOTEUR REPONDE : lui
            # demander de charger avant qu'il ecoute ne donnerait rien.
            if pseudo in A_REPRENDRE:
                REPRISE_EN_COURS.add(pseudo)
                try:
                    charger_partie_interrompue(partie, pseudo)
                finally:
                    REPRISE_EN_COURS.discard(pseudo)
        except Exception as erreur:
            ERREURS_DEMARRAGE[pseudo] = str(erreur)
        finally:
            # ⚠ TOUJOURS ICI, MEME SI `lancer_jeu` A LEVE. Avant, ce retrait
            # vivait dans le `if` ci-dessus, apres un `lancer_jeu` reussi : un
            # echec de demarrage (moteur mort, port deja pris...) laissait
            # `pseudo` dans `A_REPRENDRE` pour de bon, et `/pret` -- qui le
            # verifie desormais aussi -- restait bloque a `false` sur TOUT
            # lancement suivant de ce compte, meme sans rapport avec une
            # reprise, jusqu'au redemarrage du site.
            A_REPRENDRE.discard(pseudo)
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


def _abandonner_les_assemblees(partie) -> None:
    """KINGSFALL MULTI-TABLES (22/10/2026, decision 2 de l'utilisateur) : une table qui ferme avant la fin de sa partie compte comme une DEFAITE de son groupe
    dans chaque assemblee ou elle joue encore. Le stockage commun est un petit fichier SQLite du jeu (`assemblees.db`, a la racine du moteur) ; le module
    est autonome (stdlib), on le charge par son chemin. Ne bloque JAMAIS l'extinction d'une table."""
    try:
        import importlib.util
        chemin_module = os.path.join(RACINE_JEU, "src", "game", "operate", "assemblee.py")
        if not os.path.exists(chemin_module) or not os.path.exists(os.path.join(RACINE_JEU, "assemblees.db")):
            return
        os.environ["MCLCG_ASSEMBLEES"] = os.path.join(RACINE_JEU, "assemblees.db")
        spec = importlib.util.spec_from_file_location("assemblee_site", chemin_module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.Assemblee.AbandonnerTable(f"p{partie.emplacement}")
    except Exception as souci:
        sys.stderr.write("abandon d'assemblee non note : %r\n" % (souci,))


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
    _abandonner_les_assemblees(partie)
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


def eteindre_volontairement(code: str, cause: str = "extinction",
                            differer: bool = False):
    """La table est fermee PARCE QU'ON L'A DEMANDE : acces coupes, puis moteur.

    ⚠ ON COUPE LES ACCES D'ABORD, ON ETEINT ENSUITE, ET L'ORDRE EST TOUT.
    Les DEUX gestes qui passent par ici sont VOLONTAIRES : le bouton
    « Terminer » du site (`/eteindre`) et « Quitter la partie » du plateau
    (`/api/eteindre`). Dans les deux cas la personne dit qu'elle a fini, et
    l'on perime donc le laissez-passer du moteur, sans quoi les invites de la
    soiree gardent un cookie valable un an. Ni le faucheur ni un plantage ne
    passent par ici, et c'est voulu : une table qui redemarre toute seule ne
    doit pas laisser son proprietaire dehors (docstring de
    `revoquer_mot_de_passe_jeu`, qui l'interdit nommement).

    Et si l'on revoquait APRES, `eteindre_jeu` tenant la main jusqu'a quinze
    secondes, le `meta refresh` de la page d'attente aurait tout le temps de
    rappeler `/entrer` : un moteur repartait avec l'ANCIEN mot de passe et la
    revocation le manquait.

    `differer` coupe les acces MAINTENANT et rend la fonction qui eteindra —
    a appeler une fois qu'on a repondu.
    ⚠ C'est indispensable a l'appelant qui doit encore REPONDRE au moteur
    qu'on est en train de tuer (`/api/eteindre`) : eteindre avant de repondre,
    c'est tuer le messager, et le plateau reste sur une page morte sans savoir
    ou aller. Meme demarrer le fil une ligne trop tot laisse la course
    ouverte, et il n'y a aucune raison de la laisser ouverte.
    """
    revoquer_mot_de_passe_jeu(code)
    if not differer:
        eteindre_jeu(code, cause)
        return None

    def plus_tard():
        # ⚠ La globale `eteindre_jeu` est resolue A L'APPEL, dans le fil : un
        # test qui l'observe en la remplacant voit donc bien passer l'appel.
        threading.Thread(target=lambda: eteindre_jeu(code, cause),
                         daemon=True).start()

    return plus_tard


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
-- Rapports de bug. `hote` est le compte PROPRIETAIRE DE LA TABLE (celui que
-- designe le jeton de partie), et ne change jamais de sens : c'est lui que
-- lit `rapports_de_ses_tables`, pour que l'hote voie TOUT ce qui vient de
-- chez lui, qui que ce soit qui ecrive. `nom` est ce que la personne a tape.
--
-- `compte_verifie` (AJOUT du 25/09/2026) est une question DIFFERENTE : le
-- compte de l'AUTEUR REEL, seulement quand on le connait avec certitude —
-- le titulaire ecrivant depuis son propre siege 0, OU N'IMPORTE QUEL siege
-- s'il porte un cookie de session verifie. C'est LUI qui ouvre un ticket
-- (`_est_un_ticket`, `tickets_de`), jamais `hote` seul : un invite connecte
-- a SON PROPRE compte sur la table d'un autre a un `hote` qui n'est pas lui,
-- et un ticket qui doit pourtant lui appartenir a lui.
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
    traite_le   TEXT,
    compte_verifie TEXT
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
-- Parties lancees sur play (moteur dans le navigateur, sans compte). Anonyme :
-- ni IP, ni navigateur, ni identifiant. Seulement de quoi compter.
CREATE TABLE IF NOT EXISTS parties_play (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    jour        TEXT NOT NULL,
    mechant     TEXT,
    heros       TEXT,
    joueurs     INTEGER NOT NULL DEFAULT 1,
    mode        TEXT,
    difficulte  TEXT
);
CREATE INDEX IF NOT EXISTS parties_play_jour ON parties_play(jour);
-- LES DEMANDES DES CREATEURS (12/10/2026) : un createur (image, carte, contenu
-- fan-made) qui n'a pas ete credite, ou qui veut que ses creations soient
-- retirees, l'ecrit depuis le lien de l'accueil. Sans compte : `contact` est
-- ce qu'il a donne pour etre recontacte (e-mail ou Discord), rien d'autre.
-- `genre` vaut « crediter » ou « retirer ».
CREATE TABLE IF NOT EXISTS demandes_createurs (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    quand    TEXT NOT NULL,
    nom      TEXT NOT NULL,
    contact  TEXT NOT NULL,
    genre    TEXT NOT NULL,
    message  TEXT NOT NULL,
    etat     TEXT NOT NULL DEFAULT 'nouvelle'
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
        # L'essai « Nouvelle phase du mechant » (10/10/2026), pose par compte
        # depuis /admin : 1 = la table de ce compte montre le nouveau panneau.
        if "essai_phase" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN essai_phase INTEGER NOT NULL DEFAULT 0")
        # Le ROLE du compte : 'joueur' (defaut, tout l'existant) ou 'createur'
        # (acces au seul createur de cartes, voir `Handler._refuser_createur`).
        # Migration douce : les comptes deja en base deviennent 'joueur'.
        if "role" not in colonnes:
            cx.execute("ALTER TABLE comptes ADD COLUMN role TEXT NOT NULL DEFAULT 'joueur'")
        # Le role que l'invitation DONNE au compte qui l'utilise.
        colonnes_inv = {r["name"] for r in cx.execute("PRAGMA table_info(invitations)")}
        if "role" not in colonnes_inv:
            cx.execute("ALTER TABLE invitations ADD COLUMN role TEXT NOT NULL DEFAULT 'joueur'")
        # Meme precaution pour les bases creees avant la purge des rapports.
        colonnes_rap = {r["name"] for r in cx.execute("PRAGMA table_info(rapports)")}
        if "traite_le" not in colonnes_rap:
            cx.execute("ALTER TABLE rapports ADD COLUMN traite_le TEXT")
        # Meme precaution pour les bases creees avant le compte verifie
        # (25/09/2026). ⚠ RATTRAPAGE OBLIGATOIRE : sans lui, chaque ticket
        # DEJA OUVERT (siege 0, l'ancienne seule condition) disparaitrait de
        # `tickets_de` au premier redemarrage, remplace par le silence — pas
        # une erreur, juste plus rien. Un compte qui attendait une reponse ne
        # la verrait plus jamais. Ceux d'avant etaient TOUS au siege 0 : leur
        # auteur verifie, c'etait `hote` lui-meme.
        if "compte_verifie" not in colonnes_rap:
            cx.execute("ALTER TABLE rapports ADD COLUMN compte_verifie TEXT")
            cx.execute("UPDATE rapports SET compte_verifie = hote"
                       " WHERE siege = 0 AND hote IS NOT NULL AND hote != ''")
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
            "SELECT pseudo FROM comptes WHERE emplacement IS NULL"
            " AND role != 'createur' ORDER BY cree")]
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


ROLES = ("joueur", "createur")


def role_de(pseudo: str) -> str:
    """Le role d'un compte ('joueur' si inconnu ou si la colonne manque)."""
    ligne = compte(pseudo)
    if ligne is None or "role" not in ligne.keys():
        return "joueur"
    return ligne["role"] or "joueur"


def est_createur(pseudo: str) -> bool:
    return bool(pseudo) and pseudo != ADMIN and role_de(pseudo) == "createur"


def inscrire(pseudo: str, email: str, mot_de_passe: str, jeton: str = "") -> str:
    pseudo = (pseudo or "").strip().lower()
    email = (email or "").strip().lower()
    if not (3 <= len(pseudo) <= 24) or not pseudo.replace("_", "").replace("-", "").isalnum():
        raise ValueError(lang.t("Pseudo invalide : 3 à 24 caractères, lettres, chiffres, - et _."))
    # Controle volontairement minimal : on verifie qu'une adresse ressemble a
    # une adresse, pas qu'elle existe. Seule la validation manuelle fait foi.
    if "@" not in email or "." not in email.split("@")[-1] or len(email) < 6:
        raise ValueError(lang.t("Adresse e-mail invalide."))
    if len(mot_de_passe or "") < 8:
        raise ValueError(lang.t("Mot de passe trop court : 8 caractères au minimum."))
    if not INSCRIPTION_LIBRE and not invitation_valide(jeton) and pseudo != ADMIN:
        raise ValueError(lang.t("Il faut un lien d'invitation pour créer un compte ici."))
    with VERROU_COMPTES, _cx() as cx:
        if cx.execute("SELECT 1 FROM comptes WHERE pseudo = ?", (pseudo,)).fetchone():
            raise ValueError(lang.t("Ce pseudo est déjà pris."))
        if cx.execute("SELECT 1 FROM comptes WHERE email = ?", (email,)).fetchone():
            raise ValueError(lang.t("Cette adresse est déjà utilisée."))
        # ⚠ LE PLAFOND NE COMPTE QUE LES COMPTES VALIDES. Sinon une vague
        # d'inscriptions en attente suffirait a bloquer les vraies demandes.
        valides = cx.execute(
            "SELECT COUNT(*) FROM comptes WHERE statut = 'valide'"
            " AND role != 'createur'").fetchone()[0]
        role_invitation = "joueur"
        if jeton:
            ligne_role = cx.execute(
                "SELECT role, utilise_par FROM invitations WHERE jeton = ?", (jeton,)).fetchone()
            if ligne_role is not None and ligne_role["utilise_par"] is None:
                role_invitation = ligne_role["role"] or "joueur"
        # Un compte createur n'occupe ni place de jeu ni rang dans le plafond.
        if (valides >= MAX_COMPTES and pseudo != ADMIN
                and role_invitation != "createur"):
            raise ValueError(lang.t("Le site est complet ({n} comptes).").replace("{n}", str(MAX_COMPTES)))
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
        role = "createur" if (invite and role_invitation == "createur"
                              and pseudo != ADMIN) else "joueur"
        if role == "createur":
            libre = None       # aucune table de jeu pour un createur
        else:
            libre = _prendre_un_emplacement(cx, pseudo)
            if libre < 0:
                raise ValueError(lang.t("Plus aucun espace de jeu disponible."))
        cx.execute(
            "INSERT INTO comptes"
            " (pseudo, email, sel, empreinte, statut, cree, emplacement, role)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (pseudo, email, sel, _empreinte(mot_de_passe, sel), statut,
             _maintenant(), libre, role))
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
        raise ValueError(lang.t("Identifiant ou mot de passe incorrect."))
    # `compare_digest` : comparaison a temps constant, pour ne pas laisser
    # fuir l'empreinte par le temps de reponse.
    if not secrets.compare_digest(_empreinte(mot_de_passe, ligne["sel"]), ligne["empreinte"]):
        raise ValueError(lang.t("Identifiant ou mot de passe incorrect."))
    if ligne["statut"] == "expire":
        # ⚠ ON DIT POURQUOI, ET QUOI FAIRE. « Ton compte attend ma validation »
        # aurait envoye quelqu'un attendre indefiniment quelque chose qui ne
        # viendra pas : personne ne sait, cote site, qu'il est revenu.
        raise ValueError(
            "Ton compte a expiré : plus de %d jours sans venir, et la place est "
            "retournée au pot. Écris-moi, je te la rends." % EXPIRATION_JOURS)
    if ligne["statut"] != "valide":
        raise ValueError("Ton compte attend encore ma validation.")
    with _cx() as cx:
        cx.execute("UPDATE comptes SET derniere_connexion = ? WHERE pseudo = ?",
                   (_maintenant(), ligne["pseudo"]))
    return ligne["pseudo"]


def essai_phase_de(pseudo: str) -> bool:
    """La table de ce compte montre-t-elle la nouvelle phase du mechant (essai) ?"""
    ligne = compte(pseudo)
    return bool(ligne and "essai_phase" in ligne.keys() and ligne["essai_phase"])


def basculer_essai_phase(pseudo: str) -> None:
    """Active ou coupe l'essai pour ce compte. Pris en compte au prochain
    allumage de sa table : le moteur lit sa configuration au demarrage."""
    with VERROU_COMPTES, _cx() as cx:
        cx.execute("UPDATE comptes SET essai_phase = 1 - COALESCE(essai_phase, 0) WHERE pseudo = ?",
                   ((pseudo or "").strip().lower(),))


def changer_statut(pseudo: str, statut: str) -> None:
    if statut not in ("valide", "attente", "refuse", "expire"):
        return
    # Remettre en service un compte expire dont la place a ete recyclee : il
    # lui en faut une nouvelle, sinon il se connecte dans le vide.
    rendre_une_place = (statut == "valide" and emplacement_de(pseudo) is None
                        and role_de(pseudo) != "createur")
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
        if c["role"] == "createur":
            continue     # pas de place de jeu a rendre
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
    """Les comptes de JOUEURS. Les createurs de cartes ont leur propre liste
    (`liste_createurs`) : ils n'ont ni table, ni deck, ni presence."""
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM comptes WHERE role != 'createur' ORDER BY"
            " CASE statut WHEN 'attente' THEN 0 WHEN 'valide' THEN 1 ELSE 2 END,"
            " pseudo").fetchall()


def nb_valides() -> int:
    """Les comptes valides QUI JOUENT (les createurs ne comptent pas)."""
    with _cx() as cx:
        return cx.execute(
            "SELECT COUNT(*) FROM comptes WHERE statut = 'valide'"
            " AND role != 'createur'").fetchone()[0]


def liste_createurs():
    with _cx() as cx:
        return cx.execute(
            "SELECT * FROM comptes WHERE role = 'createur' ORDER BY pseudo").fetchall()


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


def creer_invitation(role: str = "joueur") -> str:
    """Un jeton a USAGE UNIQUE qui vaut validation.

    C'est le chemin normal : celui qui recoit le lien entre directement, sans
    passer par la file d'attente. L'inscription libre reste possible, mais
    elle, elle attend une validation a la main.
    """
    if role not in ROLES:
        raise ValueError("role inconnu")
    jeton = secrets.token_urlsafe(16)
    with _cx() as cx:
        cx.execute("INSERT INTO invitations (jeton, cree_le, role) VALUES (?, ?, ?)",
                   (jeton, _maintenant(), role))
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
        raise ValueError(lang.t("Mot de passe trop court : 8 caractères au minimum."))
    with _cx() as cx:
        l = cx.execute("SELECT pseudo, cree_le, utilise_le FROM reinitialisations WHERE jeton = ?",
                       (jeton or "",)).fetchone()
        # ⚠ Relu et consomme dans la MEME transaction, comme une invitation :
        # deux envois du formulaire ne doivent pas poser deux mots de passe.
        if l is None or l["utilise_le"] is not None or _age_secondes(l["cree_le"]) > REINITIALISATION_DUREE:
            raise ValueError("Ce lien n'est plus valable. Demande un nouveau lien à l'administrateur.")
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


# ---------------------------------------------------------------------------
# Compteur anonyme de play (09/10/2026). Le moteur de play tourne dans le
# navigateur : sans ce signal, le site ne sait rien de ce qui s'y joue.
# ---------------------------------------------------------------------------
COMPTEUR_PLAY_MAX_OCTETS = 4096
COMPTEUR_PLAY_MAX_PAR_JOUR = int(os.environ.get("COMPTEUR_PLAY_MAX_PAR_JOUR", "2000"))
_PLAY_MODES = {"solo", "campagne"}
_PLAY_DIFFICULTES = {"normal", "expert"}


def _texte_court(valeur, longueur: int = 60) -> str | None:
    """Une chaine imprimable et courte, ou None. Rien d'autre n'entre en base."""
    if not isinstance(valeur, str):
        return None
    propre = "".join(c for c in valeur if c.isprintable()).strip()
    return propre[:longueur] or None


def enregistrer_partie_play(brut: bytes) -> bool:
    """Compte une partie lancee sur play. Rend False si le signal est ignore
    (illisible, vide, ou plafond du jour atteint)."""
    try:
        donnees = json.loads(brut.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return False
    if not isinstance(donnees, dict):
        return False
    mechant = _texte_court(donnees.get("mechant"))
    heros_bruts = donnees.get("heros")
    heros = []
    if isinstance(heros_bruts, list):
        heros = [h for h in (_texte_court(x) for x in heros_bruts[:4]) if h]
    if not mechant and not heros:
        return False
    joueurs = donnees.get("joueurs")
    if not isinstance(joueurs, int) or isinstance(joueurs, bool) or not 1 <= joueurs <= 4:
        joueurs = max(1, len(heros))
    mode = donnees.get("mode") if donnees.get("mode") in _PLAY_MODES else "solo"
    difficulte = donnees.get("difficulte") if donnees.get("difficulte") in _PLAY_DIFFICULTES else None
    jour = time.strftime("%Y-%m-%d", time.gmtime())
    with _cx() as cx:
        deja = cx.execute("SELECT COUNT(*) FROM parties_play WHERE jour = ?", (jour,)).fetchone()[0]
        if deja >= COMPTEUR_PLAY_MAX_PAR_JOUR:
            return False
        cx.execute("INSERT INTO parties_play (jour, mechant, heros, joueurs, mode, difficulte)"
                   " VALUES (?, ?, ?, ?, ?, ?)",
                   (jour, mechant, json.dumps(heros, ensure_ascii=False), joueurs, mode, difficulte))
    return True


def stats_play(jours: int = 30, top: int = 10) -> dict:
    """Parties de play par jour (les `jours` derniers), et les plus joues."""
    depuis = time.strftime("%Y-%m-%d", time.gmtime(time.time() - (jours - 1) * 86400))
    with _cx() as cx:
        par_jour = [(r["jour"], r["n"]) for r in cx.execute(
            "SELECT jour, COUNT(*) AS n FROM parties_play WHERE jour >= ?"
            " GROUP BY jour ORDER BY jour DESC", (depuis,))]
        mechants = [(r["mechant"], r["n"]) for r in cx.execute(
            "SELECT mechant, COUNT(*) AS n FROM parties_play WHERE jour >= ? AND mechant IS NOT NULL"
            " GROUP BY mechant ORDER BY n DESC, mechant LIMIT ?", (depuis, top))]
        compte_heros: dict[str, int] = {}
        for r in cx.execute("SELECT heros FROM parties_play WHERE jour >= ?", (depuis,)):
            try:
                liste = json.loads(r["heros"] or "[]")
            except ValueError:
                continue
            for h in liste if isinstance(liste, list) else []:
                if isinstance(h, str):
                    compte_heros[h] = compte_heros.get(h, 0) + 1
    heros = sorted(compte_heros.items(), key=lambda x: (-x[1], x[0]))[:top]
    return {"par_jour": par_jour, "mechants": mechants, "heros": heros,
            "total": sum(n for _, n in par_jour), "jours": jours}


# Presence en direct sur play (09/10/2026) : chaque onglet ouvert envoie un
# identifiant aleatoire toutes les 60 s. EN MEMOIRE seulement (ni base, ni IP) :
# un redemarrage remet a zero, ce qui est sans gravite pour un compte « en ce
# moment ».
PRESENCE_PLAY_MAX_OCTETS = 256
PRESENCE_PLAY_DUREE = 180
PRESENCE_PLAY_MAX = 5000
_RE_UUID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
_presence_play: dict[str, float] = {}
_presence_play_verrou = threading.Lock()


def _purger_presence(maintenant: float) -> None:
    limite = maintenant - PRESENCE_PLAY_DUREE
    for cle in [c for c, t in _presence_play.items() if t < limite]:
        del _presence_play[cle]


def signaler_presence_play(brut: bytes, maintenant: float | None = None) -> bool:
    """Note un onglet de play actif. Rend False si le signal est ignore."""
    try:
        donnees = json.loads(brut.decode("utf-8"))
    except (UnicodeDecodeError, ValueError):
        return False
    ident = donnees.get("id") if isinstance(donnees, dict) else None
    if not isinstance(ident, str) or not _RE_UUID.match(ident.lower()):
        return False
    t = time.time() if maintenant is None else maintenant
    with _presence_play_verrou:
        _purger_presence(t)
        if ident.lower() not in _presence_play and len(_presence_play) >= PRESENCE_PLAY_MAX:
            return False
        _presence_play[ident.lower()] = t
    return True


def presents_play(maintenant: float | None = None) -> int:
    """Nombre d'onglets de play vus depuis moins de PRESENCE_PLAY_DUREE secondes."""
    t = time.time() if maintenant is None else maintenant
    with _presence_play_verrou:
        _purger_presence(t)
        return len(_presence_play)


def bloc_stats_play() -> str:
    """Le sous-onglet « Play » de l'administration."""
    st = stats_play()
    present = "<p class=\"sous\"><b>En ce moment sur play : %d</b></p>" % presents_play()
    if not st["total"]:
        return present + '<p class="vide">Aucune partie lancée sur play ces %d derniers jours.</p>' % st["jours"]

    def tableau(titre, lignes):
        corps = "".join('<tr><td data-label="%s">%s</td><td data-label="Parties">%d</td></tr>'
                        % (html.escape(titre.split()[0]), html.escape(str(k)), n) for k, n in lignes)
        return "<h3>%s</h3><table><tr><th>%s</th><th>Parties</th></tr>%s</table>" % (
            html.escape(titre), html.escape(titre.split()[0]), corps)

    return (present + "<p class=\"sous\">%d partie(s) lancée(s) sur play ces %d derniers jours.</p>"
            % (st["total"], st["jours"])
            + tableau("Jour (UTC)", st["par_jour"])
            + tableau("Mechants les plus joues", st["mechants"])
            + tableau("Heros les plus joues", st["heros"]))


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
        return "à l'instant"
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


# --- Inviter un joueur connecte a sa table (13/10/2026) ---------------------
# Demande de l'utilisateur : a l'etape « Coop en ligne », a cote de « Creer des
# liens », l'hote peut « Inviter quelqu'un de connecte ». L'invite voit une
# petite fenetre « X t'invite a sa partie · Rejoindre / Refuser » sur n'importe
# quelle page du site ; l'hote suit l'etat en direct sous chaque nom. Decisions
# completes : .planning/todos/2026-10-13-inviter-un-connecte.md.
#
# ⚠ EN MEMOIRE, PAS EN BASE, ET C'EST VOULU. Une invitation porte une cle de
# siege, qui meurt avec la table (`cles_sieges` change a chaque allumage) : une
# invitation qui survivrait a un redemarrage du site ouvrirait une porte qui
# n'existe plus. PARTIES vit deja en memoire pour la meme raison.
#
# ⚠ LE LIEN NE SORT QU'A L'ACCEPTATION, ET SEULEMENT POUR L'INVITE. Il ouvre
# un siege : le lister dans « invitations recues » le donnerait a quiconque
# lit la liste par-dessus l'epaule du destinataire avant qu'il ait dit oui.

# Sans reponse au-dela, l'invitation s'eteint chez l'invite et l'hote lit
# « Sans reponse · Relancer ».
DUREE_INVITATION = 120

INVITATIONS_TABLE: dict[str, dict] = {}     # id -> invitation
_VERROU_INVITATIONS = threading.Lock()


def connectes(sauf: str = "") -> list[str]:
    """Les comptes valides qui ont donne signe de vie depuis moins de DELAI_PRESENCE.

    « Connecte » au sens de la demande : une page du site ouverte et visible.
    Ce n'est PAS l'etat « partie » de `presence()`, qui dit seulement qu'un
    moteur tourne pour ce compte : il tourne des heures apres que son
    proprietaire a ferme l'onglet.
    """
    sortie = []
    for ligne in liste_comptes():
        if ligne["statut"] != "valide" or ligne["pseudo"] == sauf:
            continue
        vu = ligne["vu_le"] if "vu_le" in ligne.keys() else None
        ecart = _secondes_depuis(vu) if vu else None
        if ecart is not None and ecart < DELAI_PRESENCE:
            sortie.append(ligne["pseudo"])
    return sortie


def _etat_invitation(inv: dict, maintenant: float) -> str:
    if inv["etat"] == "envoyee" and maintenant - inv["cree"] > DUREE_INVITATION:
        return "sans_reponse"
    return inv["etat"]


def inviter_a_la_table(hote: str, invite: str, siege: int) -> "dict | str":
    """Envoie une invitation. Rend l'invitation, ou un message d'erreur."""
    if not invite or invite == hote:
        return "invite inconnu"
    if invite not in connectes(sauf=hote):
        return "pas connecte"
    partie = PARTIES.get(hote)
    if partie is None or not partie.vivant():
        return "pas de table"
    # Le siege 0 est l'hote ; au-dela du nombre de joueurs fixe par l'hote,
    # il n'y a pas de place a donner.
    if not 1 <= siege < min(4, len(partie.cles_sieges)):
        return "siege invalide"
    lien = f"{partie.base_url()}/claim_seat?p={siege}&key={partie.cles_sieges[siege]}&to=salon"
    maintenant = time.time()
    with _VERROU_INVITATIONS:
        # Une seule invitation vivante par siege : relancer ou inviter
        # quelqu'un d'autre remplace la precedente.
        for inv in INVITATIONS_TABLE.values():
            if inv["hote"] == hote and inv["siege"] == siege and inv["etat"] == "envoyee":
                inv["etat"] = "remplacee"
        inv = {"id": secrets.token_urlsafe(9), "hote": hote, "invite": invite,
               "siege": siege, "lien": lien, "etat": "envoyee", "cree": maintenant}
        INVITATIONS_TABLE[inv["id"]] = inv
        # Ménage : on ne garde pas les invitations de la veille.
        for cle in [c for c, i in INVITATIONS_TABLE.items() if maintenant - i["cree"] > 6 * 3600]:
            del INVITATIONS_TABLE[cle]
    return inv


def invitations_pour(invite: str) -> list[dict]:
    """Ce qui attend une reponse de ce compte : qui, et pour quel siege. Jamais le lien."""
    maintenant = time.time()
    with _VERROU_INVITATIONS:
        return [{"id": i["id"], "hote": i["hote"], "siege": i["siege"]}
                for i in INVITATIONS_TABLE.values()
                if i["invite"] == invite and _etat_invitation(i, maintenant) == "envoyee"]


def repondre_invitation(invite: str, ident: str, oui: bool) -> "str | None":
    """Accepte ou refuse. Rend le lien du siege si l'invite accepte, sinon None."""
    maintenant = time.time()
    with _VERROU_INVITATIONS:
        inv = INVITATIONS_TABLE.get(ident)
        if inv is None or inv["invite"] != invite or _etat_invitation(inv, maintenant) != "envoyee":
            return None
        inv["etat"] = "acceptee" if oui else "refusee"
        return inv["lien"] if oui else None


def invitations_de(hote: str) -> dict:
    """L'etat de la derniere invitation de chaque siege, pour l'hote : {siege: {invite, etat}}."""
    maintenant = time.time()
    sortie: dict = {}
    with _VERROU_INVITATIONS:
        # Ordre d'ENVOI (un dict garde l'ordre d'insertion) : la derniere
        # invitation d'un siege est celle qui compte.
        for inv in INVITATIONS_TABLE.values():
            if inv["hote"] != hote or inv["etat"] == "remplacee":
                continue
            sortie[str(inv["siege"])] = {"invite": inv["invite"],
                                         "etat": _etat_invitation(inv, maintenant)}
    return sortie


# Au-dela, on ne lit plus : un dossier de decks n'en tient jamais autant, et
# une table ne doit pas pouvoir faire lire n'importe quoi au site.
MAX_DECKS_INVITE = 200


def decks_de_l_invite(hote: str, siege: int) -> dict:
    """Les decks du COMPTE de l'invite assis a ce siege, s'il y est venu par invitation.

    Decision 3 du 13/10/2026 : l'invite qui a un compte retrouve SES decks. Ils
    vivent dans sa place (`deck/serveur-<place>/`, tools/config_serveur.py), que
    la table de l'hote ne peut pas lire : le site, lui, connait les deux.

    ⚠ ON NE LIT QUE POUR UNE INVITATION ACCEPTEE A CE SIEGE. Sans elle, le site
    ne sait pas qui est assis la (un lien copie ne dit rien du compte), et lire
    « les decks de n'importe qui » serait une fuite. Lecture seule : l'invite
    choisit, le salon enregistre la copie choisie chez l'hote.
    """
    invite = ""
    with _VERROU_INVITATIONS:
        for inv in INVITATIONS_TABLE.values():
            if inv["hote"] == hote and inv["siege"] == siege and inv["etat"] == "acceptee":
                invite = inv["invite"]
    if not invite:
        return {"invite": "", "decks": []}
    place = emplacement_de(invite)
    if not place:
        return {"invite": invite, "decks": []}
    dossier = os.path.join(RACINE_JEU, ".game", "deck", f"serveur-{place}")
    decks = []
    try:
        noms = sorted(n for n in os.listdir(dossier) if n.endswith(".json"))
    except OSError:
        noms = []
    for nom in noms[:MAX_DECKS_INVITE]:
        try:
            with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                deck = json.load(f)
        except (OSError, ValueError):
            continue
        if isinstance(deck, dict) and deck.get("hero"):
            decks.append({"id": nom[:-5], "deck": deck})
    return {"invite": invite, "decks": decks}


def decks_du_compte(pseudo: str) -> dict:
    """Les decks du COMPTE identifie par sa SESSION de site (28/10/2026).

    Jumelle de `decks_de_l_invite`, mais l'identite ne vient pas d'une
    invitation acceptee : elle vient du cookie de session (`nc_session`, resolu
    par `pseudo_de_session` cote appelant). Un invite deja CONNECTE a son compte
    dans ce navigateur retrouve ainsi SES decks dans le salon, meme venu par un
    simple lien copie. Lecture seule, comme `decks_de_l_invite` : le salon
    enregistre une copie du deck choisi chez l'hote.

    ⚠ Le pseudo ARRIVE DEJA RESOLU et verifie (session valide) : on ne lit donc
    que les decks du compte qui a prouve sa session, jamais « ceux de n'importe
    qui ». `_dossier_decks_de` borne la lecture a `deck/` (pas de lien
    symbolique qui sortirait du dossier).
    """
    if not pseudo:
        return {"pseudo": "", "decks": []}
    place = emplacement_de(pseudo)
    dossier = _dossier_decks_de(place) if place is not None else None
    if not dossier:
        return {"pseudo": pseudo, "decks": []}
    decks = []
    try:
        noms = sorted(n for n in os.listdir(dossier) if n.endswith(".json"))
    except OSError:
        noms = []
    for nom in noms[:MAX_DECKS_INVITE]:
        try:
            with open(os.path.join(dossier, nom), encoding="utf-8") as f:
                deck = json.load(f)
        except (OSError, ValueError):
            continue
        if isinstance(deck, dict) and deck.get("hero"):
            decks.append({"id": nom[:-5], "deck": deck})
    return {"pseudo": pseudo, "decks": decks}


# --------------------------------------------------------------------------
# Decks des joueurs, consultes et importes par l'administrateur (19/10/2026)
# --------------------------------------------------------------------------
# Demande du proprietaire du site : voir les decks des autres comptes et en
# importer UN, a la fois, dans son propre compte.
#
# ⚠ TOUT SE VERIFIE ICI, COTE SERVEUR (`pseudo == ADMIN` dans do_GET/do_POST),
# jamais seulement dans l'interface. Les deux routes sont
#   GET  /api/admin/decks-joueurs            : lister, par compte
#   POST /api/admin/decks-joueurs/importer   : copier UN deck chez l'admin
#
# ⚠ LECTURE SEULE SUR LES DECKS DES AUTRES. Le code ne contient aucun
# `remove`/`rename`/ecriture dans le dossier d'un autre compte : l'import LIT le
# fichier d'origine et ECRIT UNE COPIE dans le dossier de l'admin, en mode `x`
# (jamais d'ecrasement : un nom pris recoit un suffixe -2, -3...).
#
# ⚠ AUCUN CHEMIN N'EST PRIS DANS LA REQUETE. Le compte est cherche dans la base
# (son emplacement est un entier), le deck est un identifiant [A-Za-z0-9_-]
# retrouve dans le dossier ; le fichier est ensuite verifie (pas un lien, bien
# dans `deck/serveur-<n>/`). `..`, `/`, les liens et les noms exotiques sont
# refuses AVANT toute ouverture.
#
# Confidentialite : la liste ne rend que le NOM D'AFFICHAGE (le pseudo) : ni
# adresse e-mail, ni mot de passe, ni empreinte. Chaque consultation et chaque
# import est journalise dans `journal-decks-admin.log`.
DECK_ADMIN_MAX_OCTETS = 256 * 1024          # au-dela, un « deck » n'en est plus un
DECK_ADMIN_MAX_PAR_COMPTE = 200
DECK_ADMIN_IMPORTS_PAR_HEURE = 30
DECK_ADMIN_MAX_COPIES_ADMIN = 500           # decks du dossier de l'admin, au plus
JOURNAL_DECKS_ADMIN = os.environ.get(
    "JOURNAL_DECKS_ADMIN",
    os.path.join(os.path.dirname(BASE), "journal-decks-admin.log"))
_ID_DECK = re.compile(r"^[A-Za-z0-9_-]{1,60}$")
_IMPORTS_ADMIN: list[float] = []
_VERROU_DECKS_ADMIN = threading.Lock()
_NOMS_HEROS: dict[str, str] = {}


class ErreurDeckAdmin(Exception):
    """Refus clair : `code` est le statut HTTP, `args[0]` le message."""

    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def journaliser_decks_admin(action: str, **champs) -> None:
    """Une ligne JSON par evenement : qui, quoi, quand. Ne leve jamais."""
    ligne = {"quand": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "qui": ADMIN, "action": action}
    ligne.update(champs)
    try:
        with _VERROU_DECKS_ADMIN:
            with open(JOURNAL_DECKS_ADMIN, "a", encoding="utf-8") as f:
                f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
    except OSError:
        pass


def _racine_decks() -> str:
    return os.path.realpath(os.path.join(RACINE_JEU, ".game", "deck"))


def _dossier_decks_de(place) -> str | None:
    """Le dossier `deck/serveur-<place>/` de ce compte, ou None s'il n'existe pas
    ou s'il sort de `deck/` (lien symbolique)."""
    if not isinstance(place, int) or isinstance(place, bool) or place < 0:
        return None
    racine = _racine_decks()
    dossier = os.path.join(racine, "serveur-%d" % place)
    if os.path.islink(dossier) or not os.path.isdir(dossier):
        return None
    if os.path.dirname(os.path.realpath(dossier)) != racine:
        return None
    return dossier


def _fichier_deck_sur(dossier: str, identifiant: str) -> str | None:
    """Le chemin du deck `identifiant` DANS `dossier`, ou None. Rien n'est pris
    dans la requete a part l'identifiant, et celui-ci est filtre."""
    if not isinstance(identifiant, str) or not _ID_DECK.match(identifiant):
        return None
    chemin = os.path.join(dossier, identifiant + ".json")
    if os.path.islink(chemin) or not os.path.isfile(chemin):
        return None
    if os.path.dirname(os.path.realpath(chemin)) != os.path.realpath(dossier):
        return None
    return chemin


def _nom_du_heros(ids) -> str:
    """Le nom de la carte du heros, pour l'affichage ; l'identifiant sinon."""
    cle = ids[0] if isinstance(ids, list) and ids else ""
    cle = str(cle).split(",")[0].strip()
    if not _NOMS_HEROS:
        try:
            with open(os.path.join(RACINE_JEU, "data", "cards.json"), encoding="utf-8") as f:
                for cartes in json.load(f).values():
                    for c in cartes if isinstance(cartes, list) else []:
                        if isinstance(c, dict) and c.get("card_id") and c.get("name"):
                            _NOMS_HEROS[str(c["card_id"])] = str(c["name"])
        except (OSError, ValueError, AttributeError):
            _NOMS_HEROS["_"] = ""
    return _NOMS_HEROS.get(cle) or cle


def _lire_deck_sur(chemin: str):
    """Le deck (dict) ou None s'il est trop gros, illisible ou sans heros."""
    try:
        if os.path.getsize(chemin) > DECK_ADMIN_MAX_OCTETS:
            return None
        with open(chemin, encoding="utf-8") as f:
            deck = json.load(f)
    except (OSError, ValueError):
        return None
    return deck if isinstance(deck, dict) and deck.get("hero") else None


def lister_decks_des_joueurs() -> list:
    """Par compte (admin exclu) : pseudo et decks (nom, heros, nombre de cartes,
    date). Aucun champ prive du compte n'est lu."""
    sortie = []
    for c in liste_comptes():
        if c["pseudo"] == ADMIN:
            continue
        dossier = _dossier_decks_de(c["emplacement"])
        decks = []
        if dossier:
            try:
                noms = sorted(n for n in os.listdir(dossier) if n.endswith(".json"))
            except OSError:
                noms = []
            for nom in noms[:DECK_ADMIN_MAX_PAR_COMPTE]:
                identifiant = nom[:-5]
                chemin = _fichier_deck_sur(dossier, identifiant)
                deck = _lire_deck_sur(chemin) if chemin else None
                if deck is None:
                    continue
                decks.append({
                    "id": identifiant,
                    "nom": str(deck.get("name") or identifiant)[:80],
                    "heros": _nom_du_heros(deck.get("hero")),
                    "cartes": len(deck.get("player_deck") or []),
                    "date": time.strftime("%Y-%m-%d %H:%M",
                                          time.localtime(os.path.getmtime(chemin))),
                })
        if decks:
            sortie.append({"compte": c["pseudo"], "decks": decks})
    return sortie


def importer_deck_de_joueur(compte_source: str, identifiant: str) -> dict:
    """Copie UN deck de `compte_source` dans le dossier de l'admin, sous
    `de-<compte>-<deck>`. L'original n'est ni modifie ni supprime ; une copie
    existante n'est jamais ecrasee. Leve ErreurDeckAdmin."""
    source = compte(compte_source)
    if source is None or source["pseudo"] == ADMIN or source["pseudo"] != compte_source:
        raise ErreurDeckAdmin(404, "Compte introuvable.")
    chez_lui = _dossier_decks_de(source["emplacement"])
    chemin = _fichier_deck_sur(chez_lui, identifiant) if chez_lui else None
    if chemin is None:
        raise ErreurDeckAdmin(404, "Deck introuvable.")
    deck = _lire_deck_sur(chemin)
    if deck is None:
        raise ErreurDeckAdmin(422, "Deck illisible ou trop volumineux.")
    place_admin = emplacement_de(ADMIN)
    if place_admin is None:
        raise ErreurDeckAdmin(409, "Le compte administrateur n'a pas de place.")
    chez_admin = os.path.join(_racine_decks(), "serveur-%d" % place_admin)
    if os.path.islink(chez_admin):
        raise ErreurDeckAdmin(409, "Dossier de l'administrateur invalide.")
    os.makedirs(chez_admin, exist_ok=True)
    try:
        if sum(1 for n in os.listdir(chez_admin) if n.endswith(".json")) >= DECK_ADMIN_MAX_COPIES_ADMIN:
            raise ErreurDeckAdmin(409, "Trop de decks dans le compte administrateur.")
    except OSError:
        raise ErreurDeckAdmin(500, "Dossier illisible.")
    with _VERROU_DECKS_ADMIN:
        maintenant = time.time()
        _IMPORTS_ADMIN[:] = [t for t in _IMPORTS_ADMIN if maintenant - t < 3600]
        if len(_IMPORTS_ADMIN) >= DECK_ADMIN_IMPORTS_PAR_HEURE:
            raise ErreurDeckAdmin(429, "Trop d'imports cette heure-ci.")
        _IMPORTS_ADMIN.append(maintenant)
    # Meme alphabet que /save_deck : le moteur relit ce dossier tel quel.
    pseudo_net = re.sub("[^a-zA-Z0-9_-]+", "_", source["pseudo"]).strip("_")[:20] or "joueur"
    base = ("de-%s-%s" % (pseudo_net, re.sub("[^a-zA-Z0-9_-]+", "_", identifiant).strip("_")))[:56]
    copie = dict(deck)
    copie["name"] = ("%s (de %s)" % (deck.get("name") or identifiant, source["pseudo"]))[:100]
    contenu = json.dumps(copie, ensure_ascii=False, indent=4)
    for rang in range(1, 100):
        nom = base if rang == 1 else "%s-%d" % (base, rang)
        try:
            with open(os.path.join(chez_admin, nom + ".json"), "x", encoding="utf-8") as f:
                f.write(contenu)
            return {"ok": True, "fichier": nom, "compte": source["pseudo"], "deck": identifiant}
        except FileExistsError:
            continue
    raise ErreurDeckAdmin(409, "Trop de copies portant ce nom.")


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


# --------------------------------------------------------------------------
# Les demandes des createurs (12/10/2026)
# --------------------------------------------------------------------------
# Formulaire PUBLIC, sans compte (lien « ce formulaire » sous les remerciements
# de l'accueil) : n'importe qui peut ecrire. D'ou un pot de miel, un plafond par
# adresse et par heure, et des champs tronques, comme pour les rapports.
GENRES_DEMANDE_CREATEUR = ("crediter", "retirer")
DEMANDES_CREATEURS_PAR_HEURE = int(os.environ.get("DEMANDES_CREATEURS_PAR_HEURE", "5"))
_ENVOIS_CREATEURS: dict[str, list[float]] = {}
_VERROU_CREATEURS = threading.Lock()


def debit_createur_ok(adresse: str) -> bool:
    """Vrai si `adresse` peut encore envoyer une demande dans l'heure, et la compte.

    ⚠ ON COMPTE CHAQUE ENVOI, VALIDE OU NON : un robot qui enverrait des
    formulaires incomplets en boucle doit buter sur le plafond comme les autres.
    """
    maintenant = time.time()
    with _VERROU_CREATEURS:
        recents = [t for t in _ENVOIS_CREATEURS.get(adresse, []) if maintenant - t < 3600]
        if len(recents) >= DEMANDES_CREATEURS_PAR_HEURE:
            _ENVOIS_CREATEURS[adresse] = recents
            return False
        recents.append(maintenant)
        _ENVOIS_CREATEURS[adresse] = recents
        return True


def enregistrer_demande_createur(nom: str, contact: str, genre: str, message: str) -> int:
    """Range une demande et rend son numero. LEVE ValueError si un champ manque."""
    nom = " ".join(str(nom or "").split())[:80]
    contact = " ".join(str(contact or "").split())[:160]
    message = str(message or "").strip()[:4000]
    if not nom:
        raise ValueError(lang.t("Indique ton nom ou ton pseudo."))
    if not contact:
        raise ValueError(lang.t("Indique un moyen de te recontacter (e-mail ou Discord)."))
    if genre not in GENRES_DEMANDE_CREATEUR:
        raise ValueError(lang.t("Choisis le type de demande."))
    if not message:
        raise ValueError(lang.t("Écris ton message."))
    with _cx() as cx:
        curseur = cx.execute(
            "INSERT INTO demandes_createurs (quand, nom, contact, genre, message)"
            " VALUES (?,?,?,?,?)", (_maintenant(), nom, contact, genre, message))
        return int(curseur.lastrowid)


def demandes_createurs(limite: int = 100) -> list[dict]:
    """Les demandes, les nouvelles d'abord, puis les plus recentes."""
    with _cx() as cx:
        return [dict(r) for r in cx.execute(
            "SELECT * FROM demandes_createurs ORDER BY etat = 'traitee', id DESC LIMIT ?",
            (limite,))]


def marquer_demande_createur(numero: int, etat: str) -> None:
    """Passe une demande a « traitee » (ou la rouvre en « nouvelle »)."""
    if etat not in ("nouvelle", "traitee"):
        return
    with _cx() as cx:
        cx.execute("UPDATE demandes_createurs SET etat = ? WHERE id = ?", (etat, numero))


def enregistrer_rapport(hote: str, champs: dict, compte_verifie: str | None = None) -> int:
    """Range un rapport et rend son numero. La capture part sur disque.

    Rien n'est refuse pour cause de champ trop long : on TRONQUE. Un rapport
    ampute vaut mieux qu'un rapport perdu, et la personne qui l'envoie n'a
    aucun moyen de savoir ce qui passe.

    `compte_verifie` (25/09/2026) : le compte REEL de l'auteur, quand on le
    connait avec certitude (voir le commentaire de la colonne dans `SCHEMA`).
    ⚠ PAR DEFAUT (`None`), ON RETOMBE SUR LA REGLE HISTORIQUE : le titulaire
    ecrivant depuis son propre siege 0 EST son propre auteur verifie ; tout
    autre siege n'a personne de certain. Aucun appelant existant ne passe ce
    parametre, et leur comportement ne change donc pas.
    """
    nom = " ".join(str(champs.get("nom") or "").split())[:80] or "anonyme"
    description = str(champs.get("description") or "").strip()[:MAX_DESCRIPTION_CARACTERES]
    journal = str(champs.get("journal") or "")[:MAX_JOURNAL_CARACTERES]
    ecran = " ".join(str(champs.get("ecran") or "").split())[:120]
    try:
        siege = int(champs.get("siege") or 0)
    except (TypeError, ValueError):
        siege = 0
    if compte_verifie is None:
        compte_verifie = hote if siege == 0 else None

    capture = None
    brut = champs.get("capture") or ""
    if brut:
        capture = _ecrire_capture(brut)

    with _cx() as cx:
        cur = cx.execute(
            "INSERT INTO rapports (quand, hote, nom, siege, ecran, description,"
            " journal, capture, etat, compte_verifie)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'nouveau', ?)",
            (_maintenant(), hote, nom, siege, ecran, description, journal, capture,
             compte_verifie))
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
    """Ce rapport a-t-il un AUTEUR certain ?

    ⚠ `compte_verifie` REMPLACE `siege == 0` (25/09/2026), et n'est PAS
    `hote` : `hote` reste « la table », `compte_verifie` dit « qui, avec
    certitude ». Voir le commentaire de la colonne dans `SCHEMA`.
    """
    return bool(r.get("compte_verifie"))


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
        r = cx.execute("SELECT compte_verifie FROM rapports WHERE id = ?",
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
            "SELECT * FROM rapports WHERE compte_verifie = ? ORDER BY id DESC",
            (pseudo,))]
        for rapport in lignes:
            rapport["messages"] = [dict(m) for m in cx.execute(
                "SELECT * FROM rapports_messages WHERE rapport_id = ? ORDER BY id",
                (rapport["id"],))]
    return lignes


def rapports_de_ses_tables(pseudo: str) -> list[dict]:
    """TOUS les signalements venus de ses tables, quel que soit le siege.

    ⚠ A NE JAMAIS CONFONDRE AVEC `tickets_de`, ET LA DIFFERENCE EST UNE
    AUTORISATION. `tickets_de` dit ce a quoi ce compte a le droit de REPONDRE,
    et reste donc au siege 0 : le fil ne distingue que « joueur » et « admin »,
    si l'hote ecrivait dans le fil d'un invite on ne saurait plus qui a parle.
    Celle-ci dit seulement ce qu'il a le droit de VOIR, et c'est plus large :
    tout ce qui vient d'une table dont il est l'hote.

    Pourquoi elle existe (signale par un joueur le 19/09/2026) : quelqu'un qui
    joue sur SA table depuis deux appareils occupe deux sieges. Son signalement
    envoye du second n'apparaissait nulle part, et il l'a cru perdu.
    """
    if not pseudo:
        return []
    with _cx() as cx:
        lignes = [dict(r) for r in cx.execute(
            "SELECT * FROM rapports WHERE hote = ? ORDER BY id DESC", (pseudo,))]
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
    """Les rapports ACTIFS (nouveau, en cours) au complet, jamais tronqués,
    suivis des `limite` derniers rapports CLASSÉS (traité, refusé).

    Archivage du 21/10/2026 (item 23 du backlog) : avant cette distinction,
    `ORDER BY id DESC LIMIT` seul pouvait repousser hors de la fenêtre un
    rapport actif ancien derrière une pile de tickets déjà corrigés/refusés,
    si le suivi se remplissait. Les classés restent consultables (le fil et
    la capture jusqu'à la purge à 30 jours), seulement plus loin dans la
    liste une fois `limite` dépassée.
    """
    with _cx() as cx:
        actifs = [dict(r) for r in cx.execute(
            "SELECT * FROM rapports WHERE etat IN ('nouveau', 'en cours') OR etat IS NULL"
            " ORDER BY id DESC")]
        classes = [dict(r) for r in cx.execute(
            "SELECT * FROM rapports WHERE etat IN ('traite', 'refuse')"
            " ORDER BY id DESC LIMIT ?", (limite,))]
    return actifs + classes


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
ANNONCE_DEPLOIEMENT = ("Mise à jour du jeu en approche : les parties en cours "
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
# AFFICHAGE SOBRE sur les pages du site (09/10/2026) : meme reglage que le jeu
# (cle `mc_affichage_v1`), memes valeurs que la palette du plateau sobre
# (ui-app/styles/affichage-sobre.css). Desature, jamais de gris force, sans la
# trame de points. Injecte par `_repondre` apres la premiere balise meta.
SOBRE_SITE = (
    b'<script>try{if(localStorage.getItem("mc_affichage_v1")==="sobre")'
    b'document.documentElement.dataset.affichage="sobre"}catch(e){}</script>'
    b'<style>html[data-affichage="sobre"]{--bg:#232528;--panel:#2a2c30;--panel-2:#30333a;'
    b'--border:#3a3e44;--text:#e4e5e8;--muted:#a9adb4;--accent:#5c3f3f;--accent-hover:#6c4a4a;'
    b'--accent-soft:rgba(108,74,74,.18);--accent-ink:#e4e5e8;--ok:#737c62;--danger:#b39d9d;'
    b'--warn:#b3a588}html[data-affichage="sobre"] body{background-image:none!important;'
    b'background-color:#232528!important}html[data-affichage="sobre"] a{color:#9aabb6}'
    b'html[data-affichage="sobre"] img{filter:saturate(.75)}</style>'
)


PAGE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{tete}
{tete_appli}
<title>NarwhalChampions</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&display=swap">
<style>
  /* ===== REFONTE (23/09/2026) ================================================
     Alignee sur le plateau de jeu (ui-app/public/css/prepare/prepare.css) :
     fond quasi noir, le rouge Marvel comme SEULE couleur d'action, Anton pour
     les titres (meme police que l'ecran de selection de heros). Avant : une
     seule passe de couleur sur l'ancien HTML brut (liens colles par des
     « &middot; », pas de hierarchie typographique) -- signale par
     l'utilisateur comme insuffisant : « juste ajoute du rouge ». Cette passe
     change aussi la STRUCTURE (barre de nav, boutons de choix), pas
     seulement l'habillage -- voir _barre() et page_reprise().
     Pour revenir a l'ancien rendu : `git log` sur ce fichier, avant ce
     commit. */
  :root {{
    color-scheme: dark;
    --bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;
    --text:#eef1f5; --muted:#8b95a3;
    --accent:#e62429; --accent-hover:#ff3b40; --accent-soft:rgba(230,36,41,.14); --accent-ink:#fff;
    --ok:#3fb950; --danger:#f85149; --warn:#e8a53d;
    --affiche: "Anton", "Arial Narrow", sans-serif;
  }}
  * {{ box-sizing:border-box; }}
  /* Fond a trame de points (23/09/2026, demande de l'utilisateur) : meme
     esprit que les trames « comics » des cadres de cartes du jeu. Degrade
     en calque au-dessus : dense en haut, disparait vers le bas -- la
     couche de degrade RECOUVRE les points d'une couleur opaque (--bg) a
     mesure qu'on descend, elle ne les eclaircit pas. */
  body {{ margin:0; font:16px/1.55 system-ui,sans-serif; color:var(--text);
         display:flex; justify-content:center; padding:0 1.1rem 2.5rem;
         background-color:var(--bg);
         background-image:
           linear-gradient(to bottom, transparent 0%, transparent 12%, var(--bg) 60%),
           radial-gradient(rgba(230,36,41,.4) 1px, transparent 1.6px);
         background-size:100% 100%, 15px 15px;
         background-repeat:no-repeat, repeat;
         /* ⚠⚠ « fixed » RETIRE (23/09/2026, « ca rame blinde sur le
            telephone » signale juste apres le deploiement) : un fond
            attache au VIEWPORT force le navigateur a le repeindre a
            chaque frame de defilement -- il ne peut plus deleguer le
            scroll au compositeur seul. Connu pour etre couteux sur
            mobile, plus encore avec un motif REPETE (le halftone,
            15x15px). `scroll` (l'attache par defaut, l'element plutot
            que le viewport) est visuellement quasi identique sur une
            page aussi courte que celles du site, et rend le defilement
            fluide. */
         background-attachment:scroll, scroll; }}
  main {{ width:100%; max-width:40rem; padding-top:5.5rem; }}
  @media (max-width:640px) {{ main {{ padding-top:7.4rem; }} }}
  h1 {{ font:clamp(2.1rem,7vw,2.7rem)/1 var(--affiche); margin:0; font-weight:400;
       letter-spacing:.01em; text-transform:uppercase; text-wrap:balance; }}
  p.sous {{ color:var(--muted); margin:0 0 1.75rem; font-size:1.05rem; }}
  form {{ display:flex; gap:.5rem; margin-bottom:2rem; }}
  input, button {{ font:inherit; border-radius:0; border:1px solid var(--border); padding:.65rem .9rem; }}
  input {{ flex:1; background:var(--panel-2); color:inherit; }}
  input:focus-visible, button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
  button {{ background:var(--accent); color:var(--accent-ink); border-color:var(--accent);
           cursor:pointer; font-weight:700; transition:background .12s ease,transform .12s ease; }}
  button:hover {{ background:var(--accent-hover); }}
  button:active {{ transform:scale(.98); }}
  button.rouge {{ background:transparent; color:var(--muted); border-color:var(--border);
                 padding:.35rem .7rem; font-size:.85rem; font-weight:400; }}
  button.rouge:hover {{ background:var(--panel-2); color:var(--danger); border-color:var(--danger); }}
  /* Coins nets partout (23/09/2026, demande de l'utilisateur : « comme dans
     la selection de perso et de vilains », ui-app/.../prepare.css .hero-card
     n'a AUCUN border-radius) -- fini les coins arrondis herites du premier
     essai. */
  .table {{ border:1px solid var(--border); border-radius:0; padding:1.4rem 1.5rem;
           margin-bottom:1.1rem; background:var(--panel);
           border-top:3px solid var(--accent);
           box-shadow:0 24px 48px -20px rgba(0,0,0,.85), 0 8px 16px -10px rgba(0,0,0,.7);
           opacity:0; animation:entree .5s ease-out .05s forwards; }}
  @keyframes entree {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:translateY(0); }} }}
  @media (prefers-reduced-motion:reduce) {{ .table {{ animation:none; opacity:1; }} }}
  .entete-partie {{ display:flex; gap:1rem; align-items:flex-start; margin-bottom:.8rem; }}
  .entete-partie strong {{ font-size:1.25rem; font-weight:700; letter-spacing:-.01em; display:block; }}
  .portrait-vilain {{ flex:none; width:56px; height:81px; object-fit:cover; border:1px solid var(--border); }}
  .badges-partie {{ display:flex; flex-wrap:wrap; gap:.35rem; margin-top:.45rem; }}
  .badge-partie {{ font-size:.78rem; color:var(--muted); background:var(--panel-2);
                  border:1px solid var(--border); padding:.15rem .55rem; }}
  .mdp {{ color:var(--muted); font-size:.9rem; }}
  .mdp code {{ background:var(--bg); padding:.15rem .4rem; border-radius:.3rem; color:var(--text); }}
  ul {{ list-style:none; margin:0; padding:0; }}
  li {{ display:flex; align-items:center; gap:.6rem; padding:.3rem 0; }}
  li span {{ min-width:8.5rem; color:var(--muted); font-size:.9rem; }}
  li a {{ color:var(--accent); word-break:break-all; font-size:.9rem; }}
  .vide {{ color:var(--muted); }}
  /* Les deux choix de /entrer (23/09/2026) : icone + texte. L'option
     PRINCIPALE (la premiere du groupe -- « Commencer autre chose », voir
     page_reprise()) est nettement plus grande, fond rouge plein et icone
     blanche ; la secondaire reste petite et discrete. La hierarchie se voit
     avant meme de lire les mots. */
  .choix {{ display:grid; gap:.6rem; margin-bottom:1.5rem; }}
  .choix form {{ display:block; margin:0; }}
  .choix button {{ width:100%; text-align:left; border-radius:0;
                  display:flex; align-items:center; gap:.9rem; }}
  .choix form:first-child button {{ padding:1.3rem 1.4rem; }}
  .choix form:first-child .choix-icone {{ width:26px; height:26px; }}
  .choix form:first-child b {{ font-size:1.15rem; }}
  .choix form:last-child button {{ padding:.7rem 1rem; background:transparent; color:var(--text);
                                   border:1px solid var(--border); font-weight:600; }}
  .choix form:last-child button:hover {{ border-color:var(--muted); background:var(--panel-2); }}
  .choix form:last-child .choix-icone {{ width:18px; height:18px; opacity:.7; }}
  .choix form:last-child b {{ font-size:.92rem; }}
  .choix form:last-child em {{ font-size:.78rem; }}
  .choix-icone {{ flex:none; opacity:.9; }}
  .choix b {{ display:block; font-weight:700; }}
  .choix em {{ display:block; font-style:normal; opacity:.85; margin-top:.15rem; font-weight:400; }}
  button.calme {{ background:var(--panel-2); color:var(--text); border-color:var(--border); font-weight:600; }}
  button.calme:hover {{ background:#1e242e; border-color:#38404d; }}
  .places {{ display:flex; gap:.6rem; flex-wrap:wrap; align-items:center; margin:0 0 1.5rem; }}
  .places form {{ display:inline; margin:0; }}
  .places button {{ min-width:5.5rem; }}
  .places span {{ color:var(--muted); font-size:.9rem; }}
  .apres {{ display:flex; gap:.5rem; flex-wrap:wrap; align-items:center;
           margin-top:1rem; padding-top:.9rem; border-top:1px solid var(--border); }}
  .apres form {{ display:inline; margin:0; }}
  .apres span {{ color:var(--muted); font-size:.85rem; }}
  .apres button {{ background:transparent; color:var(--muted); border-color:var(--border);
                  font-size:.85rem; padding:.25rem .7rem; min-width:0; font-weight:400; }}
  .apres button:hover {{ background:var(--panel-2); color:var(--text); }}
  .apres button[disabled] {{ border-color:var(--accent); color:var(--accent); cursor:default; }}
  a.retour {{ color:var(--accent); font-size:.9rem; }}
  /* L'ATTENTE (17/09/2026). Elle etait une boite de texte grise que le
     navigateur rechargeait toutes les trois secondes : « c'est vraiment
     moche ». Le narval, une barre qui avance, et plus aucun clignotement. */
  .attente {{ display:grid; justify-items:center; gap:.9rem; text-align:center;
             padding:2.5rem 1rem 2rem; }}
  .attente strong {{ font-size:1.25rem; }}
  .attente .mdp {{ max-width:26rem; }}
  .attente-logo {{ width:min(190px,45vw); height:auto;
                  filter:drop-shadow(0 10px 26px rgba(0,0,0,.6));
                  animation:respire 2.6s ease-in-out infinite; }}
  @keyframes respire {{ 0%,100% {{ transform:scale(1); }} 50% {{ transform:scale(1.045); }} }}
  .attente-barre {{ width:min(260px,70vw); height:3px; border-radius:3px;
                   background:var(--border); overflow:hidden; }}
  .attente-barre i {{ display:block; width:40%; height:100%; background:var(--accent);
                     animation:glisse 1.5s ease-in-out infinite; }}
  @keyframes glisse {{ 0% {{ transform:translateX(-100%); }}
                      100% {{ transform:translateX(250%); }} }}
  .attente-note {{ font-size:.85rem; opacity:.75; }}
  @media (prefers-reduced-motion:reduce) {{
    .attente-logo, .attente-barre i {{ animation:none; }}
  }}
  /* La barre (23/09/2026, reecrite en vraie barre d'appli fixee -- voir
     _barre()) : logo + liens a gauche/centre, identite + deconnexion a
     droite, fond noir plein qui se detache du fond a trame en dessous. Fixee
     en haut de l'ECRAN (pas du contenu) : `main` recoit le degagement en
     haut (`padding-top`) pour ne jamais passer dessous. */
  .barre {{ position:fixed; top:0; left:0; right:0; z-index:10;
           display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1.2rem;
           padding:.7rem 1.2rem; background:#040508; border-bottom:1px solid var(--border); }}
  .barre-logo {{ display:flex; align-items:center; gap:.55rem; flex:none;
                font:1rem/1 var(--affiche); text-transform:uppercase; letter-spacing:.01em;
                color:var(--text); text-decoration:none; }}
  .barre-logo img {{ width:2.1rem; height:2.1rem; border-radius:50%; box-shadow:0 0 0 2px var(--border); }}
  .barre-qui {{ color:var(--muted); font-size:.85rem; margin-left:auto; }}
  .barre-qui strong {{ color:var(--text); }}
  .barre-nav {{ display:flex; flex-wrap:wrap; gap:.3rem 1rem; align-items:center;
               flex-basis:100%; order:3; padding-top:.5rem; border-top:1px solid var(--border); }}
  @media (min-width:641px) {{
    .barre-nav {{ flex-basis:auto; order:2; padding-top:0; border-top:0; margin-left:1.2rem; }}
    .barre-qui {{ order:3; }}
  }}
  .barre-nav a {{ color:var(--muted); font-size:.85rem; text-decoration:none; }}
  .barre-nav a:hover {{ color:var(--text); }}
  .barre-nav a.sortie {{ color:var(--muted); }}
  .barre-nav a.sortie:hover {{ color:var(--danger); }}
  /* L'interrupteur FR/EN (23/09/2026, demande de l'utilisateur) : les deux
     langues restent visibles, celle qui est active est en rouge -- un vrai
     interrupteur, pas un lien vers « l'autre » langue sans dire laquelle est
     active. */
  .lang {{ display:inline-flex; align-items:center; border:1px solid var(--border);
          font-size:.75rem; font-weight:700; text-decoration:none; overflow:hidden; }}
  .lang span {{ padding:.2rem .5rem; color:var(--muted); }}
  .lang span.lang-active {{ background:var(--accent); color:var(--accent-ink); }}
  .barre .pastille {{ background:var(--accent); color:var(--accent-ink); border-radius:1rem;
                     padding:.03rem .4rem; font-size:.72rem; font-weight:700; }}
  /* Le FIL d'un signalement (16/09/2026) : ma reponse et la sienne, distinguees
     par leur bord. Meme forme que dans /admin, pour que la meme conversation se
     lise pareil des deux cotes. */
  .fil {{ display:grid; gap:.4rem; margin:.4rem 0 .6rem; }}
  .fil .msg {{ margin:0; padding:.45rem .6rem; border-radius:0;
              background:var(--bg); border-left:3px solid var(--border); font-size:.9rem; }}
  .fil .msg.de-lui {{ border-left-color:var(--accent); }}
  .fil .msg.de-moi {{ border-left-color:var(--warn); }}
  .repondre {{ display:flex; gap:.4rem; align-items:flex-start; }}
  .repondre textarea {{ flex:1; font:inherit; background:var(--bg); color:inherit;
                       border:1px solid var(--border); border-radius:0;
                       padding:.4rem .6rem; resize:vertical; }}
  .repondre button {{ width:auto; }}
  .avert {{ border:1px solid #9e6a03; background:#1d1a0e; color:var(--warn);
           border-radius:0; padding:.7rem .9rem; margin-bottom:1.5rem; font-size:.9rem; }}
  footer {{ margin-top:2.5rem; color:#5b6270; font-size:.85rem; }}
  footer .mention-legale {{ display:block; margin-top:.9rem; font-size:.75rem; }}
  /* ===== TELEPHONE (zone 2 de la refonte du 09/10/2026, fiche
     .planning/todos/2026-10-09-mode-telephone-refonte.md) ====================
     Sous 768 px : une barre fine (logo + burger), le menu se deroule dessous,
     zones tactiles de 44 px. Au-dessus de 768 px, rien ne change. */
  .barre-burger {{ display:none; }}
  @media (max-width:767px) {{
    .barre {{ flex-wrap:wrap; gap:0; padding:.2rem .4rem .2rem 1rem; min-height:52px; }}
    .barre-logo {{ min-height:44px; }}
    .barre-burger {{ display:inline-grid; place-items:center; margin-left:auto; min-width:44px; min-height:44px;
                    padding:0; background:transparent; border:0; color:var(--text); font-size:1.5rem; line-height:1; }}
    .barre-burger:hover {{ background:transparent; }}
    .barre-qui, .barre-nav {{ display:none; }}
    .barre.ouvert .barre-qui {{ display:block; order:3; flex-basis:100%; margin:0; padding:.4rem 0 .1rem; }}
    .barre.ouvert .barre-nav {{ display:flex; order:4; flex-basis:100%; flex-direction:column; align-items:stretch;
                               gap:0; margin:0; padding:.2rem 0 .5rem; border-top:1px solid var(--border); }}
    .barre-nav a {{ display:flex; align-items:center; min-height:44px; font-size:1rem; }}
    .barre-nav a.lang {{ align-self:flex-start; margin-top:.3rem; }}
    .lang span {{ display:flex; align-items:center; min-height:42px; padding:0 .9rem; }}
    main {{ padding-top:4.4rem; }}
  }}
  /* Les tableaux deviennent des cartes empilees au telephone : une ligne = une
     carte, chaque valeur precedee de son libelle (`data-label`). */
  @media (max-width:767px) {{
    table, tbody, tr, td {{ display:block; width:100%; }}
    tr:has(> th) {{ display:none; }}
    tr {{ margin:0 0 .6rem; padding:.55rem .8rem; background:var(--panel); border:1px solid var(--border); }}
    td {{ display:flex; justify-content:space-between; gap:1rem; padding:.2rem 0; border:0; text-align:right; }}
    td::before {{ content:attr(data-label); color:var(--muted); font-size:.85rem; text-align:left; flex:none; }}
    td[colspan] {{ justify-content:flex-start; text-align:left; }}
  }}
  @media (max-width:767px) {{
    button, input, textarea {{ min-height:44px; }}
    input, textarea {{ font-size:16px; }}
    button.rouge, .apres button {{ min-height:44px; padding:.35rem .9rem; }}
    a.retour {{ display:inline-flex; align-items:center; min-height:44px; }}
    .table {{ padding:1.1rem 1rem; }}
  }}
</style>
<main>
  {barre}
  <p class="sous">{sous}</p>
  {corps}
  {bouton_appli}
  <footer>{pied}</footer>
</main>
"""

def _pied_de_page() -> str:
    """Le pied de page, dans la langue du visiteur.

    ⚠ IL ETAIT ECRIT DANS LE GABARIT, donc intraduisible : un gabarit est une
    chaine constante, evaluee une fois au chargement du module, quand aucune
    requete n'existe encore et donc aucune langue. Il recoit maintenant son
    texte a chaque rendu.
    """
    return lang.t(
        "Ton espace de jeu est à toi : tes decks, tes campagnes en cours et tes "
        "hauts faits t'y attendent d'une fois sur l'autre. Éteindre le jeu "
        "n'efface rien. Tes invités, eux, rejoignent ta partie par leur lien "
        "sans avoir besoin d'un compte. Extinction automatique au bout de "
        "{heures} h d'allumage.").replace("{heures}", str(int(DUREE_MAX_HEURES))) \
        + '<span class="mention-legale">%s</span>' % _mention_courte()


def _lignes_pied(*phrases: str) -> str:
    """Le pied des formulaires : une phrase par ligne (20/10/2026). Elles
    s'empilaient en un bloc de texte gris ; chacune a maintenant sa ligne."""
    return "".join('<span class="ligne">%s</span>' % p for p in phrases if p)


def _mention_courte() -> str:
    """La mention legale en une ligne (10/10/2026, texte valide mot pour mot
    par l'utilisateur : ne pas le reformuler). Jumelle de
    public/js/mention-legale.js, cote jeu."""
    return lang.t("Projet de fans non officiel · Marvel Champions © Fantasy Flight Games (Asmodee) · Personnages © Marvel · Il faut posséder le jeu pour jouer")


def _mention_complete() -> str:
    """La mention legale entiere, sur les pages de connexion et d'inscription."""
    return lang.t("Projet de fans, gratuit et non officiel. Marvel Champions: The Card Game est un jeu de Fantasy Flight Games (Asmodee). "
                  "Les personnages et illustrations Marvel appartiennent à Marvel. Ce site n'est ni affilié à ces sociétés ni approuvé par elles. "
                  "Il sert de vitrine et d'outil de jeu : il faut posséder le jeu pour l'utiliser.")


def _bouton_langue() -> str:
    """FR / EN, dans la barre du site.

    ⚠ SANS LUI, LA DETECTION SERAIT UNE PRISON. Un navigateur regle en anglais
    verrait un site anglais sans aucun moyen d'en sortir : le choix fait dans le
    JEU vit dans le `localStorage`, que le serveur ne lit pas. Ce bouton pose le
    cookie que `langue.detecter` regarde en premier.
    """
    # ⚠⚠ EN VRAI INTERRUPTEUR (23/09/2026, demande de l'utilisateur), pas un
    # simple lien vers l'autre langue : les DEUX libelles restent visibles,
    # celui qui correspond a la langue active est mis en avant -- un clic sur
    # l'un ou l'autre bascule (le lien vise toujours l'autre langue, un clic
    # sur la langue deja active ne fait donc rien d'inattendu). CSS pur
    # (`.lang-active`), aucun script necessaire.
    actuelle = lang.actuelle()
    vers = "fr" if actuelle == "en" else "en"
    return ('<a href="/langue?vers=%s" title="%s" class="lang">'
            '<span class="%s">FR</span><span class="%s">EN</span>'
            '</a>'
            % (vers, lang.t("Changer la langue du site"),
               "lang-active" if actuelle == "fr" else "",
               "lang-active" if actuelle == "en" else ""))


def _barre(pseudo: str) -> str:
    """La barre presente sur toutes les pages connectees : identite + menu.

    ⚠⚠ REECRITE EN VRAI MENU (23/09/2026, demande de l'utilisateur : « c'est
    pas du tout user-friendly »). Avant : UN SEUL <span>, les liens separes
    par du texte « &middot; » -- impossible a espacer, a transformer en
    puces cliquables, ou a distinguer visuellement les uns des autres. Chaque
    lien est maintenant un element propre (`.barre-nav a`), le CSS decide de
    son espacement -- rien a refaire ici si l'habillage change.
    """
    admin = (
        '<a href="/admin">%s</a>' % lang.t("Administration")
        + '<a href="/suivi">%s</a>' % lang.t("Suivi des parties")
        # Portage separe (Hogwarts Battle), visible seulement pour
        # l'administrateur : ce n'est pas un lien pour les joueurs de
        # Marvel Champions, seulement un raccourci prive.
        + '<a href="https://hogwarts.narwhalchampions.com" target="_blank" rel="noopener">Hogwarts Battle</a>'
    ) if pseudo == ADMIN else ""
    # ⚠ L'ENTREE EST LA POUR TOUT LE MONDE, le compteur seulement quand une
    # reponse attend. Une page « Mes signalements » qu'on ne trouve qu'une fois
    # prevenu n'existe pas vraiment.
    attente = reponses_non_lues(pseudo)
    signalements = ('<a href="/signalements">%s%s</a>'
                    % (lang.t("Mes signalements"),
                       ' <span class="pastille">%d</span>' % attente if attente else ""))
    # ⚠ LE RETOUR N'EST PAS UN CONFORT, C'EST LA SEULE SORTIE. Le site
    # s'installe en application (`MANIFESTE_APPLI`, `display: standalone`), donc
    # dans une fenetre SANS bouton Precedent. Signale par un joueur le
    # 19/09/2026 : arrive sur « Mes signalements », il ne pouvait en repartir
    # qu'en fermant la fenetre et en en rouvrant une. La barre est la seule
    # chose presente sur toutes les pages : c'est donc ici, et nulle part
    # ailleurs, que le retour doit vivre.
    # ⚠⚠ EN BARRE FIXE, LOGO INCLUS (23/09/2026, demande de l'utilisateur) :
    # le narval vivait avant dans le contenu de chaque page (`.marque` dans
    # PAGE) ; il vit maintenant ICI, une seule fois, puisque la barre entiere
    # est devenue fixe en haut de l'ecran sur toutes les pages connectees.
    # Le logo EST le lien « Accueil » (convention universelle) : l'ancien
    # lien texte separe a ete retire, il aurait fait doublon juste a cote.
    # ⚠ LE BURGER (zone 2 de la refonte telephone, 09/10/2026) : cache au-dessus
    # de 768 px par le CSS de la page ; au telephone, il deroule identite et
    # liens sous la barre fine.
    return ('<header class="barre">'
            '<a href="/" class="barre-logo"><img src="/narwhal.png" alt="" width="512" height="512">'
            'NarwhalChampions</a>'
            '<button type="button" class="barre-burger" aria-label="%s" aria-expanded="false" '
            'onclick="var b=this.parentNode;b.classList.toggle(\'ouvert\');'
            'this.setAttribute(\'aria-expanded\',b.classList.contains(\'ouvert\'))">&#9776;</button>'
            '<div class="barre-qui">%s <strong>%s</strong></div>'
            '<nav class="barre-nav">%s%s%s'
            '<a href="/deconnexion" class="sortie">%s</a>'
            '</nav></header>'
            % (lang.t("Menu"), lang.t("Connecté"), html.escape(pseudo),
               signalements, admin, _bouton_langue(),
               lang.t("Se déconnecter")))


def page_reprise(pseudo: str, attendue: dict) -> bytes:
    """« Ta partie t'attend » : reprendre, ou commencer autre chose.

    ⚠ ON PROPOSE, ON NE FORCE PAS (decision de l'utilisateur, 13/09/2026).
    Quelqu'un qui revient le lendemain ne veut pas forcement reprendre la
    partie de la veille, et une reprise automatique lui enleve le choix.

    ⚠ ET LA PAGE DIT D'OU VIENT LA COUPURE. « Ta table s'est fermee » sans
    raison laisse croire a un plantage ; le motif est deja traduit pour la page
    de suivi (`CAUSES_ABANDON`), on le reutilise.
    """
    motif = CAUSES_ABANDON.get(attendue.get("cause") or "", attendue.get("cause") or "")
    # Etiquettes separees (23/09/2026, demande de l'utilisateur) : avant, une
    # seule ligne « Klaw · Steve Rogers · round 1 » -- trois pastilles se
    # scannent plus vite qu'une phrase a decouper soi-meme.
    etiquettes = "".join(
        '<span class="badge-partie">%s</span>' % html.escape(x)
        for x in (attendue.get("scenario"), attendue.get("heros"),
                  ("round %d" % int(attendue.get("tour") or 0)) if attendue.get("tour") else None)
        if x)
    # Portrait du vilain (23/09/2026) : voir _portrait_vilain(). N'affiche
    # rien si le fichier n'existe pas -- jamais de repli laid.
    slug_vilain = _slug_vilain(attendue.get("scenario") or "")
    portrait = ('<img class="portrait-vilain" src="/vilains/%s.jpg" alt="" width="80" height="116">'
               % slug_vilain) if _portrait_vilain(slug_vilain) is not None else ""
    # Icones (23/09/2026, demande de l'utilisateur : rendre les deux choix
    # plus lisibles au premier coup d'oeil) : deux SVG inline minuscules,
    # sans emoji -- `currentColor` pour suivre la couleur du texte du bouton
    # (blanc sur le rouge, clair sur le gris) sans variante a maintenir.
    icone_reprendre = ('<svg class="choix-icone" viewBox="0 0 24 24" width="22" height="22" '
                       'aria-hidden="true"><path fill="currentColor" d="M8 5v14l11-7z"/></svg>')
    icone_nouvelle = ('<svg class="choix-icone" viewBox="0 0 24 24" width="22" height="22" '
                      'aria-hidden="true"><path fill="currentColor" d="M11 5h2v6h6v2h-6v6h-2v-6H5v-2h6z"/></svg>')
    # ⚠⚠ ORDRE DES BOUTONS INVERSE (23/09/2026, demande de l'utilisateur) :
    # « si quelqu'un a quitte la partie, c'est le plus souvent pour en
    # commencer une autre » -- donc « Commencer autre chose » est maintenant
    # le choix PRINCIPAL (rouge, grand), « Reprendre » repasse en secondaire
    # (bordure fine). Uniquement un choix d'AFFICHAGE : les deux restent de
    # vrais boutons, aucun forcage (voir la note en tete de fonction).
    corps = ('<div class="table">'
             '<div class="entete-partie">%s'
             '<div><strong>%s</strong>'
             '<div class="badges-partie">%s</div></div></div>'
             '<p class="mdp">%s</p>'
             '<div class="choix" style="margin-top:1rem">'
             '<form method="get" action="/nouvelle-partie">'
             '<button type="submit">%s<span><b>%s</b>'
             '<em>%s</em></span></button></form>'
             '<form method="get" action="/reprendre">'
             '<button type="submit" class="calme">%s<span><b>%s</b>'
             '<em>%s</em></span></button></form>'
             '</div></div>'
             % (portrait,
                lang.t("Ta partie t'attend"),
                etiquettes,
                lang.t("Interrompue le {quand}{motif}. Elle a été sauvegardée : "
                       "tu peux la reprendre là où tu l'avais laissée.")
                .replace("{quand}", _horodate(attendue.get("quand") or ""))
                .replace("{motif}", (", " + html.escape(motif)) if motif else ""),
                icone_nouvelle,
                lang.t("Commencer autre chose"),
                lang.t("La sauvegarde reste dans « Reprendre », sur l'écran de "
                       "préparation."),
                icone_reprendre,
                lang.t("Reprendre cette partie"),
                lang.t("On recharge la sauvegarde et on te remet au plateau.")))
    return PAGE.format(tete="", sous=lang.t("Tu étais en pleine partie."),
                       barre=_barre(pseudo), corps=corps,
                       pied=_pied_de_page(), bouton_appli=_bouton_appli()).encode("utf-8")


def etiquette_ticket(etat: str) -> str:
    """L'etat d'un ticket, tel que le JOUEUR le lit, dans sa langue.

    ⚠ UN DICTIONNAIRE CONSTANT NE POUVAIT PAS CONVENIR : il est evalue au
    chargement du module, quand aucune requete n'existe et donc aucune langue.
    """
    return {
        "nouveau": lang.t("Reçu"),
        "en cours": lang.t("En cours"),
        "traite": lang.t("Corrigé"),
        "refuse": lang.t("Refusé"),
    }.get(etat, etat)


def page_signalements(pseudo: str) -> bytes:
    """« Mes signalements » : ses bugs, leur etat, et la conversation.

    ⚠ IL VOIT TOUT CE QUI VIENT DE SES TABLES, mais ne REPOND que sur ses
    propres signalements. `rapports_de_ses_tables` cadre l'affichage,
    `tickets_de` cadre l'autorisation d'ecrire, et les deux ne doivent jamais
    etre confondues. Un rapport envoye depuis la table de quelqu'un d'autre ne
    lui appartient pas, meme s'il l'a ecrit de sa main.

    ⚠ TOUT CE QUI VIENT D'UN JOUEUR PASSE PAR `html.escape`, ici comme dans
    /admin : la description, le nom et le fil sont ecrits a la main.
    """
    tickets = rapports_de_ses_tables(pseudo)
    if not tickets:
        corps = ('<div class="table"><div class="entete">'
                 '<strong>%s</strong></div>'
                 '<p class="mdp">%s</p></div>'
                 % (lang.t("Aucun signalement"),
                    lang.t("Quand un bug te gêne en partie, le bouton "
                           "« Signaler un bug » l'envoie avec ta capture d'écran "
                           "et le journal de la partie. Tu retrouveras ici ma "
                           "réponse.")))
        return PAGE.format(tete="", sous=lang.t("Rien à suivre pour l'instant."),
                           barre=_barre(pseudo), corps=corps,
                           pied=_pied_de_page(), bouton_appli=_bouton_appli()).encode("utf-8")

    corps = ""
    for r in tickets:
        etat = r["etat"] or "nouveau"
        fil = ""
        for m in r.get("messages") or []:
            fil += ('<p class="msg %s"><b>%s</b> <span class="mdp">%s</span><br>%s</p>'
                    % ("de-lui" if m["auteur"] == "admin" else "de-moi",
                       lang.t("Réponse") if m["auteur"] == "admin" else lang.t("Moi"),
                       _horodate(m["quand"] or ""),
                       html.escape(m["texte"] or "").replace("\n", "<br>")))
        if not fil:
            fil = '<p class="mdp">%s</p>' % lang.t("Pas encore de réponse.")
        capture = ('<p><a href="/admin/capture?id=%d" target="_blank" rel="noopener">'
                   '%s</a></p>' % (r["id"], lang.t("Voir la capture"))) if r["capture"] else ""
        # Le siege n'est montre QUE s'il n'est pas le sien : « siege 0 », c'est
        # lui, et le rappeler a chaque ligne n'apprendrait rien a personne.
        siege = int(r["siege"] or 0)
        if siege:
            provenance = (' &middot; %s %d (%s)'
                          % (lang.t("siège"), siege, html.escape(r["nom"] or "")))
            # Pas de formulaire : voir `rapports_de_ses_tables`. Repondre ici
            # ferait passer l'hote pour l'auteur du signalement.
            repondre = ('<p class="mdp">%s</p>'
                        % lang.t("Envoyé depuis un autre siège de ta table : "
                                 "la réponse part à la personne qui l'a écrit."))
        else:
            provenance = ""
            repondre = ('<form method="post" action="/signalements" class="repondre">'
                        '<input type="hidden" name="id" value="%d">'
                        '<textarea name="texte" rows="2" placeholder="%s"></textarea>'
                        '<button type="submit">%s</button></form>'
                        % (r["id"], lang.t("Ajouter quelque chose"), lang.t("Envoyer")))
        corps += ('<div class="table">'
                  '<div class="entete"><strong>%s</strong>'
                  '<span class="mdp">%s &middot; %s%s</span></div>'
                  '<div class="fil">%s</div>%s%s'
                  '</div>'
                  % (html.escape((r["description"] or "")[:160]),
                     etiquette_ticket(etat),
                     _horodate(r["quand"] or ""), provenance, fil, capture, repondre))
    return PAGE.format(tete="", sous=lang.t("Ce que tu as signalé, et ma réponse."),
                       barre=_barre(pseudo), corps=corps,
                       pied=_pied_de_page(), bouton_appli=_bouton_appli()).encode("utf-8")


def page_attente(pseudo: str) -> bytes:
    """Le seul ecran du site entre la connexion et le jeu.

    Il ne s'affiche que le temps que le moteur reponde, puis la balise
    `refresh` renvoie sur `/entrer`, qui redirige vers le jeu. En regime
    normal (moteur deja allume) personne ne voit jamais cette page.
    """
    erreur = ERREURS_DEMARRAGE.get(pseudo, "")
    if erreur:
        tete = ""
        sous = lang.t("Quelque chose a coincé.")
        corps = ('<div class="table">'
                 '<div class="entete"><strong>%s</strong></div>'
                 '<p class="mdp">%s</p>'
                 '<form method="get" action="/entrer" style="margin-top:1rem">'
                 '<button type="submit">%s</button></form></div>'
                 % (lang.t("Ton jeu n'a pas démarré"), html.escape(erreur),
                    lang.t("Réessayer")))
    else:
        # ⚠ PLUS DE `meta refresh` COMME MOTEUR DE L'ATTENTE (17/09/2026).
        # Il rechargeait la page ENTIERE toutes les trois secondes : l'ecran
        # clignotait, et c'est ce que l'utilisateur a appele « vraiment moche ».
        # On interroge `/pret`, qui ne fait que REGARDER (il ne relance rien),
        # et on bascule quand le moteur repond. Le `noscript` garde l'ancien
        # comportement pour un navigateur sans JavaScript.
        tete = ('<noscript><meta http-equiv="refresh" content="3;url=/entrer"></noscript>')
        sous = lang.t("Un instant.")
        corps = ('<div class="attente">'
                 '<img class="attente-logo" src="/narwhal.png?h=%d" alt="" width="512" height="512">'
                 '<strong>%s</strong>'
                 '<p class="mdp">%s</p>'
                 '<div class="attente-barre"><i></i></div>'
                 '<p class="attente-note mdp">%s</p>'
                 '</div>'
                 '<script>'
                 '(function(){'
                 ' var essais=0;'
                 ' function voir(){'
                 '  essais++;'
                 '  fetch("/pret",{cache:"no-store"}).then(function(r){return r.json()})'
                 '   .then(function(e){ if(e&&e.pret){location.replace("/entrer");return;}'
                 '     if(e&&e.erreur){location.replace("/entrer");return;}'
                 '     setTimeout(voir, essais<10?1500:4000); })'
                 '   .catch(function(){ setTimeout(voir, 4000); });'
                 ' }'
                 ' setTimeout(voir, 1200);'
                 '})();'
                 '</script>'
                 % (narval_du_moment.tranche(),
                    lang.t("Ton jeu démarre"),
                    lang.t("Le premier allumage prend une minute ou deux. "
                           "Cette page bascule toute seule dès que c'est prêt."),
                    lang.t("Tu peux laisser cet onglet ouvert.")))
    return PAGE.format(tete=tete, sous=sous, barre=_barre(pseudo), corps=corps,
                       pied=_pied_de_page(), bouton_appli=_bouton_appli()).encode("utf-8")


# ⚠ GABARIT A PART, PAS `PAGE_FORMULAIRE` (qui impose un champ mot de passe en
# dur) NI `PAGE` (qui impose `_barre(pseudo)`, donc un compte reel -- cet
# ecran peut s'afficher a quelqu'un qui n'en a AUCUN). Meme palette que les
# deux pour rester coherent visuellement, structure propre en dessous.
PAGE_ACTIVITE_DISCORD = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titre} — NarwhalChampions</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&display=swap">
<style>
  :root {{
    color-scheme: dark;
    --bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;
    --text:#eef1f5; --muted:#8b95a3;
    --accent:#e62429; --accent-hover:#ff3b40; --accent-ink:#fff;
    --affiche: "Anton", "Arial Narrow", sans-serif;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; background:var(--bg); color:var(--text);
         min-height:100vh; display:flex; align-items:center; justify-content:center; padding:2.5rem 1.1rem; }}
  main {{ width:100%; max-width:23rem; }}
  .marque {{ display:flex; align-items:center; gap:.7rem; margin:0 0 1.6rem; }}
  .marque img {{ width:2.5rem; height:2.5rem; border-radius:50%; box-shadow:0 0 0 2px var(--border); }}
  h1 {{ font:clamp(1.5rem,6vw,1.85rem)/1 var(--affiche); margin:0; font-weight:400;
       letter-spacing:.01em; text-transform:uppercase; }}
  .carte {{ background:var(--panel); border:1px solid var(--border); border-radius:.9rem;
           padding:1.5rem 1.4rem; box-shadow:0 12px 28px -18px rgba(0,0,0,.7); }}
  .carte p {{ color:var(--muted); font-size:.9rem; margin:0 0 1.2rem; }}
  .choix {{ display:grid; gap:.7rem; }}
  a.bouton {{ display:block; text-align:center; text-decoration:none; font-weight:700;
             background:var(--panel-2); color:var(--text); border:1px solid var(--border);
             border-radius:.5rem; padding:.8rem; }}
  a.bouton.principal {{ background:var(--accent); color:var(--accent-ink); border-color:var(--accent); }}
  a.bouton:hover {{ filter:brightness(1.12); }}
  .mention-legale {{ color:#5b6270; font-size:.75rem; line-height:1.5; margin:1.2rem .1rem 0; }}
</style>
<main>
  <div class="marque"><img src="/narwhal.png" alt="" width="512" height="512"><h1>{titre}</h1></div>
  <div class="carte">
    <p>{texte}</p>
    {corps}
  </div>
  <p class="mention-legale">{mention}</p>
</main>
"""


def page_activite_discord_participant(hote: str, instance_id: str, prete: bool) -> bytes:
    """L'ecran d'un PARTICIPANT ANONYME (pas l'hote, pas connecte) qui ouvre
    l'activite Discord. Qui est connecte ne voit jamais cet ecran : il est
    assis directement (`_repondre_participant`).

    Deux issues, jamais d'inscription proposee ici (recapitulatif valide avec
    l'utilisateur, 28/09/2026) :
      - « J'ai un compte » -> `/connexion?da=...` (meme mecanisme que pour
        l'hote), puis assis directement sur SON siege, en tant que SOI-MEME.
      - « Je suis invite » -> `/activite_discord?...&invite=1` : un siege lui
        est attribue et il y est envoye, sans rien demander.

    `prete` faux : le moteur de l'hote n'a pas encore repondu (juste apres
    qu'il soit devenu hote). On repropose alors la page un peu plus tard,
    comme `page_attente` le fait pour lui.
    """
    if not prete:
        titre = lang.t("Un instant")
        texte = lang.t("La table de {hote} n'est pas encore prête. Cette page "
                       "réessaie toute seule.").replace("{hote}", html.escape(hote))
        corps = '<script>setTimeout(function(){location.reload();},3000);</script>'
        return PAGE_ACTIVITE_DISCORD.format(titre=titre, texte=texte, corps=corps, mention=_mention_courte()).encode("utf-8")

    # `da` en query, pas un cookie pose en JS : meme raison que cote hote
    # (`_activite_discord`) -- ce qui survit fiablement au POST /connexion
    # qui suit, dans le cadre Discord, c'est le champ cache du formulaire,
    # pas un cookie.
    lien_connexion = "/connexion?da=" + urllib.parse.quote(instance_id)
    lien_invite = "/activite_discord?instance_id=%s&invite=1" % urllib.parse.quote(instance_id)

    titre = lang.t("Rejoindre la table de {hote}").replace("{hote}", html.escape(hote))
    texte = lang.t("Tu peux jouer avec ton compte (tu retrouveras ce qui t'appartient), "
                   "ou simplement en invité.")
    corps = ('<div class="choix">'
             '<a class="bouton principal" href="%s">%s</a>'
             '<a class="bouton" href="%s">%s</a>'
             '</div>'
             % (html.escape(lien_connexion), lang.t("J’ai un compte"),
                html.escape(lien_invite), lang.t("Je suis invité")))
    return PAGE_ACTIVITE_DISCORD.format(titre=titre, texte=texte, corps=corps, mention=_mention_courte()).encode("utf-8")


def page_activite_discord_complete(hote: str) -> bytes:
    titre = lang.t("Table complète")
    texte = lang.t("La table de {hote} n'a plus de siège libre.").replace(
        "{hote}", html.escape(hote))
    return PAGE_ACTIVITE_DISCORD.format(titre=titre, texte=texte, corps="", mention=_mention_courte()).encode("utf-8")


# ⚠ LE SDK EST UNE COPIE LOCALE (`site/discord-sdk.mjs`, servie en
# `/discord-sdk.js`), PAS UN IMPORT DEPUIS UN CDN. Le site n'a pas de chaine
# de build JS ; le SDK est publie en ESM, d'ou un import direct. Il venait
# d'esm.sh jusqu'au 29/09/2026, mais la CSP du proxy Discord n'autorise que
# `'self'` : l'import y etait bloque sur toutes les pages suivant celle-ci, et
# Discord fermait l'activite. Pour monter de version : retelecharger le
# bundle esm.sh (`.../es2022/embedded-app-sdk.bundle.mjs`) et changer `?v=`.
# ⚠ CETTE PAGE NE SE RECHARGE JAMAIS, ET C'EST TOUT L'OBJET. Discord n'envoie
# `READY` qu'UNE fois par cadre : apres un rechargement du document,
# `sdk.ready()` ne revient plus jamais et Discord ferme l'activite quelques
# secondes plus tard (github.com/discord/embedded-app-sdk/issues/41, constate
# en prod le 29/09/2026 a chaque etape du parcours). Or le site et le jeu
# sont faits de pages pleines (connexion, attente, preparation, plateau...).
# La coquille garde donc le SDK vivant et affiche le jeu dans un cadre
# interne (meme origine, memes cookies partitionnes), qui peut changer de
# page autant qu'il veut sans que Discord ne le voie.
PAGE_ACTIVITE_DISCORD_AMORCE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>NarwhalChampions</title>
<style>
  html, body {{ margin:0; height:100%; background:#07080c; color:#eef1f5;
                font:16px system-ui,sans-serif; overflow:hidden; }}
  #etat {{ position:absolute; inset:0; display:flex; align-items:center;
           justify-content:center; opacity:.75; }}
  #jeu {{ position:absolute; inset:0; width:100%; height:100%; border:0; display:none; }}
</style>
<p id="etat">Connexion à Discord…</p>
<iframe id="jeu" title="NarwhalChampions" allow="autoplay; fullscreen"></iframe>
<script type="module">
  const etat = document.getElementById('etat');
  const jeu = document.getElementById('jeu');
  try {{
    const {{ DiscordSDK }} = await import('/discord-sdk.js?v=2.5.0');
    // Garde sur `window` : le SDK doit vivre aussi longtemps que la page.
    const sdk = window.discordSdk = new DiscordSDK({client_id!r});
    await sdk.ready();
    if (!sdk.instanceId) throw new Error('instanceId absent après ready()');
    jeu.addEventListener('load', () => {{ etat.style.display = 'none'; jeu.style.display = 'block'; }}, {{ once: true }});
    jeu.src = '/activite_discord?instance_id=' + encodeURIComponent(sdk.instanceId);
  }} catch (erreur) {{
    console.error('Activité Discord : ', erreur);
    etat.textContent = "Impossible de démarrer l'activité (" + (erreur && erreur.message || erreur) + "). "
        + "Voir DISCORD.md.";
  }}
</script>
"""


def page_activite_discord_amorce() -> bytes:
    return PAGE_ACTIVITE_DISCORD_AMORCE.format(client_id=DISCORD_CLIENT_ID).encode("utf-8")


SDK_DISCORD = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "discord-sdk.mjs"), "rb").read()


def page_enchainer(vers: str) -> bytes:
    """Une page 200 qui mene aussitot a VERS : la redirection du mode Discord
    (voir `_rediriger`)."""
    return ('<!doctype html><meta charset="utf-8">'
            '<meta http-equiv="refresh" content="0;url=%s">'
            '<title>NarwhalChampions</title>' % html.escape(vers, quote=True)).encode("utf-8")


def page_arret(pseudo: str) -> bytes:
    corps = ('<div class="table">'
             '<div class="entete"><strong>Ton jeu est éteint</strong></div>'
             '<p class="mdp">Rien n\'est perdu : tes decks, tes campagnes et tes '
             'hauts faits t\'attendent au prochain allumage.</p>'
             '<p class="mdp">Éteindre ferme aussi la porte aux invités de la '
             'partie précédente : leur lien et leur navigateur ne rouvrent plus '
             'ta table. Toi, tu rentres par ce bouton, comme d\'habitude.</p>'
             '<form method="get" action="/entrer" style="margin-top:1rem">'
             '<button type="submit">Rallumer mon jeu</button></form></div>')
    return PAGE.format(tete="", sous="À tout de suite.", barre=_barre(pseudo),
                       corps=corps, pied=_pied_de_page(), bouton_appli=_bouton_appli()).encode("utf-8")


PAGE_FORMULAIRE = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,interactive-widget=resizes-content">
<title>{titre} — NarwhalChampions</title>
{tete_appli}
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&display=swap">
<style>
  /* ===== REFONTE (20/10/2026, decision du 09/10) ===========================
     Connexion, inscription et pages cousines sur le modele de l'assistant de
     preparation : un EN-TETE FIN, une SCENE a gauche (~30 %, bord en biais,
     la mascotte du moment et le titre en affiche) et le formulaire a droite.
     Au telephone la scene devient un BANDEAU colle en haut, le formulaire
     dessous. Toutes les couleurs passent par les variables : le mode sobre
     (SOBRE_SITE) les redefinit sans rien toucher ici. */
  /*JETONS*/
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; background:var(--bg); color:var(--text);
         min-height:100vh; display:flex; flex-direction:column; }}
  .entete {{ flex:none; display:flex; align-items:center; justify-content:space-between; gap:1rem;
            height:3rem; padding:0 1.2rem; background:var(--panel); border-bottom:1px solid var(--border); }}
  .entete-marque {{ display:flex; align-items:center; gap:.6rem; font:1.15rem/1 var(--affiche);
                   letter-spacing:.04em; text-transform:uppercase; }}
  .entete-marque img {{ width:1.9rem; height:1.9rem; border-radius:50%; box-shadow:0 0 0 1px var(--border); }}
  .lang {{ display:inline-flex; align-items:center; border:1px solid var(--border);
          font-size:.8rem; font-weight:600; text-decoration:none; }}
  .lang span {{ padding:.2rem .5rem; color:var(--muted); }}
  .lang span.lang-active {{ background:var(--accent); color:var(--accent-ink); }}
  .cadre {{ flex:1; display:grid; grid-template-columns:minmax(17rem,30%) 1fr; min-height:0; }}
  .scene {{ position:relative; overflow:hidden; display:flex; flex-direction:column; justify-content:flex-end;
           gap:1.2rem; padding:2rem 5rem 2.6rem 2rem;
           background:radial-gradient(circle at 35% 38%, var(--accent-soft), transparent 62%), var(--panel);
           clip-path:polygon(0 0,100% 0,calc(100% - 3.5rem) 100%,0 100%); }}
  .scene img {{ width:min(100%,14rem); aspect-ratio:1; height:auto; border-radius:50%;
               box-shadow:0 0 0 2px var(--border), 0 18px 40px -16px rgba(0,0,0,.8); }}
  h1 {{ font:clamp(1.9rem,3.3vw,3rem)/1 var(--affiche); margin:0; font-weight:400;
       letter-spacing:.01em; text-transform:uppercase; text-wrap:balance; }}
  .contenu {{ display:flex; align-items:center; justify-content:center; padding:2rem 1.5rem; }}
  .colonne {{ width:100%; max-width:24rem; }}
  .carte {{ background:var(--panel); border:1px solid var(--border); border-radius:.9rem;
           padding:1.5rem 1.4rem; box-shadow:0 12px 28px -18px rgba(0,0,0,.7); }}
  form {{ margin:0; }}
  label {{ display:block; margin-bottom:1rem; font-size:.88rem; color:var(--muted); }}
  input {{ width:100%; box-sizing:border-box; font:inherit; margin-top:.35rem;
          background:var(--panel-2); color:inherit; border:1px solid var(--border);
          border-radius:.5rem; padding:.65rem .9rem; }}
  input:focus-visible, button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
  button {{ width:100%; font:inherit; font-weight:700; background:var(--accent); color:var(--accent-ink);
           border:0; border-radius:.5rem; padding:.8rem; cursor:pointer; transition:background .12s ease; }}
  button:hover {{ background:var(--accent-hover); }}
  .erreur {{ border:1px solid var(--danger); background:#1d1113; color:#ff7b72;
            border-radius:.5rem; padding:.7rem .9rem; margin-bottom:1.2rem; font-size:.9rem; }}
  /* Le pied : une ligne par phrase, lisible (la premiere, celle qui sert, en clair). */
  .pied {{ margin:1.1rem .1rem 0; color:var(--muted); font-size:.85rem; line-height:1.55; }}
  .pied .ligne {{ display:block; margin-top:.4rem; }}
  .pied .ligne:first-child {{ margin-top:0; color:var(--text); font-size:.92rem; }}
  .mention-legale {{ color:var(--muted); opacity:.75; font-size:.72rem; line-height:1.5; margin:1.4rem .1rem 0; }}
  a {{ color:var(--accent); }}
  /* TELEPHONE : la scene devient un bandeau fin colle en haut (mascotte + titre
     sur une ligne), le formulaire juste dessous, champs et bouton de 44 px. Le
     clavier ne cache pas le bouton : la page retrecit avec lui
     (`interactive-widget`), et le champ touche fait defiler jusqu'au bouton
     (script plus bas). Au-dessus de 768 px, c'est la mise en page a deux
     colonnes. */
  @media (max-width:767px) {{
    body {{ min-height:100dvh; padding-bottom:1.5rem; }}
    /* L'en-tete se reduit a la bascule FR / EN, posee sur la droite du bandeau (20/10/2026). */
    .entete {{ position:fixed; top:0; right:0; z-index:6; height:56px; padding:0 .7rem; background:none;
              border:0; pointer-events:none; }}
    .entete-marque {{ display:none; }}
    .entete .lang {{ pointer-events:auto; background:var(--panel); }}
    .cadre {{ display:block; }}
    .scene {{ position:sticky; top:0; z-index:5; flex-direction:row; justify-content:flex-start; align-items:center; gap:.7rem;
             min-height:56px; padding:.4rem 1rem; clip-path:none; border-bottom:1px solid var(--border);
             background:linear-gradient(90deg, var(--accent-soft), transparent 70%), var(--panel); }}
    .scene img {{ width:2.3rem; box-shadow:0 0 0 1px var(--border); }}
    h1 {{ font-size:1.35rem; }}
    .contenu {{ display:block; padding:1rem 0 0; }}
    .colonne {{ max-width:none; }}
    .carte {{ margin:0 1rem; padding:1.1rem 1rem; border-radius:.7rem; }}
    label {{ margin-bottom:.8rem; }}
    input {{ min-height:44px; font-size:16px; }}
    button {{ min-height:48px; }}
    .pied, .mention-legale {{ margin-left:1rem; margin-right:1rem; }}
    .pied a {{ display:inline-flex; align-items:center; min-height:44px; min-width:44px; }}
    .lang span {{ display:flex; align-items:center; min-height:40px; padding:0 .8rem; }}
  }}
</style>
<header class="entete">
  <span class="entete-marque"><img src="/narwhal.png" alt="" width="512" height="512">NarwhalChampions</span>
  {langue}
</header>
<div class="cadre">
  <aside class="scene"><img src="/narwhal.png" alt="" width="512" height="512"><h1>{titre}</h1></aside>
  <main class="contenu"><div class="colonne">
    <div class="carte">
      {erreur}
      <form method="post" action="{action}">
        {champs}
        <label>{mdp}<input name="mdp" type="password" autocomplete="{auto}" required></label>
        <button type="submit">{bouton}</button>
      </form>
    </div>
    <div class="pied">{pied}</div>
    <p class="mention-legale">{mention}</p>
    {bouton_appli}
  </div></main>
</div>
<script>(function(){{
  // Telephone : le clavier ne doit pas cacher le bouton d'envoi. Au toucher
  // d'un champ, une fois le clavier ouvert, on amene le bouton dans l'ecran.
  if (!window.matchMedia("(max-width: 767px)").matches) return;
  var bouton = document.querySelector("form button[type=submit]");
  if (!bouton) return;
  document.addEventListener("focusin", function (e) {{
    if (!e.target.matches || !e.target.matches("input")) return;
    setTimeout(function () {{ bouton.scrollIntoView({{ block: "nearest" }}); }}, 300);
  }});
}})();</script>
"""

PAGE_ADMIN = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Administration — NarwhalChampions</title>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&display=swap">
<style>
  /* ===== REFONTE (23/09/2026) =================================================
     La page etait UN SEUL long defilement (Annonce, Comptes, Invitations, Mots
     de passe, Rapports, Joueurs, Parties, Journal, empiles) -- signale par
     l'utilisateur : « la page est beaucoup trop longue ». Elle passe en
     ONGLETS : un seul groupe visible a la fois, memorise (localStorage) d'une
     visite a l'autre, sauf premiere visite ou l'onglet qui attend le plus est
     choisi (voir ADMIN_ONGLETS_SCRIPT). Meme palette/typo/trame que le reste
     du site (voir PAGE) -- dupliquee ici, aucun mecanisme d'inclusion partagee
     dans ce depot. */
  :root {{
    color-scheme: dark;
    --bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;
    --text:#eef1f5; --muted:#8b95a3;
    --accent:#e62429; --accent-hover:#ff3b40; --accent-soft:rgba(230,36,41,.14); --accent-ink:#fff;
    --ok:#3fb950; --danger:#f85149; --warn:#e8a53d;
    --affiche: "Anton", "Arial Narrow", sans-serif;
  }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font:16px/1.5 system-ui,sans-serif; color:var(--text);
         display:flex; justify-content:center; padding:0 1.1rem 2.5rem;
         background-color:var(--bg);
         background-image:
           linear-gradient(to bottom, transparent 0%, transparent 12%, var(--bg) 60%),
           radial-gradient(rgba(230,36,41,.4) 1px, transparent 1.6px);
         background-size:100% 100%, 15px 15px;
         background-repeat:no-repeat, repeat;
         /* ⚠⚠ « fixed » RETIRE (23/09/2026, « ca rame blinde sur le
            telephone » signale juste apres le deploiement) : un fond
            attache au VIEWPORT force le navigateur a le repeindre a
            chaque frame de defilement -- il ne peut plus deleguer le
            scroll au compositeur seul. Connu pour etre couteux sur
            mobile, plus encore avec un motif REPETE (le halftone,
            15x15px). `scroll` (l'attache par defaut, l'element plutot
            que le viewport) est visuellement quasi identique sur une
            page aussi courte que celles du site, et rend le defilement
            fluide. */
         background-attachment:scroll, scroll; }}
  /* Elargie (23/09/2026, demande de l'utilisateur) : les fiches de comptes et
     les rapports respirent mieux sur une page d'outil que sur une page de
     lecture -- 40rem (comme /entrer) etait etroit pour ce contenu-la. */
  main {{ width:100%; max-width:60rem; padding-top:5.5rem; }}
  @media (max-width:640px) {{ main {{ padding-top:7.4rem; }} }}
  h1 {{ font:clamp(1.7rem,5vw,2.2rem)/1 var(--affiche); margin:0 0 1.1rem; font-weight:400;
       letter-spacing:.01em; text-transform:uppercase; }}
  p.sous {{ color:var(--muted); margin:0 0 1.2rem; }}
  table {{ width:100%; border-collapse:collapse; }}
  th, td {{ text-align:left; padding:.6rem .4rem; border-bottom:1px solid var(--border); }}
  th {{ color:var(--muted); font-weight:500; font-size:.85rem; }}
  button {{ font:inherit; font-size:.85rem; font-weight:600; border-radius:0; padding:.4rem .8rem;
           cursor:pointer; border:1px solid var(--border); background:transparent; color:inherit; }}
  button:hover {{ background:var(--panel-2); }}
  button:focus-visible {{ outline:2px solid var(--accent); outline-offset:2px; }}
  button.oui {{ border-color:var(--ok); color:var(--ok); }}
  button.oui:hover {{ background:rgba(63,185,80,.12); }}
  button.non {{ border-color:var(--danger); color:var(--danger); }}
  button.non:hover {{ background:rgba(248,81,73,.12); }}
  code {{ background:var(--panel-2); padding:.2rem .45rem; border-radius:.2rem;
         font-size:.8rem; word-break:break-all; }}
  form {{ display:inline; margin-right:.3rem; }}
  a {{ color:var(--accent); }}
  /* ===== La barre fixe (identique a PAGE, voir _barre()) ===================== */
  .barre {{ position:fixed; top:0; left:0; right:0; z-index:10;
           display:flex; flex-wrap:wrap; align-items:center; gap:.5rem 1.2rem;
           padding:.7rem 1.2rem; background:#040508; border-bottom:1px solid var(--border); }}
  .barre-logo {{ display:flex; align-items:center; gap:.55rem; flex:none;
                font:1rem/1 var(--affiche); text-transform:uppercase; letter-spacing:.01em;
                color:var(--text); text-decoration:none; }}
  .barre-logo img {{ width:2.1rem; height:2.1rem; border-radius:50%; box-shadow:0 0 0 2px var(--border); }}
  .barre-qui {{ color:var(--muted); font-size:.85rem; margin-left:auto; }}
  .barre-qui strong {{ color:var(--text); }}
  .barre-nav {{ display:flex; flex-wrap:wrap; gap:.3rem 1rem; align-items:center;
               flex-basis:100%; order:3; padding-top:.5rem; border-top:1px solid var(--border); }}
  @media (min-width:641px) {{
    .barre-nav {{ flex-basis:auto; order:2; padding-top:0; border-top:0; margin-left:1.2rem; }}
    .barre-qui {{ order:3; }}
  }}
  .barre-nav a {{ color:var(--muted); font-size:.85rem; text-decoration:none; }}
  .barre-nav a:hover {{ color:var(--text); }}
  .barre-nav a.sortie {{ color:var(--muted); }}
  .barre-nav a.sortie:hover {{ color:var(--danger); }}
  .lang {{ display:inline-flex; align-items:center; border:1px solid var(--border);
          font-size:.75rem; font-weight:700; text-decoration:none; overflow:hidden; }}
  .lang span {{ padding:.2rem .5rem; color:var(--muted); }}
  .lang span.lang-active {{ background:var(--accent); color:var(--accent-ink); }}
  .barre .pastille {{ background:var(--accent); color:var(--accent-ink); border-radius:1rem;
                     padding:.03rem .4rem; font-size:.72rem; font-weight:700; }}
  /* ===== L'annonce : toujours visible, repliee (23/09/2026) ================== */
  .annonce-bloc {{ margin:0 0 1.6rem; padding:.9rem 1.1rem; background:var(--panel);
                  border:1px solid var(--border); border-top:3px solid var(--accent); }}
  .annonce-ligne {{ display:flex; gap:1rem; flex-wrap:wrap; align-items:center; justify-content:space-between; }}
  .annonce-etat {{ margin:0; color:var(--muted); font-size:.92rem; flex:1; min-width:12rem; }}
  .annonce-boutons {{ display:flex; gap:.5rem; flex-wrap:wrap; }}
  .annonce-toggle {{ background:transparent; color:var(--text); border:1px solid var(--border);
                    font-size:.82rem; padding:.4rem .8rem; }}
  .annonce-toggle:hover {{ border-color:var(--accent); color:var(--accent); }}
  .annonce-form {{ margin-top:.9rem; padding-top:.9rem; border-top:1px solid var(--border); }}
  .annonce-form form {{ display:block; }}
  /* ===== Les onglets principaux ============================================= */
  .onglets {{ position:sticky; top:5.5rem; z-index:9; display:flex; gap:.3rem; overflow-x:auto;
             -webkit-overflow-scrolling:touch; background:var(--bg); padding:.6rem 0 .5rem;
             margin-bottom:1.4rem; border-bottom:1px solid var(--border); scrollbar-width:none; }}
  .onglets::-webkit-scrollbar {{ display:none; }}
  @media (max-width:640px) {{ .onglets {{ top:7.4rem; }} }}
  .onglet {{ flex:none; display:flex; align-items:center; gap:.4rem; font:inherit; font-weight:700;
            font-size:.88rem; background:transparent; color:var(--muted); border:1px solid var(--border);
            border-radius:0; padding:.55rem 1rem; cursor:pointer; white-space:nowrap; }}
  .onglet:hover {{ color:var(--text); border-color:#38404d; }}
  .onglet[aria-selected="true"] {{ background:var(--accent); border-color:var(--accent); color:var(--accent-ink); }}
  .pastille-onglet {{ background:#fff; color:var(--accent); border-radius:1rem; font-size:.72rem;
                     font-weight:700; padding:.03rem .42rem; line-height:1.4; }}
  .panneau[hidden] {{ display:none; }}
  /* ===== Les sous-onglets : plus discrets, un cran en dessous (23/09/2026,
     demande de l'utilisateur : garder la hierarchie visible) ================= */
  .sous-onglets {{ display:flex; gap:1.2rem; margin-bottom:1.1rem; border-bottom:1px solid var(--border); }}
  .sous-onglet {{ background:transparent; border:0; border-bottom:2px solid transparent; border-radius:0;
                color:var(--muted); font:inherit; font-size:.82rem; font-weight:600; padding:.45rem 0;
                cursor:pointer; }}
  .sous-onglet:hover {{ color:var(--text); }}
  .sous-onglet[aria-selected="true"] {{ color:var(--accent); border-bottom-color:var(--accent); }}
  .sous-onglet .compte {{ color:inherit; opacity:.7; font-weight:400; margin-left:.3rem; }}
  .sous-panneau[hidden] {{ display:none; }}
  .dj-compte {{ background:var(--panel); border:1px solid var(--border); border-radius:.6rem; padding:.8rem 1rem; margin-bottom:.8rem; }}
  .dj-compte h3 {{ margin:0 0 .5rem; font-size:1rem; }}
  .dj-compte ul {{ list-style:none; margin:0; padding:0; }}
  .dj-deck {{ display:flex; justify-content:space-between; align-items:center; gap:.8rem; padding:.5rem 0; border-top:1px solid var(--border); }}
  .dj-infos {{ display:flex; flex-direction:column; min-width:0; }}
  .dj-meta {{ color:var(--muted); font-size:.8rem; }}
  .dj-importer, .dj-actualiser {{ background:var(--accent); color:var(--accent-ink); border:0; border-radius:.4rem; padding:.4rem .8rem; font:inherit; font-weight:700; cursor:pointer; flex:none; }}
  .dj-importer:hover, .dj-actualiser:hover {{ background:var(--accent-hover); }}
  .dj-importer:disabled {{ opacity:.5; cursor:wait; }}
  .dj-message {{ min-height:1.4rem; margin:.5rem 0; font-weight:600; }}
  .dj-ok {{ color:#6fcf8f; }}
  .dj-erreur {{ color:#ff6b6b; }}
  /* Les comptes, en fiches (23/09/2026, demande de l'utilisateur : le
     tableau a 6 colonnes etait illisible, surtout etroit). Une pastille
     d'initiale, le nom et son statut sur une ligne, le reste en meta. Les
     invitations et mots de passe oublies reprennent la meme fiche, pour la
     coherence (23/09/2026). */
  .comptes {{ display:grid; gap:.5rem; margin-bottom:1rem; }}
  .compte-ligne {{ display:flex; align-items:center; gap:.85rem; flex-wrap:wrap;
                  background:var(--panel); border:1px solid var(--border); border-radius:0;
                  padding:.7rem .9rem; }}
  .compte-avatar {{ flex:none; width:2.1rem; height:2.1rem; border-radius:50%; background:var(--panel-2);
                    border:1px solid var(--border); display:flex; align-items:center; justify-content:center;
                    font-weight:700; font-size:.9rem; color:var(--muted); }}
  .compte-info {{ flex:1; min-width:10rem; }}
  .compte-nom {{ font-weight:700; display:flex; align-items:center; gap:.5rem; flex-wrap:wrap; }}
  .compte-meta {{ color:var(--muted); font-size:.8rem; margin-top:.1rem; }}
  /* Actions en icones discretes (23/09/2026, demande de l'utilisateur) :
     invisibles au repos, revelees au survol/focus -- sauf tactile
     (`pointer:coarse`, meme convention que _bouton_appli()) ou il n'y a pas
     de survol possible, donc toujours visibles. */
  .compte-actions {{ display:flex; gap:.3rem; flex-wrap:wrap; opacity:0; transition:opacity .12s ease; }}
  .compte-ligne:hover .compte-actions, .compte-ligne:focus-within .compte-actions {{ opacity:1; }}
  @media (pointer:coarse) {{ .compte-actions {{ opacity:1; }} }}
  .compte-actions button {{ width:1.9rem; height:1.9rem; padding:0; display:inline-flex;
                           align-items:center; justify-content:center; }}
  .icone-action {{ width:15px; height:15px; }}
  .etat-pastille {{ font-size:.68rem; text-transform:uppercase; letter-spacing:.04em;
                    border-radius:.3rem; padding:.08rem .4rem; border:1px solid; font-weight:600; }}
  .etat-pastille.oui {{ color:var(--ok); border-color:var(--ok); }}
  .etat-pastille.non {{ color:var(--danger); border-color:var(--danger); }}
  .etat-pastille.attente {{ color:var(--warn); border-color:var(--warn); }}
  .rapport {{ border:1px solid var(--border); border-radius:0; margin-bottom:.6rem;
             background:var(--panel); }}
  .rapport[open] {{ border-color:#38404d; }}
  .rapport > summary {{ cursor:pointer; padding:.6rem .8rem; list-style:none;
                       display:flex; gap:.6rem; align-items:baseline; flex-wrap:wrap; }}
  .rapport > summary::-webkit-details-marker {{ display:none; }}
  .rapport .quoi {{ flex:1; min-width:12rem; }}
  .rapport .meta {{ color:var(--muted); font-size:.8rem; }}
  .rapport .corps {{ padding:0 .8rem .8rem; }}
  .rapport pre {{ background:var(--bg); border:1px solid var(--border); border-radius:.3rem;
                 padding:.6rem; max-height:22rem; overflow:auto; font-size:.78rem;
                 white-space:pre-wrap; word-break:break-word; }}
  .rapport img {{ max-width:100%; border:1px solid var(--border); border-radius:.3rem; }}
  .etat {{ font-size:.72rem; text-transform:uppercase; letter-spacing:.04em;
          border-radius:.3rem; padding:.1rem .45rem; border:1px solid; }}
  .etat.nouveau {{ color:var(--warn); border-color:var(--warn); }}
  .etat.encours {{ color:var(--accent); border-color:var(--accent); }}
  .etat.traite {{ color:var(--ok); border-color:var(--ok); }}
  .etat.refuse {{ color:var(--muted); border-color:var(--muted); }}
  /* Le FIL d'un ticket (16/09/2026) : ce que j'ai repondu, ce que le joueur a
     repondu. Les deux camps se distinguent par leur bord, pas par un alignement
     a droite : une conversation a deux voix, pas une messagerie. */
  .fil {{ margin:.6rem 0; display:grid; gap:.4rem; }}
  .fil .msg {{ margin:0; padding:.45rem .6rem; border-radius:.3rem;
              background:var(--bg); border-left:3px solid var(--border); font-size:.88rem; }}
  .fil .msg.de-moi {{ border-left-color:var(--accent); }}
  .fil .msg.de-lui {{ border-left-color:var(--warn); }}
  .fil .msg b {{ font-size:.8rem; }}
  .repondre {{ display:flex; gap:.4rem; align-items:flex-start; margin-top:.2rem; }}
  .repondre textarea {{ flex:1; font:inherit; background:var(--bg); color:inherit;
                       border:1px solid var(--border); border-radius:.3rem; padding:.4rem .6rem;
                       resize:vertical; }}
  .pastille {{ font-size:.8rem; vertical-align:middle; background:var(--accent);
              color:var(--accent-ink); border-radius:1rem; padding:.05rem .5rem; }}
  .groupe {{ margin:.6rem 0; }}
  .groupe > summary {{ cursor:pointer; color:var(--text); font-size:.9rem; padding:.3rem 0;
                      display:flex; gap:.5rem; align-items:center; }}
  .msg {{ border-left:3px solid var(--border); padding:.3rem .6rem; margin:.35rem 0;
         font-size:.9rem; }}
  .msg.moi {{ border-color:var(--accent); }}
  .msg.lui {{ border-color:var(--ok); }}
  .msg .meta {{ color:#5b6270; font-size:.75rem; }}
  .voir-plus {{ display:block; width:100%; margin-top:.6rem; background:transparent;
               color:var(--muted); border:1px dashed var(--border); font-weight:600; }}
  .voir-plus:hover {{ color:var(--text); border-color:var(--muted); }}
  /* ===== TELEPHONE (zone 2 de la refonte du 09/10/2026, fiche
     .planning/todos/2026-10-09-mode-telephone-refonte.md) ====================
     Sous 768 px : une barre fine (logo + burger), le menu se deroule dessous,
     zones tactiles de 44 px. Au-dessus de 768 px, rien ne change. */
  .barre-burger {{ display:none; }}
  @media (max-width:767px) {{
    .barre {{ flex-wrap:wrap; gap:0; padding:.2rem .4rem .2rem 1rem; min-height:52px; }}
    .barre-logo {{ min-height:44px; }}
    .barre-burger {{ display:inline-grid; place-items:center; margin-left:auto; min-width:44px; min-height:44px;
                    padding:0; background:transparent; border:0; color:var(--text); font-size:1.5rem; line-height:1; }}
    .barre-burger:hover {{ background:transparent; }}
    .barre-qui, .barre-nav {{ display:none; }}
    .barre.ouvert .barre-qui {{ display:block; order:3; flex-basis:100%; margin:0; padding:.4rem 0 .1rem; }}
    .barre.ouvert .barre-nav {{ display:flex; order:4; flex-basis:100%; flex-direction:column; align-items:stretch;
                               gap:0; margin:0; padding:.2rem 0 .5rem; border-top:1px solid var(--border); }}
    .barre-nav a {{ display:flex; align-items:center; min-height:44px; font-size:1rem; }}
    .barre-nav a.lang {{ align-self:flex-start; margin-top:.3rem; }}
    .lang span {{ display:flex; align-items:center; min-height:42px; padding:0 .9rem; }}
    main {{ padding-top:4.4rem; }}
  }}
  /* Les tableaux deviennent des cartes empilees au telephone : une ligne = une
     carte, chaque valeur precedee de son libelle (`data-label`). */
  @media (max-width:767px) {{
    table, tbody, tr, td {{ display:block; width:100%; }}
    tr:has(> th) {{ display:none; }}
    tr {{ margin:0 0 .6rem; padding:.55rem .8rem; background:var(--panel); border:1px solid var(--border); }}
    td {{ display:flex; justify-content:space-between; gap:1rem; padding:.2rem 0; border:0; text-align:right; }}
    td::before {{ content:attr(data-label); color:var(--muted); font-size:.85rem; text-align:left; flex:none; }}
    td[colspan] {{ justify-content:flex-start; text-align:left; }}
  }}
  @media (max-width:767px) {{
    /* Telephone : tous les onglets se voient (ils passent a la ligne) au lieu de defiler de cote sans rien dire. */
    .onglets {{ top:52px; flex-wrap:wrap; overflow-x:visible; }}
    .onglet {{ flex:1 1 auto; justify-content:center; }}
    .onglet, .sous-onglet, .annonce-toggle, button {{ min-height:44px; }}
    .sous-onglets {{ overflow-x:auto; scrollbar-width:none; gap:1rem; }}
    .sous-onglet {{ flex:none; min-width:44px; }}
    .compte-actions button {{ width:44px; height:44px; }}
    .rapport > summary, .groupe > summary {{ min-height:44px; align-items:center; }}
    input, textarea, select {{ min-height:44px; font-size:16px; }}
    .repondre {{ flex-direction:column; align-items:stretch; }}
    p.sous a, .rapport a, .corps a {{ display:inline-flex; align-items:center; min-height:44px; min-width:44px; }}
  }}
</style>
{styles_suivi}
<main>
  {barre}
  <h1>Administration</h1>

  <!-- L'ANNONCE EST TOUJOURS VISIBLE, AU-DESSUS DES ONGLETS, ET C'EST VOULU.
       On vient ici pour la poser quand le deploiement est deja lance dans
       l'autre fenetre : elle doit tomber sous la main, jamais cachee dans un
       onglet. Repliee par defaut (23/09/2026, demande de l'utilisateur) :
       une ligne d'etat + un bouton qui deplie le formulaire. -->
  <div class="annonce-bloc">
    <div class="annonce-ligne">
      <p class="annonce-etat">{annonce_etat}</p>
      <div class="annonce-boutons">
        {annonce_annuler}
        <button type="button" class="annonce-toggle" id="annonce-toggle"
                data-ouvert="Fermer" data-ferme="Créer une annonce">Créer une annonce</button>
      </div>
    </div>
    <div class="annonce-form" id="annonce-form" hidden>
      <form method="post" action="/admin">
        <input type="hidden" name="action" value="annonce">
        <label style="color:var(--muted);font-size:.9rem">Dans
          <input name="minutes" type="number" min="1" max="{annonce_max}" value="10"
                 style="width:4.5rem;font:inherit;background:var(--panel-2);color:inherit;
                        border:1px solid var(--border);border-radius:0;padding:.3rem .5rem">
          minutes</label>
        <input name="texte" type="text" maxlength="400" placeholder="Message (vide = préavis de mise à jour)"
               style="width:100%;box-sizing:border-box;margin:.5rem 0;font:inherit;
                      background:var(--panel-2);color:inherit;border:1px solid var(--border);
                      border-radius:0;padding:.4rem .6rem">
        <button class="oui" type="submit">Prévenir</button>
      </form>
    </div>
  </div>

  <nav class="onglets" id="onglets" role="tablist">
    <button type="button" class="onglet" data-onglet="comptes" data-n="{n_comptes}" role="tab">Comptes{badge_comptes}</button>
    <button type="button" class="onglet" data-onglet="rapports" data-n="{n_rapports}" role="tab">Rapports{badge_rapports}</button>
    <button type="button" class="onglet" data-onglet="joueurs" data-n="{n_joueurs}" role="tab">Joueurs{badge_joueurs}</button>
    <button type="button" class="onglet" data-onglet="parties" data-n="0" role="tab">Parties</button>
    <button type="button" class="onglet" data-onglet="journal" data-n="0" role="tab">Journal</button>
    <button type="button" class="onglet" data-onglet="decks" data-n="0" role="tab">{titre_decks}</button>
  </nav>

  <section class="panneau" data-panneau="comptes">
    <nav class="sous-onglets">
      <button type="button" class="sous-onglet" data-sous="comptes-liste" role="tab">Comptes</button>
      <button type="button" class="sous-onglet" data-sous="comptes-invitations" role="tab">Invitations <span class="compte">{nb_invitations}</span></button>
      <button type="button" class="sous-onglet" data-sous="comptes-createurs" role="tab">Créateurs de cartes <span class="compte">{nb_createurs}</span></button>
      <button type="button" class="sous-onglet" data-sous="comptes-mdp" role="tab">Mots de passe <span class="compte">{nb_reinit}</span></button>
    </nav>
    <div class="sous-panneau" data-sous-panneau="comptes-liste">
      <p class="sous">{valides} validé(s) sur {max}. {regle_expiration}
      <a href="/">Retour au site</a></p>
      <div class="comptes">
        {lignes}
      </div>
    </div>
    <div class="sous-panneau" data-sous-panneau="comptes-invitations" hidden>
      <p class="sous">Un lien vaut une place, une seule fois. Celui qui le reçoit
      entre directement, sans passer par la file d'attente.</p>
      <form method="post" action="/admin" style="margin-bottom:1rem">
        <input type="hidden" name="action" value="inviter">
        <button class="oui" type="submit">Créer un lien d'invitation</button>
      </form>
      <div class="comptes">
        {invitations}
      </div>
    </div>
    <div class="sous-panneau" data-sous-panneau="comptes-createurs" hidden>
      <p class="sous">Un compte « créateur de cartes » n'a accès qu'au créateur de
      cartes : ni le jeu, ni cette administration. Il se crée par un lien
      d'invitation à usage unique, à copier et à transmettre. Désactiver un
      compte coupe sa session ; ses projets restent.</p>
      <form method="post" action="/admin" style="margin-bottom:1rem">
        <input type="hidden" name="action" value="inviter_createur">
        <button class="oui" type="submit">Inviter un créateur de cartes</button>
      </form>
      <div class="comptes">
        {createurs}
      </div>
    </div>
    <div class="sous-panneau" data-sous-panneau="comptes-mdp" hidden>
      <p class="sous">Le bouton « Mot de passe » d'un compte crée un lien à usage
      unique, valable 24 heures. Transmets-le à la personne : elle y choisit son
      nouveau mot de passe, et ses anciennes sessions sont fermées.</p>
      <div class="comptes">
        {reinitialisations}
      </div>
    </div>
  </section>

  <section class="panneau" data-panneau="rapports" hidden>
    <p class="sous">Les 60 derniers, le plus récent en haut, rangés par état
    (code couleur, comme sur chaque rapport). Déplie pour voir la capture et
    le journal de la partie.</p>
    {rapports}
  </section>

  <section class="panneau" data-panneau="joueurs" hidden>
    <p class="sous">Qui est là, et de quoi on se parle. Un message part tout de
    suite : la personne voit une pastille dans son jeu, et te répond de là.</p>
    {salon}
  </section>

  <section class="panneau" data-panneau="parties" hidden>
    <div id="suivi">
      <div id="erreur" class="erreur" hidden></div>
      <nav class="sous-onglets">
        <button type="button" class="sous-onglet" data-sous="parties-encours" role="tab">En cours</button>
        <button type="button" class="sous-onglet" data-sous="parties-historique" role="tab">Historique</button>
        <button type="button" class="sous-onglet" data-sous="parties-revoir" role="tab">À revoir</button>
        <button type="button" class="sous-onglet" data-sous="parties-play" role="tab">Play</button>
      </nav>
      <div class="sous-panneau" data-sous-panneau="parties-play" hidden>
        <p class="sous">Les parties lancées sur play (le jeu dans le navigateur, sans compte).
        Compteur anonyme : ni adresse, ni identifiant.</p>
        {stats_play}
      </div>
      <div class="sous-panneau" data-sous-panneau="parties-revoir" hidden>
        <p class="sous">Les 3 dernières parties TERMINÉES de chaque joueur (rangées chez l'hôte de la
        table). Télécharge le fichier, puis ouvre-le dans « Revoir » sur l'écran de préparation.</p>
        {parties_a_revoir}
      </div>
      <div class="sous-panneau" data-sous-panneau="parties-encours">
        <p class="sous">Qui joue en ce moment. Rafraîchi tout seul toutes les
        30 s <small id="maj" style="color:var(--muted)">chargement…</small>.</p>
        <div id="encours"><p class="vide">…</p></div>
      </div>
      <div class="sous-panneau" data-sous-panneau="parties-historique" hidden>
        <p class="sous">Les {suivi_max} dernières parties finies : héros, deck,
        aspect, méchant, rounds et résultat. Les abandons sont en orange. 20
        affichées d'abord, le reste sur demande. La même chose, à épingler sur
        le téléphone : <a href="/suivi">page de suivi</a>.</p>
        <div id="terminees"><p class="vide">…</p></div>
      </div>
    </div>
  </section>

  <section class="panneau" data-panneau="journal" hidden>
    <p class="sous">Allumage et extinction des 25 dernières tables.</p>
    <table>
      <tr><th>Table</th><th>Hôte</th><th>Ouverte le</th><th>Fermée le</th></tr>
      {parties}
    </table>
  </section>

  <section class="panneau" data-panneau="decks" hidden>
    {panneau_decks}
  </section>
</main>
{script_suivi}
{script_onglets}
{script_decks}
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
        return "à l'instant"
    if secondes < 5400:
        return "depuis %d min" % round(secondes / 60)
    if secondes < 172800:
        return "depuis %d h" % round(secondes / 3600)
    return "depuis %d j" % round(secondes / 86400)


def _il_y_a_horodatage(quand: float) -> str:
    ecart = max(0, time.time() - float(quand))
    if ecart < 90:
        return "à l'instant"
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
  /* REFONTE (25/09/2026) : palette bleu-gris GitHub-dark remplacee par les
     variables communes (voir le `:root` de PAGE_SUIVI). Les couleurs
     D'ASPECT (Aggression/Justice/Leadership/Protection/Pool/Determination)
     ne sont PAS touchees : elles codent le jeu, pas le theme du site. */
  #suivi h2 { font-size:.8rem; text-transform:uppercase; letter-spacing:.08em; color:var(--muted); margin:1.2rem 0 .5rem; }
  #suivi .carte { border:1px solid var(--border); border-radius:.7rem; padding:.7rem .85rem; margin-bottom:.55rem; background:var(--panel); }
  #suivi .carte.live { border-color:var(--ok); box-shadow: inset 3px 0 0 var(--ok); }
  #suivi .carte.abandon { box-shadow: inset 3px 0 0 var(--warn); }
  #suivi .carte.attente { border-color:var(--border); opacity:.75; }
  #suivi .ligne { display:flex; justify-content:space-between; gap:.6rem; align-items:baseline; }
  #suivi .qui { font-weight:600; }
  #suivi .quand { color:var(--muted); font-size:.8rem; white-space:nowrap; }
  #suivi .heros { font-size:1.05rem; margin:.15rem 0; }
  #suivi .heros .aspect { font-size:.75rem; padding:.05rem .4rem; border-radius:.3rem; margin-left:.3rem; vertical-align:middle; background:var(--border); }
  /* Le nom du deck : discret, il accompagne le heros sans lui voler la ligne. */
  #suivi .heros .deck { color:var(--muted); font-size:.78rem; margin-left:.4rem; }
  #suivi .aspect.Aggression { background:#8b1e1e; } #suivi .aspect.Justice { background:#8a6d00; color:#fff; }
  #suivi .aspect.Leadership { background:#1f4e8c; } #suivi .aspect.Protection { background:#1e6b3a; }
  #suivi .aspect.Pool { background:#6b1e8c; } #suivi .aspect.Determination { background:#5a2d8c; }
  #suivi .contre { color:var(--text); }
  #suivi .contre b { color:var(--text); }
  #suivi .bas { display:flex; gap:.9rem; flex-wrap:wrap; color:var(--muted); font-size:.85rem; margin-top:.25rem; }
  /* Les boutons « Regarder », un par siege. Discrets : la liste sert d'abord a
     LIRE ce qui se passe ; on ne clique que quand on veut voir de pres. */
  #suivi .regards { display:flex; gap:.4rem; flex-wrap:wrap; margin-left:auto; }
  #suivi a.regarder { color:var(--accent); text-decoration:none; border:1px solid var(--border);
                      border-radius:.4rem; padding:.1rem .5rem; font-size:.8rem; }
  #suivi a.regarder:hover { border-color:var(--accent); background:var(--accent-soft); }
  #suivi .res { font-weight:700; }
  #suivi .res.v { color:var(--ok); } #suivi .res.d { color:var(--danger); } #suivi .res.a { color:var(--warn); }
  #suivi .pv { font-variant-numeric: tabular-nums; }
  #suivi .vide { color:var(--muted); font-style:italic; }
  #suivi details.groupe { margin:.4rem 0; }
  #suivi details.groupe > summary { cursor:pointer; color:var(--text); font-size:.9rem; padding:.35rem 0; }
  #suivi .erreur { border:1px solid var(--danger); background:#1d1113; color:var(--danger); padding:.6rem .8rem; border-radius:.5rem; }
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

# Le pilote des onglets de /admin (23/09/2026). CHAINE PYTHON ORDINAIRE, PAS
# formatee par `.format()` : passee telle quelle a PAGE_ADMIN via
# `{script_onglets}`, exactement comme SUIVI_STYLE_BLOC/SUIVI_SCRIPT plus haut
# -- aucune accolade a doubler ici.
ADMIN_ONGLETS_SCRIPT = """<script>
(function () {
  var CLE = "admin-onglet";
  var onglets = Array.prototype.slice.call(document.querySelectorAll(".onglet"));
  var panneaux = Array.prototype.slice.call(document.querySelectorAll(".panneau"));

  function choisir(id, memoriser) {
    onglets.forEach(function (b) {
      b.setAttribute("aria-selected", b.dataset.onglet === id ? "true" : "false");
    });
    panneaux.forEach(function (p) { p.hidden = p.dataset.panneau !== id; });
    if (memoriser !== false) {
      try { localStorage.setItem(CLE, id); } catch (e) {}
    }
  }
  onglets.forEach(function (b) {
    b.addEventListener("click", function () { choisir(b.dataset.onglet); });
  });

  // Premiere visite (rien en memoire) : on ouvre l'onglet qui attend le plus
  // de monde, plutot que « Comptes » par defaut sans raison.
  var depart = null;
  try { depart = localStorage.getItem(CLE); } catch (e) {}
  if (!depart || !onglets.some(function (b) { return b.dataset.onglet === depart; })) {
    var meilleur = onglets[0], max = -1;
    onglets.forEach(function (b) {
      var n = parseInt(b.dataset.n || "0", 10);
      if (n > max) { max = n; meilleur = b; }
    });
    depart = meilleur.dataset.onglet;
  }
  choisir(depart, false);

  // Les sous-onglets : meme mecanique, un groupe independant par conteneur.
  Array.prototype.slice.call(document.querySelectorAll(".sous-onglets")).forEach(function (nav) {
    var boutons = Array.prototype.slice.call(nav.querySelectorAll(".sous-onglet"));
    var conteneur = nav.parentElement;
    function choisirSous(id) {
      boutons.forEach(function (b) {
        b.setAttribute("aria-selected", b.dataset.sous === id ? "true" : "false");
      });
      Array.prototype.slice.call(conteneur.querySelectorAll(".sous-panneau")).forEach(function (p) {
        p.hidden = p.dataset.sousPanneau !== id;
      });
    }
    boutons.forEach(function (b) {
      b.addEventListener("click", function () { choisirSous(b.dataset.sous); });
    });
  });

  // L'annonce : un bouton deplie le formulaire de creation (23/09/2026).
  var toggle = document.getElementById("annonce-toggle");
  var form = document.getElementById("annonce-form");
  if (toggle && form) {
    toggle.addEventListener("click", function () {
      form.hidden = !form.hidden;
      toggle.textContent = form.hidden ? toggle.dataset.ferme : toggle.dataset.ouvert;
    });
  }

  // L'historique des parties : 20 affichées d'abord, le reste sur demande
  // (23/09/2026). ⚠ ON NE TOUCHE PAS A SUIVI_SCRIPT (partage avec /suivi,
  // hors perimetre de cette refonte) : ce bloc observe seulement le DOM
  // qu'il produit dans #terminees, et le complete sans le modifier.
  //
  // ⚠⚠ BOUCLE INFINIE CORRIGEE (23/09/2026, page « ne repond pas » signalee
  // par l'utilisateur juste apres le deploiement). `terminees.appendChild`
  // EST une mutation "childList" sur le noeud observe : l'observateur se
  // redeclenchait donc lui-meme a chaque bouton pose, en boucle, sans jamais
  // s'arreter -- exactement le genre de piege documente pour tout
  // MutationObserver qui ecrit dans le noeud qu'il observe. Corrige en le
  // DECONNECTANT le temps de ses propres ecritures (`disconnect()` /
  // `observe()` autour du bloc), pour qu'il ne reagisse qu'aux VRAIS
  // rafraichissements de SUIVI_SCRIPT (qui remplace tout `#terminees` toutes
  // les 30 s), jamais a ses propres changements.
  var terminees = document.getElementById("terminees");
  if (terminees) {
    var LIMITE = 20, deploye = false;
    var observateur = new MutationObserver(function () { limiter(); });
    function limiter() {
      if (deploye) return;
      observateur.disconnect();
      var ancien = terminees.querySelector(".voir-plus");
      if (ancien) ancien.remove();
      var cartes = Array.prototype.slice.call(terminees.querySelectorAll(".carte"));
      if (cartes.length > LIMITE) {
        var caches = 0;
        cartes.forEach(function (c, i) { if (i >= LIMITE) { c.hidden = true; caches++; } });
        var bouton = document.createElement("button");
        bouton.type = "button";
        bouton.className = "voir-plus";
        bouton.textContent = "Voir " + caches + " de plus";
        bouton.addEventListener("click", function () {
          deploye = true;
          cartes.forEach(function (c) { c.hidden = false; });
          bouton.remove();
        });
        terminees.appendChild(bouton);
      }
      observateur.observe(terminees, {childList: true});
    }
    observateur.observe(terminees, {childList: true});
  }
})();
</script>"""

PAGE_SUIVI = """<!doctype html>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#07080c">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<link rel="manifest" href="/suivi.webmanifest">
<link rel="icon" href="/suivi-192.png">
<link rel="apple-touch-icon" href="/suivi-192.png">
<title>Suivi des parties</title>
<style>
  /* ===== REFONTE (25/09/2026), a la suite de celle du 23/09/2026 =============
     `/suivi` etait restee hors perimetre (page admin secondaire, deja
     presentable en cartes) et gardait donc l'ancienne palette bleu-gris
     (GitHub dark : #0e1116, liens #58a6ff...). Memes variables que PAGE /
     PAGE_FORMULAIRE / PAGE_ADMIN -- dupliquees ici, meme raison qu'elles :
     aucun mecanisme d'inclusion partagee dans ce depot. Pas de trame a
     points ni de degrade de fond : cette page est une liste dense a lire
     vite, pas un ecran d'accueil. */
  :root {
    color-scheme: dark;
    --bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;
    --text:#eef1f5; --muted:#8b95a3;
    --accent:#e62429; --accent-hover:#ff3b40; --accent-soft:rgba(230,36,41,.14); --accent-ink:#fff;
    --ok:#3fb950; --danger:#f85149; --warn:#e8a53d;
  }
  * { box-sizing: border-box; }
  body { margin:0; font:15px/1.4 system-ui,sans-serif; background:var(--bg); color:var(--text);
         padding: max(.8rem, env(safe-area-inset-top)) .8rem 2rem; }
  h1 { font-size:1.15rem; margin:.2rem 0 .8rem; display:flex; justify-content:space-between; align-items:baseline; }
  h1 small { color:var(--muted); font-weight:normal; font-size:.8rem; }
  .pied { color:var(--muted); font-size:.75rem; margin-top:1.5rem; text-align:center; }
  .pied a { color:var(--muted); }
  /* Telephone (zone 2 de la refonte du 09/10/2026) : liens de 44 px. */
  @media (max-width:767px) {
    .pied a { display:inline-flex; align-items:center; justify-content:center; min-height:44px; min-width:44px; }
  }
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
    "background_color": "#07080c",
    "theme_color": "#07080c",
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
  <h1>{titre}</h1>
  <p>{corps}</p>
  <button onclick="location.replace('/entrer')">{bouton}</button>
</main>
"""


def page_hors_ligne() -> bytes:
    """« Pas de connexion », dans la langue du visiteur.

    ⚠ C'ETAIT UNE CONSTANTE DEJA ENCODEE, donc figee en francais. Elle est
    servie par le serveur comme les autres : rien n'empeche de la traduire.
    """
    # ⚠ PAS DE `.format` ICI, ET C'EST MESURE : cette page porte sa feuille de
    # style, donc des accolades que `.format` prendrait pour des champs (la
    # route est tombee des le premier essai). On substitue nos trois champs a
    # la main, le CSS n'a rien a subir.
    return (PAGE_HORS_LIGNE
            .replace("{titre}", lang.t("Pas de connexion"))
            .replace("{corps}", lang.t(
                "NarwhalChampions a besoin du réseau pour tourner : la partie "
                "se joue sur le serveur, pas sur ton téléphone. Reconnecte-toi "
                "et réessaie."))
            .replace("{bouton}", lang.t("Réessayer"))
            ).encode("utf-8")

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
              # ⚠ PAS DE CLE `?h=` ICI. Cette en-tete est substituee dans les
              # gabarits AU DEMARRAGE : une tranche horaire calculee a cet
              # endroit resterait celle du lancement du serveur (meme piege que
              # les constantes de langue, 16/09). La fraicheur est donnee par
              # l'en-tete HTTP de la route, qui fait revalider l'icone.
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
def _bouton_appli() -> str:
    """Le bloc « Installer l'application », dans la langue du visiteur.

    ⚠ C'ETAIT UNE CONSTANTE, donc figee a la langue du chargement du module,
    c'est-a-dire au demarrage du serveur, quand aucun visiteur n'existe.
    """
    return (
    '<div id="appli-installer" hidden style="margin:1.2rem 0 0;padding:.8rem .9rem;'
    'border:1px solid var(--border);border-radius:.5rem;background:var(--panel-2);font-size:.9rem">'
    '<button id="appli-bouton" type="button" style="width:100%;font:inherit;font-weight:600;background:var(--accent);'
    'color:var(--accent-ink);border:0;border-radius:.5rem;padding:.7rem;cursor:pointer">'
    + lang.t("Installer l'application sur ce téléphone") + '</button>'
    '<p id="appli-ios" hidden style="margin:.4rem 0 0;color:var(--muted)">'
    + lang.t("Sur iPhone : bouton Partager, puis « Sur l'écran d'accueil ».") + '</p>'
    # ⚠ DIT AVANT L'INSTALLATION, pas apres. Une icone sur l'ecran d'accueil
    # laisse croire au hors ligne ; le jeu tourne sur le serveur, il n'y a
    # rien a jouer sans connexion.
    '<p style="margin:.5rem 0 0;color:var(--muted);font-size:.85rem">'
    + lang.t("C'est un raccourci vers le jeu, pas une version hors ligne : "
             "il faut une connexion pour jouer.") + '</p>'
    '</div>'
    '<script>(function(){'
    'var bloc=document.getElementById("appli-installer"),bouton=document.getElementById("appli-bouton"),'
    'ios=document.getElementById("appli-ios"),retenu=null;'
    'if(window.matchMedia("(display-mode: standalone)").matches||navigator.standalone===true)return;'
    # ⚠⚠ CORRECTIF (23/09/2026, signale par l'utilisateur : « ca s'affiche
    # aussi sur ordi, ca va pas ca »). Le texte dit « sur ce telephone » --
    # Chrome/Edge de BUREAU proposent pourtant `beforeinstallprompt` eux
    # aussi (ils savent installer une PWA sur le bureau). `pointer: coarse`
    # est vrai sur un ecran tactile, faux avec une souris : c'est le signal
    # le plus fiable pour « vrai telephone/tablette », plus robuste qu'un
    # `navigator.userAgent` a maintenir a la main.
    'if(!window.matchMedia("(pointer: coarse)").matches)return;'
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
# ⚠ LA TETE EST SUBSTITUEE UNE FOIS, LE BOUTON A CHAQUE RENDU (16/09/2026).
# La tete ne porte aucun texte : elle peut rester figee. Le bouton, lui, parle
# au visiteur, et une constante serait figee a la langue du DEMARRAGE DU
# SERVEUR, quand aucun visiteur n'existe. `{bouton_appli}` reste donc un champ
# que chaque `.format` remplit avec `_bouton_appli()`.
PAGE = PAGE.replace("{tete_appli}", _TETE_POUR_FORMAT)
PAGE_FORMULAIRE = PAGE_FORMULAIRE.replace("{tete_appli}", _TETE_POUR_FORMAT)

# LES COULEURS DES PAGES DE FORMULAIRE (20/10/2026, decision de l'utilisateur :
# « passer ces pages en Epure »). EPURE_FORMULAIRE = True : les jetons de
# `Fusion/marvel-lcg-src/public/css/affichage-epure-pages.css` (fond #111318,
# surface #1c2028, champ #292e38, filet #383e49, accent bleu Captain #3f86e0,
# titres Bangers). False : l'ancien habillage rouge du site, conserve tel quel.
# ⚠ Une seule bascule pour TOUT le gabarit (connexion, inscription,
# reinitialisation, confirmations, page des createurs), pour qu'elles restent
# coherentes entre elles. Le mode sobre (SOBRE_SITE) redefinit ces variables
# par-dessus, dans les deux cas.
EPURE_FORMULAIRE = True
_JETONS_FORMULAIRE_ROUGE = """:root {{
    color-scheme: dark;
    --bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;
    --text:#eef1f5; --muted:#8b95a3;
    --accent:#e62429; --accent-hover:#ff3b40; --accent-soft:rgba(230,36,41,.14); --accent-ink:#fff;
    --danger:#f85149;
    --affiche: "Anton", "Arial Narrow", sans-serif;
  }}"""
_JETONS_FORMULAIRE_EPURE = """:root {{
    color-scheme: dark;
    --bg:#111318; --panel:#1c2028; --panel-2:#292e38; --border:#383e49;
    --text:#f2f3f5; --muted:#9da5b3;
    --accent:#3f86e0; --accent-hover:#5a9bf0; --accent-soft:rgba(63,134,224,.16); --accent-ink:#fff;
    --danger:#f85149;
    --affiche: "Bangers", "Anton", Impact, "Arial Black", sans-serif;
  }}"""
PAGE_FORMULAIRE = PAGE_FORMULAIRE.replace(
    "/*JETONS*/", _JETONS_FORMULAIRE_EPURE if EPURE_FORMULAIRE else _JETONS_FORMULAIRE_ROUGE)
if EPURE_FORMULAIRE:
    PAGE_FORMULAIRE = PAGE_FORMULAIRE.replace("family=Anton&display", "family=Bangers&display")

# L'ADMINISTRATION, LE SUIVI ET LA PAGE DU SITE AU MEME HABILLAGE (24/10/2026, remarque de l'utilisateur : « les pages d'admin
# ne sont pas aux bonnes couleurs, meme sur PC, ca ne va pas avec le reste du style du site »). Ces trois gabarits gardaient
# l'ancien rouge alors que les formulaires sont passes a l'Epure : meme bascule (`EPURE_FORMULAIRE`), memes valeurs.
_ROUGE_VERS_EPURE = (
    ("--bg:#07080c; --panel:#12151b; --panel-2:#181d26; --border:#262b35;", "--bg:#111318; --panel:#1c2028; --panel-2:#292e38; --border:#383e49;"),
    ("--text:#eef1f5; --muted:#8b95a3;", "--text:#f2f3f5; --muted:#9da5b3;"),
    ("--accent:#e62429; --accent-hover:#ff3b40; --accent-soft:rgba(230,36,41,.14);", "--accent:#3f86e0; --accent-hover:#5a9bf0; --accent-soft:rgba(63,134,224,.16);"),
    ("--accent:#e62429; --accent-hover:#ff3b40;", "--accent:#3f86e0; --accent-hover:#5a9bf0;"),
    ("rgba(230,36,41,.4)", "rgba(63,134,224,.4)"),
    ('--affiche: "Anton", "Arial Narrow", sans-serif;', '--affiche: "Bangers", "Anton", Impact, "Arial Black", sans-serif;'),
    ("family=Anton&display", "family=Bangers&display"),
)


def _en_epure(gabarit: str) -> str:
    for ancien, nouveau in _ROUGE_VERS_EPURE:
        gabarit = gabarit.replace(ancien, nouveau)
    return gabarit


if EPURE_FORMULAIRE:
    PAGE = _en_epure(PAGE)
    PAGE_ADMIN = _en_epure(PAGE_ADMIN)
    PAGE_SUIVI = _en_epure(PAGE_SUIVI)

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


def _textes_decks_joueurs() -> dict:
    return {
        "aucun": lang.t("Aucun deck enregistré par les autres comptes."),
        "cartes": lang.t("cartes"),
        "importer": lang.t("Importer dans mon compte"),
        "confirmer": lang.t("Importer le deck « {deck} » de {compte} dans votre compte ? L'original ne sera pas modifié."),
        "reussi": lang.t("Deck importé dans votre compte sous le nom « {fichier} »."),
        "echec_import": lang.t("L'import a échoué."),
        "echec_liste": lang.t("La liste des decks n'a pas pu être chargée."),
    }


def _panneau_decks_joueurs() -> str:
    return (
        '<p class="sous">%s</p>'
        '<p><button type="button" class="dj-actualiser">%s</button></p>'
        '<div class="dj-message" role="status" aria-live="polite"></div>'
        '<div class="dj-liste"><p class="vide">…</p></div>'
        % (html.escape(lang.t("Les decks enregistrés par les autres comptes, en lecture seule. Chaque consultation et chaque import est journalisé.")),
           html.escape(lang.t("Actualiser"))))


def _script_decks_joueurs() -> str:
    """Le script de l'onglet. Le panneau ne charge la liste qu'a l'ouverture de
    l'onglet : chaque chargement est une consultation journalisee."""
    with open(os.path.join(RACINE_SITE, "static", "admin-decks-joueurs.js"), encoding="utf-8") as f:
        code = f.read().replace("</", "<\\/")
    textes = json.dumps(_textes_decks_joueurs(), ensure_ascii=False).replace("</", "<\\/")
    demarrage = (
        "(function(){"
        "var z=document.querySelector('[data-panneau=\"decks\"]');"
        "var b=document.querySelector('.onglet[data-onglet=\"decks\"]');var f=false;"
        "function go(){if(f||!z||!window.DecksJoueursAdmin)return;f=true;"
        "window.DecksJoueursAdmin.monter(z," + textes + ");}"
        "if(b){b.addEventListener('click',go);"
        "if(b.getAttribute('aria-selected')==='true')go();}})();")
    return "<script>" + code + "\n" + demarrage + "</script>"


# La page des demandes des createurs (12/10/2026) : le gabarit commun des
# formulaires, dont le `<form>` (qui impose un champ mot de passe) est remplace
# par un champ libre. ⚠ LEVE si le bloc n'est pas trouve : un `sub` muet
# laisserait le champ mot de passe sur un formulaire public.
PAGE_CONTACT_CREATEURS, _n_form = re.subn(
    r'<form method="post" action="\{action\}">.*?</form>', "{formulaire}",
    PAGE_FORMULAIRE, count=1, flags=re.S)
if _n_form != 1:
    raise RuntimeError("PAGE_FORMULAIRE n'a plus de <form> : la page des createurs ne peut pas s'en servir")


def _icone_appli(nom: str) -> bytes | None:
    # ⚠ DEUX FAMILLES D'IMAGES, ET ELLES NE SUIVENT PAS LA MEME REGLE.
    #
    # `favicon.png` et `narwhal.png` sont la MASCOTTE : elles changent toutes
    # les trois heures (narval.py), dans l'onglet comme sur les pages.
    #
    # `app-192.png` et `app-512.png` sont les icones de l'APPLI installee : on
    # n'y touche pas. Elles gardent leur fond opaque, qu'un ecran d'accueil de
    # telephone attend, et une icone qui changerait toute seule sur le bureau
    # de quelqu'un n'est pas une bonne surprise.
    if nom in ("favicon.png", "narwhal.png"):
        nom = narval_du_moment.fichier()
    elif nom not in ("app-192.png", "app-512.png"):
        return None
    try:
        with open(os.path.join(RACINE_SITE, "static", nom), "rb") as f:
            return f.read()
    except OSError:
        # Une mascotte absente ne doit pas rendre le site sans icone : on
        # retombe sur la premiere de la liste.
        try:
            secours = "narwhal-%s.png" % narval_du_moment.NARVALS[0]
            with open(os.path.join(RACINE_SITE, "static", secours), "rb") as f:
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


# ⚠ PORTRAIT DU VILAIN sur /entrer (23/09/2026, demande de l'utilisateur :
# rendre la carte « Ta partie t'attend » plus concrete). Le site et le
# moteur de jeu sont deux serveurs SEPARES (narwhalchampions.com vs
# p<N>.narwhalchampions.com) : le site n'a jamais eu de vignettes de cartes,
# il faut donc les lui donner. Convention volontairement simple pour ne PAS
# construire un annuaire nom -> card_id tout de suite : un fichier
# `static/vilains/<slug>.jpg` (slug = nom en minuscules, non-alphanumerique
# -> "_") sert de portrait pour ce vilain. Absent -> pas de portrait, la
# carte reste sans image plutot que de planter ou d'afficher un repli laid.
# `_slug_vilain` est reutilisee par la route ET par page_reprise() : les deux
# DOIVENT produire le meme nom de fichier pour un meme nom de vilain.
def _slug_vilain(nom: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (nom or "").strip().lower()).strip("_")


def _portrait_vilain(slug: str) -> bytes | None:
    # `_slug_vilain` ne produit jamais de "/" ni de "..", mais on protege
    # quand meme l'entree venant de l'URL (`self.chemin`), qui elle n'est PAS
    # passee par cette fonction.
    if not re.fullmatch(r"[a-z0-9_]{1,40}", slug or ""):
        return None
    try:
        with open(os.path.join(RACINE_SITE, "static", "vilains", "%s.jpg" % slug), "rb") as f:
            return f.read()
    except OSError:
        return None


# --- Puzzles publies (E7, docs/puzzle/PLAN.md) : la logique est dans puzzles_publies.py et api_puzzles.py.
_PUZZLES_PUBLIES = []


def puzzles_publies():
    """Le serveur de puzzles, cree au premier appel (il charge le catalogue des cartes)."""
    if not _PUZZLES_PUBLIES:
        import puzzles_publies as _pp
        _PUZZLES_PUBLIES.append(_pp.PuzzlesPublies(BASE))
    return _PUZZLES_PUBLIES[0]


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

    def _repondre(self, code: int, corps: bytes, type_mime="text/html; charset=utf-8",
                  entetes: list[tuple[str, str]] | None = None):
        if type_mime.startswith("text/html") and b'<meta charset="utf-8">' in corps:
            corps = corps.replace(b'<meta charset="utf-8">', b'<meta charset="utf-8">' + SOBRE_SITE, 1)
        self.send_response(code)
        self.send_header("Content-Type", type_mime)
        self.send_header("Content-Length", str(len(corps)))
        for nom, valeur in (entetes or []):
            self.send_header(nom, valeur)
        self.end_headers()
        self.wfile.write(corps)

    def _rediriger(self, vers="/", entetes: list[tuple[str, str]] | None = None):
        """303 vers VERS, avec ENTETES (des `Set-Cookie`, en general).

        ⚠ DANS DISCORD, JAMAIS DE VRAIE REDIRECTION. Le proxy de Discord
        (`<id>.discordsays.com`) SUIT lui-meme les 3xx et rend la page finale
        en 200 : les `Set-Cookie` de la reponse de redirection sont perdus, et
        l'adresse du cadre ne change pas. Mesure au `curl` le 29/09/2026 :
        l'hote se connectait, puis tombait sur « Introuvable » faute de
        `nc_table`. On rend donc une page 200 qui porte les cookies et enchaine
        d'elle-meme (`meta refresh`, qui passe la CSP du proxy).
        """
        if self._cadre_discord():
            self._repondre(200, page_enchainer(vers), entetes=entetes)
            return
        self.send_response(303)
        self.send_header("Location", vers)
        for nom, valeur in (entetes or []):
            self.send_header(nom, valeur)
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _entrer_dans_partie(self, pseudo: str, proposer_reprise: bool = True,
                             joueurs: int = 1,
                             entetes_supplementaires: list[tuple[str, str]] | None = None
                             ) -> None:
        """Demarre/rejoint le moteur de PSEUDO, et repond en consequence.

        Coeur de `/entrer`, extrait pour etre reutilise par l'hote d'une
        activite Discord (`_activite_discord`) : une fois identifie, il suit
        EXACTEMENT le meme chemin que quelqu'un qui clique sur « Entrer »
        depuis le site. `proposer_reprise=False` saute la question « reprendre
        ta derniere partie ? » -- l'activite Discord n'a pas de bandeau pour la
        poser, elle entre directement (comme `/reprendre` le fait deja).

        `joueurs` : voir `lancer_jeu`. Applique aussi a une table DEJA
        allumee (jamais retreci) : l'hote peut ouvrir l'activite Discord sur
        une table qu'il avait deja lancee seul depuis le site.

        `entetes_supplementaires` : pour poser le cookie de session dans LA
        MEME reponse que celle qui entre dans la partie (POST /connexion,
        flux Discord). Le detour normal, une redirection puis une nouvelle
        requete qui relit le cookie, echoue dans le cadre Discord (le
        navigateur ne renvoie pas fiablement un cookie pose depuis ce
        contexte -- constate en prod le 29/09/2026).
        """
        toucher_presence(pseudo)
        partie = jeu_de(pseudo)
        # ⚠ LA QUESTION NE SE POSE QUE TABLE ETEINTE. Une partie interrompue
        # n'existe que parce que la table a ete tuee ; si le moteur tourne
        # deja, il n'y a rien a reprendre et rien a demander.
        if proposer_reprise and (partie is None or not partie.vivant()):
            attendue = partie_interrompue(pseudo)
            if attendue:
                self._repondre(200, page_reprise(pseudo, attendue),
                                entetes=entetes_supplementaires)
                return
        if partie is not None and partie.vivant() and _moteur_repond(partie.port):
            partie.joueurs = max(partie.joueurs, joueurs)
            # Redirection vers un AUTRE hote (p<N>.domaine) : c'est voulu, le
            # client du jeu utilise des chemins absolus et ne supporte pas
            # d'etre servi sous un prefixe (voir l'en-tete du fichier).
            entetes = list(entetes_supplementaires or [])
            if self._cadre_discord():
                entetes += self._cookie_table(partie)
            self._rediriger(self._lien_dans_cadre(partie.lien_hote()), entetes)
            return
        demarrer_en_fond(pseudo, joueurs)
        self._repondre(200, page_attente(pseudo), entetes=entetes_supplementaires)

    def _activite_discord(self, pseudo: str | None) -> None:
        """`/activite_discord?instance_id=...` : point d'entree du salon vocal.

        Voir `role_activite_discord` pour la decision. Ici, seulement la mise
        en forme HTTP de chacun de ses trois cas.
        """
        instance_id = (self.parametres.get("instance_id") or [""])[0]
        if not instance_id:
            self._repondre(400, b"instance_id manquant.", "text/plain; charset=utf-8")
            return
        role, hote = role_activite_discord(instance_id, pseudo)
        if role == "connexion_requise":
            # Retenu le temps de la connexion (courte duree, un seul aller-
            # retour) : `/connexion` (POST) le relit pour revenir ICI au lieu
            # de `/entrer`, sans quoi l'hote se retrouverait sur l'ecran du
            # SITE au lieu de celui de SON activite Discord.
            #
            # ⚠ `da` EN QUERY, PAS SEULEMENT LE COOKIE. Constate en prod le
            # 29/09/2026 : le cadre Discord ne renvoie pas fiablement le
            # cookie pose ici jusqu'au POST /connexion qui suit. Le cookie
            # reste pose en secours (navigateur normal, hors Discord), mais
            # `/connexion` place aussi `da` dans un champ cache du formulaire,
            # qui lui survit toujours au POST.
            self._rediriger(
                "/connexion?da=" + urllib.parse.quote(instance_id),
                [("Set-Cookie",
                  f"nc_discord_attente={urllib.parse.quote(instance_id)}; HttpOnly;"
                  f" Path=/; Max-Age=600" + self._attributs_cookie())])
            return
        if role == "hote":
            # 4 sieges d'emblee : le salon vocal peut compter jusqu'a 4
            # personnes, et `.liens()` (vu par les participants juste en
            # dessous) n'expose que les sieges couverts par `joueurs`.
            self._entrer_dans_partie(hote, proposer_reprise=False, joueurs=4)
            return
        # role == "participant" : rejoint la table de HOTE. Connecte -> assis
        # directement ; anonyme -> "j'ai un compte" ou "je suis invite",
        # jamais d'inscription (recapitulatif valide avec l'utilisateur).
        self._repondre_participant(hote or "", instance_id, identite=pseudo)

    def _repondre_participant(self, hote: str, instance_id: str,
                              entetes: list[tuple[str, str]] | None = None,
                              identite: str | None = None) -> None:
        """Assoit un participant a la table de HOTE, ou lui demande qui il est.

        `identite` : son pseudo s'il est connecte. Sinon, un invite qui a
        clique « Je suis invite » (`?invite=1`) recoit un jeton anonyme en
        cookie (`nc_discord_invite`), pour retrouver LE MEME siege s'il
        revient. Sans l'un ni l'autre : l'ecran a deux boutons.

        Le lien de siege et le cookie `nc_table` sont adaptes au cadre Discord
        (voir `_lien_dans_cadre`).
        """
        partie = jeu_de(hote) if hote else None
        entetes = list(entetes or [])
        if partie is None or not partie.vivant():
            self._repondre(200, page_activite_discord_participant(hote, instance_id, prete=False),
                           entetes=entetes)
            return
        if identite is None and (self.parametres.get("invite") or [""])[0]:
            identite = self._cookie("nc_discord_invite")
            if not identite:
                identite = "invite:" + secrets.token_urlsafe(12)
                entetes.append(("Set-Cookie", "nc_discord_invite=%s; HttpOnly; Path=/; Max-Age=86400%s"
                                % (identite, self._attributs_cookie())))
        if identite is None:
            self._repondre(200, page_activite_discord_participant(hote, instance_id, prete=True),
                           entetes=entetes)
            return
        siege = siege_activite_discord(
            instance_id, identite, [l for l in partie.liens() if l["siege"] != 0])
        if siege is None:
            self._repondre(200, page_activite_discord_complete(hote), entetes=entetes)
            return
        if self._cadre_discord():
            entetes += self._cookie_table(partie)
        self._rediriger(self._lien_dans_cadre(siege["url"]), entetes)

    def _cookie(self, nom: str) -> str | None:
        """La valeur d'UN cookie nomme, ou None. Pendant de `_session`, pour
        les cookies qui ne portent pas une session (ex. `nc_discord_attente`)."""
        brut = self.headers.get("Cookie") or ""
        for morceau in brut.split(";"):
            cle, _, valeur = morceau.strip().partition("=")
            if cle == nom:
                return urllib.parse.unquote(valeur)
        return None

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

    def _cadre_discord(self) -> bool:
        """Vrai si la requete vient de l'activite Discord.

        Le « Root Mapping » Discord vise `discord.<domaine>`, et Caddy n'y
        envoie que ce cas. Voir `docs/reference/DISCORD.md`.
        """
        return (self.headers.get("Host") or "").split(":")[0].startswith("discord.")

    def _attributs_cookie(self, domaine_parent: bool = False) -> str:
        """La queue d'un `Set-Cookie` (apres `Path=/...`).

        ⚠ DANS DISCORD, `Lax` ET `Domain=` SONT TOUS DEUX REFUSES. La page y
        vit dans un iframe tiers servi depuis `<id>.discordsays.com` : le
        navigateur n'envoie jamais un cookie `Lax` dans ce cadre, et rejette
        un `Domain=.<domaine>` qui ne correspond pas a l'hote qu'il voit.
        Discord exige `SameSite=None; Partitioned`, sans domaine (doc
        « Networking » des activites). C'est ce qui renvoyait l'hote sur le
        formulaire de connexion a chaque etape (29/09/2026).
        """
        if self._cadre_discord():
            return "; SameSite=None; Secure; Partitioned"
        domaine = ("; Domain=.%s" % DOMAINE) if (domaine_parent and DOMAINE) else ""
        return "; SameSite=Lax" + domaine + self._secure()

    def _cookie_table(self, partie) -> list[tuple[str, str]]:
        """Le cookie qui dit a Caddy vers QUELLE table envoyer ce navigateur.

        Sur `discord.<domaine>`, un seul hote porte toutes les tables (Discord
        ne sait charger qu'une origine). Caddy lit `nc_table` et aiguille vers
        le port de la table ; sans lui, tout va a l'orchestrateur.
        """
        return [("Set-Cookie", "nc_table=%d; HttpOnly; Path=/; Max-Age=%d%s"
                 % (partie.emplacement, DUREE_SESSION_JOURS * 86400,
                    self._attributs_cookie()))]

    def _lien_dans_cadre(self, url: str) -> str:
        """En mode Discord, `https://pN.<domaine>/x?y` devient `/x?y` : la
        table est servie sur l'hote courant, via le cookie `nc_table`."""
        if not self._cadre_discord():
            return url
        morceaux = urllib.parse.urlsplit(url)
        return morceaux.path + ("?" + morceaux.query if morceaux.query else "")

    def _formulaire(
        self, quoi: str, erreur: str = "", jeton: str = "", instance_discord: str = ""
    ) -> bytes:
        inscription = quoi == "inscription"
        champs = ('<input type="hidden" name="i" value="%s">'
                  '<label>%s<input name="pseudo" autocomplete="username" required></label>'
                  '<label>%s<input name="email" type="email" '
                  'autocomplete="email" required></label>'
                  % (html.escape(jeton), lang.t("Pseudo"),
                     lang.t("Adresse e-mail"))) if inscription else (
                  '<label>%s<input name="pseudo" '
                  'autocomplete="username" required></label>'
                  % lang.t("Pseudo ou adresse e-mail"))
        # ⚠ SURVIT AU POST LA OU LE COOKIE NE SURVIT PAS TOUJOURS. Le cadre
        # Discord (iframe + proxy `.proxy/`) ne renvoie pas toujours le cookie
        # `nc_discord_attente` pose par la redirection precedente -- constate
        # en prod le 29/09/2026 (POST /connexion reussi, mais le cookie relu
        # etait vide, et la personne retombait sur `/entrer` au lieu de sa
        # table Discord). Un champ cache voyage dans le CORPS du POST, jamais
        # sujet aux regles de cookies cross-site.
        if instance_discord:
            champs += '<input type="hidden" name="da" value="%s">' % html.escape(instance_discord)
        return PAGE_FORMULAIRE.format(
                langue=_bouton_langue(),
            titre=lang.t("Créer un compte") if inscription else lang.t("Se connecter"),
            action="/inscription" if inscription else "/connexion",
            bouton=lang.t("Demander un compte") if inscription else lang.t("Entrer"),
            auto="new-password" if inscription else "current-password",
            mdp=lang.t("Mot de passe"),
            champs=champs,
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            bouton_appli=_bouton_appli(), mention=_mention_complete(),
            pied=_lignes_pied(*((lang.t("Tu es invité : ton compte sera actif tout de suite.")
                   if invitation_valide(jeton) else
                   lang.t("Ton compte devra être validé à la main avant de servir."),
                  lang.t('Déjà un compte ? <a href="/connexion">Se connecter</a>.'))
                  if inscription else
                  (lang.t('Pas encore de compte ? <a href="/inscription">En demander un</a>.'),
                  lang.t("Mot de passe oublié ? Demande un lien de réinitialisation à l'administrateur."),
                  # ⚠ LA REGLE EST ANNONCEE, PAS SUBIE. Le site ne sait pas
                  # envoyer de courriel : personne ne peut etre prevenu de son
                  # expiration. La seule facon honnete de la faire accepter est
                  # de l'ecrire la ou tout le monde passe.
                  lang.t("Les places sont comptées : {jours} jours sans venir et la tienne"
                         " retourne au pot. Écris-moi, je te la rends.").replace(
                      "{jours}", str(EXPIRATION_JOURS))))),
        ).encode("utf-8")

    def _page_contact_createurs(self, erreur: str = "", valeurs: dict | None = None,
                                envoye: bool = False) -> bytes:
        """Le formulaire public des createurs, ou sa confirmation (`envoye`).

        TOUT ce que le visiteur a tape et qu'on lui remontre (en cas d'erreur)
        passe par html.escape."""
        v = {k: html.escape(str((valeurs or {}).get(k, ""))) for k in ("nom", "contact", "genre", "message")}
        if envoye:
            formulaire = ('<p style="margin:0;color:var(--text)">%s</p>'
                          % lang.t("Merci, ta demande est bien arrivée. Je te réponds dès que possible."))
        else:
            options = "".join(
                '<option value="%s"%s>%s</option>' % (g, " selected" if v["genre"] == g else "", libelle)
                for g, libelle in (("crediter", lang.t("Me créditer")),
                                   ("retirer", lang.t("Retirer mes créations"))))
            formulaire = (
                '<style>select,textarea{{width:100%;box-sizing:border-box;font:inherit;margin-top:.35rem;'
                'background:var(--panel-2);color:inherit;border:1px solid var(--border);'
                'border-radius:.5rem;padding:.65rem .9rem}}textarea{{min-height:8rem;resize:vertical}}'
                '.pot{{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}}</style>'
                .replace("{{", "{").replace("}}", "}")
                + '<form method="post" action="/contact-createurs">'
                '<div class="pot" aria-hidden="true"><label>Site web<input name="site_web" '
                'tabindex="-1" autocomplete="off"></label></div>'
                '<label>%s<input name="nom" maxlength="80" required value="%s"></label>'
                '<label>%s<input name="contact" maxlength="160" required value="%s"></label>'
                '<label>%s<select name="genre" required>%s</select></label>'
                '<label>%s<textarea name="message" maxlength="4000" required>%s</textarea></label>'
                '<button type="submit">%s</button></form>'
                % (lang.t("Ton nom ou pseudo"), v["nom"],
                   lang.t("Comment te recontacter (e-mail ou Discord)"), v["contact"],
                   lang.t("Ta demande"), options,
                   lang.t("Ton message : ce que tu as créé, et où ça apparaît sur le site"), v["message"],
                   lang.t("Envoyer")))
        return PAGE_CONTACT_CREATEURS.format(
            langue=_bouton_langue(),
            titre=lang.t("Crédits et retrait"),
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            formulaire=formulaire,
            pied=lang.t("Si j'ai oublié de te créditer, ou si tu veux que tes créations soient"
                        " retirées du site, dis-le-moi ici. Je lis chaque demande."),
            mention=_mention_complete(), bouton_appli=_bouton_appli(),
        ).encode("utf-8")

    def _formulaire_reinitialisation(self, jeton: str, erreur: str = "") -> bytes:
        """Le formulaire du nouveau mot de passe, sur le gabarit commun."""
        return PAGE_FORMULAIRE.format(
                langue=_bouton_langue(),
            titre=lang.t("Nouveau mot de passe"),
            action="/reinitialisation", bouton=lang.t("Enregistrer"), auto="new-password",
            mdp=lang.t("Mot de passe"),
            champs='<input type="hidden" name="r" value="%s">' % html.escape(jeton),
            erreur='<div class="erreur">%s</div>' % html.escape(erreur) if erreur else "",
            bouton_appli=_bouton_appli(), mention=_mention_complete(),
            pied=_lignes_pied(lang.t("Huit caractères au minimum. Tes sessions ouvertes seront fermées."),
                              lang.t('<a href="/connexion">Se connecter</a>.')),
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

    @staticmethod
    def _parties_a_revoir() -> str:
        blocs = []
        for pseudo, parties in parties_des_joueurs().items():
            liens = "".join(
                '<li><a href="/admin/partie-joueur?j=%s&amp;n=%d">%s</a></li>'
                % (urllib.parse.quote(pseudo), rang, html.escape(nom))
                for rang, nom in enumerate(parties))
            blocs.append("<h3>%s</h3><ul>%s</ul>" % (html.escape(pseudo), liens))
        return "".join(blocs) or '<p class="vide">Aucune partie terminee rangee pour le moment.</p>'

    def _servir_partie_joueur(self) -> None:
        # Le joueur et le fichier sont pris DANS LA LISTE, jamais dans l'adresse.
        requete = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        demande = requete.get("j", [""])[0]
        try:
            rang = int(requete.get("n", ["-1"])[0])
        except ValueError:
            rang = -1
        parties = parties_des_joueurs()
        pseudo = next((p for p in parties if p == demande), None)
        if pseudo is None or not 0 <= rang < len(parties[pseudo]):
            self._repondre(404, b"Aucune partie.", "text/plain; charset=utf-8")
            return
        nom = parties[pseudo][rang]
        try:
            with open(os.path.join(DOSSIER_PARTIES_JOUEURS, pseudo, nom), "rb") as f:
                contenu = f.read()
        except OSError:
            self._repondre(404, b"Partie introuvable.", "text/plain; charset=utf-8")
            return
        self._repondre(200, contenu, "application/octet-stream",
                       [("Content-Disposition", 'attachment; filename="%s-%s"' % (pseudo, nom))])

    def _page_sauvegardes(self) -> bytes:
        lignes = []
        for rang, nom in enumerate(sauvegardes_du_code()):
            try:
                taille = os.path.getsize(os.path.join(DOSSIER_SAUVEGARDES_CODE, nom)) / 1e6
            except OSError:
                continue
            lignes.append('<li><a href="/admin/sauvegarde-code?n=%d">%s</a> (%.0f Mo)%s</li>'
                          % (rang, html.escape(nom), taille, " &larr; la plus récente" if rang == 0 else ""))
        corps = "".join(lignes) or "<li>Aucune sauvegarde pour l'instant : elle se crée au prochain déploiement.</li>"
        return ("<!doctype html><meta charset=utf-8>"
                "<meta name=viewport content='width=device-width,initial-scale=1'>"
                "<title>Sauvegardes du code</title>"
                "<body style='font-family:system-ui;background:#111318;color:#f2f3f5;padding:clamp(1rem,4vw,2rem);"
                "overflow-wrap:anywhere'>"
                "<p><a href='/admin'>&larr; Administration</a></p>"
                "<h1>Sauvegardes du code</h1>"
                "<p>Tout le projet sans les images, historique compris. Un zip par déploiement, les 5 derniers. "
                "La notice de restauration est dans le zip (LISEZ-MOI.txt).</p>"
                "<ul style='line-height:2'>%s</ul>"
                "<h2>Images</h2>"
                "<p><a href='/admin/images'>Toutes les images (scans, vignettes, HD, sons, documents), environ 2,5 Go</a>"
                " : un fichier .tar fabriqué à l'instant depuis le serveur. Après une restauration, l'extraire dans "
                "<code>Fusion/marvel-lcg-src/</code> (il contient le dossier <code>assets/</code>).</p>"
                "<style>a{color:#5a9bf0}</style></body>" % corps).encode("utf-8")

    def _servir_images(self) -> None:
        import tarfile
        if not os.path.isdir(DOSSIER_ASSETS):
            self._repondre(404, b"Dossier des images introuvable.", "text/plain; charset=utf-8")
            return
        self.send_response(200)
        self.send_header("Content-Type", "application/x-tar")
        self.send_header("Content-Disposition",
                         'attachment; filename="images-%s.tar"' % time.strftime("%Y%m%d"))
        self.send_header("Connection", "close")
        self.end_headers()
        try:
            with tarfile.open(fileobj=self.wfile, mode="w|") as archive:
                archive.add(DOSSIER_ASSETS, arcname="assets")
        except (BrokenPipeError, ConnectionResetError):
            pass  # telechargement interrompu par le navigateur
        self.close_connection = True

    def _servir_sauvegarde(self) -> None:
        requete = urllib.parse.urlparse(self.path).query
        try:
            rang = int(urllib.parse.parse_qs(requete).get("n", ["0"])[0])
        except ValueError:
            rang = -1
        noms = sauvegardes_du_code()
        if not 0 <= rang < len(noms):
            self._repondre(404, b"Aucune sauvegarde.", "text/plain; charset=utf-8")
            return
        chemin = os.path.join(DOSSIER_SAUVEGARDES_CODE, noms[rang])
        try:
            taille = os.path.getsize(chemin)
            fichier = open(chemin, "rb")
        except OSError:
            self._repondre(404, b"Sauvegarde introuvable.", "text/plain; charset=utf-8")
            return
        with fichier:
            self.send_response(200)
            self.send_header("Content-Type", "application/zip")
            self.send_header("Content-Length", str(taille))
            self.send_header("Content-Disposition", 'attachment; filename="%s"' % noms[rang])
            self.end_headers()
            while True:
                morceau = fichier.read(1 << 20)
                if not morceau:
                    break
                self.wfile.write(morceau)

    def _page_admin(self) -> bytes:
        # ⚠⚠ COMPTES EN FICHES, PAS EN TABLEAU (23/09/2026, demande de
        # l'utilisateur : « c'est pas du tout user-friendly »). Un <table>
        # de 6 colonnes serrait pseudo/adresse/dates/statut/actions sur une
        # seule ligne minuscule, illisible sur telephone (le seul endroit ou
        # un tableau HTML ne peut pas defiler horizontalement sans y penser).
        # Chaque compte est maintenant une fiche : initiale en pastille,
        # pseudo + statut sur une ligne, le reste en meta juste dessous.
        # Les actions sont des ICONES DISCRETES (23/09/2026, demande de
        # l'utilisateur) : invisibles au repos (`.compte-actions`, voir CSS),
        # revelees au survol/tap -- Invitations et Mots de passe reprennent la
        # meme fiche et les memes icones, pour la coherence.
        ICONE_CHECK = 'M9 16.17 4.83 12l-1.42 1.41L9 19l12-12-1.41-1.42z'
        ICONE_CROIX = ('M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59'
                       ' 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z')
        ICONE_ESSAI = ('M7 2v2h1v6.17L3.29 18.5A2 2 0 0 0 5 21.5h14a2 2 0 0 0 1.71-3'
                       'L16 10.17V4h1V2H7zm3 2h4v6.83L16.83 15H7.17L10 10.83V4z')
        ICONE_CLE = ('M7 14a5 5 0 1 1 4.9-6H21v4h-2v3h-3v-3H11.9A5 5 0 0 1 7 14z'
                     'm0-2a3 3 0 1 0 0-6 3 3 0 0 0 0 6z')
        icone_svg = ('<svg class="icone-action" viewBox="0 0 24 24" aria-hidden="true">'
                    '<path fill="currentColor" d="%s"/></svg>')
        comptes_liste = liste_comptes()
        lignes = []
        for c in comptes_liste:
            statut = c["statut"]
            actions = ""
            if c["pseudo"] != ADMIN:
                for cible, classe, libelle, icone in (
                        ("valide", "oui", "Valider", ICONE_CHECK),
                        ("refuse", "non", "Refuser", ICONE_CROIX)):
                    if statut != cible:
                        actions += ('<form method="post" action="/admin">'
                                    '<input type="hidden" name="pseudo" value="%s">'
                                    '<input type="hidden" name="statut" value="%s">'
                                    '<button class="%s" type="submit" title="%s" aria-label="%s">%s</button>'
                                    '</form>'
                                    % (html.escape(c["pseudo"]), cible, classe, libelle,
                                       libelle, icone_svg % icone))
                actions += ('<form method="post" action="/admin">'
                            '<input type="hidden" name="action" value="reinitialiser">'
                            '<input type="hidden" name="pseudo" value="%s">'
                            '<button type="submit" title="Mot de passe"'
                            ' aria-label="Créer un lien pour choisir un nouveau mot de passe">%s</button>'
                            '</form>' % (html.escape(c["pseudo"]), icone_svg % ICONE_CLE))
            essai = bool("essai_phase" in c.keys() and c["essai_phase"])
            actions += ('<form method="post" action="/admin">'
                        '<input type="hidden" name="action" value="essai_phase">'
                        '<input type="hidden" name="pseudo" value="%s">'
                        '<button class="%s" type="submit" title="%s" aria-label="%s">%s</button>'
                        '</form>' % (html.escape(c["pseudo"]), "oui" if essai else "",
                                     "Nouvelle phase du méchant (essai) : %s" % ("activée" if essai else "coupée"),
                                     "Activer ou couper la nouvelle phase du méchant (essai)",
                                     icone_svg % ICONE_ESSAI))
            classe_etat = {"valide": "oui", "refuse": "non"}.get(statut, "attente")
            initiale = (c["pseudo"] or "?")[:1].upper()
            lignes.append(
                '<div class="compte-ligne">'
                '<div class="compte-avatar">%s</div>'
                '<div class="compte-info">'
                '<div class="compte-nom">%s <span class="etat-pastille %s">%s</span>%s</div>'
                '<div class="compte-meta">%s &middot; demande le %s &middot; %s</div>'
                '</div>'
                '<div class="compte-actions">%s</div>'
                '</div>'
                % (html.escape(initiale), html.escape(c["pseudo"]), classe_etat, html.escape(statut),
                   ' <span class="etat-pastille attente">essai phase</span>' if essai else '',
                   html.escape(c["email"] or "—"), html.escape(c["cree"] or "?"),
                   html.escape(_visite_lisible(c)), actions))
        n_comptes = sum(1 for c in comptes_liste if c["statut"] not in ("valide", "refuse"))
        # Les comptes createur de cartes : leur propre liste, avec activer /
        # desactiver (statut valide <-> refuse, ce qui coupe leurs sessions).
        createurs = []
        for c in liste_createurs():
            actif = c["statut"] == "valide"
            cible = "refuse" if actif else "valide"
            libelle = "Désactiver" if actif else "Réactiver"
            createurs.append(
                '<div class="compte-ligne">'
                '<div class="compte-avatar">%s</div>'
                '<div class="compte-info">'
                '<div class="compte-nom">%s <span class="etat-pastille %s">%s</span></div>'
                '<div class="compte-meta">%s &middot; créé le %s &middot; %s</div>'
                '</div>'
                '<div class="compte-actions">'
                '<form method="post" action="/admin">'
                '<input type="hidden" name="pseudo" value="%s">'
                '<input type="hidden" name="statut" value="%s">'
                '<button class="%s" type="submit" title="%s" aria-label="%s le compte">%s</button>'
                '</form>'
                '<form method="post" action="/admin">'
                '<input type="hidden" name="action" value="reinitialiser">'
                '<input type="hidden" name="pseudo" value="%s">'
                '<button type="submit" title="Mot de passe"'
                ' aria-label="Créer un lien pour choisir un nouveau mot de passe">%s</button>'
                '</form></div></div>'
                % (html.escape((c["pseudo"] or "?")[:1].upper()), html.escape(c["pseudo"]),
                   "oui" if actif else "non", "actif" if actif else html.escape(c["statut"]),
                   html.escape(c["email"] or "—"), html.escape(c["cree"] or "?"),
                   html.escape(_visite_lisible(c)),
                   html.escape(c["pseudo"]), cible, "non" if actif else "oui", libelle, libelle,
                   icone_svg % (ICONE_CROIX if actif else ICONE_CHECK),
                   html.escape(c["pseudo"]), icone_svg % ICONE_CLE))
        if not createurs:
            createurs.append('<p class="sous">Aucun créateur de cartes. Invite-en un ci-dessus.</p>')
        base = ("https://%s" % DOMAINE) if DOMAINE else "http://127.0.0.1:%d" % PORT_SITE
        # Invitations et mots de passe oublies, en fiches (23/09/2026) : avant,
        # deux tableaux a part -- desormais la meme carte que Comptes.
        inv = []
        for i in invitations_libres():
            lien = "%s/inscription?i=%s" % (base, i["jeton"])
            inv.append(
                '<div class="compte-ligne">'
                '<div class="compte-avatar">?</div>'
                '<div class="compte-info">'
                '<div class="compte-nom">Lien d\'invitation%s <span class="etat-pastille attente">libre</span></div>'
                '<div class="compte-meta"><code>%s</code> &middot; créé le %s</div>'
                '</div>'
                '<div class="compte-actions"><form method="post" action="/admin">'
                '<input type="hidden" name="action" value="annuler">'
                '<input type="hidden" name="jeton" value="%s">'
                '<button class="non" type="submit" title="Annuler" aria-label="Annuler cette invitation">%s</button>'
                '</form></div></div>'
                % (' créateur de cartes' if i["role"] == "createur" else "",
                   html.escape(lien), _horodate(i["cree_le"]), html.escape(i["jeton"]),
                   icone_svg % ICONE_CROIX))
        for i in invitations_utilisees():
            initiale = (i["utilise_par"] or "?")[:1].upper()
            inv.append(
                '<div class="compte-ligne">'
                '<div class="compte-avatar">%s</div>'
                '<div class="compte-info">'
                '<div class="compte-nom">%s <span class="etat-pastille oui">utilisée</span></div>'
                '<div class="compte-meta">créé le %s &middot; utilisée le %s</div>'
                '</div></div>'
                % (html.escape(initiale), html.escape(i["utilise_par"] or "?"),
                   _horodate(i["cree_le"]), html.escape(i["utilise_le"] or "")))
        if not inv:
            inv.append('<p class="sous">Aucune invitation. Crée-en une ci-dessus.</p>')
        reinit = []
        for r in reinitialisations_ouvertes():
            lien = "%s/reinitialisation?r=%s" % (base, r["jeton"])
            initiale = (r["pseudo"] or "?")[:1].upper()
            reinit.append(
                '<div class="compte-ligne">'
                '<div class="compte-avatar">%s</div>'
                '<div class="compte-info">'
                '<div class="compte-nom">%s</div>'
                '<div class="compte-meta"><code>%s</code> &middot; créé le %s</div>'
                '</div>'
                '<div class="compte-actions"><form method="post" action="/admin">'
                '<input type="hidden" name="action" value="reinit_annuler">'
                '<input type="hidden" name="jeton" value="%s">'
                '<button class="non" type="submit" title="Annuler" aria-label="Annuler ce lien">%s</button>'
                '</form></div></div>'
                % (html.escape(initiale), html.escape(r["pseudo"]), html.escape(lien),
                   _horodate(r["cree_le"]), html.escape(r["jeton"]), icone_svg % ICONE_CROIX))
        if not reinit:
            reinit.append('<p class="sous">Aucun lien en cours. Le bouton '
                          '« Mot de passe » d\'un compte en crée un.</p>')
        # Rapports : groupes repliables par etat, chacun avec un compte en
        # COULEUR (23/09/2026, demande de l'utilisateur) -- meme code couleur
        # que le badge de chaque rapport individuel (`.etat.*`, voir
        # _bloc_rapport), pour que le groupe se lise d'un coup d'oeil.
        classes_etat = {"nouveau": "nouveau", "en cours": "encours",
                        "traite": "traite", "refuse": "refuse"}
        tous_rapports = liste_rapports()
        rapports = ""
        for etat_r in ETATS_RAPPORT:
            libelle_r = LIBELLES_ETAT_RAPPORT.get(etat_r, etat_r.capitalize())
            groupe = [r for r in tous_rapports if (r["etat"] or "nouveau") == etat_r]
            if not groupe:
                continue
            rapports += ('<details class="groupe"%s><summary>%s '
                        '<span class="etat %s">%d</span></summary>%s</details>'
                        % (" open" if etat_r == "nouveau" else "", libelle_r,
                           classes_etat.get(etat_r, "nouveau"), len(groupe),
                           "".join(self._bloc_rapport(r) for r in groupe)))
        if not rapports:
            rapports = '<p class="sous">Aucun rapport. Bonne nouvelle.</p>'
        rapports = self._bloc_demandes_createurs() + rapports
        # L'annonce : son etat en une phrase, et le bouton d'annulation qui
        # n'existe que s'il y a quelque chose a annuler.
        en_cours = annonce_courante()
        if en_cours is None:
            annonce_etat = ("Aucune annonce. Le message apparaît en haut du "
                            "plateau et de l'assistant, avec le décompte, "
                            "chez tous les joueurs connectés.")
            annonce_annuler = ""
        else:
            annonce_etat = ('Annonce en cours, encore %d minute(s) : « %s »'
                            % (max(1, round(en_cours["secondes"] / 60)),
                               html.escape(en_cours["texte"])))
            # ⚠ UN FORMULAIRE A PART, PAS UN SECOND BOUTON. Dans le
            # formulaire ci-dessus, le champ cache `action` part en premier et
            # `_champs` ne garde que la premiere valeur : le bouton d'annulation
            # aurait repose une annonce au lieu de l'effacer.
            annonce_annuler = ('<form method="post" action="/admin">'
                               '<input type="hidden" name="action" value="annonce_annuler">'
                               '<button class="non" type="submit">Annuler l\'annonce</button>'
                               '</form>')
        # Le panneau des joueurs : un bloc par personne, avec sa conversation
        # et de quoi repondre. ⚠ ON MONTRE TOUT LE MONDE, pas seulement ceux
        # qui sont en ligne : ecrire a quelqu'un d'absent est justement l'usage
        # le plus courant, il lira en revenant.
        qui = presence()
        attente_salon = messages_non_lus(ADMIN)
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
                '<input name="texte" maxlength="%d" placeholder="Écrire à %s" required'
                ' style="flex:1;font:inherit;background:var(--panel-2);color:inherit;'
                'border:1px solid var(--border);border-radius:0;padding:.4rem .6rem">'
                '<button class="oui" type="submit">Envoyer</button>'
                '</form></div></details>'
                % (" open" if nouveau else "",
                   html.escape(personne["pseudo"]),
                   '<span class="pastille">nouveau</span>' if nouveau else "",
                   html.escape(personne["detail"]),
                   lignes_msg, html.escape(personne["pseudo"]),
                   TAILLE_MESSAGE, html.escape(personne["pseudo"])))
        if not salon:
            salon = '<p class="sous">Aucun compte validé à qui écrire.</p>'
        nb_invitations = len(invitations_libres()) + len(invitations_utilisees())
        nb_reinit = len(reinitialisations_ouvertes())
        n_rapports = nb_rapports_nouveaux()
        n_joueurs = attente_salon["nouveaux"]
        parties = "".join(
            # `data-label` : au telephone, chaque ligne devient une carte.
            '<tr><td data-label="Table">%s</td><td data-label="Hôte">%s</td>'
            '<td data-label="Ouverte le">%s</td><td data-label="Fermee le">%s</td></tr>' % (
                html.escape(p["nom"]), html.escape(p["hote"]),
                html.escape(p["ouverte_le"]),
                html.escape(p["fermee_le"] or "en cours"))
            for p in dernieres_parties())
        if not parties:
            parties = '<tr><td colspan="4">Aucune partie pour le moment.</td></tr>'

        def badge(n: int) -> str:
            return '<span class="pastille-onglet">%d</span>' % n if n else ""

        # ⚠ Le bloc de suivi et ses styles passent en ARGUMENTS, jamais dans
        # le gabarit : PAGE_ADMIN est une chaine `.format`, ou chaque accolade
        # de CSS ou de JavaScript devrait etre doublee. Meme chose pour le
        # script des onglets (ADMIN_ONGLETS_SCRIPT).
        return PAGE_ADMIN.format(barre=_barre(ADMIN),
                                 valides=nb_valides(), max=MAX_COMPTES,
                                 lignes="".join(lignes),
                                 invitations="".join(inv),
                                 createurs="".join(createurs), nb_createurs=len(liste_createurs()),
                                 reinitialisations="".join(reinit),
                                 rapports=rapports,
                                 salon=salon,
                                 regle_expiration=(
                                     "Sans visite pendant %d jours, un compte passe"
                                     " en « expire » : sa place retourne au pot, ses"
                                     " decks et ses campagnes l'attendent tant que"
                                     " personne ne la prend. « Valider » le remet en"
                                     " service." % EXPIRATION_JOURS),
                                 annonce_etat=annonce_etat,
                                 annonce_annuler=annonce_annuler,
                                 annonce_max=ANNONCE_MINUTES_MAX,
                                 nb_invitations=nb_invitations, nb_reinit=nb_reinit,
                                 n_comptes=n_comptes, n_rapports=n_rapports, n_joueurs=n_joueurs,
                                 badge_comptes=badge(n_comptes),
                                 badge_rapports=badge(n_rapports),
                                 badge_joueurs=badge(n_joueurs),
                                 parties=parties,
                                 parties_a_revoir=self._parties_a_revoir(),
                                 stats_play=bloc_stats_play(),
                                 suivi_max=SUIVI_TERMINEES_MAX,
                                 styles_suivi=SUIVI_STYLE_BLOC,
                                 script_suivi=SUIVI_SCRIPT,
                                 titre_decks=html.escape(lang.t("Decks des joueurs")),
                                 panneau_decks=_panneau_decks_joueurs(),
                                 script_decks=_script_decks_joueurs(),
                                 script_onglets=ADMIN_ONGLETS_SCRIPT).encode("utf-8")

    @staticmethod
    def _bloc_demandes_createurs() -> str:
        """Les demandes des createurs (12/10/2026), en tete du panneau des
        rapports. TOUT ce qui vient du formulaire passe par html.escape : il est
        public, n'importe qui y ecrit."""
        demandes = demandes_createurs()
        nouvelles = sum(1 for d in demandes if d["etat"] != "traitee")
        if not demandes:
            corps = '<p class="sous">Aucune demande pour le moment.</p>'
        else:
            corps = ""
            for d in demandes:
                bouton = ""
                if d["etat"] != "traitee":
                    bouton = ('<form method="post" action="/admin">'
                              '<input type="hidden" name="action" value="createur_traitee">'
                              '<input type="hidden" name="id" value="%d">'
                              '<button type="submit">Traitee</button></form>' % d["id"])
                genre = "Me créditer" if d["genre"] == "crediter" else "Retirer mes créations"
                corps += ('<details class="rapport">'
                          '<summary><span class="etat %s">%s</span>'
                          '<span class="quoi">%s</span>'
                          '<span class="meta">%s &middot; %s &middot; %s</span></summary>'
                          '<div class="corps"><p>%s</p><p>%s</p></div></details>'
                          % ("traite" if d["etat"] == "traitee" else "nouveau",
                             html.escape(d["etat"]), html.escape(genre),
                             html.escape(d["nom"]), html.escape(d["contact"]),
                             _horodate(d["quand"] or ""),
                             html.escape(d["message"]).replace("\n", "<br>"), bouton))
        return ('<details class="groupe"%s><summary>Demandes des créateurs '
                '<span class="etat nouveau">%d</span></summary>%s</details>'
                % (" open" if nouvelles else "", nouvelles, corps))

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
            journal = '<p class="sous">Aucun journal (rapport envoyé hors partie).</p>'
        ou = r["ecran"] or "?"
        if r["siege"]:
            ou += " · siège %d" % r["siege"]

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
                    '<textarea name="texte" rows="2" placeholder="Répondre à %s"></textarea>'
                    '<button type="submit">Répondre</button></form>'
                    % (r["id"], html.escape(r["hote"] or "")))
        else:
            fil = ('<p class="sous">Rapport envoyé depuis un siège invité : on ne '
                   'sait pas à quel compte il appartient, il n\'y a donc pas de fil.</p>')

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

    def _api_puzzle(self, methode: str) -> bool:
        """Les routes /api/puzzle/... : JSON, sans compte ni cookie. Vrai si la route est la leur."""
        import api_puzzles
        if not api_puzzles.est_route_puzzle(self.chemin):
            return False
        corps = b""
        if methode == "POST":
            taille = self._taille_corps()
            if taille < 0 or taille > api_puzzles.CORPS_MAX_OCTETS:
                self._corps_refuse()
                return True
            corps = self.rfile.read(taille)
        statut, contenu, entetes = api_puzzles.traiter(
            puzzles_publies(), methode, self.chemin, self.parametres, corps, self._adresse_client(),
            self.headers.get("Origin", ""), DOMAINE)
        donnees = b"" if statut == 204 else json.dumps(contenu, ensure_ascii=False).encode("utf-8")
        self._repondre(statut, donnees, "application/json; charset=utf-8", entetes)
        return True

    def do_OPTIONS(self):
        if not self._api_puzzle("OPTIONS"):
            self._repondre(404, b"", "text/plain; charset=utf-8")

    def do_GET(self):
        if self._api_puzzle("GET"):
            return
        self._poser_langue()
        pseudo = self._session()
        if self._refuser_createur(pseudo, "GET"):
            return
        if self._route_createur("GET", pseudo):
            return
        if self.chemin in ("/", "/index.html"):
            # ⚠ C'EST ICI, ET PAS SUR `/activite`, QUE DISCORD CHARGE SON
            # CADRE. Le « Root Mapping » du panneau developpeur pointe
            # TOUJOURS vers la racine du domaine cible, jamais vers un autre
            # chemin -- on ne peut pas le faire viser `/activite`. Trouve le
            # 29/09/2026 : l'activite se fermait toute seule au bout de
            # quelques secondes, le temps que Discord abandonne un cadre qui
            # ne repondait jamais a sa poignee de main, parce que cette route
            # servait la page d'accueil ordinaire au lieu de l'amorce du SDK.
            # `frame_id` est un parametre que Discord seul pose ; sa presence
            # suffit a distinguer ce cas, sans toucher a la route `/activite`
            # elle-meme (gardee pour un lien direct, ou un futur mapping qui
            # la viserait explicitement).
            if DISCORD_CLIENT_ID and self.parametres.get("frame_id"):
                # Chaque lancement repart de zero : un `nc_table` reste d'une
                # activite precedente enverrait sinon ce navigateur sur une
                # table qui n'est peut-etre plus la sienne.
                self._repondre(200, page_activite_discord_amorce(), entetes=[
                    ("Set-Cookie", "nc_table=; HttpOnly; Path=/; Max-Age=0"
                     + self._attributs_cookie())])
                return
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
            self._entrer_dans_partie(pseudo, proposer_reprise=self.chemin == "/entrer")
        elif self.chemin == "/activite_discord":
            self._activite_discord(pseudo)
        elif self.chemin == "/discord-sdk.js":
            # ⚠ SERVI D'ICI, PAS D'UN CDN. La CSP du proxy Discord n'autorise
            # que `'self'` : un `import('https://esm.sh/...')` y est bloque
            # (constate le 29/09/2026).
            # Versionne par `?v=` cote appelant (Cloudflare, devant le proxy
            # Discord, garde les `.js` par adresse complete) : cache long sans risque.
            if not DISCORD_CLIENT_ID:
                self._repondre(404, b"", "text/javascript; charset=utf-8")
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
            self.send_header("Content-Length", str(len(SDK_DISCORD)))
            self.end_headers()
            self.wfile.write(SDK_DISCORD)
        elif self.chemin == "/activite":
            # ⚠ C'EST CETTE ADRESSE QUE LE PANNEAU DEVELOPPEUR DISCORD DOIT
            # VISER (« Root Mapping »), PAS `/activite_discord`. Discord la
            # charge dans son propre cadre, SANS `instance_id` dans l'adresse
            # -- le SDK embarque (cote navigateur) l'obtient par sa propre
            # poignee de main, puis redirige lui-meme vers
            # `/activite_discord?instance_id=...`. Voir DISCORD.md.
            if not DISCORD_CLIENT_ID:
                self._repondre(404, ("Activité Discord non configurée "
                                    "(DISCORD_CLIENT_ID absent).").encode("utf-8"),
                               "text/plain; charset=utf-8")
                return
            self._repondre(200, page_activite_discord_amorce())
        elif self.chemin == "/pret":
            # ⚠ CETTE ROUTE NE DEMARRE RIEN, et c'est tout son interet. La page
            # d'attente l'interroge toutes les 1,5 s : si elle appelait
            # `demarrer_en_fond`, elle relancerait un allumage a chaque tour et
            # effacerait l'erreur du precedent (le defaut du 16/09). Elle se
            # contente de dire ou en est le moteur.
            if not pseudo:
                self._repondre(200, b'{"pret":false,"erreur":"deconnecte"}',
                               "application/json; charset=utf-8")
                return
            partie = jeu_de(pseudo)
            # ⚠ PAS PRET TANT QUE LA REPRISE EST EN ATTENTE OU EN COURS.
            #
            # ⚠⚠ COURSE ENCORE OUVERTE (24/09/2026, apres le correctif du
            # 23/09 qui n'a corrige qu'une MOITIE de la fenetre). Cette route
            # ne verifiait que `REPRISE_EN_COURS`, ajoute par `demarrer_en_fond`
            # SEULEMENT APRES que `lancer_jeu` soit revenu ET que
            # `journal_partie_ouverte` ait fini. Entre le moment ou le moteur
            # commence a repondre (`_moteur_repond` devient vrai) et celui ou
            # ce fil de fond atteint enfin `REPRISE_EN_COURS.add(...)`, cette
            # route-ci -- interrogee par une requete TOUT A FAIT SEPAREE, sur
            # un autre fil -- voyait deja le moteur repondre et rendait
            # `pret: true` la premiere. Le joueur repartait sur l'ecran par
            # defaut, sa sauvegarde se rechargeant une ou deux secondes plus
            # tard, sans que rien ne le lui montre. Constate en partie
            # (compte arnaud, 24/09/2026 18:52 UTC, partie Crossbones/Shuri
            # jamais rechargee) : `.site/moteur-1.log` de cette relance
            # commence directement sur « Select Hero and Villain », aucune
            # trace de chargement.
            #
            # `A_REPRENDRE` est pose de facon SYNCHRONE par la route
            # `/reprendre`, avant meme que `demarrer_en_fond` ne soit appelee :
            # aucune requete posterieure ne peut donc jamais le voir vide alors
            # qu'une reprise reste a faire. Le verifier ICI AUSSI ferme la
            # fenetre entiere, du clic jusqu'a la fin du chargement.
            pret = bool(partie and partie.vivant() and _moteur_repond(partie.port)
                       and pseudo not in A_REPRENDRE
                       and pseudo not in REPRISE_EN_COURS)
            self._repondre(200, json.dumps({
                "pret": pret,
                "erreur": ERREURS_DEMARRAGE.get(pseudo, ""),
            }).encode("utf-8"), "application/json; charset=utf-8")
        elif self.chemin == "/arret":
            if not pseudo:
                self._rediriger("/")
                return
            self._repondre(200, page_arret(pseudo))
        elif self.chemin == "/langue":
            # ⚠ LE COOKIE EST POSE SUR LE DOMAINE PARENT quand il y en a un :
            # le site vit sur `<domaine>` et les tables sur `p<N>.<domaine>`.
            # Pose sans domaine, le choix ne suivrait pas d'un ecran a l'autre.
            vers = (self.parametres.get("vers") or ["fr"])[0]
            vers = vers if vers in lang.LANGUES else "fr"
            retour = self.headers.get("Referer") or "/"
            # On ne renvoie QUE vers le site lui-meme : un Referer est ecrit par
            # le navigateur, donc par n'importe qui.
            if "://" in retour and DOMAINE and DOMAINE not in retour:
                retour = "/"
            self.send_response(303)
            self.send_header("Location", retour)
            cookie = ("%s=%s; Path=/; Max-Age=31536000; SameSite=Lax"
                      % (lang.COOKIE_LANGUE, vers))
            if DOMAINE:
                cookie += "; Domain=.%s" % DOMAINE
            self.send_header("Set-Cookie", cookie + self._secure())
            self.send_header("Content-Length", "0")
            self.end_headers()
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
        elif self.chemin == "/contact-createurs":
            # Public et sans compte : le lien vient de l'accueil du jeu.
            self._repondre(200, self._page_contact_createurs())
        elif self.chemin.startswith("/inscription"):
            requete = urllib.parse.urlparse(self.path)
            jeton = urllib.parse.parse_qs(requete.query).get("i", [""])[0]
            if not INSCRIPTION_LIBRE and not invitation_valide(jeton):
                self._repondre(403, self._formulaire(
                    "inscription", lang.t("Il faut un lien d'invitation pour créer un compte ici.")))
                return
            self._repondre(200, self._formulaire("inscription", jeton=jeton))
        elif self.chemin == "/connexion":
            # `da` (query) prend le pas sur le cookie : c'est lui que porte
            # desormais le lien Discord (voir `_formulaire`), le cookie n'etant
            # garde qu'en secours pour un navigateur hors contexte Discord.
            instance_discord = (self.parametres.get("da") or [""])[0] or (
                self._cookie("nc_discord_attente") or "")
            self._repondre(200, self._formulaire("connexion", instance_discord=instance_discord))
        elif self.chemin == "/deconnexion":
            brut = self.headers.get("Cookie") or ""
            for morceau in brut.split(";"):
                nom, _, valeur = morceau.strip().partition("=")
                if nom == "nc_session":
                    fermer_session(valeur)
            self.send_response(303)
            self.send_header("Location", "/")
            # Les memes attributs qu'a la pose (Domain compris, 25/09/2026) :
            # un cookie efface doit ressembler a celui qu'il remplace, sans
            # quoi certains navigateurs gardent l'ancien a cote.
            domaine = ("; Domain=.%s" % DOMAINE) if DOMAINE else ""
            self.send_header("Set-Cookie",
                             f"nc_session=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0{domaine}"
                             + self._secure())
            self.send_header("Content-Length", "0")
            self.end_headers()
        elif self.chemin.startswith("/reinitialisation"):
            jeton = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("r", [""])[0]
            if reinitialisation_valide(jeton) is None:
                self._repondre(410, self._formulaire_reinitialisation(
                    "", "Ce lien n'est plus valable. Demande un nouveau lien à l'administrateur."))
                return
            self._repondre(200, self._formulaire_reinitialisation(jeton))
        elif self.chemin == "/admin":
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
                return
            self._repondre(200, self._page_admin())
        elif self.chemin == "/suivi":
            # La page de suivi nomme les joueurs : reservee a l'administrateur,
            # comme /admin. Un visiteur non connecte est envoye au formulaire.
            if not pseudo:
                self._rediriger("/")
                return
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
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
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
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
        elif self.chemin == "/api/admin/decks-joueurs":
            # Reserve a l'administrateur, VERIFIE ICI (19/10/2026). Un visiteur
            # sans session recoit 403 comme un joueur : on ne dit pas si la
            # route existe.
            if pseudo != ADMIN:
                self._repondre(403, b'{"error":"admin"}', "application/json; charset=utf-8")
                return
            comptes_decks = lister_decks_des_joueurs()
            journaliser_decks_admin(
                "consultation", comptes=len(comptes_decks),
                decks=sum(len(c["decks"]) for c in comptes_decks))
            corps = json.dumps({"comptes": comptes_decks}, ensure_ascii=False).encode("utf-8")
            self._repondre(200, corps, "application/json; charset=utf-8",
                           [("Cache-Control", "no-store")])
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
            self._repondre(200, page_hors_ligne(), "text/html; charset=utf-8")
        elif self.chemin == "/sw.js":
            # ⚠ SANS CACHE HTTP non plus : un worker mis en cache par le
            # navigateur survivrait a sa propre mise a jour.
            self._repondre(200, SERVICE_WORKER, "application/javascript; charset=utf-8")
        elif self.chemin in ("/app-192.png", "/app-512.png", "/favicon.png",
                             "/favicon.ico", "/narwhal.png"):
            # /favicon.ico : les navigateurs le demandent d'office, on leur
            # rend le meme narval plutot qu'un 404 a chaque page.
            image = _icone_appli("favicon.png" if self.chemin == "/favicon.ico" else self.chemin[1:])
            if image is None:
                self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")
                return
            # ⚠ LA MASCOTTE CHANGE TOUTES LES TROIS HEURES, PAS L'ICONE DE
            # L'APPLI. On donne donc un cache COURT aux deux images qui
            # tournent : sans lui le navigateur garde l'ancien narval pendant
            # des heures, et le changement ne se verrait jamais. Dix minutes de
            # retard au pire, sur une rotation de trois heures.
            tourne = self.chemin in ("/favicon.png", "/favicon.ico", "/narwhal.png")
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.send_header("Cache-Control",
                             "public, max-age=600" if tourne else "public, max-age=86400")
            self.send_header("Content-Length", str(len(image)))
            self.end_headers()
            self.wfile.write(image)
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
        elif self.chemin.startswith("/vilains/") and self.chemin.endswith(".jpg"):
            # Portrait de vilain pour /entrer, voir _portrait_vilain(). Public
            # (pas de session requise) : ce ne sont que des illustrations de
            # cartes deja imprimees, rien de prive.
            image = _portrait_vilain(self.chemin[len("/vilains/"):-len(".jpg")])
            if image is None:
                self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")
                return
            self.send_response(200)
            self.send_header("Content-Type", "image/jpeg")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Content-Length", str(len(image)))
            self.end_headers()
            self.wfile.write(image)
        elif self.chemin == "/admin/sauvegardes":
            # La liste des sauvegardes du code, reservee a l'administrateur.
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
                return
            self._repondre(200, self._page_sauvegardes())
        elif self.chemin == "/admin/images":
            # Toutes les images d'un bloc (tar), fabrique A LA VOLEE : toujours
            # a jour, rien de stocke en double. Plusieurs Go : le site sert un
            # fil par requete, les joueurs ne l'attendent pas.
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
                return
            self._servir_images()
        elif self.chemin == "/admin/partie-joueur":
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
                return
            self._servir_partie_joueur()
        elif self.chemin == "/admin/sauvegarde-code":
            # Le zip designe par son RANG dans la liste (0 = le plus recent),
            # jamais par un nom venu de l'adresse : pas de traversee de dossier.
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
                return
            self._servir_sauvegarde()
        elif self.chemin.startswith("/admin/capture"):
            # La capture d'un rapport, reservee a l'administrateur comme la
            # page qui l'affiche. On ne sert JAMAIS le nom de fichier venu de
            # l'adresse : on lit celui que la base associe au numero demande,
            # sans quoi n'importe quel chemin sortirait du dossier.
            if pseudo != ADMIN:
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"), "text/plain; charset=utf-8")
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

    # ------------------------------------------------------------------
    # Createur de cartes : isolement, pages statiques, API de stockage
    # ------------------------------------------------------------------
    # ⚠ ISOLEMENT PAR LISTE BLANCHE, A L'ENTREE DE CHAQUE do_*. Un compte
    # `createur` ne passe que par ces chemins ; tout le reste (jeu, admin,
    # decks, parties, API du moteur...) est refuse AVANT d'atteindre la moindre
    # route, y compris celles qu'on ajoutera plus tard : un oubli ne peut donc
    # pas ouvrir une porte, il ferme une page de trop. Public = sans session
    # de toute facon (connexion, inscription, mot de passe oublie, deconnexion).
    _CREATEUR_EXACT = frozenset({
        "/createur-cartes.html", "/connexion", "/deconnexion", "/inscription",
        "/reinitialisation", "/favicon.ico", "/favicon.png"})
    _CREATEUR_PREFIXES = ("/createur-cartes/", "/api/createur/")

    def _chemin_createur_permis(self) -> bool:
        chemin = self.chemin
        return chemin in self._CREATEUR_EXACT or chemin.startswith(self._CREATEUR_PREFIXES)

    def _refuser_createur(self, pseudo, methode: str) -> bool:
        """True si la requete vient d'un createur ET sort de son perimetre
        (la reponse est alors deja envoyee)."""
        if not pseudo or not est_createur(pseudo) or self._chemin_createur_permis():
            return False
        if methode != "GET":
            self._raccrocher()      # le corps n'est pas lu
        if methode == "GET" and self.chemin in ("/", "/index.html", "/entrer"):
            self._rediriger("/createur-cartes.html")
        else:
            self._repondre(403, "Réservé aux joueurs : ton compte ne donne accès"
                                " qu'au créateur de cartes.".encode("utf-8"),
                           "text/plain; charset=utf-8", [("Cache-Control", "no-store")])
        return True

    _MIME_CREATEUR = {
        ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
        ".mjs": "text/javascript; charset=utf-8", ".css": "text/css; charset=utf-8",
        ".json": "application/json; charset=utf-8", ".svg": "image/svg+xml",
        ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
        ".webp": "image/webp", ".gif": "image/gif", ".ico": "image/x-icon",
        ".woff": "font/woff", ".woff2": "font/woff2", ".ttf": "font/ttf",
        ".otf": "font/otf", ".txt": "text/plain; charset=utf-8",
    }

    def _json(self, code: int, objet) -> None:
        self._repondre(code, json.dumps(objet, ensure_ascii=False).encode("utf-8"),
                       "application/json; charset=utf-8",
                       [("Cache-Control", "no-store"), ("X-Content-Type-Options", "nosniff")])

    def _chemin_statique_createur(self) -> str | None:
        """Le fichier du jeu que ce chemin designe, ou None. Aucune sortie du
        dossier public du jeu : segments filtres, puis realpath verifie."""
        racine = os.path.realpath(DOSSIER_PUBLIC_JEU)
        if self.chemin == "/createur-cartes.html":
            relatif = ["createur-cartes.html"]
        else:
            brut = urllib.parse.unquote(self.chemin[len("/createur-cartes/"):])
            if "\x00" in brut or "\\" in brut:
                return None
            segments = brut.split("/")
            if any(seg in ("", ".", "..") or seg.startswith(".") for seg in segments):
                return None
            relatif = ["createur-cartes"] + segments
        chemin = os.path.realpath(os.path.join(racine, *relatif))
        if not chemin.startswith(racine + os.sep) or not os.path.isfile(chemin):
            return None
        if os.path.splitext(chemin)[1].lower() not in self._MIME_CREATEUR:
            return None
        return chemin

    def _route_createur(self, methode: str, pseudo) -> bool:
        """Traite les routes du createur de cartes. True si la requete est la
        sienne (reponse envoyee), False pour laisser le reste du site faire."""
        chemin = self.chemin
        statique = (chemin == "/createur-cartes.html"
                    or chemin.startswith("/createur-cartes/"))
        api = chemin.startswith("/api/createur/")
        if not (statique or api):
            return False
        if methode != "GET":
            if api:
                pass     # le corps est lu (ou refuse) par `_api_createur`
            else:
                self._raccrocher()
        if not pseudo:
            if api:
                self._raccrocher()
                self._json(401, {"erreur": "Connexion requise."})
            elif methode == "GET":
                self._rediriger("/")
            else:
                self._repondre(405, b"", "text/plain; charset=utf-8")
            return True
        # 28/10/2026 : ouvert a TOUT compte connecte (joueurs, createurs, admin),
        # sur decision de l'admin. Chacun reste isole : ses projets seulement.
        if statique:
            if methode != "GET":
                self._repondre(405, b"", "text/plain; charset=utf-8")
                return True
            fichier = self._chemin_statique_createur()
            if fichier is None:
                self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")
                return True
            with open(fichier, "rb") as f:
                corps = f.read()
            self._repondre(200, corps, self._MIME_CREATEUR[os.path.splitext(fichier)[1].lower()],
                           [("Cache-Control", "no-cache"), ("X-Content-Type-Options", "nosniff")])
            return True
        self._api_createur(methode, pseudo)
        return True

    def _api_createur(self, methode: str, pseudo: str) -> None:
        """/api/createur/projets, /projet/<id>, /projet/<id>/versions[/<n>].

        Chacun ne voit que SES projets ; l'administrateur LIT ceux des autres
        par `?compte=<pseudo>`, sans jamais les ecrire."""
        ecriture = methode in ("PUT", "DELETE")
        try:
            demande = (self.parametres.get("compte") or [""])[0].strip().lower()
            if demande and demande != pseudo:
                if pseudo != ADMIN or ecriture:
                    raise createur_cartes.ErreurCreateur(
                        403, "Les projets d'un autre compte ne sont pas accessibles.")
                cible = createur_cartes.compte_valide(demande)
                ligne = compte(cible)
                if ligne is None:
                    raise createur_cartes.ErreurCreateur(404, "Compte introuvable.")
            else:
                cible = createur_cartes.compte_valide(pseudo)
            if ecriture:
                # Meme origine obligatoire : le cookie est SameSite=Lax, ceci
                # double la protection contre une requete venue d'ailleurs.
                origine = self.headers.get("Origin")
                if origine and (urllib.parse.urlparse(origine).netloc
                                != (self.headers.get("Host") or "")):
                    raise createur_cartes.ErreurCreateur(403, "Origine refusée.")
            morceaux = self.chemin[len("/api/createur/"):].split("/")
            racine = DOSSIER_CREATEUR
            if morceaux == ["projets"] and methode == "GET":
                self._json(200, {"projets": createur_cartes.lister(racine, cible),
                                 "utilise": createur_cartes.usage_octets(racine, cible),
                                 "quota": QUOTA_CREATEUR_OCTETS})
                return
            if len(morceaux) >= 2 and morceaux[0] == "projet":
                identifiant = createur_cartes.id_valide(morceaux[1])
                reste = morceaux[2:]
                if not reste and methode == "GET":
                    self._repondre(200, createur_cartes.lire(racine, cible, identifiant),
                                   "application/json; charset=utf-8",
                                   [("Cache-Control", "no-store"),
                                    ("X-Content-Type-Options", "nosniff")])
                    return
                if not reste and methode == "PUT":
                    octets = self._corps_projet()
                    meta = createur_cartes.ecrire(racine, cible, identifiant, octets,
                                                  QUOTA_CREATEUR_OCTETS, MAX_PROJET_OCTETS)
                    self._json(200, meta)
                    return
                if not reste and methode == "DELETE":
                    createur_cartes.supprimer(racine, cible, identifiant)
                    self._json(200, {"supprime": identifiant})
                    return
                if reste == ["versions"] and methode == "GET":
                    self._json(200, {"versions": createur_cartes.versions(racine, cible, identifiant)})
                    return
                if len(reste) == 2 and reste[0] == "versions" and methode == "GET":
                    self._repondre(200, createur_cartes.lire_version(racine, cible, identifiant, reste[1]),
                                   "application/json; charset=utf-8",
                                   [("Cache-Control", "no-store"),
                                    ("X-Content-Type-Options", "nosniff")])
                    return
            if ecriture:
                self._raccrocher()
            raise createur_cartes.ErreurCreateur(404, "Route inconnue.")
        except createur_cartes.ErreurCreateur as e:
            if ecriture:
                self._raccrocher()      # corps eventuellement non lu
            self._json(e.code, {"erreur": e.message})

    def _corps_projet(self) -> bytes:
        """Le corps d'un PUT de projet, plafonne sur l'ANNONCE avant lecture."""
        if "application/json" not in (self.headers.get("Content-Type") or "").lower():
            raise createur_cartes.ErreurCreateur(415, "Content-Type : application/json attendu.")
        brut = self.headers.get("Content-Length")
        try:
            taille = int(brut)
        except (TypeError, ValueError):
            raise createur_cartes.ErreurCreateur(411, "Content-Length obligatoire.")
        if taille < 0:
            raise createur_cartes.ErreurCreateur(400, "Content-Length invalide.")
        if taille > MAX_PROJET_OCTETS:
            raise createur_cartes.ErreurCreateur(
                413, "Projet trop volumineux : %d Mo au maximum." % (MAX_PROJET_OCTETS // (1024 * 1024)))
        corps = self.rfile.read(taille)
        if len(corps) != taille:
            raise createur_cartes.ErreurCreateur(400, "Corps incomplet.")
        return corps

    def do_PUT(self):
        self._poser_langue()
        pseudo = self._session()
        if self._refuser_createur(pseudo, "PUT"):
            return
        if not self._route_createur("PUT", pseudo):
            self._raccrocher()
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")

    def do_DELETE(self):
        self._poser_langue()
        pseudo = self._session()
        if self._refuser_createur(pseudo, "DELETE"):
            return
        if not self._route_createur("DELETE", pseudo):
            self._raccrocher()
            self._repondre(404, b"Introuvable", "text/plain; charset=utf-8")

    def _poser_langue(self) -> None:
        """La langue de CE visiteur, pour toute la duree de CETTE requete.

        ⚠ Un fil par requete (`ThreadingHTTPServer`) : deux visiteurs peuvent
        lire deux langues a la meme seconde. C'est pour cela que la langue vit
        dans le fil et non dans une globale.
        """
        lang.poser(lang.detecter(self.headers.get("Cookie") or "",
                                 self.headers.get("Accept-Language") or ""))

    def do_POST(self):
        if self._api_puzzle("POST"):
            return
        self._poser_langue()
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
        if self._refuser_createur(self._session(), "POST"):
            return

        if self.chemin == "/compteur_play":
            # Sans compte et sans cookie : play n'en a pas. Plafond propre a
            # cette route, juge sur l'annonce AVANT de lire, comme plus haut.
            taille = self._taille_corps()
            if taille > COMPTEUR_PLAY_MAX_OCTETS:
                self._corps_refuse()
                return
            enregistrer_partie_play(self.rfile.read(taille))
            # play. est isole (COEP require-corp, pour Safari, 12/10/2026) : sans
            # CORP, le navigateur refuse cette reponse venue du site principal.
            self._repondre(204, b"", "text/plain; charset=utf-8",
                           [("Cross-Origin-Resource-Policy", "same-site")])
            return

        if self.chemin == "/presence_play":
            taille = self._taille_corps()
            if taille > PRESENCE_PLAY_MAX_OCTETS:
                self._corps_refuse()
                return
            signaler_presence_play(self.rfile.read(taille))
            # play. est isole (COEP require-corp, pour Safari, 12/10/2026) : sans
            # CORP, le navigateur refuse cette reponse venue du site principal.
            self._repondre(204, b"", "text/plain; charset=utf-8",
                           [("Cross-Origin-Resource-Policy", "same-site")])
            return

        if self.chemin == "/contact-createurs":
            # Sans compte : le corps est deja plafonne par MAX_CORPS_OCTETS.
            # ⚠ LE FREIN PASSE AVANT LA LECTURE DES CHAMPS, et compte chaque
            # envoi : voir `debit_createur_ok`.
            if not debit_createur_ok(self._adresse_client()):
                self._raccrocher()
                self._repondre(429, self._page_contact_createurs(
                    lang.t("Trop de demandes depuis ta connexion. Réessaie dans une heure.")))
                return
            champs = self._champs()
            # Le pot de miel : un humain ne voit pas ce champ et le laisse vide.
            # Un robot qui le remplit recoit la meme confirmation, sans rien
            # enregistrer : il n'apprend pas qu'il a ete repere.
            if str(champs.get("site_web", "")).strip():
                self._repondre(200, self._page_contact_createurs(envoye=True))
                return
            try:
                enregistrer_demande_createur(champs.get("nom", ""), champs.get("contact", ""),
                                             champs.get("genre", ""), champs.get("message", ""))
            except ValueError as erreur:
                self._repondre(400, self._page_contact_createurs(str(erreur), champs))
                return
            self._repondre(200, self._page_contact_createurs(envoye=True))
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
                langue=_bouton_langue(),
                titre=lang.t("Demande enregistrée"), action="/connexion",
                bouton=lang.t("Entrer"), auto="current-password", erreur="",
                mdp=lang.t("Mot de passe"),
                bouton_appli=_bouton_appli(), mention=_mention_complete(),
                champs='<label>%s<input name="pseudo" '
                       'autocomplete="username" required></label>'
                       % lang.t("Pseudo ou adresse e-mail"),
                pied=(lang.t("Ton compte est actif : connecte-toi.") if invite else
                      lang.t("Ton compte attend une validation manuelle. Reviens une fois"
                             " qu'elle est faite."))).encode("utf-8"))

        elif self.chemin == "/reinitialisation":
            champs = self._champs()
            try:
                qui = reinitialiser_mot_de_passe(champs.get("r", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire_reinitialisation(champs.get("r", ""), str(erreur)))
                return
            self._repondre(200, PAGE_FORMULAIRE.format(
                langue=_bouton_langue(),
                titre=lang.t("Mot de passe enregistré"), action="/connexion",
                bouton=lang.t("Entrer"), auto="current-password", erreur="",
                mdp=lang.t("Mot de passe"),
                champs='<label>%s<input name="pseudo" '
                       'autocomplete="username" value="%s" required></label>'
                       % (lang.t("Pseudo ou adresse e-mail"), html.escape(qui)),
                bouton_appli=_bouton_appli(), mention=_mention_complete(),
                pied=lang.t("Ton nouveau mot de passe est en place : connecte-toi.")).encode("utf-8"))

        elif self.chemin == "/connexion":
            champs = self._champs()
            # Le champ cache `da` (voir `_formulaire`) prend le pas sur le
            # cookie : c'est lui qui survit fiablement au POST dans le cadre
            # Discord. Repasse sur chaque reaffichage du formulaire (erreurs
            # ci-dessous) pour ne pas perdre le fil en cas de faute de frappe.
            instance_en_attente = champs.get("da", "") or (
                self._cookie("nc_discord_attente") or "")
            cle = cle_frein(self._adresse_client())
            # ⚠ ON LIT LE COMPTEUR AVANT DE L'INCREMENTER. Compter au fil de la
            # lecture ferait qu'une adresse deja bloquee continuerait de charger
            # son propre compteur, et le frein ne se relacherait jamais.
            reste = attente_connexion(cle)
            if reste:
                self._repondre(429, self._formulaire(
                    "connexion", "Trop de tentatives. Réessaie dans %s."
                                 % delai_lisible(reste),
                    instance_discord=instance_en_attente))
                return
            compter_tentative(cle)
            try:
                qui = verifier(champs.get("pseudo", ""), champs.get("mdp", ""))
            except ValueError as erreur:
                self._repondre(400, self._formulaire(
                    "connexion", str(erreur), instance_discord=instance_en_attente))
                return
            # Reussite : on relache le frein, pour que ses propres fautes de
            # frappe ne poursuivent pas quelqu'un qui a fini par entrer.
            oublier_tentatives(cle)
            createur = est_createur(qui)
            jeton = ouvrir_session(qui)
            # Sans ceci, « en ligne » n'apparaitrait presque jamais : la
            # presence n'etait rafraichie que par le MOTEUR, donc uniquement
            # pendant qu'une partie tourne. On la touche des l'entree sur le
            # site, ce qui couvre le moment ou le moteur demarre encore.
            if not createur:
                toucher_presence(qui)
            # HttpOnly : le cookie n'est pas lisible en JavaScript.
            # SameSite=Lax : il ne part pas sur une requete venue d'un autre site.
            # Secure : il ne part pas en clair. Sans lui, une premiere visite
            # tapee en `http://` envoyait le cookie sur le reseau avant meme que
            # Caddy n'ait eu le temps de rediriger vers HTTPS.
            # Domain=.DOMAINE (25/09/2026, meme raison que le cookie de langue
            # ci-dessous) : le site vit sur `<domaine>`, les tables sur
            # `p<N>.<domaine>`. Sans le domaine parent, un invite connecte sur
            # son PROPRE compte (depuis un second appareil ou un autre onglet)
            # arrive sur une table sans que celle-ci sache qui il est reellement
            # — son signalement de bug est alors attribue a l'hote de la table,
            # jamais a lui. Voir `post_rapport_bug` (moteur) et `/api/bug`
            # ci-dessous, qui relaient desormais ce cookie pour resoudre le vrai
            # compte.
            # Dans Discord, `_attributs_cookie` remplace tout cela par
            # `SameSite=None; Partitioned`, sans domaine (voir sa doc).
            cookie_session = (
                f"nc_session={jeton}; HttpOnly; Path=/;"
                f" Max-Age={DUREE_SESSION_JOURS * 86400}"
                + self._attributs_cookie(domaine_parent=True))

            if createur:
                # Ni table, ni activite Discord : le seul endroit permis.
                self._rediriger("/createur-cartes.html", [("Set-Cookie", cookie_session)])
                return

            if instance_en_attente:
                # ⚠ RESOLU ICI, PAS PAR UNE REDIRECTION VERS `/activite_discord`.
                # Constate en prod le 29/09/2026 : dans le cadre Discord, le
                # cookie qu'on vient de poser (`nc_session` juste au-dessus)
                # n'est pas renvoye de facon fiable sur la requete SUIVANTE --
                # `role_activite_discord` relu depuis `/activite_discord` ne
                # voyait donc jamais ce `qui` et redemandait la connexion en
                # boucle. `qui` est deja connu ICI, dans CETTE reponse : le
                # role se tranche tout de suite, sans nouvel aller-retour qui
                # dependrait d'un cookie.
                role, hote = role_activite_discord(instance_en_attente, qui)
                effacer_attente = (
                    "nc_discord_attente=; HttpOnly; Path=/; Max-Age=0"
                    + self._attributs_cookie())
                entetes = [("Set-Cookie", cookie_session),
                           ("Set-Cookie", effacer_attente)]
                if role == "hote":
                    self._entrer_dans_partie(
                        qui, proposer_reprise=False, joueurs=4,
                        entetes_supplementaires=entetes)
                else:
                    self._repondre_participant(hote or "", instance_en_attente, entetes,
                                               identite=qui)
                return

            self._rediriger("/entrer", [("Set-Cookie", cookie_session)])

        elif self.chemin == "/api/admin/decks-joueurs/importer":
            # Reserve a l'administrateur, verifie AVANT de lire le corps. En-tete
            # `X-Importer-Deck` exige : un formulaire d'un autre site ne peut
            # pas l'ajouter (en plus du cookie SameSite=Lax).
            if pseudo != ADMIN:
                self._raccrocher()
                self._repondre(403, b'{"error":"admin"}', "application/json; charset=utf-8")
                return
            if self.headers.get("X-Importer-Deck") != "1" or self._taille_corps() > 4096:
                self._raccrocher()
                self._repondre(400, b'{"error":"requete"}', "application/json; charset=utf-8")
                return
            champs = self._champs()
            cible = str(champs.get("compte", ""))
            identifiant = str(champs.get("deck", ""))
            try:
                resultat = importer_deck_de_joueur(cible, identifiant)
                code = 200
                journaliser_decks_admin("import", compte=cible, deck=identifiant,
                                        copie=resultat["fichier"], resultat="ok")
            except ErreurDeckAdmin as erreur:
                code = erreur.code
                resultat = {"ok": False, "error": str(erreur)}
                journaliser_decks_admin("import", compte=cible[:40], deck=identifiant[:80],
                                        resultat="refuse %d" % code)
            self._repondre(code, json.dumps(resultat, ensure_ascii=False).encode("utf-8"),
                           "application/json; charset=utf-8")
        elif self.chemin == "/admin":
            # Le controle passe AVANT la lecture du corps : un inconnu n'a pas
            # a faire allouer un octet sur une route qui va le refuser.
            if pseudo != ADMIN:
                self._raccrocher()
                self._repondre(403, "Réservé à l'administrateur.".encode("utf-8"),
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
            elif action == "inviter_createur":
                creer_invitation("createur")
            elif action == "annuler":
                supprimer_invitation(champs.get("jeton", ""))
            elif action == "reinitialiser":
                try:
                    creer_reinitialisation(champs.get("pseudo", ""))
                except ValueError:
                    pass          # compte inconnu : rien a creer, la page se reaffiche
            elif action == "reinit_annuler":
                supprimer_reinitialisation(champs.get("jeton", ""))
            elif action == "essai_phase":
                basculer_essai_phase(champs.get("pseudo", ""))
            elif action == "createur_traitee":
                try:
                    marquer_demande_createur(int(champs.get("id", "0")), "traitee")
                except ValueError:
                    pass
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
                           "/api/prives", "/api/prives_lus", "/api/eteindre",
                           "/api/connectes", "/api/inviter", "/api/invitations",
                           "/api/invitation_reponse", "/api/invitations_envoyees",
                           "/api/decks_invite", "/api/decks_compte", "/api/connexion"):
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
                # ⚠ CORRECTIF (25/09/2026). `qui` ne dit que de quelle TABLE le
                # rapport vient (le titulaire du jeton de partie), et le reste
                # tel quel : `rapports_de_ses_tables` en depend pour que l'hote
                # voie TOUT ce qui se passe chez lui. Ce qui manquait, c'est
                # l'AUTEUR REEL quand ce n'est pas lui : un invite connecte a
                # son PROPRE compte sur un autre onglet ou un autre appareil
                # n'ouvrait aucune conversation possible (fiche
                # `2026-09-19-file-d-attente-et-deploiement.md`). Le moteur
                # relaie maintenant le cookie de session du NAVIGATEUR
                # (`post_rapport_bug`, possible depuis que ce cookie porte
                # `Domain=.<domaine>`) ; on le verifie ICI, cote site, seul a
                # savoir resoudre une session. Une session invalide ou absente
                # (invite jamais connecte) laisse `compte_verifie` a son
                # defaut (`enregistrer_rapport` retombe sur la regle du siege
                # 0), comportement inchange.
                auteur_reel = pseudo_de_session(str(champs.get("nc_session") or ""))
                numero = enregistrer_rapport(qui, champs, compte_verifie=auteur_reel or None)
                self._repondre(200, json.dumps({"ok": True, "numero": numero}).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/eteindre":
                # « Quitter la partie » depuis le PLATEAU : c'est le pendant
                # interne du bouton « Terminer » du site. L'hote ferme sa
                # table, elle cesse d'exister, l'emplacement est rendu et les
                # invites sont mis dehors.
                #
                # ⚠ QUI A LE DROIT EST DECIDE PAR LE MOTEUR, PAS ICI. Le jeton
                # dit de quelle TABLE vient l'appel, pas qui l'a clique : c'est
                # `/quitter_la_table` (server_get.py) qui exige le siege 0,
                # cookie en main. Un invite n'arrive donc jamais jusqu'ici.
                #
                # ⚠ ET ON REPOND AVANT D'ETEINDRE, DANS CET ORDRE EXACT :
                # acces coupes, reponse partie, PUIS le fil qui tue. Celui qui
                # attend cette reponse est le moteur qu'on tue : demarrer le
                # fil ne serait-ce qu'une ligne plus tot laisse une course ou
                # le messager meurt avant d'avoir parle.
                #
                # L'adresse d'atterrissage part d'ICI parce que le site est le
                # seul a connaitre son domaine public : le plateau, lui, est
                # servi par un moteur qui n'aura plus de page a lui offrir.
                # ⚠ ET `finally`, PAS UNE LIGNE APRES. `_repondre` ecrit sur la
                # socket, et le client d'en face est le moteur : son
                # `_appeler_site` coupe a dix secondes. Une revocation qui
                # traine sur un verrou sqlite au-dela de ce plafond fait lever
                # l'ecriture, et sans ce filet le fil ne partait jamais — mot
                # de passe revoque, moteur vivant, emplacement pris jusqu'au
                # faucheur. Les acces sont deja coupes a ce stade : il n'y a
                # plus aucune raison de ne pas aller au bout.
                eteindre = eteindre_volontairement(qui, "quitte depuis le plateau",
                                                   differer=True)
                racine = (f"https://{DOMAINE}" if DOMAINE
                          else f"http://127.0.0.1:{PORT_SITE}")
                try:
                    self._repondre(200, json.dumps({"ok": True,
                                                    "url": racine + "/arret"}).encode("utf-8"),
                                   "application/json; charset=utf-8")
                finally:
                    eteindre()
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
            # --- Inviter un connecte (13/10/2026) ----------------------------
            # `qui` est le titulaire de la table qui relaie : l'hote quand il
            # invite, l'invite quand il lit ou repond depuis SA table. Le moteur
            # n'ouvre ces routes qu'au siege 0 (server_get.py).
            if self.chemin == "/api/connectes":
                self._repondre(200, json.dumps({"connectes": connectes(sauf=qui)},
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/inviter":
                try:
                    siege = int(champs.get("siege", "0") or "0")
                except ValueError:
                    siege = 0
                resultat = inviter_a_la_table(qui, str(champs.get("a") or ""), siege)
                if isinstance(resultat, str):
                    self._repondre(400, json.dumps({"error": resultat}).encode("utf-8"),
                                   "application/json; charset=utf-8")
                    return
                self._repondre(200, b'{"ok":true}', "application/json; charset=utf-8")
                return
            if self.chemin == "/api/invitations":
                # ⚠ CE SONDAGE-CI VAUT SIGNE DE VIE, contrairement a /api/prives.
                # « Connecte » veut dire ici « une page du site ouverte sous ses
                # yeux » : c'est exactement ce qu'il prouve, puisque le module
                # des invitations (public/js/invitations.js) se tait des que
                # l'onglet est cache. Sans lui, personne n'etait jamais « en
                # ligne » plus de deux minutes apres son arrivee.
                toucher_presence(qui)
                self._repondre(200, json.dumps({"invitations": invitations_pour(qui)},
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/invitation_reponse":
                oui = str(champs.get("oui", "")) == "1"
                lien = repondre_invitation(qui, str(champs.get("id") or ""), oui)
                if oui and not lien:
                    self._repondre(409, b'{"error":"invitation expiree"}',
                                   "application/json; charset=utf-8")
                    return
                self._repondre(200, json.dumps({"ok": True, "lien": lien or ""}).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/decks_invite":
                try:
                    siege = int(champs.get("siege", "0") or "0")
                except ValueError:
                    siege = 0
                self._repondre(200, json.dumps(decks_de_l_invite(qui, siege),
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/connexion":
                # L'invite se CONNECTE a son compte depuis le salon (cas B,
                # 28/10/2026). `qui` (jeton de partie) prouve seulement que
                # l'appel vient d'un moteur legitime ; l'identite verifiee est
                # celle du couple pseudo/mdp. L'anti-flood porte sur l'ADRESSE
                # reelle du navigateur, relayee par le moteur (la connexion ici
                # vient de 127.0.0.1, inexploitable comme cle). Reussite : on
                # rend le jeton de session, que le MOTEUR posera en cookie
                # nc_session (Domain=.<domaine>) sur sa reponse au navigateur.
                adresse = str(champs.get("adresse", "") or "") or "?"
                cle = cle_frein(adresse)
                reste = attente_connexion(cle)
                if reste:
                    self._repondre(200, json.dumps(
                        {"ok": False, "erreur": "Trop de tentatives. Réessaie dans %s." % delai_lisible(reste)},
                        ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
                    return
                compter_tentative(cle)
                try:
                    pseudo = verifier(str(champs.get("pseudo", "") or ""), str(champs.get("mdp", "") or ""))
                except ValueError as erreur:
                    self._repondre(200, json.dumps({"ok": False, "erreur": str(erreur)},
                        ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
                    return
                oublier_tentatives(cle)
                jeton = ouvrir_session(pseudo)
                toucher_presence(pseudo)
                self._repondre(200, json.dumps({"ok": True, "jeton": jeton, "pseudo": pseudo},
                    ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")
                return
            if self.chemin == "/api/decks_compte":
                # Les decks du compte DEJA CONNECTE dans le navigateur de
                # l'invite : son cookie de session, relaye par le moteur, dit
                # qui il est (seul le site sait lire une session). `qui` (le
                # jeton de partie) prouve seulement que l'appel vient d'un
                # moteur legitime ; l'identite qui COMPTE est celle de la
                # session. Session absente/invalide (invite jamais connecte) :
                # liste vide, comme `get_decks_invite` sans invitation.
                pseudo = pseudo_de_session(str(champs.get("nc_session") or ""))
                self._repondre(200, json.dumps(decks_du_compte(pseudo or ""),
                                               ensure_ascii=False).encode("utf-8"),
                               "application/json; charset=utf-8")
                return
            if self.chemin == "/api/invitations_envoyees":
                self._repondre(200, json.dumps({"sieges": invitations_de(qui)},
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
            # Acces coupes d'abord, moteur ensuite : l'ordre et le piege qu'il
            # evite sont ecrits une seule fois, dans `eteindre_volontairement`.
            # On n'eteint QUE son propre jeu : le code est le pseudo.
            eteindre_volontairement(pseudo)
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
