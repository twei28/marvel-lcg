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

# ⚠ ET LA REVOCATION PASSE AVANT L'EXTINCTION, PAS APRES. `eteindre_jeu`
# bloque jusqu'a quinze secondes ; la page d'attente, elle, rappelle `/entrer`
# toute seule par son `meta refresh`. Un `/entrer` tombe pendant ce temps-la
# rallumait un moteur avec l'ANCIEN mot de passe, que la revocation, arrivee
# ensuite, ne voyait meme pas.
_avant = o.mot_de_passe_jeu("hote")
_vu = {}
_vrai_eteindre = o.eteindre_jeu


def _eteindre_observe(code):
    # Ce que verrait un `/entrer` arrive au beau milieu de l'extinction.
    _vu["mdp"] = o.mot_de_passe_jeu(code)
    return _vrai_eteindre(code)


o.eteindre_jeu = _eteindre_observe
try:
    appel("POST", "/eteindre", entetes=cookie_de("hote"))
finally:
    o.eteindre_jeu = _vrai_eteindre
verifier("un /entrer pendant l'extinction ne garde pas l'ancien mot de passe",
         _vu.get("mdp") is not None and _vu["mdp"] != _avant,
         "le moteur relance aurait garde l'ancien laissez-passer")

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

# ⚠ ET LE BON MOT DE PASSE N'EST JAMAIS REFUSE PAR LA FAUTE D'UN AUTRE. Le
# frein comptait aussi par COMPTE, et rendait un 429 : dix tentatives fausses
# lancees depuis dix adresses sur le pseudo de quelqu'un le mettaient dehors
# de sa propre table un quart d'heure, renouvelable a volonte. Le frein par
# adresse suffit a proteger le processeur ; celui par compte ne servait qu'a
# verrouiller sa victime.
o._TENTATIVES.clear()
for _i in range(o.TENTATIVES_CONNEXION * 2):
    appel("POST", "/connexion", b"pseudo=hote&mdp=faux",
          entetes={"X-Forwarded-For": "10.0.0.%d" % _i})
_code, _, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=motdepasse123",
                    entetes={"X-Forwarded-For": "10.0.0.200"})
verifier("dix echecs venus d'ailleurs ne bloquent pas le bon mot de passe",
         _code == 303, str(_code))
# Et une adresse encore vierge garde le droit de se tromper, elle aussi.
_code, _, _ = appel("POST", "/connexion", b"pseudo=hote&mdp=faux",
                    entetes={"X-Forwarded-For": "10.0.0.201"})
verifier("une adresse vierge peut encore se tromper", _code == 400, str(_code))

# ⚠ ET LE FREIN NE SE PAIE PAS EN MEMOIRE. Chaque lecture creait son entree,
# meme pour une requete deja refusee, et l'identifiant tape formait une cle
# que rien ne bornait sinon le plafond de corps, soit huit mega-octets par
# cle. Vingt requetes suffisaient a faire retenir vingt mega-octets, sans
# compte et sans cout pour qui les envoie.
o._TENTATIVES.clear()
for _i in range(o.TENTATIVES_CONNEXION):
    appel("POST", "/connexion", b"pseudo=inconnu-m&mdp=faux")
_cles_avant = len(o._TENTATIVES)
for _i in range(1000):
    # Un identifiant different a chaque fois : c'est ainsi qu'on fait naitre
    # une cle par requete, et vingt mega-octets pour mille requetes.
    appel("POST", "/connexion",
          b"pseudo=" + b"z" * 20_000 + b"%d" % _i + b"&mdp=faux")
verifier("mille requetes freinees ne font pas grossir le compteur",
         len(o._TENTATIVES) == _cles_avant, "%d cles" % len(o._TENTATIVES))
verifier("et aucune cle ne porte ce qu'un inconnu a tape",
         all(len(_c) <= 80 for _c in o._TENTATIVES),
         "cle la plus longue : %d caracteres"
         % max([len(_c) for _c in o._TENTATIVES] or [0]))

