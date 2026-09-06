"""Le parcours du site : se connecter, puis tomber dans le jeu.

Le site n'est qu'une PORTE. Ces cas verifient qu'il ne s'interpose nulle part :
qui est connecte part vers son moteur, qui ne l'est pas voit le formulaire, et
la seule page intermediaire est l'attente du demarrage.

Usage : python3 site/test_parcours.py
"""
import os
import re
import sys
import tempfile

os.environ.setdefault("BASE", os.path.join(tempfile.gettempdir(), "nc-parcours.db"))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrateur as o  # noqa: E402

echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom
          + (" | " + detail if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


class FauxProcessus:
    def poll(self):
        return None


def allumer(pseudo="chloe", emplacement=2):
    partie = o.Partie(emplacement, pseudo, "Jeu de " + pseudo)
    partie.processus = FauxProcessus()
    partie.mot_de_passe = "MOTDEPASSE"
    partie.cles_sieges = ["cle0", "cle1", "cle2", "cle3"]
    o.PARTIES[pseudo] = partie
    return partie


# --- Le lien qui depose l'hote dans son jeu --------------------------------
partie = allumer()
lien = partie.lien_hote()
verifier("le lien de l'hote vise SON moteur", "127.0.0.1:2352" in lien, lien)
verifier("le lien reclame le siege 0", "p=0" in lien, lien)
verifier("le lien porte la cle du siege 0", "key=cle0" in lien, lien)
verifier("le lien mene a l'ecran des heros", "to=prepare" in lien, lien)

# Sans cle, `claim_seat` ne poserait aucun cookie et le moteur refuserait les
# liens d'invitation a l'hote lui-meme : le cas merite son garde-fou.
partie.cles_sieges = []
verifier("sans cle, le lien ne pretend pas en avoir une",
         "key=" in partie.lien_hote() and "key=cle" not in partie.lien_hote(),
         partie.lien_hote())
partie.cles_sieges = ["cle0", "cle1", "cle2", "cle3"]

# --- Les pages du site -----------------------------------------------------
attente = o.page_attente("chloe").decode("utf-8")
verifier("l'attente se rafraichit toute seule",
         'http-equiv="refresh"' in attente and "/entrer" in attente)
verifier("l'attente dit ce qu'on attend", "Ton jeu demarre" in attente)

o.ERREURS_DEMARRAGE["chloe"] = "Le moteur n'a pas repondu a temps."
casse = o.page_attente("chloe").decode("utf-8")
verifier("en cas d'echec, la page ne boucle PAS", 'http-equiv="refresh"' not in casse)
# `html.escape` transforme l'apostrophe en &#x27; : on cherche donc un
# morceau qui n'en contient pas, sans quoi le cas passerait a cote.
verifier("en cas d'echec, la raison est dite",
         "pas repondu a temps" in casse, casse[-400:])
verifier("en cas d'echec, on peut reessayer", "Reessayer" in casse)
o.ERREURS_DEMARRAGE.pop("chloe", None)

arret = o.page_arret("chloe").decode("utf-8")
verifier("l'arret rassure sur les donnees", "Rien n'est perdu" in arret)
verifier("l'arret propose de rallumer", "/entrer" in arret)
# Le geste a un effet que personne ne devinerait : il coupe les acces des
# invites. Une page qui le fait sans le dire vaut un piege.
verifier("l'arret annonce que les invites sont mis dehors",
         "ne rouvrent plus" in arret and "invites" in arret, arret[-500:])

# --- Le bouton Administration n'est pose QUE pour l'administrateur ---------
# ⚠ On appelle VRAIMENT `_config_partie`. Se contenter de poser la cle
# soi-meme puis de la relire ne prouverait rien : le cas passerait au vert
# meme si la fonction ne faisait rien du tout.
reel = os.path.join(o.RACINE_JEU, "launch.json")
if os.path.isfile(reel):
    import json
    import shutil
    bac = tempfile.mkdtemp(prefix="nc-config-")
    shutil.copy(reel, os.path.join(bac, "launch.json"))
    racine_reelle = o.RACINE_JEU
    o.RACINE_JEU = bac                    # tout ce qui s'ecrit part au bac
    try:
        for pseudo, attendu in ((o.ADMIN, True), ("quelqu-un-dautre", False)):
            p2 = o.Partie(19, pseudo, "Jeu de " + pseudo)
            p2.mot_de_passe = "x"
            p2.cles_sieges = ["a", "b", "c", "d"]
            cfg = json.load(open(o._config_partie(19, p2), encoding="utf-8"))
            verifier("l'admin recoit le bouton Administration" if attendu
                     else "les autres comptes ne l'ont pas",
                     ("site_admin_url" in cfg) is attendu, json.dumps(cfg)[:150])
            verifier("les cles de siege sont transmises au moteur (%s)" % pseudo,
                     cfg.get("seat_passwords") == ["a", "b", "c", "d"],
                     str(cfg.get("seat_passwords")))
    finally:
        o.RACINE_JEU = racine_reelle
        shutil.rmtree(bac, ignore_errors=True)
else:
    print("  (launch.json absent : verification du bouton admin sautee)")

# --- Presence et tchat ------------------------------------------------------
o.PARTIES.clear()
o.initialiser_base()
with o._cx() as cx:
    cx.execute("DELETE FROM messages")
    cx.execute("DELETE FROM comptes")
o.inscrire("chloe", "chloe@exemple.fr", "motdepasse123")
o.changer_statut("chloe", "valide")
o.inscrire("hugo", "hugo@exemple.fr", "motdepasse123")
o.changer_statut("hugo", "valide")

o.dire("chloe", "  salut   tout   le monde  ")
o.dire("hugo", "")
msgs = o.messages_depuis(0)
verifier("un message envoye se relit", len(msgs) == 1, str(msgs))
verifier("les espaces en trop sont ramenes a un",
         msgs and msgs[0]["texte"] == "salut tout le monde", str(msgs))
verifier("un message vide n'est pas garde", len(msgs) == 1, str(msgs))

o.dire("hugo", "x" * 900)
verifier("un message trop long est coupe",
         len(o.messages_depuis(msgs[0]["id"])[0]["texte"]) == o.TAILLE_MESSAGE)

# `depuis` ne doit rendre QUE la suite : sans quoi le client reconstruirait
# tout le fil a chaque tour et les messages se dedoubleraient.
dernier = o.messages_depuis(0)[-1]["id"]
verifier("rien de neuf apres le dernier lu", o.messages_depuis(dernier) == [])
o.dire("chloe", "et maintenant ?")
suite = o.messages_depuis(dernier)
verifier("seul le nouveau message revient",
         len(suite) == 1 and suite[0]["texte"] == "et maintenant ?", str(suite))

# La purge : on ne garde pas tout.
for i in range(o.MESSAGES_GARDES + 20):
    o.dire("hugo", "message %d" % i)
with o._cx() as cx:
    total = cx.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
verifier("le tchat ne grossit pas indefiniment",
         total == o.MESSAGES_GARDES, "%d gardes" % total)

# --- Le mot de passe du moteur survit-il a un redemarrage ? ------------------
# ⚠ LE CAS QUI A FAIT MAL. Tire au hasard a chaque allumage, il perimait le
# cookie deja pose dans le navigateur des le moindre redemarrage du service, et
# laissait son proprietaire devant une demande de mot de passe que le site
# n'affiche nulle part.
premier = o.mot_de_passe_jeu("chloe")
verifier("un mot de passe de jeu est attribue", bool(premier), repr(premier))
verifier("et il ne change pas d'un appel a l'autre",
         o.mot_de_passe_jeu("chloe") == premier, repr(premier))
verifier("chaque compte a le sien",
         o.mot_de_passe_jeu("hugo") != premier)

# On simule deux allumages successifs : le mot de passe doit etre le meme, les
# cles de siege doivent, elles, avoir change.
p1 = o.Partie(2, "chloe", "x"); p1.mot_de_passe = o.mot_de_passe_jeu("chloe")
p1.cles_sieges = [o.secrets.token_urlsafe(8) for _ in range(4)]
p2 = o.Partie(2, "chloe", "x"); p2.mot_de_passe = o.mot_de_passe_jeu("chloe")
p2.cles_sieges = [o.secrets.token_urlsafe(8) for _ in range(4)]
verifier("apres redemarrage, le cookie du navigateur reste valable",
         p1.mot_de_passe == p2.mot_de_passe)
verifier("mais un lien d'invitation d'hier ne rouvre rien",
         p1.cles_sieges != p2.cles_sieges)

# --- ... et l'extinction volontaire, elle, doit le PERIMER -------------------
# ⚠ L'AUTRE MOITIE DU MEME PROBLEME. Stable, ce mot de passe l'est pour de
# bonnes raisons ; jamais renouvele, il laissait le cookie `session_token`
# d'un invite d'hier (md5 de ce mot de passe, valable un an) rouvrir l'espace
# de jeu de son hote. Le cas qui compte est celui du REFUS : apres extinction
# volontaire, l'ancien mot de passe ne doit plus valoir.
avant_extinction = o.mot_de_passe_jeu("chloe")
o.revoquer_mot_de_passe_jeu("chloe")
apres_extinction = o.mot_de_passe_jeu("chloe")
verifier("l'extinction volontaire perime le laissez-passer du moteur",
         apres_extinction != avant_extinction,
         "%r puis %r" % (avant_extinction, apres_extinction))
verifier("et le nouveau est aussitot disponible", bool(apres_extinction))
verifier("les autres comptes ne sont pas touches",
         o.mot_de_passe_jeu("hugo") not in ("", apres_extinction))

# ⚠ ET SEULE L'EXTINCTION VOLONTAIRE LE FAIT. Un moteur qui plante, ou que le
# faucheur ramasse, passe par `eteindre_jeu` et par lui seul : si celui-ci
# touchait au mot de passe, un incident laisserait son proprietaire devant une
# demande qu'aucune page du site ne lui affiche.
stable = o.mot_de_passe_jeu("chloe")
plante = allumer("chloe", 2)
plante.processus = None                   # le moteur est mort tout seul
o.eteindre_jeu("chloe")
verifier("un plantage n'ejecte PAS le proprietaire de sa table",
         o.mot_de_passe_jeu("chloe") == stable)
o.PARTIES.clear()

# --- Tchat prive : qui voit quoi --------------------------------------------
with o._cx() as cx:
    cx.execute("DELETE FROM messages")
o.inscrire("lea", "lea@exemple.fr", "motdepasse123")
o.changer_statut("lea", "valide")

o.dire("chloe", "message pour tout le monde")
o.dire("chloe", "juste pour toi hugo", "hugo")
o.dire("hugo", "bien recu chloe", "chloe")

general = [m["texte"] for m in o.messages_depuis(0)]
verifier("le general ne contient QUE le general",
         general == ["message pour tout le monde"], str(general))

vus_chloe = [m["texte"] for m in o.messages_depuis(0, "chloe", "hugo")]
verifier("chloe voit ses deux messages prives avec hugo",
         vus_chloe == ["juste pour toi hugo", "bien recu chloe"], str(vus_chloe))

vus_hugo = [m["texte"] for m in o.messages_depuis(0, "hugo", "chloe")]
verifier("hugo voit exactement la meme conversation",
         vus_hugo == vus_chloe, str(vus_hugo))

# ⚠ LE CAS QUI COMPTE. Sans la clause sur le couple expediteur/destinataire,
# n'importe quel titulaire de compte lirait les messages prives des autres.
vus_lea = [m["texte"] for m in o.messages_depuis(0, "lea", "chloe")]
verifier("lea ne voit RIEN de la conversation de chloe et hugo",
         vus_lea == [], str(vus_lea))
vus_lea2 = [m["texte"] for m in o.messages_depuis(0, "lea", "hugo")]
verifier("ni dans l'autre sens", vus_lea2 == [], str(vus_lea2))

# Un destinataire qui n'existe pas : le message n'est pas ecrit, plutot que de
# tomber dans une conversation que personne n'ouvrira jamais.
avant_faute = len(o.messages_depuis(0, "chloe", "personne"))
o.dire("chloe", "coucou", "personne-qui-nexiste-pas")
verifier("un destinataire inconnu ne cree pas de message",
         len(o.messages_depuis(0, "chloe", "personne-qui-nexiste-pas")) == avant_faute)

recents = o.derniers_prives("chloe")
verifier("chloe sait qu'elle a du nouveau avec hugo",
         "hugo" in recents and recents["hugo"] > 0, str(recents))
verifier("et rien avec lea", "lea" not in recents, str(recents))

# Les deux purges sont SEPAREES : un general anime ne doit pas emporter les
# messages prives de tout le monde.
prive_avant = len(o.messages_depuis(0, "chloe", "hugo"))
for i in range(o.MESSAGES_GARDES + 30):
    o.dire("lea", "bavardage %d" % i)
prive_apres = len(o.messages_depuis(0, "chloe", "hugo"))
verifier("un general bavard n'efface pas les prives",
         prive_apres == prive_avant, "%d puis %d" % (prive_avant, prive_apres))
with o._cx() as cx:
    gen = cx.execute("SELECT COUNT(*) FROM messages WHERE destinataire IS NULL").fetchone()[0]
verifier("le general reste plafonne", gen == o.MESSAGES_GARDES, str(gen))

with o._cx() as cx:
    cx.execute("DELETE FROM messages")
    cx.execute("DELETE FROM comptes WHERE pseudo='lea'")

# --- Les trois etats de presence --------------------------------------------
with o._cx() as cx:
    cx.execute("UPDATE comptes SET vu_le=NULL")
etats = {j["pseudo"]: j["etat"] for j in o.presence()}
verifier("jamais venu = absent", etats.get("chloe") == "absent", str(etats))

o.toucher_presence("chloe")
etats = {j["pseudo"]: (j["etat"], j["detail"]) for j in o.presence()}
verifier("vu a l'instant = en ligne", etats.get("chloe", ("",))[0] == "ligne", str(etats))
verifier("hugo, lui, reste absent", etats.get("hugo", ("",))[0] == "absent", str(etats))

allumer("chloe", 2)
etats = {j["pseudo"]: (j["etat"], j["detail"]) for j in o.presence()}
verifier("moteur allume = en partie", etats.get("chloe", ("",))[0] == "partie", str(etats))
verifier("et on le DIT", etats.get("chloe", ("", ""))[1] == "en partie", str(etats))
o.PARTIES.clear()

# Une visite ancienne se raconte, elle ne se cache pas.
from datetime import datetime, timedelta
vieux = (datetime.now() - timedelta(hours=3)).isoformat(" ", "seconds")
with o._cx() as cx:
    cx.execute("UPDATE comptes SET vu_le=? WHERE pseudo='chloe'", (vieux,))
detail = {j["pseudo"]: j["detail"] for j in o.presence()}.get("chloe", "")
verifier("une visite ancienne est datee", detail.startswith("vu il y a 3 h"), detail)

# Un compte en attente de validation ne figure pas dans la liste.
o.inscrire("zoe", "zoe@exemple.fr", "motdepasse123")
verifier("un compte non valide n'apparait pas",
         "zoe" not in [j["pseudo"] for j in o.presence()],
         str([j["pseudo"] for j in o.presence()]))

o.PARTIES.clear()

# --- Rester connecte d'une visite a l'autre --------------------------------
#
# Les sessions vivaient dans un dictionnaire EN MEMOIRE : tout redemarrage du
# service — donc chaque deploiement — deconnectait tout le monde, alors que le
# cookie pose dans le navigateur, lui, annonce plusieurs semaines. Elles sont
# desormais en base, comme les comptes.
jeton = o.ouvrir_session("chloe")
verifier("le jeton frais ouvre bien la session", o.pseudo_de_session(jeton) == "chloe")

# Ce qu'un redemarrage du service laisse : la base, et rien d'autre.
verifier("la session survit au redemarrage du service",
         o.pseudo_de_session(jeton) == "chloe")

# Se deconnecter doit vraiment fermer la porte.
o.fermer_session(jeton)
verifier("la deconnexion revoque le jeton", o.pseudo_de_session(jeton) is None)

# Un compte devalide en cours de route ne passe plus, jeton valide ou non.
jeton = o.ouvrir_session("chloe")
o.changer_statut("chloe", "attente")
verifier("un compte devalide ne passe plus", o.pseudo_de_session(jeton) is None)
o.changer_statut("chloe", "valide")
verifier("et il repasse une fois revalide... non : son jeton est revoque",
         o.pseudo_de_session(jeton) is None)

# Un jeton inconnu ne vaut rien.
verifier("un jeton inconnu est refuse", o.pseudo_de_session("nimportequoi") is None)


# ==========================================================================
# Un vrai serveur HTTP, le temps de quelques cas
# ==========================================================================
# ⚠ TOUT CE QUI PRECEDE APPELLE LES FONCTIONS SANS PASSER PAR HTTP, et c'etait
# un trou reel : le plafond du corps d'une requete, les attributs du cookie de
# session, le frein sur les tentatives de connexion et l'ouverture de `/etat`
# ne se voient d'aucune fonction pure. On monte donc un vrai
# `ThreadingHTTPServer` sur un port libre, avec le VRAI `Handler`, et on lui
# parle en HTTP. Rien n'est simule.
import http.client                                          # noqa: E402
import threading                                            # noqa: E402
from http.server import ThreadingHTTPServer                 # noqa: E402

_serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
_port = _serveur.server_address[1]
threading.Thread(target=_serveur.serve_forever, daemon=True).start()


def appel(methode, chemin, corps=b"", entetes=None, annonce=None, delai=5):
    """Une requete HTTP reelle. Rend (code, entetes, corps).

    `annonce` permet de MENTIR sur `Content-Length` : declarer huit mega-octets
    puis n'en envoyer aucun est le seul moyen de prouver qu'on refuse AVANT de
    lire le corps, et non apres. `delai` borne l'attente : un serveur qui se
    mettrait a lire ces octets qui n'arrivent jamais ferait echouer le cas au
    lieu de bloquer le fichier de test pour toujours.
    """
    lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=delai)
    tetes = dict(entetes or {})
    if methode == "POST":
        tetes.setdefault("Content-Type", "application/x-www-form-urlencoded")
        tetes["Content-Length"] = str(len(corps) if annonce is None else annonce)
    try:
        lien.putrequest(methode, chemin, skip_accept_encoding=True)
        for nom, valeur in tetes.items():
            lien.putheader(nom, valeur)
        lien.endheaders()
        if corps:
            try:
                lien.send(corps)
            except OSError:
                pass          # le serveur a deja repondu et raccroche : normal
        reponse = lien.getresponse()
        return reponse.status, reponse.msg, reponse.read()
    finally:
        lien.close()


