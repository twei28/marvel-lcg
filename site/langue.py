"""La langue du visiteur, et les mots du site.

⚠ POURQUOI CE FICHIER EXISTE. Le jeu est bilingue depuis longtemps (l'assistant,
le plateau, le deck builder et le salon partagent un `t()` et un dictionnaire).
Le SITE, lui, etait ecrit en francais en dur : accueil, connexion, inscription,
reprise, signalements. Un anglophone tombait dessus a chaque visite.

⚠ LE POINT DUR : LE SERVEUR NE VOIT PAS LE `localStorage`, ou le jeu garde la
langue choisie. Il s'appuie donc, dans cet ordre :

  1. le COOKIE `nc_langue`, pose par le site ET par le jeu (sur le domaine
     parent) : le choix fait en partie suit sur le site, et reciproquement ;
  2. l'en-tete `Accept-Language` du navigateur, pour une premiere visite ;
  3. le francais.

⚠ LA LANGUE VIT DANS LE FIL DE LA REQUETE, pas dans une variable globale. Le
site tourne sur `ThreadingHTTPServer` : un fil par requete, donc deux visiteurs
peuvent lire deux langues a la meme seconde. Une globale les melangerait.
"""
import threading

LANGUES = ("fr", "en")
COOKIE_LANGUE = "nc_langue"

_courante = threading.local()


def poser(langue: str) -> None:
    """Fixe la langue du fil courant, pour toute la duree de la requete."""
    _courante.valeur = langue if langue in LANGUES else "fr"


def actuelle() -> str:
    return getattr(_courante, "valeur", "fr")


def _du_cookie(entete_cookie: str) -> str:
    for morceau in (entete_cookie or "").split(";"):
        nom, _, valeur = morceau.strip().partition("=")
        if nom == COOKIE_LANGUE and valeur in LANGUES:
            return valeur
    return ""


def _de_l_entete(accept_language: str) -> str:
    """La premiere langue reconnue de `Accept-Language`, ou ''.

    On ne lit que le DEBUT de chaque element : « en-GB » vaut « en ». Les
    poids (`;q=0.8`) sont ignores : les navigateurs listent deja par ordre de
    preference, et une gestion fine ne changerait rien a un choix binaire.
    """
    for element in (accept_language or "").split(","):
        code = element.strip().split(";")[0].strip().lower()[:2]
        if code in LANGUES:
            return code
    return ""


def detecter(entete_cookie: str = "", accept_language: str = "") -> str:
    """La langue a servir a ce visiteur. Voir l'ordre en tete de fichier."""
    return _du_cookie(entete_cookie) or _de_l_entete(accept_language) or "fr"