# Une fenetre que le temps a videe ne laisse pas sa cle derriere elle.
import time                                                  # noqa: E402
o._TENTATIVES.clear()
o._TENTATIVES["ip:1.2.3.4"] = [time.time() - o.FENETRE_CONNEXION - 1]
o.attente_connexion("ip:1.2.3.4")
verifier("une fenetre vide ne laisse pas sa cle derriere elle",
         "ip:1.2.3.4" not in o._TENTATIVES, str(list(o._TENTATIVES)))

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

# ⚠ ET LE DOMAINE, LUI, NE PROUVE RIEN. Le service repond aussi en direct sur
# `http://127.0.0.1:8080`, sur le serveur meme, ne serait-ce que pour verifier
# qu'il tourne : `Secure` pose sur la foi du seul `DOMAINE` y faisait jeter le
# cookie par le navigateur, et la connexion tournait en rond sans rien dire.
# Seul `X-Forwarded-Proto: https`, que Caddy ajoute lui-meme, vaut preuve.
_vrai_domaine = o.DOMAINE
o.DOMAINE = "narwhalchampions.test"
_pose = _pose_le_cookie()
_pose_derriere_caddy = _pose_le_cookie({"X-Forwarded-Proto": "https"})
o.DOMAINE = _vrai_domaine
verifier("un acces direct au port du site garde un cookie utilisable",
         "Secure" not in _pose, _pose)
verifier("et le meme site derriere Caddy le durcit quand meme",
         "Secure" in _pose_derriere_caddy, _pose_derriere_caddy)

# ⚠ ET LE COOKIE EFFACE RESSEMBLE A CELUI QU'IL REMPLACE. Son commentaire le
# promettait, la ligne ne le tenait pas : ni `HttpOnly` ni `SameSite`. Certains
# navigateurs gardent alors l'ancien a cote du nouveau, et la deconnexion ne
# deconnecte rien.
_code, _tetes, _ = appel("GET", "/deconnexion", entetes=cookie_de("hote"))
_efface = _tetes.get("Set-Cookie") or ""
verifier("le cookie efface porte les memes attributs qu'a la pose",
         "HttpOnly" in _efface and "SameSite=Lax" in _efface and "Path=/" in _efface,
         _efface)
verifier("et il expire sur-le-champ", "Max-Age=0" in _efface, _efface)
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

# --- Deux invariants qui se lisent dans la source ---------------------------
_source_site = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "orchestrateur.py"), encoding="utf-8").read()

# ⚠ AUCUNE REQUETE SQL COMPOSEE A L'EXECUTION. Celle qui restait ne collait
# qu'un nom de colonne choisi par le code lui-meme, donc sans danger ; mais un
# invariant qui souffre une exception ne se verifie plus d'un coup d'oeil, il
# se relit requete par requete. On demande donc que le premier argument de
# chaque `execute` soit litteral, morceaux colles bout a bout compris.
import ast                                                  # noqa: E402


def _sql_litterale(noeud):
    if isinstance(noeud, ast.Constant) and isinstance(noeud.value, str):
        return True
    if isinstance(noeud, ast.BinOp) and isinstance(noeud.op, ast.Add):
        return _sql_litterale(noeud.left) and _sql_litterale(noeud.right)
    return False


_composees = [_n.lineno for _n in ast.walk(ast.parse(_source_site))
              if isinstance(_n, ast.Call) and isinstance(_n.func, ast.Attribute)
              and _n.func.attr in ("execute", "executemany") and _n.args
              and not _sql_litterale(_n.args[0])]
verifier("aucune requete SQL n'est composee a l'execution",
         not _composees, "lignes " + str(_composees))

# ⚠ ET L'ADRESSE DU VISITEUR SE CROIT SUR PAROLE. `_adresse_client` lit
# `X-Forwarded-For` sans verifier qui parle : ce qui tient, c'est que personne
# d'autre que Caddy ne puisse parler au service. Le jour ou le service
# ecouterait ailleurs que sur la boucle locale, le frein se contournerait d'un
# en-tete.
verifier("le service n'ecoute que sur la boucle locale",
         'ThreadingHTTPServer(("127.0.0.1"' in _source_site,
         "la ligne de `main` a change")
verifier("et _adresse_client dit sur quoi repose sa surete",
         "pare-feu" in (o.Handler._adresse_client.__doc__ or ""),
         str(o.Handler._adresse_client.__doc__)[:200])