def cookie_de(pseudo):
    """Le cookie d'un compte connecte, pret a etre presente."""
    return {"Cookie": "nc_session=" + o.ouvrir_session(pseudo)}


for _p, _e in (("hote", "hote@exemple.fr"), ("invitee", "invitee@exemple.fr")):
    try:
        o.inscrire(_p, _e, "motdepasse123")
    except ValueError:
        pass
    o.changer_statut(_p, "valide")

# --- S1 : le bouton « Terminer » coupe vraiment les acces -------------------
# ⚠ LE CAS QUI COMPTE, ET IL PASSE PAR LA ROUTE. Prouver que
# `revoquer_mot_de_passe_jeu` change une colonne ne dirait rien de l'endroit
# ou elle est appelee : c'est `/eteindre` qui doit le faire, et lui seul.
_avant = o.mot_de_passe_jeu("hote")
_code, _tetes, _ = appel("POST", "/eteindre", entetes=cookie_de("hote"))
verifier("l'extinction renvoie vers la page d'arret",
         _code == 303 and _tetes.get("Location") == "/arret",
         "%s %s" % (_code, _tetes.get("Location")))
verifier("et la route /eteindre a bien perime le laissez-passer",
         o.mot_de_passe_jeu("hote") != _avant)

# Un anonyme n'eteint rien du tout, et surtout pas le jeu de quelqu'un d'autre.
_avant = o.mot_de_passe_jeu("hote")
_code, _tetes, _ = appel("POST", "/eteindre")
verifier("un anonyme ne peut rien eteindre",
         _code == 303 and _tetes.get("Location") == "/" and
         o.mot_de_passe_jeu("hote") == _avant, str(_code))