# ---------------------------------------------------------------------------
# Les mots du site
#
# ⚠ LA CLE EST LA PHRASE FRANCAISE, comme dans `dico-en.js` cote jeu. Deux
# avantages : le code reste lisible sans dictionnaire sous les yeux, et une
# phrase oubliee s'affiche en francais plutot que de casser la page.
#
# ⚠ ET UNE GATE LES COMPTE : `site/test_langue.py` refuse toute phrase passee a
# `t()` qui n'aurait pas sa traduction. Sans elle, l'anglais se serait degrade
# a chaque ajout, exactement comme c'est arrive au jeu le 15/09/2026.
# ---------------------------------------------------------------------------
DICO_EN: dict[str, str] = {
    # --- Le squelette de toutes les pages -----------------------------------
    "Ton espace de jeu est a toi : tes decks, tes campagnes en cours et tes "
    "hauts faits t'y attendent d'une fois sur l'autre. Eteindre le jeu "
    "n'efface rien. Tes invites, eux, rejoignent ta partie par leur lien "
    "sans avoir besoin d'un compte. Extinction automatique au bout de "
    "{heures} h d'allumage.":
        "This space is yours: your decks, your campaigns in progress and your "
        "achievements are waiting for you from one visit to the next. Shutting "
        "the game down erases nothing. Your guests join your table through "
        "their own link, no account needed. Automatic shutdown after {heures} "
        "h of uptime.",

    # --- Connexion et inscription -------------------------------------------
    "Se connecter": "Sign in",
    "Creer un compte": "Create an account",
    "Demander un compte": "Request an account",
    "Entrer": "Enter",
    "Pseudo": "Username",
    "Adresse e-mail": "Email address",
    "Pseudo ou adresse e-mail": "Username or email address",
    "Tu es invite : ton compte sera actif tout de suite.":
        "You have an invitation: your account will be active right away.",
    "Ton compte devra etre valide a la main avant de servir.":
        "Your account will have to be approved by hand before it works.",
    'Deja un compte ? <a href="/connexion">Se connecter</a>.':
        'Already have an account? <a href="/connexion">Sign in</a>.',
    'Pas encore de compte ? <a href="/inscription">En demander un</a>.':
        'No account yet? <a href="/inscription">Request one</a>.',
    "Mot de passe oublie ? Demande un lien de reinitialisation a l'administrateur.":
        "Forgotten your password? Ask the administrator for a reset link.",
    "Les places sont comptees : {jours} jours sans venir et la tienne"
    " retourne au pot. Ecris-moi, je te la rends.":
        "Seats are limited: {jours} days without visiting and yours goes back "
        "to the pool. Write to me and I will give it back.",

    # --- La barre, en haut de chaque page -----------------------------------
    "Connecte": "Signed in",
    "Se deconnecter": "Sign out",
    "Mes signalements": "My reports",

    # --- Le suivi d'un signalement ------------------------------------------
    "Ce que tu as signale, et ma reponse.": "What you reported, and my answer.",
    "Rien a suivre pour l'instant.": "Nothing to follow yet.",
    "Aucun signalement": "No reports",
    "Quand un bug te gene en partie, le bouton « Signaler un bug » l'envoie "
    "avec ta capture d'ecran et le journal de la partie. Tu retrouveras ici ma "
    "reponse.":
        "When a bug gets in your way during a game, the “Report a bug” button "
        "sends it along with your screenshot and the game log. My answer will "
        "be waiting for you here.",
    "Pas encore de reponse.": "No answer yet.",
    "Voir la capture": "View the screenshot",
    "Ajouter quelque chose": "Add something",
    "Envoyer": "Send",
    "Reponse": "Answer",
    "Moi": "Me",
    # Les quatre etats d'un ticket, tels que le joueur les lit.
    "Recu": "Received",
    "En cours": "In progress",
    "Corrige": "Fixed",
    "Refuse": "Declined",

    # --- « Ta partie t'attend » ---------------------------------------------
    "Tu etais en pleine partie.": "You were in the middle of a game.",
    "Ta partie t'attend": "Your game is waiting",
    "Interrompue le {quand}{motif}. Elle a ete sauvegardee : "
    "tu peux la reprendre la ou tu l'avais laissee.":
        "Interrupted on {quand}{motif}. It was saved: you can pick it up right "
        "where you left off.",
    "Reprendre cette partie": "Resume this game",
    "On recharge la sauvegarde et on te remet au plateau.":
        "We load the save and put you back at the table.",
    "Commencer autre chose": "Start something else",
    "La sauvegarde reste dans « Reprendre », sur l'ecran de preparation.":
        "The save stays under “Resume”, on the setup screen.",

    # --- Le temps que la table s'allume -------------------------------------
    "Un instant.": "One moment.",
    "Ton jeu demarre": "Your game is starting",
    "Le premier allumage prend une minute ou deux. "
    "Cette page bascule toute seule des que c'est pret.":
        "The first start takes a minute or two. This page will switch over on "
        "its own as soon as it is ready.",
    "Quelque chose a coince.": "Something went wrong.",
    "Ton jeu n'a pas demarre": "Your game did not start",
    "Reessayer": "Try again",

    # --- Ce qui peut refuser une connexion ou une inscription ---------------
    "Pseudo invalide : 3 a 24 caracteres, lettres, chiffres, - et _.":
        "Invalid username: 3 to 24 characters, letters, digits, - and _.",
    "Adresse e-mail invalide.": "Invalid email address.",
    "Mot de passe trop court : 8 caracteres au minimum.":
        "Password too short: 8 characters minimum.",
    "Il faut un lien d'invitation pour creer un compte ici.":
        "You need an invitation link to create an account here.",
    "Ce pseudo est deja pris.": "That username is already taken.",
    "Cette adresse est deja utilisee.": "That address is already in use.",
    "Plus aucun espace de jeu disponible.": "No game space left.",
    "Identifiant ou mot de passe incorrect.":
        "Incorrect username or password.",

    # --- Le bouton FR / EN du site ------------------------------------------
    "Changer la langue du site": "Change the language of the site",

    # --- L'appli sur le telephone -------------------------------------------
    "Installer l'application sur ce telephone":
        "Install the app on this phone",
    "Sur iPhone : bouton Partager, puis « Sur l'ecran d'accueil ».":
        "On iPhone: Share button, then “Add to Home Screen”.",
    "C'est un raccourci vers le jeu, pas une version hors ligne : "
    "il faut une connexion pour jouer.":
        "This is a shortcut to the game, not an offline version: you need a "
        "connection to play.",

    # --- Quand le reseau manque ---------------------------------------------
    "Pas de connexion": "No connection",
    "NarwhalChampions a besoin du reseau pour tourner : la partie "
    "se joue sur le serveur, pas sur ton telephone. Reconnecte-toi "
    "et reessaie.":
        "NarwhalChampions needs the network to run: the game is played on the "
        "server, not on your phone. Get back online and try again.",

    # --- Apres une reinitialisation de mot de passe -------------------------
    "Mot de passe enregistre": "Password saved",
    "Ton nouveau mot de passe est en place : connecte-toi.":
        "Your new password is set: sign in.",
}


def t(texte: str) -> str:
    """La phrase dans la langue du visiteur."""
    if actuelle() != "en":
        return texte
    return DICO_EN.get(texte, texte)