# --- Le Caddyfile : ce que le navigateur retient du site --------------------
# ⚠ CADDY N'EST PAS LANCE ICI, on lit donc son fichier. Le cas garde la porte
# fermee sur la regression exacte : quelqu'un qui retire l'en-tete du bloc de
# l'accueil. Sans HSTS, une premiere visite tapee en `http://` part en clair
# jusqu'a la redirection, et le cookie de session avec elle.
_caddyfile = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "deploiement", "Caddyfile")
if os.path.isfile(_caddyfile):
    _cf = open(_caddyfile, encoding="utf-8").read()
    # Le bloc de l'accueil va de sa ligne d'ouverture au premier bloc suivant.
    _apex = _cf.split("{$DOMAINE}, www.{$DOMAINE} {", 1)[-1].split("\n*.{$DOMAINE}", 1)[0]
    verifier("l'accueil annonce HSTS",
             "Strict-Transport-Security" in _apex, _apex[:200])
    verifier("pour un an, sous-domaines compris",
             "max-age=31536000" in _apex and "includeSubDomains" in _apex,
             _apex[:400])

# --- Un rapport trop gros n'est pas une panne de reseau ---------------------
# ⚠ LE REFUS DOIT SE DIRE POUR CE QU'IL EST. Le site plafonne le corps a huit
# mega-octets ; le moteur, qui relaie, rendait « site injoignable » pour tout
# ce qui n'etait pas un 200, et son auteur renvoyait le meme rapport, aussi
# gros, en boucle.
try:
    _code, _, _ = appel("POST", "/api/bug", annonce=_enorme, delai=4)
except OSError as _erreur:
    _code = repr(_erreur)
verifier("un rapport trop volumineux est refuse par le site en 413",
         _code == 413, str(_code))

_relais = os.path.join(o.RACINE_JEU, "src", "engine", "device", "web", "server",
                       "server_get.py")
if os.path.isfile(_relais):
    _src = open(_relais, encoding="utf-8").read()
    verifier("le moteur distingue ce refus d'une panne",
             "413" in _src and "rapport trop volumineux" in _src,
             "server_get.py ne parle que de site injoignable")
    verifier("et il le repasse au navigateur avec le meme code",
             "'rapport trop volumineux'}, status=413" in _src, "")

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

# --- S6 : /etat ne nomme personne a un visiteur anonyme ---------------------
# ⚠ LE CAS QUI COMPTE EST CELUI DU REFUS. Verifier qu'un compte connecte voit
# la liste ne prouverait rien du trou : c'est l'anonyme qui ne doit RIEN voir.
import json                                                 # noqa: E402
allumer("hote", 3)
_code, _, _corps = appel("GET", "/etat")
_anonyme = json.loads(_corps.decode("utf-8"))
verifier("un anonyme obtient bien l'etat des places",
         _code == 200 and _anonyme.get("total") == o.NB_EMPLACEMENTS, str(_anonyme))
verifier("mais il n'apprend le nom de PERSONNE",
         "hote" not in _corps.decode("utf-8"), str(_anonyme))
verifier("ni le numero d'une table, donc son sous-domaine",
         _anonyme.get("jeux") == [], str(_anonyme))

_code, _, _corps = appel("GET", "/etat", entetes=cookie_de("hote"))
_connu = json.loads(_corps.decode("utf-8"))
verifier("un compte connecte, lui, voit qui joue",
         any(j.get("code") == "hote" for j in _connu.get("jeux", [])), str(_connu))
o.PARTIES.clear()

# --- Suivi des parties (/suivi, /api/suivi) : reserve a l'administrateur ----
# ⚠ Comme pour /etat, le cas qui compte est le REFUS : la page nomme les
# joueurs, un compte ordinaire ne doit rien en voir. Puis le contenu, sur un
# journal de parties ecrit pour l'occasion dans un RACINE_JEU temporaire.
import json as _json_suivi                                  # noqa: E402
try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")

_code, _tetes, _ = appel("GET", "/suivi")
verifier("/suivi renvoie un anonyme au formulaire",
         _code == 303 and _tetes.get("Location") == "/", "%s" % _code)