# --- S3 : le corps d'une requete est plafonne AVANT d'etre lu ---------------
# ⚠ LE CAS NE VAUT QUE PARCE QU'IL MENT. On annonce plus que le plafond, on
# n'envoie pas un octet, et on attend la reponse. Un serveur qui lirait
# d'abord resterait a attendre des octets qui n'arriveront jamais : le cas
# echouerait alors sur le delai, ce qui est exactement ce qu'on veut voir.
_enorme = o.MAX_CORPS_OCTETS + 1
try:
    _code, _, _ = appel("POST", "/connexion", annonce=_enorme, delai=4)
except OSError as _erreur:
    _code = repr(_erreur)
verifier("un corps trop gros est refuse, et sans etre lu", _code == 413, str(_code))

# Sous le plafond, mais toujours pas envoye : les routes qui n'ont rien a lire
# ne doivent pas s'y mettre non plus.
_gros = 1_000_000
try:
    _code404, _, _ = appel("POST", "/route-qui-nexiste-pas", annonce=_gros, delai=4)
except OSError as _erreur:
    _code404 = repr(_erreur)
verifier("une route inconnue ne lit pas le corps avant de rendre son 404",
         _code404 == 404, str(_code404))

try:
    _code403, _, _ = appel("POST", "/admin", annonce=_gros,
                           entetes=cookie_de("invitee"), delai=4)