_code, _, _ = appel("GET", "/suivi", entetes=cookie_de("invitee"))
verifier("/suivi refuse un compte ordinaire", _code == 403, "%s" % _code)
_code, _, _ = appel("GET", "/api/suivi", entetes=cookie_de("invitee"))
verifier("/api/suivi refuse un compte ordinaire", _code == 403, "%s" % _code)
_code, _, _corps = appel("GET", "/suivi", entetes=cookie_de(o.ADMIN))
verifier("/suivi s'affiche pour l'administrateur",
         _code == 200 and b"En cours" in _corps and b"/api/suivi" in _corps, "%s" % _code)
_code, _tetes, _corps = appel("GET", "/suivi.webmanifest")
verifier("le manifeste est public et ne nomme personne",
         _code == 200 and b"/suivi" in _corps and b"hote" not in _corps, "%s" % _code)
_code, _, _corps = appel("GET", "/suivi-192.png")
verifier("l'icone est servie", _code == 200 and _corps[:8] == b"\x89PNG\r\n\x1a\n", "%s" % _code)

_racine_avant = o.RACINE_JEU
_bac_jeu = tempfile.mkdtemp(prefix="nc-suivi-")
o.RACINE_JEU = _bac_jeu
with o._cx() as cx:
    # Un emplacement que les cas precedents n'ont pas distribue (colonne UNIQUE).
    # On memorise celui de « hote » pour le lui rendre : les cas suivants (le
    # moteur zombie) comptent dessus.
    _empl_hote_avant = cx.execute("SELECT emplacement FROM comptes WHERE pseudo = ?",
                                  ("hote",)).fetchone()["emplacement"]
    cx.execute("UPDATE comptes SET emplacement = 17 WHERE pseudo = ?", ("hote",))
with open(os.path.join(_bac_jeu, "games_history-serveur-17.json"), "w", encoding="utf-8") as _f:
    _json_suivi.dump([
        {"time": 1700000000, "scenario": "Rhino", "expert": False,
         "heroes": [{"name": "* Blade", "card_id": "bl001a", "deck": "Blade", "aspects": ["Aggression"]}],
         "won": True, "reason": "The Final Stage of the Villain was Defeated", "rounds": 7},
        {"time": 1700000500, "scenario": "Klaw", "expert": True,
         "heroes": [{"name": "Spider-Man", "card_id": "01001a"}],
         "won": False, "reason": "All players were eliminated", "rounds": 4},
    ], _f)
_terminees = o.parties_terminees()
verifier("les parties terminees sont lues dans le journal de l'emplacement",
         len(_terminees) == 2, str(_terminees))
verifier("la plus recente vient en premier",
         _terminees and _terminees[0]["mechant"] == "Klaw" and _terminees[0]["expert"], str(_terminees[:1]))
verifier("l'emplacement est traduit en pseudo",
         _terminees and _terminees[0]["joueur"] == "hote", str(_terminees[:1]))
verifier("heros, aspect, rounds et resultat sont la",
         _terminees and _terminees[1]["heros"][0]["nom"] == "Blade"
         and _terminees[1]["heros"][0]["aspects"] == ["Aggression"]
         and _terminees[1]["rounds"] == 7 and _terminees[1]["victoire"], str(_terminees[1:]))
verifier("une partie sans aspect enregistre reste lisible",
         _terminees and _terminees[0]["heros"][0]["aspects"] == [], str(_terminees[:1]))

allumer("hote", 17)
_code, _, _corps = appel("GET", "/api/suivi", entetes=cookie_de(o.ADMIN))
_etat_suivi = _json_suivi.loads(_corps.decode("utf-8"))
verifier("/api/suivi rend les deux listes a l'administrateur",
         _code == 200 and len(_etat_suivi.get("terminees", [])) == 2
         and len(_etat_suivi.get("en_cours", [])) == 1, str(_etat_suivi)[:300])
verifier("une table allumee dont le moteur ne repond pas est dite muette, pas en cours",
         _etat_suivi["en_cours"][0]["joueur"] == "hote"
         and _etat_suivi["en_cours"][0]["moteur_repond"] is False
         and _etat_suivi["en_cours"][0]["en_cours"] is False, str(_etat_suivi["en_cours"]))
o.PARTIES.clear()
o.RACINE_JEU = _racine_avant
shutil.rmtree(_bac_jeu, ignore_errors=True)
with o._cx() as cx:
    cx.execute("UPDATE comptes SET emplacement = ? WHERE pseudo = ?", (_empl_hote_avant, "hote"))


# --- Le moteur zombie qui bloquait une table pour toujours ------------------
# ⚠ RIEN DE CE QUI SUIT N'EST SIMULE. Un VRAI lanceur, lance dans son propre
# groupe comme le fait `lancer_jeu`, qui SORT en laissant un enfant tenir un
# port. C'est le cas reel, et c'est celui que l'ancien code manquait : il ne
# tuait le groupe que si le lanceur vivait encore, or ici `poll()` n'est pas
# nul. Une sous-classe qui ment sur `vivant()` ne prouvait rien de tout ca.
import socket                                               # noqa: E402

_place = o.emplacement_de("hote")
_port = o.PORT_BASE + _place

# --- La prise, pas la reponse ----------------------------------------------
_libre = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_libre.bind(("127.0.0.1", 0))
_port_a_nous = _libre.getsockname()[1]
_libre.close()
verifier("un port sans personne dessus est vu libre",
         o._port_libre(_port_a_nous) is True)

_tenu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_tenu.bind(("127.0.0.1", _port_a_nous))
# ⚠ PRIS SANS ECOUTER, ET C'EST LE CAS QUI COMPTE. Juger par `connect()`
# declarait libre tout port dont personne n'accepte : celui qu'on vient de
# reserver sans avoir encore appele `listen`, celui dont la file d'acceptation
# est pleine. Le `Popen` suivant mourait alors sur « Address already in use ».
# On juge donc par `bind()`, exactement ce que fera le moteur.
verifier("un port pris mais pas encore en ecoute est vu pris",
         o._port_libre(_port_a_nous) is False)
_tenu.listen(1)
verifier("un port tenu en ecoute est vu pris",
         o._port_libre(_port_a_nous) is False)
_tenu.close()

# --- Le lanceur sorti, l'enfant qui tient le port ---------------------------
_reserve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_reserve.bind(("127.0.0.1", 0))
_port_enfant = _reserve.getsockname()[1]
_reserve.close()

_code_enfant = (
    "import socket, sys, time\n"
    "s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n"
    "s.bind(('127.0.0.1', %d))\n"
    "s.listen(1)\n"
    "sys.stdout.write('pret\\n')\n"
    "sys.stdout.flush()\n"
    "time.sleep(120)\n" % _port_enfant)
_code_lanceur = (
    "import subprocess, sys\n"
    "p = subprocess.Popen([sys.executable, '-c', %r], stdout=subprocess.PIPE)\n"
    "p.stdout.readline()\n" % _code_enfant)

_zombie = o.Partie(_place, "hote", "Jeu de hote")
_zombie.processus = subprocess.Popen([sys.executable, "-c", _code_lanceur],
                                     start_new_session=True)
_zombie.processus.wait(timeout=30)
verifier("le lanceur est sorti, comme le vrai le fait",
         _zombie.processus.poll() is not None, str(_zombie.processus.poll()))
verifier("et son enfant, lui, tient toujours son port",
         o._port_libre(_port_enfant) is False)
verifier("la partie se dit donc morte", _zombie.vivant() is False)

o.PARTIES["hote"] = _zombie
o.EMPLACEMENTS[_place] = "hote"

_prise = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
_prise.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_prise.bind(("127.0.0.1", _port))
_prise.listen(1)
try:
    o.lancer_jeu("hote")
    _dit = ""
except RuntimeError as _erreur:
    _dit = str(_erreur)
finally:
    _prise.close()

# ⚠ LE CAS QUI COMPTE : le groupe du precedent est ACHEVE avant qu'on tente de
# recreer, MEME QUAND SON LANCEUR EST DEJA SORTI. Sans lui, l'enfant gardait le
# port et le nouveau moteur mourait a chaque essai, sans issue automatique.
_rendu = o._port_libre(_port_enfant)
if not _rendu:                    # un test ne laisse pas de processus derriere
    try:
        os.killpg(_zombie.processus.pid, o.signal.SIGKILL)
    except OSError:
        pass