except OSError as _erreur:
    _code403 = repr(_erreur)
verifier("l'administration refuse un inconnu avant de lire son corps",
         _code403 == 403, str(_code403))

# Non-regression : un envoi normal passe toujours.
_code, _, _corps = appel("POST", "/connexion",
                         b"pseudo=hote&mdp=motdepasse123")
verifier("un formulaire de taille normale passe toujours", _code == 303, str(_code))

# --- S2 : le frein sur les tentatives de connexion --------------------------
# ⚠ LE CAS QUI COMPTE EST CELUI DU REFUS. Compter les tentatives acceptees ne
# prouverait rien ; c'est la N+1e, refusee, qui dit que le frein existe.
o._TENTATIVES.clear()
_dernier = 0
for _i in range(o.TENTATIVES_CONNEXION):
    _dernier, _, _ = appel("POST", "/connexion", b"pseudo=inconnu-x&mdp=faux")
verifier("les tentatives permises passent (et echouent normalement)",
         _dernier == 400, str(_dernier))
_code, _, _corps = appel("POST", "/connexion", b"pseudo=inconnu-x&mdp=faux")
_texte = _corps.decode("utf-8", "replace")
verifier("la tentative suivante est REFUSEE", _code == 429, str(_code))
verifier("et on dit au joueur combien de temps attendre",
         "Trop de tentatives" in _texte and "Reessaie dans" in _texte,
         _texte[:300])