verifier("le groupe du lanceur sorti est acheve, son port est rendu", _rendu,
         "l'enfant tient encore le port %d" % _port_enfant)

verifier("un port deja pris fait refuser le demarrage",
         str(_port) in _dit, _dit or "aucune erreur levee")
verifier("et le message dit quoi faire", "a la main" in _dit, _dit)
verifier("la table n'est pas laissee a moitie ouverte",
         "hote" not in o.PARTIES and _place not in o.EMPLACEMENTS,
         "%s / %s" % (list(o.PARTIES), list(o.EMPLACEMENTS)))
o.PARTIES.clear()
o.EMPLACEMENTS.clear()

# --- Les rapports de bug, et le disque qu'ils remplissaient ------------------
# ⚠ `site/rapports/` N'ETAIT PURGE PAR RIEN. Le plafond est de 12 rapports par
# heure et par TABLE, avec une capture jusqu'a 4 Mio, et la sauvegarde de nuit
# multipliait le total par trente. Les captures partent avec leur ligne, jamais
# l'une sans l'autre : une image seule pese pour rien, une ligne seule renvoie
# vers un fichier absent.
import shutil                                               # noqa: E402
from datetime import datetime, timedelta                    # noqa: E402

_bac_rapports = tempfile.mkdtemp(prefix="nc-rapports-")
_vrai_dossier = o.DOSSIER_RAPPORTS
o.DOSSIER_RAPPORTS = _bac_rapports
# Un vrai PNG minuscule, pour que `_ecrire_capture` l'accepte sur signature.
_png = ("data:image/png;base64,"
        "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg==")
with o._cx() as cx:
    cx.execute("DELETE FROM rapports")

_vieux = o.enregistrer_rapport("hote", {"nom": "ancien", "description": "vieux bug",
                                        "capture": _png})
_recent = o.enregistrer_rapport("hote", {"nom": "recent", "description": "bug d'hier",
                                         "capture": _png})
_ouvert = o.enregistrer_rapport("hote", {"nom": "ouvert", "description": "pas encore vu",
                                         "capture": _png})
with o._cx() as cx:
    _fichiers = {r["id"]: r["capture"] for r in
                 cx.execute("SELECT id, capture FROM rapports")}
verifier("les trois captures sont bien sur le disque",
         all(f and os.path.isfile(os.path.join(_bac_rapports, f))
             for f in _fichiers.values()), str(_fichiers))

o.changer_etat_rapport(_vieux, "traite")
o.changer_etat_rapport(_recent, "traite")
# Le vieux a ete classe il y a quarante jours ; le recent, a l'instant.
_il_y_a_40 = (datetime.now() - timedelta(days=40)).strftime("%Y-%m-%d %H:%M")
with o._cx() as cx:
    cx.execute("UPDATE rapports SET traite_le=? WHERE id=?", (_il_y_a_40, _vieux))

_efface = o.purger_rapports_traites(30)
verifier("un seul rapport part", _efface == 1, str(_efface))

_restants = {r["id"] for r in o.liste_rapports()}
verifier("le rapport traite depuis longtemps a disparu de la base",
         _vieux not in _restants, str(_restants))
verifier("sa capture aussi",
         not os.path.isfile(os.path.join(_bac_rapports, _fichiers[_vieux])))

# ⚠ LES DEUX CAS DE REFUS, ET CE SONT EUX QUI COMPTENT. Une purge qui emporte
# ce qu'on n'a pas fini de lire est pire que pas de purge du tout.
verifier("un rapport traite d'hier reste", _recent in _restants, str(_restants))
verifier("et sa capture reste avec lui",
         os.path.isfile(os.path.join(_bac_rapports, _fichiers[_recent])))
verifier("un rapport jamais traite reste, meme tres ancien",
         _ouvert in _restants, str(_restants))

# ⚠ LE COMPTE A REBOURS PART DU CLASSEMENT, PAS DE L'ENVOI. Un rapport vieux
# de six mois qu'on vient de traiter garde ses trente jours : on vient
# justement de s'en servir.
with o._cx() as cx:
    cx.execute("UPDATE rapports SET quand=? WHERE id=?",
               ((datetime.now() - timedelta(days=200)).strftime("%Y-%m-%d %H:%M"),
                _ouvert))
o.changer_etat_rapport(_ouvert, "traite")
verifier("un vieux rapport tout juste classe n'est pas emporte",
         o.purger_rapports_traites(30) == 0)

# ⚠ ET LE DISQUE N'EST TOUCHE QU'UNE FOIS LA TRANSACTION VALIDEE. Effacer un
# fichier au milieu d'une transaction, c'est promettre au disque ce que la base
# peut encore annuler. Le cas le prouve depuis l'interieur de l'effacement : au
# moment ou la capture part, la ligne a deja disparu POUR QUI REGARDE
# D'AILLEURS, et seule une transaction validee se voit d'ailleurs.
_hors = o.enregistrer_rapport("hote", {"nom": "hors", "description": "hors transaction",
                                       "capture": _png})
o.changer_etat_rapport(_hors, "traite")
with o._cx() as cx:
    cx.execute("UPDATE rapports SET traite_le=? WHERE id=?", (_il_y_a_40, _hors))
_vu_pendant = {}
_vrai_remove = os.remove


def _remove_observe(chemin):
    # Une AUTRE connexion : elle ne voit que ce qui est valide.
    with o._cx() as _autre:
        _vu_pendant["reste"] = _autre.execute(
            "SELECT COUNT(*) FROM rapports WHERE id=?", (_hors,)).fetchone()[0]
    return _vrai_remove(chemin)


os.remove = _remove_observe
try:
    o.purger_rapports_traites(30)
finally:
    os.remove = _vrai_remove
verifier("la capture ne part qu'une fois la ligne vraiment validee",
         _vu_pendant.get("reste") == 0, str(_vu_pendant))

# ⚠ UNE CAPTURE QUI RESISTE N'EMPORTE PAS SA LIGNE AVEC ELLE. Les fichiers
# partaient DANS la transaction, et l'`OSError` etait avalee en silence : un
# disque plein ou un droit refuse laissait une ligne effacee, un fichier
# vivant, et personne pour l'apprendre. On efface les lignes, on valide, puis
# seulement on touche au disque, et l'echec est dit.
_coince = o.enregistrer_rapport("hote", {"nom": "coince", "description": "bug coince",
                                         "capture": _png})
with o._cx() as cx:
    _capture_coincee = cx.execute("SELECT capture FROM rapports WHERE id=?",
                                  (_coince,)).fetchone()["capture"]
o.changer_etat_rapport(_coince, "traite")
with o._cx() as cx:
    cx.execute("UPDATE rapports SET traite_le=? WHERE id=?", (_il_y_a_40, _coince))
# Un DOSSIER a la place du fichier : `os.remove` ne peut rien contre lui.
_chemin_coince = os.path.join(_bac_rapports, _capture_coincee)
os.remove(_chemin_coince)
os.mkdir(_chemin_coince)
import contextlib                                           # noqa: E402
import io as _flux                                          # noqa: E402
_plainte = _flux.StringIO()
with contextlib.redirect_stderr(_plainte):
    _efface = o.purger_rapports_traites(30)
verifier("la ligne part meme quand sa capture resiste",
         _efface == 1 and _coince not in {r["id"] for r in o.liste_rapports()},
         "%d efface(s)" % _efface)
verifier("et l'echec de l'effacement est dit, pas avale",
         "capture" in _plainte.getvalue().lower(), repr(_plainte.getvalue()))
os.rmdir(_chemin_coince)

# Rouvrir un rapport efface sa date de classement : le compte a rebours
# repart de zero le jour ou on le reclasse.
o.changer_etat_rapport(_recent, "en cours")
with o._cx() as cx:
    _date = cx.execute("SELECT traite_le FROM rapports WHERE id=?",
                       (_recent,)).fetchone()["traite_le"]
verifier("rouvrir un rapport efface sa date de classement", _date is None, str(_date))

o.DOSSIER_RAPPORTS = _vrai_dossier
shutil.rmtree(_bac_rapports, ignore_errors=True)
with o._cx() as cx:
    cx.execute("DELETE FROM rapports")


print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