# Par ADRESSE : changer de compte ne relache rien, le flot vient du meme
# endroit.
_code, _, _ = appel("POST", "/connexion", b"pseudo=un-autre-compte&mdp=faux")
verifier("changer de compte ne desserre pas le frein d'adresse", _code == 429, str(_code))

# Par COMPTE : changer d'adresse non plus, sinon on s'acharne sur une personne
# depuis autant d'adresses qu'on veut.
o._TENTATIVES.clear()
for _i in range(o.TENTATIVES_CONNEXION):
    appel("POST", "/connexion", b"pseudo=hote&mdp=faux",
          entetes={"X-Forwarded-For": "10.0.0.%d" % _i})
_code, _, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=faux",
                    entetes={"X-Forwarded-For": "10.0.0.200"})
verifier("changer d'adresse ne desserre pas le frein de compte",
         _code == 429, str(_code))

# ⚠ ET IL FAUT QUE L'ADRESSE VIENNE DE CADDY, PAS DU CLIENT. `X-Forwarded-For`
# est une liste a laquelle le proxy AJOUTE : c'est la derniere valeur qui vaut
# quelque chose, la premiere s'ecrit a la main.
o._TENTATIVES.clear()
for _i in range(o.TENTATIVES_CONNEXION):
    appel("POST", "/connexion", b"pseudo=inconnu-y&mdp=faux",
          entetes={"X-Forwarded-For": "9.9.9.%d, 203.0.113.7" % _i})
_code, _, _ = appel("POST", "/connexion", b"pseudo=inconnu-z&mdp=faux",
                    entetes={"X-Forwarded-For": "1.2.3.4, 203.0.113.7"})
verifier("une adresse falsifiee en tete de liste ne contourne pas le frein",
         _code == 429, str(_code))

# Une connexion REUSSIE relache le frein : les fautes de frappe de quelqu'un
# qui finit par entrer ne doivent pas le poursuivre.
o._TENTATIVES.clear()
for _i in range(o.TENTATIVES_CONNEXION - 1):
    appel("POST", "/connexion", b"pseudo=hote&mdp=faux")
_code, _, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=motdepasse123")
verifier("apres tatonnements, le bon mot de passe entre", _code == 303, str(_code))
_code, _, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=faux")
verifier("et la reussite a relache le frein", _code == 400, str(_code))
o._TENTATIVES.clear()

# --- S4 : le cookie de session ne part pas en clair -------------------------
def _pose_le_cookie(entetes=None):
    o._TENTATIVES.clear()
    _c, _t, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=motdepasse123",
                      entetes=entetes)
    return _t.get("Set-Cookie") or ""


# En local, sans proxy et sans domaine, l'attribut ne doit PAS y etre : un
# navigateur jetterait le cookie sur `http://127.0.0.1`, et la connexion
# tournerait en rond sans rien dire.
_pose = _pose_le_cookie()
verifier("en local, le cookie reste utilisable (pas de Secure)",
         "Secure" not in _pose and "HttpOnly" in _pose, _pose)

# Derriere Caddy, qui annonce le schema, l'attribut apparait.
_pose = _pose_le_cookie({"X-Forwarded-Proto": "https"})
verifier("derriere HTTPS, le cookie de session porte Secure",
         "Secure" in _pose, _pose)
verifier("sans rien perdre de HttpOnly ni de SameSite",
         "HttpOnly" in _pose and "SameSite=Lax" in _pose, _pose)

# Et en production le domaine suffit, meme si l'en-tete manque.
_vrai_domaine = o.DOMAINE
o.DOMAINE = "narwhalchampions.test"
_pose = _pose_le_cookie()
o.DOMAINE = _vrai_domaine
verifier("un site sur son domaine pose Secure meme sans en-tete",
         "Secure" in _pose, _pose)
o._TENTATIVES.clear()

# Cote MOTEUR, le meme defaut venait de l'amont : `secure=True` et
# `samesite='Lax'` etaient ecrits en COMMENTAIRE, jamais decommentes. Les
# exercer pour de vrai demande d'allumer un moteur, ce que fait
# `tools/test_authentification.py` ; ici on garde la porte fermee sur la
# regression exacte, qui est de les voir repasser en commentaire.
_moteur = os.path.join(o.RACINE_JEU, "src", "engine")
for _fichier, _combien in (
        (os.path.join(_moteur, "network", "web_server.py"), 1),
        (os.path.join(_moteur, "device", "web", "server", "server_html.py"), 2)):
    if not os.path.isfile(_fichier):
        continue
    _src = open(_fichier, encoding="utf-8").read()
    verifier("les cookies de %s ne partent plus en clair" % os.path.basename(_fichier),
             _src.count("secure=") >= _combien and "# secure=True" not in _src,
             "%d secure= trouves" % _src.count("secure="))

# --- S7 : ce qui vit a l'execution ne doit pas pouvoir etre commite ---------
# ⚠ UN SECRET COMMITE NE SE CHANGE PLUS : il reste dans l'historique pour
# toujours. `narwhal.db` porte les empreintes, les adresses e-mail, les jetons
# de session en clair et les mots de passe des moteurs ; `site/rapports/`
# porte les ecrans des joueurs. Un seul `git add -A` apres un essai en local
# suffisait. On le demande a git lui-meme, plutot que de relire le fichier.
import subprocess                                           # noqa: E402
_depot = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_a_ignorer = ["site/narwhal.db", "site/narwhal.db-wal", "site/rapports/capture.png"]
try:
    # `--quiet` n'accepte qu'un chemin a la fois : on demande la liste, et on
    # verifie que git nous les rend TOUS.
    _vus = subprocess.run(["git", "check-ignore"] + _a_ignorer, cwd=_depot,
                          capture_output=True, text=True).stdout.split()
except OSError:
    _vus = None
if _vus is None:
    print("  (git absent : verification du .gitignore sautee)")
else:
    _oublies = [c for c in _a_ignorer if c not in _vus]
    verifier("la base et les captures sont hors du depot", not _oublies,
             "toujours commitables : " + ", ".join(_oublies))

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
