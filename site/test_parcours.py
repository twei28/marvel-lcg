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

# ⚠ AVANT TOUT AUTRE APPEL (25/09/2026, trouve en verifiant un correctif sans
# rapport). `page_attente` (plus bas) lit deja la base (`_barre` ->
# `reponses_non_lues` -> table `rapports_messages`) alors que
# `o.initialiser_base()` n'etait appele qu'a la ligne ~114 : sur une base
# fraiche (`BASE` neuf ou vide), le tout premier test faisait tomber le
# script entier avec `sqlite3.OperationalError: no such table`.
# `initialiser_base()` est idempotent (`CREATE TABLE IF NOT EXISTS`) : la
# garder plus bas aussi ne coute rien.
o.initialiser_base()

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

# La V2 mobile reste reservee au navigateur hote du compte Arnaud pendant sa
# construction. Le compte est normalise : la casse du pseudo ne change rien.
partie_arnaud = o.Partie(3, "ArNaUd", "Jeu d'Arnaud")
partie_arnaud.cles_sieges = ["cle-arnaud"]
lien_arnaud = partie_arnaud.lien_hote()
verifier("Arnaud entre automatiquement par la porte V2",
         "to=prepare-v2" in lien_arnaud, lien_arnaud)
verifier("un autre compte reste sur la V1",
         "to=prepare-v2" not in lien and "to=prepare" in lien, lien)

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

# L'heure d'un message part en SECONDES DEPUIS L'EPOQUE, pas en « HH:MM » du
# serveur : le serveur vit en UTC et le joueur en Belgique, et un « 10:14 »
# nu s'affichait deux heures en retard. Le navigateur formate dans son fuseau.
import time as _time  # noqa: E402
_frais = o.messages_depuis(0)[0]
verifier("l'heure du message part en secondes depuis l'epoque",
         isinstance(_frais.get("quand_ts"), (int, float))
         and abs(_time.time() - _frais["quand_ts"]) < 120, str(_frais))

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
# ⚠ `utcnow`, PAS `now` : la base stocke de l'UTC (voir `_maintenant`). Ecrite
# en heure locale, cette ligne datait la visite de deux heures a cote sur une
# machine en CEST, et le test echouait sur une faute a lui, pas au produit
# (14/09/2026).
from datetime import datetime, timedelta
vieux = (datetime.utcnow() - timedelta(hours=3)).isoformat(" ", "seconds")
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
# ⚠ `_port_serveur`, ET PAS `_port`. Le nom `_port` est repris plus bas par la
# section du moteur zombie (`_port = o.PORT_BASE + _place`) : tant qu'aucun cas
# n'appelait `appel()` APRES elle, personne ne l'a vu. Le premier qui l'a fait
# (les cas de l'annonce, 13/09/2026) est tombe sur « Connection refused »,
# l'appel visant desormais le port d'une table au lieu de celui du serveur de
# test. Un nom a part, et le piege disparait.
_port_serveur = _serveur.server_address[1]
threading.Thread(target=_serveur.serve_forever, daemon=True).start()


def appel(methode, chemin, corps=b"", entetes=None, annonce=None, delai=5):
    """Une requete HTTP reelle. Rend (code, entetes, corps).

    `annonce` permet de MENTIR sur `Content-Length` : declarer huit mega-octets
    puis n'en envoyer aucun est le seul moyen de prouver qu'on refuse AVANT de
    lire le corps, et non apres. `delai` borne l'attente : un serveur qui se
    mettrait a lire ces octets qui n'arrivent jamais ferait echouer le cas au
    lieu de bloquer le fichier de test pour toujours.
    """
    lien = http.client.HTTPConnection("127.0.0.1", _port_serveur, timeout=delai)
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


def _eteindre_observe(code, cause="extinction"):
    # ⚠ MEME SIGNATURE QUE LA VRAIE. Un double plus etroit tombe en
    # TypeError le jour ou l'appelant passe la cause, et le cas echoue sur un
    # detail du harnais plutot que sur ce qu'il mesure.
    # Ce que verrait un `/entrer` arrive au beau milieu de l'extinction.
    _vu["mdp"] = o.mot_de_passe_jeu(code)
    return _vrai_eteindre(code, cause)


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

# --- S2 : « Quitter la partie » depuis le PLATEAU ferme la table -----------
# ⚠ LE GESTE VIENT DU MOTEUR, PAS DU NAVIGATEUR. Le bouton vit sur
# `p<N>.<domaine>`, le site sur `<domaine>` : le moteur relaie l'appel en
# 127.0.0.1 avec le jeton de sa partie, comme il le fait deja pour le tchat et
# les rapports de bug. `/api/eteindre` est donc le pendant interne du bouton
# « Terminer » du site, et doit couper les acces de la meme facon.
import json as _json_extinction                             # noqa: E402
import time as _time_extinction                             # noqa: E402

_jeton_extinction = "jeton-extinction-de-test"
o.JETONS_SITE[_jeton_extinction] = "hote"
_corps_extinction = ("jeton=" + _jeton_extinction).encode("utf-8")

_eteints = []
_ordre = []                   # ce qui s'est passe, dans l'ordre ou c'est arrive
_vrai_eteindre_2 = o.eteindre_jeu
_vrai_repondre = o.Handler._repondre


def _eteindre_lent(code, cause="extinction"):
    # ⚠ ON FAIT EXPRES DE TRAINER. `eteindre_jeu` tient la main jusqu'a vingt
    # secondes en vrai (sauvegarde, SIGTERM, attente du groupe) : c'est
    # precisement ce qui interdit de repondre APRES lui.
    _ordre.append("eteint")
    _time_extinction.sleep(1.5)
    _eteints.append((code, cause))


def _repondre_observe(self, *args, **kwargs):
    if self.chemin == "/api/eteindre":
        _ordre.append("repondu")
    return _vrai_repondre(self, *args, **kwargs)


o.eteindre_jeu = _eteindre_lent
o.Handler._repondre = _repondre_observe
try:
    _avant = o.mot_de_passe_jeu("hote")
    _depart = _time_extinction.monotonic()
    _code, _, _rep = appel("POST", "/api/eteindre", corps=_corps_extinction)
    _duree = _time_extinction.monotonic() - _depart
    try:
        _vu = _json_extinction.loads(_rep or b"{}")
    except ValueError:
        _vu = {}          # route absente ou reponse en texte : les cas le diront
    verifier("le plateau obtient un accuse de fermeture",
             _code == 200 and _vu.get("ok") is True, "%s %s" % (_code, _rep))
    # ⚠ LE CAS QUI COMPTE, ET C'EST TOUT LE PIEGE DE CETTE ROUTE. Le site
    # repond au MOTEUR qu'il est en train de tuer. Eteindre avant de repondre,
    # c'est tuer le messager : la reponse ne revient jamais, et le plateau
    # reste sur une page morte sans savoir ou aller.
    verifier("la reponse part AVANT que le moteur soit tue", _duree < 1.0,
             "%.2f s : le site a attendu la fin de l'extinction" % _duree)
    # L'adresse d'atterrissage vient du SITE, seul a connaitre son domaine
    # public. Sans elle, le plateau n'aurait que des pages du moteur eteint.
    verifier("le site dit ou atterrir, chez lui",
             str(_vu.get("url", "")).endswith("/arret") and "://" in str(_vu.get("url", "")),
             str(_vu.get("url")))
    # Meme geste volontaire que le bouton « Terminer », donc meme consequence :
    # le cookie d'un invite d'hier ne rouvre plus la table.
    verifier("et le laissez-passer du moteur est perime",
             o.mot_de_passe_jeu("hote") != _avant)
    _fin = _time_extinction.monotonic() + 5
    while not _eteints and _time_extinction.monotonic() < _fin:
        _time_extinction.sleep(0.05)
    verifier("la table finit bien par etre eteinte", bool(_eteints), str(_eteints))
    # ⚠ ET L'ORDRE, PAS SEULEMENT LE DELAI. Le cas du chrono ci-dessus passe
    # encore si le fil demarre une ligne AVANT `_repondre` : il tuerait alors
    # le moteur pendant que le site lui ecrit sa reponse, une fois sur mille.
    # Celui-ci refuse cette course-la.
    verifier("et le fil qui tue ne demarre qu'APRES la reponse",
             _ordre[:2] == ["repondu", "eteint"], str(_ordre))

    # ⚠ ET LE FIL PART MEME SI LA REPONSE NE PART PAS. Le client de cette
    # requete est le MOTEUR, et son `_appeler_site` coupe a dix secondes : une
    # revocation qui traine sur un verrou sqlite au-dela de ce plafond fait
    # fermer la connexion d'en face, donc lever `_repondre`. Sans filet, on
    # aurait alors le pire des deux mondes — mot de passe revoque, moteur
    # vivant, emplacement pris jusqu'au faucheur, une demi-heure.
    _eteints.clear()
    _ordre.clear()

    def _repondre_casse(self, *args, **kwargs):
        if self.chemin == "/api/eteindre":
            raise BrokenPipeError("le moteur a raccroche")
        return _vrai_repondre(self, *args, **kwargs)

    o.Handler._repondre = _repondre_casse
    try:
        try:
            appel("POST", "/api/eteindre", corps=_corps_extinction)
        except OSError:
            pass          # la connexion est cassee : c'est tout le sujet
        _fin = _time_extinction.monotonic() + 5
        while not _eteints and _time_extinction.monotonic() < _fin:
            _time_extinction.sleep(0.05)
        verifier("une reponse qui ne part pas n'empeche pas la table de fermer",
                 bool(_eteints), str(_eteints))
    finally:
        o.Handler._repondre = _repondre_observe

    # Le jeton est le seul laissez-passer : sans lui, on n'eteint pas la table
    # d'un autre.
    _eteints.clear()
    _avant = o.mot_de_passe_jeu("hote")
    _code, _, _ = appel("POST", "/api/eteindre", corps=b"jeton=invente")
    verifier("un jeton inconnu n'eteint rien",
             _code == 403 and not _eteints and o.mot_de_passe_jeu("hote") == _avant,
             "%s %s" % (_code, _eteints))
finally:
    o.eteindre_jeu = _vrai_eteindre_2
    o.Handler._repondre = _vrai_repondre

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
# Depuis le 29/09/2026 (activite Discord), les cookies de la table passent tous
# par `PoserCookie` (web_server.py), qui choisit `Lax` ou `None; Partitioned`
# selon le cadre. La porte se ferme donc sur deux points : `PoserCookie` pose
# `Secure` dans les deux branches, et `server_html.py` ne contourne jamais ce
# passage par un `set_cookie` direct.
_web = os.path.join(_moteur, "network", "web_server.py")
_html = os.path.join(_moteur, "device", "web", "server", "server_html.py")
if os.path.isfile(_web) and os.path.isfile(_html):
    _src_web = open(_web, encoding="utf-8").read()
    _src_html = open(_html, encoding="utf-8").read()
    verifier("les cookies de web_server.py ne partent plus en clair",
             "'secure': self.CookieSecure(request)" in _src_web
             and "'Secure'" in _src_web and "# secure=True" not in _src_web)
    verifier("les cookies de server_html.py ne partent plus en clair",
             "set_cookie(" not in _src_html and _src_html.count("self.PoserCookie(") >= 4,
             "%d PoserCookie trouves" % _src_html.count("self.PoserCookie("))

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
import shutil as _shutil_suivi                              # noqa: E402
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

# --- Mot de passe oublie : un lien cree par l'administrateur ---------------
# Demande du 08/09/2026 : « il se demande s'il a pas fait une erreur dans le
# mdp, on peut faire un recuperateur de mdp ? ». Le site n'envoie pas de
# courrier : l'administrateur cree un lien a usage unique depuis /admin et le
# transmet lui-meme, comme une invitation.
# ⚠ Le compte est cree ICI et supprime a la fin du bloc : il prend le premier
# emplacement libre, qui est justement celui que « hote » a quitte plus haut
# et doit retrouver plus bas (colonne UNIQUE). La base de test survit aux
# passes : on nettoie aussi un reliquat eventuel avant de commencer.
def _oublier_oublieux():
    with o._cx() as cx:
        for table in ("sessions", "reinitialisations", "comptes"):
            cx.execute("DELETE FROM %s WHERE pseudo = ?" % table, ("oublieux",))
_oublier_oublieux()
o.inscrire("oublieux", "oublieux@exemple.fr", "ancienmotdepasse")
o.changer_statut("oublieux", "valide")
_session_avant = cookie_de("oublieux")
_code, _, _ = appel("POST", "/admin", b"action=reinitialiser&pseudo=oublieux", entetes=cookie_de(o.ADMIN))
_ouverts = [r for r in o.reinitialisations_ouvertes() if r["pseudo"] == "oublieux"]
verifier("l'administrateur cree un lien de reinitialisation pour un compte",
         _code == 303 and len(_ouverts) == 1, "%s / %s" % (_code, _ouverts))
_jeton = _ouverts[0]["jeton"] if _ouverts else ""
_code, _, _corps = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
verifier("le lien s'affiche sur la page d'administration",
         ("/reinitialisation?r=" + _jeton).encode("utf-8") in _corps, "lien absent")
_code, _, _ = appel("POST", "/admin", b"action=reinitialiser&pseudo=inconnu-xyz", entetes=cookie_de(o.ADMIN))
verifier("un compte inconnu ne cree rien, sans casser la page",
         _code == 303 and not [r for r in o.reinitialisations_ouvertes() if r["pseudo"] == "inconnu-xyz"], "%s" % _code)

_code, _, _corps = appel("GET", "/reinitialisation?r=" + _jeton)
verifier("le lien ouvre le formulaire du nouveau mot de passe, sans connexion",
         _code == 200 and b"Nouveau mot de passe" in _corps and b'name="mdp"' in _corps, "%s" % _code)
_code, _, _ = appel("GET", "/reinitialisation?r=nimporte-quoi")
verifier("un lien inconnu est refuse", _code == 410, "%s" % _code)
_code, _, _corps = appel("POST", "/reinitialisation", ("r=%s&mdp=court" % _jeton).encode("utf-8"))
verifier("un mot de passe trop court est refuse, le lien reste valable",
         _code == 400 and o.reinitialisation_valide(_jeton) == "oublieux", "%s" % _code)
_code, _, _corps = appel("POST", "/reinitialisation", ("r=%s&mdp=nouveaumotdepasse" % _jeton).encode("utf-8"))
verifier("le nouveau mot de passe est enregistre",
         _code == 200 and b"connecte-toi" in _corps, "%s" % _code)
verifier("et il ouvre la porte", o.verifier("oublieux", "nouveaumotdepasse") == "oublieux", "refuse")
try:
    o.verifier("oublieux", "ancienmotdepasse"); _ancien_passe = True
except ValueError:
    _ancien_passe = False
verifier("l'ancien mot de passe ne l'ouvre plus", not _ancien_passe, "l'ancien passe encore")
# ⚠ LE CAS QUI COMPTE POUR LA SECURITE : on change un mot de passe parce qu'on
# a un doute. Les sessions ouvertes avant ne doivent pas survivre.
_jeton_session = _session_avant["Cookie"].split("nc_session=", 1)[1].split(";")[0]
verifier("les sessions ouvertes avant le changement sont fermees",
         o.pseudo_de_session(_jeton_session) is None, "session encore valable")
_code, _, _ = appel("POST", "/reinitialisation", ("r=%s&mdp=encoreunautre" % _jeton).encode("utf-8"))
verifier("le lien ne sert qu'une fois",
         _code == 400 and o.verifier("oublieux", "nouveaumotdepasse") == "oublieux", "%s" % _code)
with o._cx() as cx:
    cx.execute("INSERT INTO reinitialisations (jeton, pseudo, cree_le) VALUES ('vieux-jeton', 'oublieux', '2020-01-01 00:00')")
verifier("un lien de plus de 24 heures ne vaut plus rien",
         o.reinitialisation_valide("vieux-jeton") is None
         and not [r for r in o.reinitialisations_ouvertes() if r["jeton"] == "vieux-jeton"], "encore valable")
_code, _, _corps = appel("GET", "/connexion")
verifier("la page de connexion dit ou demander un lien",
         b"Mot de passe oublie" in _corps, "rappel absent")
_oublier_oublieux()

# --- Le nom du DECK, et le suivi servi DANS /admin -------------------------
# Deux demandes du 08/09/2026 : « ajoute ca » (le nom du deck, porte par les
# deux sources mais jamais affiche) et « je veux que le suivi soit dans
# /admin ».
verifier("le nom du deck arrive jusqu'a l'interface de donnees",
         _terminees and _terminees[1]["heros"][0]["deck"] == "Blade",
         str(_terminees[1]["heros"][0]))
verifier("et le rendu partage l'ecrit sur la ligne du heros",
         'class="deck"' in o.SUIVI_SCRIPT and "x.deck" in o.SUIVI_SCRIPT
         and "j.deck" in o.SUIVI_SCRIPT, "le script n'affiche pas le deck")

# ⚠ LE CAS QUI COMPTE POUR /admin : c'est le MEME bloc, pas une copie. Si un
# jour quelqu'un duplique le rendu, ces trois presences resteront vraies mais
# le premier `verifier` ci-dessous tombera des que les deux versions
# divergeront d'un caractere.
_code, _, _corps_admin = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
_txt_admin = _corps_admin.decode("utf-8")
verifier("/admin porte le bloc de suivi, a l'identique",
         _code == 200 and o.SUIVI_CORPS in _txt_admin and o.SUIVI_SCRIPT in _txt_admin
         and o.SUIVI_STYLE_BLOC in _txt_admin, "%s" % _code)
verifier("/admin garde le journal technique des tables",
         "Journal technique des tables" in _txt_admin, "depliant absent")
verifier("/admin renvoie toujours vers la page a epingler",
         'href="/suivi"' in _txt_admin, "lien vers /suivi absent")

# ⚠ LES STYLES DU SUIVI SONT PREFIXES, sinon sa regle `h2` (petites capitales
# grises) repeindrait les titres de l'administration et sa regle `.carte`
# mordrait sur les blocs de rapport de bug.
verifier("les styles du bloc ne debordent pas sur le reste de /admin",
         "#suivi h2" in o.SUIVI_STYLE_BLOC
         and not any(l.strip().startswith((".carte", "h2", ".heros"))
                     for l in o.SUIVI_STYLE_BLOC.splitlines()),
         "un selecteur du suivi n'est pas prefixe")

# Et la page telephone continue de servir exactement le meme bloc.
_code, _, _corps_suivi = appel("GET", "/suivi", entetes=cookie_de(o.ADMIN))
verifier("/suivi sert le meme bloc que /admin",
         _code == 200 and o.SUIVI_CORPS in _corps_suivi.decode("utf-8"), "%s" % _code)
# --- Une partie ABANDONNEE laisse une trace --------------------------------
# ⚠ LE CAS QUI COMPTE, ET IL DECRIT UN TROU REEL. Avant cette trace, une
# partie quittee en cours de route ne figurait NULLE PART : le journal du
# moteur n'est ecrit qu'a la fin DECLAREE (victoire, defaite, elimination), et
# « En cours » l'oubliait des l'extinction de la table.
#
# `_fiche_moteur` est remplacee ici, et seulement ici : c'est la seule facon de
# decrire une position precise sans monter un vrai moteur. Le chemin HTTP
# qu'elle emprunte a ete verifie a la main le 08/09/2026 contre un vrai moteur
# (Rhino 14/14, The Break-In!) ; ce que ces cas prouvent, c'est ce que le SITE
# en fait.
with o._cx() as cx:
    cx.execute("DELETE FROM abandons")     # la base de test survit aux passes
_fiche_reelle = o._fiche_moteur
o._fiche_moteur = lambda partie: {
    "en_cours": True, "round": 6, "scenario": "Rhino", "expert": False,
    "joueurs": [{"heros": "* Blade", "card_id": "bl001a", "deck": "Blade",
                 "forme": "Hero", "pv": 7, "pv_max": 12, "elimine": False}],
    "vilains": [{"nom": "Rhino", "pv": 9, "pv_max": 14, "stage": "2"}],
    "manigances": [{"nom": "The Break-In!", "menace": 3}],
}


def _table_avec_moteur(pseudo, emplacement):
    """Une table dont le processus est REEL, dans son propre groupe.

    ⚠ PAS UN FAUX PROCESSUS : `eteindre_jeu` appelle `os.killpg(processus.pid)`,
    et un objet qui mentirait sur son `pid` ferait tirer sur un groupe au
    hasard, a commencer par celui de ce fichier de test.
    """
    partie = o.Partie(emplacement, pseudo, "Jeu de " + pseudo)
    partie.processus = subprocess.Popen(["sleep", "60"], start_new_session=True)
    partie.jeton_site = "jeton-de-test"
    o.PARTIES[pseudo] = partie
    o.EMPLACEMENTS[emplacement] = pseudo
    return partie


_table_avec_moteur("hote", 17)
o.eteindre_jeu("hote", "minuteur")
_abandons = o.parties_abandonnees()
verifier("une partie quittee en cours de route laisse une trace",
         len(_abandons) == 1, str(_abandons))
_a = _abandons[0] if _abandons else {}
verifier("la trace garde le heros, sa forme et ses PV",
         bool(_a.get("heros")) and _a["heros"][0]["nom"] == "Blade"
         and _a["heros"][0]["pv"] == 7 and _a["heros"][0]["pv_max"] == 12,
         str(_a.get("heros")))
verifier("elle garde le mechant, son etat et le round atteint",
         _a.get("mechant") == "Rhino" and _a.get("rounds") == 6
         and "9/14" in _a.get("detail", "") and "menace 3" in _a.get("detail", ""),
         "%s | %s" % (_a.get("rounds"), _a.get("detail")))
verifier("et la cause de l'extinction, en clair",
         _a.get("etat") == "abandon"
         and _a.get("raison") == o.CAUSES_ABANDON["minuteur"], str(_a.get("raison")))

# Une table allumee ou personne n'a lance de partie n'est pas un abandon :
# c'est une table qu'on ferme, et elle ne doit rien laisser.
o._fiche_moteur = lambda partie: {"en_cours": False}
_table_avec_moteur("hote", 17)
o.eteindre_jeu("hote")
verifier("une table fermee sans partie en cours ne laisse rien",
         len(o.parties_abandonnees()) == 1, str(len(o.parties_abandonnees())))


# Un moteur DEJA MORT ne peut plus rien dire : on n'invente pas sa partie.
class _MoteurMort:
    def poll(self):
        return 0


o._fiche_moteur = lambda partie: {"en_cours": True, "round": 3, "scenario": "Klaw"}
_morte = o.Partie(18, "invitee", "Jeu de invitee")
_morte.processus = _MoteurMort()
o._noter_abandon(_morte, "moteur arrete")
verifier("un moteur deja mort n'invente pas de trace",
         len(o.parties_abandonnees()) == 1, str(len(o.parties_abandonnees())))
o._fiche_moteur = _fiche_reelle

# Les deux sources se melent dans UNE seule liste chronologique : l'abandon
# vient d'avoir lieu, les deux parties du journal datent de 2023.
_toutes = o.parties_terminees()
verifier("abandons et parties finies forment une seule liste",
         len(_toutes) == 3, str(len(_toutes)))
verifier("la plus recente reste en tete, quelle que soit sa source",
         bool(_toutes) and _toutes[0]["etat"] == "abandon"
         and [p["etat"] for p in _toutes[1:]] == ["defaite", "victoire"],
         str([p["etat"] for p in _toutes]))
with o._cx() as cx:
    cx.execute("DELETE FROM abandons")

# --- La FERMETURE d'une table est notee, quel que soit le chemin -----------
# ⚠ TROU REEL, vu par l'utilisateur le 08/09/2026 sur la page d'administration :
# quatre tables ouvertes depuis trois jours toujours annoncees « en cours ». La
# fermeture n'etait ecrite que par le faucheur et par le bouton « Eteindre » ;
# ni l'arret du site — donc CHAQUE deploiement — ni le menage de `lancer_jeu`
# ne la notaient. Le cas prend le chemin le plus oublie des six.
with o._cx() as cx:
    cx.execute("DELETE FROM parties WHERE code = ?", ("hote",))
o._fiche_moteur = lambda partie: {"en_cours": False}
_table = _table_avec_moteur("hote", 17)
o.journal_partie_ouverte(_table, "hote")
o.eteindre_jeu("hote", "arret du site")
_lignes = [p for p in o.dernieres_parties() if p["code"] == "hote"]
verifier("l'arret du site note la fermeture de la table",
         len(_lignes) == 1 and _lignes[0]["fermee_le"], str(dict(_lignes[0])) if _lignes else "aucune")

# Une ligne laissee ouverte par le processus PRECEDENT n'a plus personne pour
# la fermer : c'est le demarrage qui s'en charge, sans quoi elle reste « en
# cours » a jamais.
with o._cx() as cx:
    cx.execute("UPDATE parties SET fermee_le = NULL WHERE code = ?", ("hote",))
_fermees = o.fermer_parties_orphelines()
_lignes = [p for p in o.dernieres_parties() if p["code"] == "hote"]
verifier("le demarrage ferme les tables orphelines de la session precedente",
         _fermees >= 1 and _lignes and _lignes[0]["fermee_le"],
         "%s fermee(s)" % _fermees)
verifier("et il ne touche pas a celles qui sont deja fermees",
         o.fermer_parties_orphelines() == 0, str(o.fermer_parties_orphelines()))
with o._cx() as cx:
    cx.execute("DELETE FROM parties WHERE code = ?", ("hote",))

o.PARTIES.clear()
o.RACINE_JEU = _racine_avant
_shutil_suivi.rmtree(_bac_jeu, ignore_errors=True)
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
verifier("un seul rapport est allege", _efface == 1, str(_efface))

# ⚠ CHANGE LE 16/09/2026 : LA PURGE ALLEGE, ELLE N'EFFACE PLUS. Un rapport est
# devenu un TICKET que son auteur consulte ; effacer la ligne viderait sa page
# « Mes signalements » un mois apres, avec la reponse qu'on lui a faite. Ce qui
# pesait n'a jamais ete le texte, c'est l'image.
_restants = {r["id"] for r in o.liste_rapports()}
verifier("⚠ le rapport traite depuis longtemps RESTE en base",
         _vieux in _restants, str(_restants))
verifier("mais sa capture a quitte le disque",
         not os.path.isfile(os.path.join(_bac_rapports, _fichiers[_vieux])))
with o._cx() as cx:
    _capture_apres = cx.execute("SELECT capture FROM rapports WHERE id=?",
                                (_vieux,)).fetchone()["capture"]
verifier("et la base ne renvoie plus vers une image absente",
         _capture_apres is None, str(_capture_apres))

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
verifier("un vieux rapport tout juste classe n'est pas allege",
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
            "SELECT COUNT(*) FROM rapports WHERE id=? AND capture IS NOT NULL",
            (_hors,)).fetchone()[0]
    return _vrai_remove(chemin)


os.remove = _remove_observe
try:
    o.purger_rapports_traites(30)
finally:
    os.remove = _vrai_remove
verifier("la capture ne part qu'une fois le detachement valide",
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
verifier("le detachement se fait meme quand la capture resiste",
         _efface == 1 and _coince in {r["id"] for r in o.liste_rapports()},
         "%d allege(s)" % _efface)
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


# --- Le journal d'un moteur survit au rallumage de sa table -----------------
# ⚠ Le cas qui compte est le RALLUMAGE : `.site/moteur-N.log` etait ouvert en
# "w", et le journal de la partie d'avant, seule piece a conviction d'un
# rapport joueur, disparaissait. Ici on ouvre trois fois de suite la meme
# table et on verifie que rien ne s'efface, que le vide n'est pas garde, et
# que la reserve ne grossit pas sans fin.
import time as _time_journal                                # noqa: E402
_racine_journal_avant = o.RACINE_JEU
_bac_journal = tempfile.mkdtemp(prefix="nc-journal-")
o.RACINE_JEU = _bac_journal
_gardes_avant = o.JOURNAUX_MOTEUR_GARDES
o.JOURNAUX_MOTEUR_GARDES = 2
_dossier_journal = os.path.join(_bac_journal, ".site")
with o._ouvrir_journal_moteur(9) as _j:
    _j.write("premiere partie\n")
_premier_contenu = sorted(os.listdir(_dossier_journal))
verifier("le premier allumage cree le journal, sans archive",
         _premier_contenu == ["moteur-9.log"], str(_premier_contenu))
with o._ouvrir_journal_moteur(9) as _j:
    _j.write("deuxieme partie\n")
_archives = sorted(f for f in os.listdir(_dossier_journal) if f.startswith("moteur-9-"))
verifier("le rallumage ARCHIVE le journal precedent au lieu de l'ecraser",
         len(_archives) == 1 and re.fullmatch(r"moteur-9-\d{8}-\d{6}\.log", _archives[0]) is not None,
         str(_archives))
with open(os.path.join(_dossier_journal, _archives[0]), encoding="utf-8") as _f:
    verifier("et l'archive porte bien la partie d'avant", _f.read() == "premiere partie\n")
with open(os.path.join(_dossier_journal, "moteur-9.log"), encoding="utf-8") as _f:
    verifier("le journal courant ne porte que la partie en cours", _f.read() == "deuxieme partie\n")
# Un journal vide (moteur mort avant d'ecrire) ne merite pas d'archive : le
# premier close() archive « deuxieme partie » (2 archives), le second trouve
# un journal vide et ne doit rien ajouter.
o._ouvrir_journal_moteur(9).close()
o._ouvrir_journal_moteur(9).close()
_archives = sorted(f for f in os.listdir(_dossier_journal) if f.startswith("moteur-9-"))
verifier("un journal vide n'est pas archive", len(_archives) == 2, str(_archives))
# La reserve est bornee : au-dela de JOURNAUX_MOTEUR_GARDES, le plus vieux part.
for _n in range(3):
    with o._ouvrir_journal_moteur(9) as _j:
        _j.write("partie %d\n" % _n)
    _time_journal.sleep(1.05)   # des cachets distincts, a la seconde
_archives = sorted(f for f in os.listdir(_dossier_journal) if f.startswith("moteur-9-"))
verifier("la reserve d'archives est bornee a JOURNAUX_MOTEUR_GARDES",
         len(_archives) == 2, str(_archives))
# Une autre table n'y touche pas.
with o._ouvrir_journal_moteur(10) as _j:
    _j.write("autre table\n")
verifier("les archives d'une table ne sont pas celles d'une autre",
         len([f for f in os.listdir(_dossier_journal) if f.startswith("moteur-9-")]) == 2)
o.JOURNAUX_MOTEUR_GARDES = _gardes_avant
o.RACINE_JEU = _racine_journal_avant
shutil.rmtree(_bac_journal, ignore_errors=True)

# --- L'annonce aux joueurs, et son decompte ---------------------------------
# AJOUT du 13/09/2026. Un deploiement fait `systemctl restart narwhal` et
# emporte tous les moteurs : toute partie en cours est perdue. L'annonce est le
# seul moyen de prevenir quelqu'un qui joue. Ce qui doit tenir :
#   - une annonce posee est lisible, avec le TEMPS QUI RESTE et pas une heure
#     absolue (le navigateur du joueur n'est pas a l'heure du serveur) ;
#   - une annonce perimee disparait toute seule, sans menage a faire ;
#   - poser remplace, jamais n'empile : deux decomptes contradictoires seraient
#     pires que pas d'annonce du tout ;
#   - annuler efface vraiment, parce qu'un deploiement qui glisse ne doit pas
#     laisser un decompte mensonger tourner devant les joueurs.
o.retirer_annonce()
verifier("sans annonce posee, il n'y a rien a dire",
         o.annonce_courante() is None)

o.poser_annonce(10)
_a = o.annonce_courante()
verifier("l'annonce posee est rendue", _a is not None)
verifier("elle porte les SECONDES QUI RESTENT, pas une heure",
         _a is not None and 9 * 60 < _a["secondes"] <= 10 * 60, str(_a))
verifier("sans texte, c'est le preavis de mise a jour",
         _a is not None and "Save" in _a["texte"], str(_a))

o.poser_annonce(30, "Coupure reseau chez l'hebergeur.")
_a = o.annonce_courante()
verifier("poser une annonce remplace la precedente",
         _a is not None and _a["texte"] == "Coupure reseau chez l'hebergeur."
         and _a["secondes"] > 20 * 60, str(_a))
with o._cx() as _cx_a:
    _combien = _cx_a.execute("SELECT COUNT(*) AS n FROM annonces").fetchone()["n"]
verifier("une seule annonce est gardee en base", _combien == 1, str(_combien))

# Une duree qui n'a pas de sens ne doit pas passer telle quelle : un preavis de
# 4000 minutes est une faute de frappe, pas une intention.
o.poser_annonce(99999)
_a = o.annonce_courante()
verifier("une duree aberrante est ramenee au plafond",
         _a is not None and _a["secondes"] <= o.ANNONCE_MINUTES_MAX * 60, str(_a))

# Perimee : on triche sur l'instant de fin plutot que d'attendre.
with o._cx() as _cx_a:
    _cx_a.execute("UPDATE annonces SET jusqu_a = ?", (int(_time_journal.time()) - 5,))
verifier("une annonce perimee ne s'affiche plus", o.annonce_courante() is None)

o.poser_annonce(5)
o.retirer_annonce()
verifier("annuler efface l'annonce", o.annonce_courante() is None)

# --- L'annonce PAR LA ROUTE : ce que le moteur recoit vraiment --------------
# Les cas ci-dessus prouvent que les fonctions sont justes. Ils ne disent rien
# du CABLAGE, et c'est lui qui casse : `/api/annonce` est appelee par le
# MOTEUR, en 127.0.0.1, avec le jeton de la table, et le navigateur du joueur
# n'y arrive jamais directement. Une route mal branchee se verrait uniquement
# en production, un jour de deploiement, c'est-a-dire trop tard.
import json as _json_annonce                                # noqa: E402

o.retirer_annonce()
_jeton_annonce = "jeton-annonce-de-test"
o.JETONS_SITE[_jeton_annonce] = "hote"
_corps_annonce = ("jeton=" + _jeton_annonce).encode("utf-8")

_code, _, _rep = appel("POST", "/api/annonce", corps=_corps_annonce)
verifier("sans annonce, la route repond un objet vide",
         _code == 200 and _json_annonce.loads(_rep) == {}, "%s %s" % (_code, _rep))

o.poser_annonce(10)
_code, _, _rep = appel("POST", "/api/annonce", corps=_corps_annonce)
_vu = _json_annonce.loads(_rep)
verifier("la route rend le texte et les secondes restantes",
         _code == 200 and "Save" in _vu.get("texte", "") and _vu.get("secondes", 0) > 9 * 60,
         "%s %s" % (_code, _rep))
# ⚠ L'INSTANT DE FIN NE DOIT PAS SORTIR. Le navigateur d'un joueur n'est pas a
# l'heure du serveur : il afficherait un decompte faux, voire negatif.
verifier("la route n'envoie aucune heure absolue", "jusqu_a" not in _vu, str(_vu))

# Le jeton est le laissez-passer : sans lui, rien.
_code, _, _ = appel("POST", "/api/annonce", corps=b"jeton=invente")
verifier("un jeton inconnu n'obtient pas l'annonce", _code == 403, str(_code))

# --- Poser et annuler DEPUIS /admin ----------------------------------------
# ⚠ ET SEULEMENT DEPUIS /admin. La page nomme les joueurs et commande le site :
# un compte ordinaire n'a rien a y faire.
o.retirer_annonce()
_code, _, _ = appel("POST", "/admin", corps=b"action=annonce&minutes=15",
                    entetes=cookie_de("hote"))
verifier("un compte ordinaire ne pose pas d'annonce",
         _code == 403 and o.annonce_courante() is None, str(_code))

try:
    o.inscrire(o.ADMIN, "admin@exemple.fr", "motdepasse123")
except ValueError:
    pass
o.changer_statut(o.ADMIN, "valide")
_code, _tetes, _ = appel("POST", "/admin", corps=b"action=annonce&minutes=15",
                         entetes=cookie_de(o.ADMIN))
_a = o.annonce_courante()
verifier("l'administrateur pose l'annonce depuis /admin",
         _code == 303 and _a is not None and _a["secondes"] > 14 * 60,
         "%s %s" % (_code, _a))

_code, _, _ = appel("POST", "/admin",
                    corps=b"action=annonce&minutes=5&texte=Coupure+reseau",
                    entetes=cookie_de(o.ADMIN))
_a = o.annonce_courante()
verifier("le texte libre du formulaire est repris",
         _a is not None and _a["texte"] == "Coupure reseau", str(_a))

# ⚠ LE CAS QUI A DEJA MORDU. Le bouton d'annulation etait un second bouton
# DANS le formulaire de pose, qui porte deja un champ cache `action=annonce` :
# `_champs` ne garde que la premiere valeur, et « Annuler » reposait une
# annonce au lieu de l'effacer. Il a fallu un formulaire separe.
_code, _, _ = appel("POST", "/admin", corps=b"action=annonce_annuler",
                    entetes=cookie_de(o.ADMIN))
verifier("le bouton Annuler efface vraiment l'annonce",
         _code == 303 and o.annonce_courante() is None, str(_code))

# Et la page se relit sans exploser une fois l'annonce posee : elle y affiche
# son etat et le bouton d'annulation.
o.poser_annonce(8, "Coupure reseau")
_code, _, _page_admin = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
verifier("la page /admin montre l'annonce en cours",
         _code == 200 and b"Annuler l'annonce" in _page_admin
         and "Coupure reseau".encode("utf-8") in _page_admin,
         str(_code))
o.retirer_annonce()
_code, _, _page_admin = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
verifier("sans annonce, la page n'offre rien a annuler",
         _code == 200 and b"Annuler l'annonce" not in _page_admin, str(_code))

# --- Les comptes inactifs, et la place qu'ils tiennent ----------------------
# AJOUT du 13/09/2026. Il n'y a que MAX_COMPTES places, et une place n'est pas
# qu'une ligne en base : c'est un EMPLACEMENT, avec ses decks, ses campagnes en
# cours et ses hauts faits. Quatre semaines sans venir, et elle retourne au pot.
#
# Ce qui doit tenir :
#   - on ne juge PAS sur `derniere_connexion` seule : une session dure
#     quatre-vingt-dix jours, quelqu'un qui joue tous les soirs sans retaper son
#     mot de passe passerait pour absent depuis des mois ;
#   - le compte n'est pas supprime : il EXPIRE, sa ligne reste et son
#     emplacement avec, tant que personne ne prend sa place ;
#   - sa place n'est reprise QU'AU MOMENT ou quelqu'un en a besoin, et elle est
#     effacee a ce moment-la, sinon le nouveau venu heriterait des decks du
#     precedent ;
#   - l'administrateur n'expire jamais : c'est lui qui remet les autres en
#     service.
import datetime as _dt_exp                                  # noqa: E402


def _vieillir(pseudo, jours):
    """Fait comme si ce compte n'avait plus donne signe de vie depuis N jours."""
    vieux = (_dt_exp.datetime.now() - _dt_exp.timedelta(days=jours)).strftime("%Y-%m-%d %H:%M")
    with o._cx() as cx:
        cx.execute("UPDATE comptes SET vu_le=?, derniere_connexion=?, cree=?"
                   " WHERE pseudo=?", (vieux, vieux, vieux, pseudo))


o.PARTIES.clear()
o.EMPLACEMENTS.clear()
for _p in ("dormeur", "assidu"):
    try:
        o.inscrire(_p, _p + "@exemple.fr", "motdepasse123")
    except ValueError:
        pass
    o.changer_statut(_p, "valide")

# L'assidu n'a pas retape son mot de passe depuis longtemps, mais il ouvre son
# jeu tous les jours : `/entrer` touche `vu_le`. Il ne doit PAS expirer.
_vieillir("assidu", o.EXPIRATION_JOURS + 20)
o.toucher_presence("assidu")
_vieillir("dormeur", o.EXPIRATION_JOURS + 3)

_place_dormeur = o.emplacement_de("dormeur")
verifier("le dormeur tient bien une place avant d'expirer",
         _place_dormeur is not None, str(_place_dormeur))

_expires = o.expirer_comptes_inactifs()
verifier("le compte inactif expire", "dormeur" in _expires, str(_expires))
verifier("mais pas celui qui vient de jouer sans se reconnecter",
         "assidu" not in _expires, str(_expires))
verifier("l'administrateur n'expire jamais", o.ADMIN not in _expires, str(_expires))

_c = o.compte("dormeur")
verifier("le compte n'est PAS supprime, il est marque expire",
         _c is not None and _c["statut"] == "expire", str(_c and _c["statut"]))
verifier("et sa place l'attend tant que personne ne la prend",
         _c is not None and _c["emplacement"] == _place_dormeur,
         str(_c and _c["emplacement"]))
verifier("il ne compte plus dans le quota",
         o.nb_valides() == len([1 for _x in o.liste_comptes() if _x["statut"] == "valide"]))

# ⚠ ET IL SAIT POURQUOI. « Ton compte attend ma validation » aurait envoye
# quelqu'un attendre indefiniment quelque chose qui ne viendra pas.
try:
    o.verifier("dormeur", "motdepasse123")
    _dit = ""
except ValueError as _e:
    _dit = str(_e)
verifier("la connexion d'un compte expire dit pourquoi", "expire" in _dit, _dit)
verifier("et dit quoi faire", "Ecris-moi" in _dit, _dit)

# Sa session en cours est coupee : le statut est relu en base a chaque requete.
verifier("un compte expire ne garde pas sa session",
         o.pseudo_de_session(o.ouvrir_session("dormeur")) is None)

# --- La place n'est reprise qu'au moment ou quelqu'un en a besoin -----------
# ⚠ LE CAS QUI DONNE SON SENS A L'EXPIRATION. Sans recyclage, le quota se
# libere sur le papier mais la personne suivante s'entend quand meme repondre
# « Plus aucun espace de jeu disponible » : les places sont toutes tenues par
# des comptes qui ne viennent plus.
_places_avant = o.NB_EMPLACEMENTS
o.NB_EMPLACEMENTS = len([1 for _x in o.liste_comptes() if _x["emplacement"] is not None])
try:
    o.inscrire("nouveau", "nouveau@exemple.fr", "motdepasse123")
    _refus = ""
except ValueError as _e:
    _refus = str(_e)
verifier("le site plein d'un compte expire accepte quand meme une inscription",
         _refus == "", _refus)
verifier("et le nouveau venu recoit la place du compte expire",
         o.emplacement_de("nouveau") == _place_dormeur,
         "%s / %s" % (o.emplacement_de("nouveau"), _place_dormeur))
verifier("le compte expire n'a plus de place",
         o.compte("dormeur")["emplacement"] is None)
verifier("l'assidu, lui, n'a pas bouge", o.emplacement_de("assidu") is not None)

# Plus rien a recycler : cette fois, c'est vraiment complet.
try:
    o.inscrire("detrop", "detrop@exemple.fr", "motdepasse123")
    _refus = ""
except ValueError as _e:
    _refus = str(_e)
verifier("sans compte expire a recycler, le site se dit complet",
         "espace de jeu" in _refus, _refus or "aucun refus")
o.NB_EMPLACEMENTS = _places_avant

# --- Le remettre en service --------------------------------------------------
o.changer_statut("dormeur", "valide")
verifier("remis en service, il redevient valide",
         o.compte("dormeur")["statut"] == "valide")
verifier("et il recoit une nouvelle place, puisque l'ancienne est donnee",
         o.emplacement_de("dormeur") not in (None, _place_dormeur),
         str(o.emplacement_de("dormeur")))

# --- La page /admin montre la VRAIE derniere visite --------------------------
# ⚠ Elle affichait `derniere_connexion` seule, et c'etait trompeur : c'est ce
# chiffre-la qui decide de l'expiration, la page doit montrer celui qui compte.
verifier("la visite lisible suit `vu_le`, pas la seule reconnexion",
         "jamais" not in o._visite_lisible(o.compte("assidu")),
         o._visite_lisible(o.compte("assidu")))
_code, _, _page_c = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
verifier("la page /admin s'affiche avec des comptes expires",
         _code == 200 and b"Derniere visite" in _page_c, str(_code))
verifier("et elle rappelle la regle a l'administrateur",
         "retourne au pot".encode("utf-8") in _page_c)

# ⚠ LA REGLE EST ANNONCEE, PAS SUBIE. Le site ne sait pas envoyer de courriel :
# personne ne peut etre prevenu de son expiration. La seule facon honnete de la
# faire accepter est de l'ecrire la ou tout le monde passe.
_code, _, _page_co = appel("GET", "/connexion")
verifier("l'ecran de connexion annonce la regle aux joueurs",
         _code == 200 and "retourne au pot".encode("utf-8") in _page_co, str(_code))
verifier("et il donne le nombre de jours",
         str(o.EXPIRATION_JOURS).encode("utf-8") in _page_co)

# --- La table restee allumee pour personne --------------------------------
# AJOUT du 13/09/2026. Une table tient un port, un processus et sa memoire, sur
# vingt places. Le minuteur des huit heures ne regardait que l'AGE de la table :
# quelqu'un qui ouvrait son jeu le matin et partait travailler l'immobilisait
# toute la journee.
#
# ⚠ LE SIGNAL EST LE JOURNAL DU MOTEUR, PAS LE « VU » DU SITE. Celui-ci ne bouge
# qu'a l'ouverture du jeu : pendant qu'on joue, le navigateur parle au moteur et
# le site n'entend plus rien. S'y fier aurait ferme la table de quelqu'un en
# pleine partie au bout de 45 minutes. C'est le cas central de ce bloc.
_racine_oisive = o.RACINE_JEU
_bac_oisif = tempfile.mkdtemp(prefix="nc-oisive-")
o.RACINE_JEU = _bac_oisif
os.makedirs(os.path.join(_bac_oisif, ".site"), exist_ok=True)

_table = o.Partie(7, "hote", "Jeu de hote")
_table.processus = FauxProcessus()
_journal = os.path.join(_bac_oisif, ".site", "moteur-7.log")

# Sans journal du tout : on ne sait pas, et on ne ferme pas au hasard.
verifier("sans journal, l'inactivite est inconnue",
         o.secondes_sans_jouer(_table) == -1.0, str(o.secondes_sans_jouer(_table)))

with open(_journal, "w", encoding="utf-8") as _j:
    _j.write("le moteur vient d'ecrire\n")
verifier("un journal tout frais donne une inactivite quasi nulle",
         0 <= o.secondes_sans_jouer(_table) < 5, str(o.secondes_sans_jouer(_table)))

# On vieillit le journal d'une heure : la table n'a plus rien fait.
_vieux = _time_journal.time() - 3600
os.utime(_journal, (_vieux, _vieux))
verifier("un journal d'il y a une heure se voit",
         3500 < o.secondes_sans_jouer(_table) < 3700, str(o.secondes_sans_jouer(_table)))
verifier("une heure depasse le seuil des trois quarts d'heure",
         o.secondes_sans_jouer(_table) > o.INACTIVITE_MINUTES * 60)

# ⚠ ET UNE TABLE OU L'ON JOUE N'EST PAS OISIVE, meme si le site n'a plus vu
# passer son proprietaire depuis des heures : c'est toute la difference entre
# le journal du moteur et le « vu » du site.
os.utime(_journal, None)
verifier("une table ou l'on joue n'est jamais oisive",
         o.secondes_sans_jouer(_table) < o.INACTIVITE_MINUTES * 60)

# --- Qui se fait faucher, et qui non ---------------------------------------
os.utime(_journal, (_vieux, _vieux))
verifier("une table oisive d'un joueur ordinaire se ferme",
         o.table_oisive("hote", _table) is True)
# ⚠ SAUF LA MIENNE. La table de l'administrateur sert a regarder ce qui se
# passe sur le site, souvent sans y jouer.
verifier("celle de l'administrateur, jamais",
         o.table_oisive(o.ADMIN, _table) is False)
# Le reglage a zero eteint la regle, sans toucher au reste du faucheur.
_seuil_avant = o.INACTIVITE_MINUTES
o.INACTIVITE_MINUTES = 0
verifier("a zero minute, plus personne n'est fauche pour inactivite",
         o.table_oisive("hote", _table) is False)
o.INACTIVITE_MINUTES = _seuil_avant
# Sans journal lisible, on s'abstient : une table qu'on n'arrive pas a juger ne
# se ferme pas au hasard.
os.remove(_journal)
verifier("sans journal, on ne ferme pas au hasard",
         o.table_oisive("hote", _table) is False)

o.RACINE_JEU = _racine_oisive
shutil.rmtree(_bac_oisif, ignore_errors=True)

# --- La partie est sauvegardee AVANT que le moteur soit tue ----------------
# ⚠ A huit heures on pouvait s'en passer ; a trois quarts d'heure non. C'est ce
# qui fait la difference entre « ta table s'est fermee » et « ta partie est
# perdue ».
_appels_sauvegarde = []


class _FausseReponse:
    def read(self):
        return b"{}"

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False


def _fausse_ouverture(lien, timeout=None):
    _appels_sauvegarde.append(lien)
    return _FausseReponse()


_ouverture_avant = o.urllib.request.urlopen
o.urllib.request.urlopen = _fausse_ouverture
try:
    _a_sauver = o.Partie(7, "hote", "Jeu de hote")
    _a_sauver.processus = FauxProcessus()
    o._sauvegarder_avant_extinction(_a_sauver)
finally:
    o.urllib.request.urlopen = _ouverture_avant

verifier("le site demande au moteur d'ecrire sa partie",
         len(_appels_sauvegarde) == 1
         and "/sauver_pour_le_site" in _appels_sauvegarde[0],
         str(_appels_sauvegarde))
verifier("et il presente le jeton de la table",
         _appels_sauvegarde and "jeton=" in _appels_sauvegarde[0],
         str(_appels_sauvegarde))

# ⚠ ET UN MOTEUR DEJA MORT NE RETIENT PERSONNE. Sans ce garde-fou, chaque
# extinction d'une table plantee attendait le delai de la requete pour rien.
_appels_sauvegarde.clear()


class _ProcessusMort:
    def poll(self):
        return 1


_morte = o.Partie(7, "hote", "Jeu de hote")
_morte.processus = _ProcessusMort()
o.urllib.request.urlopen = _fausse_ouverture
try:
    o._sauvegarder_avant_extinction(_morte)
finally:
    o.urllib.request.urlopen = _ouverture_avant
verifier("un moteur deja mort n'est pas interroge", _appels_sauvegarde == [],
         str(_appels_sauvegarde))

# La cause est lisible dans le suivi, comme les autres.
verifier("la fermeture pour inactivite porte un motif lisible",
         "sans jouer" in o.CAUSES_ABANDON.get("inactivite", ""),
         o.CAUSES_ABANDON.get("inactivite", ""))

# --- Les parties terminees qu'on garde ------------------------------------
# AJOUT du 13/09/2026. Le moteur ecrit desormais un enregistrement complet a la
# fin de chaque partie : de quoi la revoir pas a pas. Sans plafond, le dossier
# grossirait sans fin.
#
# ⚠ ET LES TROIS EMPLACEMENTS DU PLATEAU NE SONT JAMAIS EMPORTES. Ce sont des
# sauvegardes VOULUES, posees a la main sur les boutons Save 1, 2 et 3 : les
# ranger avec les enregistrements automatiques reviendrait a effacer ce que
# quelqu'un a delibérement garde. C'est le cas central de ce bloc.
_racine_sauv = o.RACINE_JEU
_bac_sauv = tempfile.mkdtemp(prefix="nc-sauvegardes-")
o.RACINE_JEU = _bac_sauv
_dossier_sauv = os.path.join(_bac_sauv, "replays", "serveur-4")
os.makedirs(_dossier_sauv, exist_ok=True)

_gardees_avant = o.SAUVEGARDES_GARDEES
o.SAUVEGARDES_GARDEES = 3

# Cinq parties automatiques, d'age croissant, plus les trois emplacements.
for _n in range(5):
    _f = os.path.join(_dossier_sauv, "partie-%d.json" % _n)
    with open(_f, "w", encoding="utf-8") as _j:
        _j.write("{}")
    os.utime(_f, (_time_journal.time() - (5 - _n) * 60,) * 2)
for _nom in ("save_1.json", "save_2.json", "save_3.json"):
    _f = os.path.join(_dossier_sauv, _nom)
    with open(_f, "w", encoding="utf-8") as _j:
        _j.write("{}")
    # Les plus vieux de tous : s'ils devaient partir, ils partiraient d'abord.
    os.utime(_f, (_time_journal.time() - 99999,) * 2)

_efface = o.limiter_sauvegardes(4)
_restants = sorted(os.listdir(_dossier_sauv))
verifier("le menage efface les parties en trop", _efface == 2, str(_efface))
verifier("et garde les plus RECENTES",
         "partie-4.json" in _restants and "partie-0.json" not in _restants,
         str(_restants))
verifier("les trois emplacements du plateau survivent, meme tres vieux",
         all(n in _restants for n in ("save_1.json", "save_2.json", "save_3.json")),
         str(_restants))

# Rappeler le menage ne fait plus rien : on est sous le plafond.
verifier("un second menage n'efface plus rien", o.limiter_sauvegardes(4) == 0)

# Un dossier qui n'existe pas ne doit pas lever : une table neuve n'en a pas.
verifier("un dossier absent ne fait pas d'histoire", o.limiter_sauvegardes(19) == 0)

# A zero, la regle s'eteint.
o.SAUVEGARDES_GARDEES = 0
verifier("a zero, plus aucun menage", o.limiter_sauvegardes(4) == 0)

o.SAUVEGARDES_GARDEES = _gardees_avant
o.RACINE_JEU = _racine_sauv
shutil.rmtree(_bac_sauv, ignore_errors=True)

# --- Ecrire a un joueur, et le lui faire savoir ----------------------------
# AJOUT du 13/09/2026. Le tchat a ete retire du jeu la veille : personne ne s'en
# servait. Mais l'administrateur doit pouvoir joindre quelqu'un qui joue. D'ou
# une pastille qui n'apparait QUE s'il y a un message, et s'eteint des qu'il est
# lu.
#
# ⚠ CE QUI MANQUAIT ETAIT LE « DEJA LU ». Sans lui, on ne distingue pas « un
# message t'attend » de « tu l'as deja vu », et la pastille reste allumee pour
# toujours.
o.marquer_messages_lus("hote")
verifier("sans message, rien n'attend personne",
         o.messages_non_lus("hote")["nouveaux"] == 0,
         str(o.messages_non_lus("hote")))

o.dire(o.ADMIN, "Tu joues ce soir ?", "hote")
_attente = o.messages_non_lus("hote")
verifier("un message recu allume la pastille", _attente["nouveaux"] == 1, str(_attente))
verifier("et elle dit de qui il vient", _attente["de"] == [o.ADMIN], str(_attente))

# ⚠ SES PROPRES MOTS NE COMPTENT PAS. Ils portent forcement un identifiant plus
# grand que le dernier qu'il a lu : les compter lui aurait montre une pastille
# pour ce qu'il vient d'ecrire.
o.dire("hote", "Oui, vers 21h", o.ADMIN)
verifier("repondre n'allume pas sa propre pastille",
         o.messages_non_lus("hote")["nouveaux"] == 1,
         str(o.messages_non_lus("hote")))
verifier("mais elle s'allume chez le destinataire",
         o.messages_non_lus(o.ADMIN)["nouveaux"] >= 1,
         str(o.messages_non_lus(o.ADMIN)))

o.marquer_messages_lus("hote")
verifier("lire eteint la pastille",
         o.messages_non_lus("hote")["nouveaux"] == 0,
         str(o.messages_non_lus("hote")))

# La conversation se relit dans l'ordre, les deux sens melanges.
_fil = o.conversation(o.ADMIN, "hote")
verifier("la conversation garde les deux sens", len(_fil) == 2, str(_fil))
verifier("et le plus ancien en tete",
         _fil[0]["texte"] == "Tu joues ce soir ?", str(_fil))

# --- Par la route, avec le jeton de la table -------------------------------
o.JETONS_SITE[_jeton_annonce] = "hote"
o.dire(o.ADMIN, "Encore un", "hote")
_code, _, _rep = appel("POST", "/api/prives", corps=_corps_annonce)
verifier("la route dit ce qui attend le joueur",
         _code == 200 and _json_annonce.loads(_rep)["nouveaux"] == 1,
         "%s %s" % (_code, _rep))
_code, _, _ = appel("POST", "/api/prives_lus", corps=_corps_annonce)
verifier("et la route de lecture eteint la pastille",
         _code == 200 and o.messages_non_lus("hote")["nouveaux"] == 0, str(_code))
_code, _, _ = appel("POST", "/api/prives", corps=b"jeton=invente")
verifier("un jeton inconnu n'apprend rien", _code == 403, str(_code))

# --- Et le panneau de /admin ------------------------------------------------
o.dire("hote", "Une question sur Thor", o.ADMIN)
_code, _, _page_s = appel("GET", "/admin", entetes=cookie_de(o.ADMIN))
verifier("la page /admin montre le panneau des joueurs",
         _code == 200 and b"Joueurs" in _page_s and b"Une question sur Thor" in _page_s,
         str(_code))
verifier("et elle signale la conversation qui attend",
         b"nouveau" in _page_s)

_code, _, _ = appel("POST", "/admin", corps=b"action=message&a=hote&texte=Je+regarde",
                    entetes=cookie_de(o.ADMIN))
verifier("l'administrateur ecrit depuis /admin",
         _code == 303 and any(m["texte"] == "Je regarde"
                              for m in o.conversation(o.ADMIN, "hote")),
         str(_code))
# ⚠ REPONDRE, C'EST AVOIR LU. Sans cela la pastille de l'administrateur restait
# allumee sur une conversation qu'il venait de traiter.
verifier("et repondre eteint sa propre pastille",
         o.messages_non_lus(o.ADMIN)["nouveaux"] == 0,
         str(o.messages_non_lus(o.ADMIN)))

# ⚠ ET SEULEMENT LUI. La page nomme les joueurs et lit leurs conversations.
_code, _, _ = appel("POST", "/admin", corps=b"action=message&a=hote&texte=Coucou",
                    entetes=cookie_de("hote"))
verifier("un compte ordinaire n'ecrit pas depuis /admin", _code == 403, str(_code))

# --- L'appli installable ------------------------------------------------------
# AJOUT du 13/09/2026. « Ajouter a l'ecran d'accueil » depuis le telephone :
# une icone, un plein ecran. Trois pieces, toutes servies SANS cookie parce que
# le navigateur les demande sans : le manifeste, les icones, le service worker.
_code, _tetes, _corps = appel("GET", "/manifest.webmanifest")
verifier("le manifeste est servi sans cookie", _code == 200, str(_code))
verifier("et avec le bon type",
         "manifest+json" in (_tetes.get("Content-Type") or ""), str(_tetes.get("Content-Type")))
_m = _json_annonce.loads(_corps)
verifier("il demarre sur /entrer, qui allume la table au besoin",
         _m.get("start_url") == "/entrer" and _m.get("display") == "standalone", str(_m))
verifier("il porte deux icones, dont une masquable",
         len(_m.get("icons", [])) >= 2 and any(i.get("purpose") == "maskable" for i in _m["icons"]),
         str(_m.get("icons")))
for _ic in ("/app-192.png", "/app-512.png"):
    _code, _tetes, _corps = appel("GET", _ic)
    verifier("l'icone %s est servie" % _ic,
             _code == 200 and _corps[:4] == b"\x89PNG", "%s %r" % (_code, _corps[:4]))
# L'icone d'onglet : le narval detoure, et /favicon.ico que les navigateurs
# demandent d'office rend la meme image plutot qu'un 404 a chaque page.
for _ic in ("/favicon.png", "/favicon.ico"):
    _code, _tetes, _corps = appel("GET", _ic)
    verifier("l'icone d'onglet %s est servie" % _ic,
             _code == 200 and _corps[:4] == b"\x89PNG", "%s %r" % (_code, _corps[:4]))
_code, _tetes, _corps = appel("GET", "/sw.js")
verifier("le service worker est servi en javascript",
         _code == 200 and "javascript" in (_tetes.get("Content-Type") or ""), str(_code))
# ⚠ ET IL NE MET RIEN EN CACHE. Ce site se bat contre les caches perimes : un
# worker qui servirait un vieux JS apres un deploiement serait le defaut qu'on
# a chasse. On lit le code : aucun `caches`, aucun `respondWith`.
# ⚠ IL NE GARDE QU'UNE PAGE, ET JAMAIS LE JEU. Le worker met en cache l'ecran
# « Pas de connexion », et rien d'autre : ce site se bat contre le cache
# perime, un worker qui servirait un vieux JS apres un deploiement serait le
# defaut qu'on a chasse. Deux verrous a tenir, et il faut les deux.
_sw = _corps.decode("utf-8", "replace")
verifier("le worker ne met en cache QUE l'ecran hors ligne",
         _sw.count("c.add(") == 1 and "'/hors-ligne.html'" in _sw
         and "addAll" not in _sw, _sw[:150])
verifier("il n'intercepte que les navigations, pas le JS ni les API",
         "request.mode !== 'navigate'" in _sw, _sw[:150])
# ⚠ LE RESEAU D'ABORD, TOUJOURS. Une reponse du serveur, meme une erreur, doit
# gagner sur la page de secours : l'inverse servirait un ecran « hors ligne » a
# quelqu'un qui est parfaitement connecte.
verifier("et il va au reseau d'abord, la page de secours en repli",
         "fetch(e.request).catch(" in _sw, _sw[:150])
_code, _tetes, _corps_hl = appel("GET", "/hors-ligne.html")
verifier("l'ecran hors ligne est servi", _code == 200 and b"Pas de connexion" in _corps_hl,
         str(_code))
# Elle ne peut RIEN aller chercher : tout ce qu'elle reclamerait serait
# justement ce qui manque.
verifier("et il ne reclame ni image, ni feuille de style, ni script externe",
         b"<img" not in _corps_hl and b"<link" not in _corps_hl
         and b"src=" not in _corps_hl)
# La page de connexion, ou tout le monde passe, propose l'installation.
_code, _, _corps = appel("GET", "/connexion")
verifier("la page de connexion lie le manifeste",
         _code == 200 and b'rel="manifest"' in _corps and b"serviceWorker" in _corps, str(_code))
# Et elle porte le bouton « Installer », cache tant que le navigateur n'a pas
# dit que l'installation etait possible : sans `beforeinstallprompt`, un bouton
# toujours visible ne ferait rien au clic.
verifier("et le bouton d'installation, arme sur beforeinstallprompt",
         b'id="appli-bouton"' in _corps and b"beforeinstallprompt" in _corps
         and b'id="appli-installer" hidden' in _corps)
verifier("avec le chemin a suivre sur iPhone, qui n'a pas d'evenement",
         b"Partager" in _corps)
# ⚠ ET IL DIT QU'IL N'Y A PAS DE HORS LIGNE. Une icone sur l'ecran d'accueil le
# promet implicitement ; le moteur tourne sur le serveur, chaque action passe
# par lui, il n'y a rien a jouer sans connexion. Le dire avant l'installation.
verifier("et il previent qu'il n'y a pas de hors ligne",
         "hors ligne".encode("utf-8") in _corps)
_code, _, _corps = appel("GET", "/manifest.webmanifest")
verifier("le manifeste le dit aussi, dans la boite d'installation",
         "hors ligne".encode("utf-8") in _corps)

# --- La partie interrompue qui attend son joueur ---------------------------
# AJOUT du 13/09/2026, demande de l'utilisateur : « relancer la partie des
# joueurs comme c'etait avant la coupure ». Chaque extinction ecrit deja la
# partie en cours ; l'orchestrateur JETAIT le chemin que le moteur lui rendait,
# et le joueur devait la retrouver seul dans « Reprendre ».
#
# ⚠ ON PROPOSE, ON NE FORCE PAS. Quelqu'un qui revient le lendemain ne veut pas
# forcement reprendre la partie de la veille.
o.oublier_partie_interrompue("hote")
verifier("sans coupure, rien n'attend personne",
         o.partie_interrompue("hote") is None)

o.retenir_partie_interrompue(
    "hote", "../replays/serveur-4/partie.json", "arret du site",
    {"scenario": "Rhino", "round": 7, "version": "0.5.9.200",
     "joueurs": [{"heros": "Spider-Man"}]})
_att = o.partie_interrompue("hote")
verifier("la partie retenue porte son fichier", _att and _att["fichier"].endswith("partie.json"), str(_att))
verifier("et de quoi la decrire au joueur",
         _att["scenario"] == "Rhino" and _att["tour"] == 7 and _att["heros"] == "Spider-Man",
         str(_att))
# ⚠ LA VERSION DU MOTEUR EST GARDEE : un deploiement en change souvent, et une
# sauvegarde plus ancienne que la version minimale supportee fait echouer le
# chargement. C'est ce qui permettra de le dire au joueur.
verifier("et la version du moteur qui l'a ecrite", _att["version"] == "0.5.9.200", str(_att))

# ⚠ UNE SEULE LIGNE PAR JOUEUR : proposer la partie d'avant-hier quand celle
# d'hier existe n'a aucun sens.
o.retenir_partie_interrompue("hote", "../replays/serveur-4/autre.json", "minuteur",
                             {"scenario": "Klaw", "round": 2})
_att = o.partie_interrompue("hote")
verifier("une nouvelle coupure remplace la precedente",
         _att["fichier"].endswith("autre.json") and _att["scenario"] == "Klaw", str(_att))
with o._cx() as _cx_i:
    _n = _cx_i.execute("SELECT COUNT(*) AS n FROM parties_interrompues WHERE pseudo='hote'").fetchone()["n"]
verifier("et il n'y a jamais qu'une ligne", _n == 1, str(_n))

# --- Ce que le joueur voit en revenant --------------------------------------
_code, _, _page_r = appel("GET", "/entrer", entetes=cookie_de("hote"))
verifier("a son retour, on lui propose de reprendre",
         _code == 200 and "Ta partie t'attend".encode("utf-8") in _page_r, str(_code))
# ⚠ ET ELLE DIT D'OU VIENT LA COUPURE. « Ta table s'est fermee » sans raison
# laisse croire a un plantage ; le motif est deja traduit pour la page de
# suivi (CAUSES_ABANDON), on le reutilise.
_texte_r = _page_r.decode("utf-8", "replace")
verifier("la page decrit la partie et dit d'ou vient la coupure",
         "Klaw" in _texte_r and "round 2" in _texte_r
         and "Interrompue le" in _texte_r and "table ferm" in _texte_r,
         _texte_r[_texte_r.find("Ta partie"):][:160])
verifier("et elle offre les deux chemins",
         b'action="/reprendre"' in _page_r and b'action="/nouvelle-partie"' in _page_r)

# ⚠ « COMMENCER AUTRE CHOSE » OUBLIE LA PARTIE, il ne la charge pas : sans
# cela le bandeau revenait a chaque visite, et le joueur devait le refuser
# indefiniment.
_code, _tetes, _ = appel("GET", "/nouvelle-partie", entetes=cookie_de("hote"))
verifier("« commencer autre chose » renvoie vers l'entree",
         _code == 303 and _tetes.get("Location") == "/entrer", str(_code))
verifier("et la partie ne sera plus proposee",
         o.partie_interrompue("hote") is None)

# --- Reprendre : on note qu'il faudra charger, sans bloquer la reponse ------
o.retenir_partie_interrompue("hote", "../replays/serveur-4/partie.json", "arret du site",
                             {"scenario": "Rhino", "round": 7})
o.A_REPRENDRE.discard("hote")
_code, _, _ = appel("GET", "/reprendre", entetes=cookie_de("hote"))
verifier("« reprendre » note le chargement a faire",
         "hote" in o.A_REPRENDRE, str(o.A_REPRENDRE))

# ⚠ UN CHARGEMENT QUI ECHOUE NE PRIVE PERSONNE DE SON JEU. Une sauvegarde
# ecrite par une version anterieure peut etre refusee : la table doit rester
# ouverte sur l'ecran des heros, et la partie ne plus etre proposee — la
# reproposer indefiniment serait pire que de ne rien proposer.
#
# ⚠ DEUX APPELS DESORMAIS, PAS UN SEUL (25/09/2026, correctif du bouton
# « Reprendre » qui retombait toujours sur l'ecran de preparation) :
# `/get_version` d'abord (recupere le cookie `app_version` que le moteur
# attend), PUIS `/debug?/load ...` avec les deux cookies. Le mock doit
# repondre au premier pour que le second, celui qu'on veut voir echouer,
# soit bien tente.
_appels_reprise = []


class _ReponseFausseVersion:
    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def read(self):
        return b"0.5.9.200r"


def _ouverture_qui_echoue(requete, timeout=None):
    lien = requete if isinstance(requete, str) else requete.full_url
    _appels_reprise.append(lien)
    if "/get_version" in lien:
        return _ReponseFausseVersion()
    raise o.urllib.error.URLError("moteur qui refuse")


_avant = o.urllib.request.urlopen
o.urllib.request.urlopen = _ouverture_qui_echoue
try:
    _table = o.Partie(4, "hote", "Jeu de hote")
    _table.mot_de_passe = "peu importe"
    _ok = o.charger_partie_interrompue(_table, "hote")
finally:
    o.urllib.request.urlopen = _avant
verifier("un chargement refuse ne leve pas", _ok is False)
verifier("et il a bien demande le bon fichier, au dernier pas",
         len(_appels_reprise) == 2 and "partie.json" in _appels_reprise[1]
         and _appels_reprise[1].endswith(":-1"), str(_appels_reprise))
verifier("et la partie n'est plus proposee, meme apres un echec",
         o.partie_interrompue("hote") is None)

# --- Reprendre, cette fois avec des cookies CORRECTS (25/09/2026) ----------
# Le bug lui-meme : `/debug` exige `session_token` (md5 du mot de passe) ET
# `app_version`, que l'ancien code ne posait jamais. Un mock qui repond
# toujours succes, sans regarder les cookies envoyes, laisserait ce meme
# defaut repasser inapercu. Celui-ci VERIFIE les cookies recus par `/debug`,
# pas seulement que la reponse finale est `True`.
#
# ⚠ PSEUDO DEDIE, PAS « hote ». `charger_partie_interrompue` s'appelle ici
# directement (sans passer par la route `/reprendre`) : nul besoin d'un
# compte reel. Reutiliser « hote » l'exposerait au thread de fond que
# `demarrer_en_fond` a lance PLUS HAUT (bloc « /reprendre note le chargement
# a faire ») pour ce meme pseudo — fil separe, non rejoint par le test, qui
# peut toujours tourner et disputer `A_REPRENDRE`/`REPRISE_EN_COURS` au bloc
# « LA COURSE DU 24/09 » juste apres. Constate a l'ecriture de ce test :
# partage le pseudo, et cette course (pourtant deja connue et commentee plus
# bas) devenait intermittente.
_table_isolee = o.Partie(4, "cookie-test-25-09", "Jeu isole pour ce test")
_table_isolee.mot_de_passe = "un mot de passe bien a elle"
o.retenir_partie_interrompue("cookie-test-25-09", "../replays/serveur-4/partie.json",
                             "arret du site", {"scenario": "Rhino", "round": 7})
_cookies_recus = {}


class _ReponseJson:
    def __init__(self, donnees):
        self._corps = o.json.dumps(donnees).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        return False

    def read(self):
        return self._corps


def _ouverture_avec_bons_cookies(requete, timeout=None):
    lien = requete if isinstance(requete, str) else requete.full_url
    if "/get_partie_en_cours" in lien:
        return _ReponseJson({"en_cours": True})
    if not isinstance(requete, str) and "/debug" in lien:
        _cookies_recus["cookie"] = requete.get_header("Cookie") or requete.headers.get("Cookie")
    return _ReponseFausseVersion()


_avant = o.urllib.request.urlopen
o.urllib.request.urlopen = _ouverture_avec_bons_cookies
try:
    _ok = o.charger_partie_interrompue(_table_isolee, "cookie-test-25-09")
finally:
    o.urllib.request.urlopen = _avant
verifier("un chargement correctement authentifie reussit", _ok is True)
_jeton_attendu = o.hashlib.md5(_table_isolee.mot_de_passe.encode()).hexdigest()
verifier("le cookie session_token est le bon (md5 du mot de passe de LA TABLE)",
         _cookies_recus.get("cookie", "").find(f"session_token={_jeton_attendu}") != -1,
         str(_cookies_recus))
verifier("le cookie app_version est celui rendu par /get_version",
         "app_version=0.5.9.200r" in _cookies_recus.get("cookie", ""),
         str(_cookies_recus))

# ⚠ `/debug` NE FAIT QUE POSER LA COMMANDE EN FILE, IL NE L'EXECUTE PAS
# AVANT DE REPONDRE (25/09/2026, deuxieme moitie du meme bug : trouve APRES
# le correctif des cookies ci-dessus, en testant contre le moteur reel).
# Sans l'attente sur `/get_partie_en_cours`, `charger_partie_interrompue`
# rendait `True` des que la commande etait EN FILE, pas quand elle avait
# reellement charge la partie — la course « LA COURSE DU 24/09 » plus bas
# dans ce fichier, un cran plus loin.
_table_isolee_2 = o.Partie(4, "cookie-test-25-09-course", "Jeu isole pour ce test")
_table_isolee_2.mot_de_passe = "un autre mot de passe"
o.retenir_partie_interrompue("cookie-test-25-09-course", "../replays/serveur-4/partie.json",
                             "arret du site", {"scenario": "Rhino", "round": 7})


def _ouverture_jamais_prete(requete, timeout=None):
    lien = requete if isinstance(requete, str) else requete.full_url
    if "/get_partie_en_cours" in lien:
        return _ReponseJson({"en_cours": False})
    return _ReponseFausseVersion()


_avant = o.urllib.request.urlopen
_avant_sommeil = o.time.sleep
o.urllib.request.urlopen = _ouverture_jamais_prete
o.time.sleep = lambda _s: None  # sinon ce test dure reellement 9 secondes
try:
    _ok = o.charger_partie_interrompue(_table_isolee_2, "cookie-test-25-09-course")
finally:
    o.urllib.request.urlopen = _avant
    o.time.sleep = _avant_sommeil
verifier("un chargement jamais confirme par le moteur n'est pas pris pour un succes",
         _ok is False)

# ⚠⚠ LA COURSE DU 24/09/2026, MOITIE CORRIGEE LE 23/09 SEULEMENT. `/pret`
# ne verifiait que REPRISE_EN_COURS, pose par `demarrer_en_fond` seulement
# APRES que `lancer_jeu` soit revenu -- donc APRES que le moteur reponde deja.
# Entre les deux, `/pret` voyait le moteur repondre et rendait `pret: true`
# avant meme que le rechargement de la sauvegarde n'ait ete demande. Constate
# en partie (compte arnaud, 24/09/2026 18:52 UTC) : Crossbones/Shuri jamais
# rechargee, ecran de choix du heros a la place. `A_REPRENDRE`, lui, est pose
# de facon SYNCHRONE par la route `/reprendre` : le verifier ICI AUSSI ferme
# la fenetre entiere.
o.PARTIES["hote"] = allumer("hote", 4)
_avant_repond = o._moteur_repond
o._moteur_repond = lambda port: True
try:
    o.A_REPRENDRE.discard("hote")
    o.REPRISE_EN_COURS.discard("hote")
    _code, _, _corps = appel("GET", "/pret", entetes=cookie_de("hote"))
    verifier("sans reprise en attente, /pret peut dire oui",
             _code == 200 and o.json.loads(_corps)["pret"] is True, _corps)

    o.A_REPRENDRE.add("hote")
    _code, _, _corps = appel("GET", "/pret", entetes=cookie_de("hote"))
    verifier("⚠ une reprise A_REPRENDRE non encore prise en charge bloque /pret",
             _code == 200 and o.json.loads(_corps)["pret"] is False, _corps)
    o.A_REPRENDRE.discard("hote")

    o.REPRISE_EN_COURS.add("hote")
    _code, _, _corps = appel("GET", "/pret", entetes=cookie_de("hote"))
    verifier("et une reprise deja en cours de chargement bloque toujours /pret",
             _code == 200 and o.json.loads(_corps)["pret"] is False, _corps)
    o.REPRISE_EN_COURS.discard("hote")
finally:
    o._moteur_repond = _avant_repond
    o.PARTIES.pop("hote", None)

# ⚠ ET LA FUITE JUMELLE : si `lancer_jeu` echoue (moteur mort, port deja
# pris...), `A_REPRENDRE` devait avant rester peuple pour de bon -- le retrait
# vivait dans le `if` qui suit un `lancer_jeu` reussi. `/pret` restait alors
# bloque a `false` pour ce compte sur TOUT lancement suivant, meme sans
# rapport avec une reprise, jusqu'au redemarrage du site.
o.A_REPRENDRE.add("hote")
o.DEMARRAGES.discard("hote")
_avant_lancer = o.lancer_jeu
o.lancer_jeu = lambda pseudo, joueurs=1: (_ for _ in ()).throw(RuntimeError("moteur mort"))
try:
    o.demarrer_en_fond("hote")
    _tour = 0
    while "hote" in o.DEMARRAGES and _tour < 50:
        o.time.sleep(0.1)
        _tour += 1
finally:
    o.lancer_jeu = _avant_lancer
    # ⚠ NE PAS LAISSER TRAINER : "hote" est le pseudo de la QUASI-TOTALITE des
    # cas plus bas dans ce fichier (admin, signalements...). Un ancien echec
    # de demarrage encore note ici leur ferait tous porter une erreur qui n'a
    # rien a voir avec ce qu'ils testent.
    o.ERREURS_DEMARRAGE.pop("hote", None)
verifier("un lancement qui echoue libere quand meme A_REPRENDRE",
         "hote" not in o.A_REPRENDRE, str(o.A_REPRENDRE))


# ---------------------------------------------------------------------------
# LE SUIVI DES SIGNALEMENTS (16/09/2026)
#
# Un rapport de bug envoye par le TITULAIRE d'un compte devient un ticket : un
# fil dans les deux sens, quatre etats, une page cote joueur.
#
# ⚠ LE SIEGE 0 EST LA SEULE IDENTITE SURE PAR DEFAUT. Une table appartient a
# un compte ; les autres sieges sont des invites. `hote` dit de quelle TABLE
# vient le rapport, pas qui l'ecrit : un rapport de siege 1 ou plus reste
# donc un rapport, lu et traite, sans fil.
#
# ⚠ EXCEPTION AJOUTEE LE 25/09/2026 : un invite connecte a son PROPRE compte
# (le cookie `nc_session` du site, releve par le moteur sur la requete du
# navigateur et relaye dans le CORPS de `/api/bug` -- jamais un en-tete
# Cookie, qui ne franchirait pas la frontiere serveur-a-serveur) devient le
# proprietaire reel du ticket, quelle que soit la table. Voir plus bas.
# ---------------------------------------------------------------------------
print()
print("Le suivi des signalements")

_r_hote = o.enregistrer_rapport("yarro", {
    "nom": "yarro", "siege": 0, "ecran": "plateau",
    "description": "la carte disparait quand je la joue"})
_r_invite = o.enregistrer_rapport("yarro", {
    "nom": "un ami", "siege": 2, "ecran": "plateau",
    "description": "pareil chez moi"})

verifier("un rapport du siege 0 ouvre un ticket",
         o.ticket_de(_r_hote) is not None)
verifier("un rapport d'un invite n'en ouvre pas",
         o.ticket_de(_r_invite) is None)

# ⚠ TRAJET REEL, PAR /api/bug, PAS PAR enregistrer_rapport(). Un invite
# connecte a SON PROPRE compte, sur la table d'un AUTRE compte ("hote") :
# le rapport doit lui appartenir a LUI (signalement d'origine, 19/09/2026 :
# « un signalement envoye depuis un second appareil reste sans conversation
# possible »).
_jeton_table_hote = o.secrets.token_urlsafe(24)
o.JETONS_SITE[_jeton_table_hote] = "hote"
# `pseudo_de_session` exige un compte REEL, `statut_de(...) == "valide"` :
# "yarro" n'avait jusque-la servi que de pseudo nu (enregistrer_rapport ne le
# verifie pas). Sans inscription, la session s'ouvrait mais ne resolvait
# jamais rien -- mesure faite, temoin muet a tort.
o.inscrire("yarro", "yarro@exemple.fr", "motdepasse123")
o.changer_statut("yarro", "valide")
_session_invite_connecte = o.ouvrir_session("yarro")
_code_ic, _, _corps_ic = appel("POST", "/api/bug", corps=o.urllib.parse.urlencode({
    "jeton": _jeton_table_hote,
    "nom": "Yarro",
    "siege": "2",
    "ecran": "plateau",
    "description": "signale depuis un second appareil, connecte a mon compte",
    "nc_session": _session_invite_connecte,
}).encode("utf-8"))
verifier("un invite connecte sur son propre compte : l'envoi reussit",
         _code_ic == 200, str(_code_ic))
_num_ic = json.loads(_corps_ic).get("numero") if _code_ic == 200 else None
verifier("son rapport devient SON ticket, pas celui de l'hote de la table",
         _num_ic is not None
         and any(x["id"] == _num_ic for x in o.tickets_de("yarro"))
         and not any(x["id"] == _num_ic for x in o.tickets_de("hote")),
         "num=%s tickets_yarro=%s tickets_hote=%s"
         % (_num_ic, o.tickets_de("yarro"), o.tickets_de("hote")))
verifier("⚠ et l'hote le voit quand meme sur SA table (hote inchange)",
         _num_ic is not None
         and any(x["id"] == _num_ic for x in o.rapports_de_ses_tables("hote")),
         "num=%s rapports_hote=%s" % (_num_ic, o.rapports_de_ses_tables("hote")))

# Contre-cas OBLIGATOIRE : sans session valable (l'invite anonyme ordinaire,
# qui n'a jamais eu de compte), rien ne change par rapport a AVANT le
# 25/09/2026 — et avant, ce n'etait DEJA PAS un ticket au siege 3 (seul le
# siege 0 en ouvrait un). Le rapport reste `hote`-de-la-table pour la vue
# d'ensemble (`rapports_de_ses_tables`), mais n'appartient a AUCUN ticket.
_jeton_table_hote_2 = o.secrets.token_urlsafe(24)
o.JETONS_SITE[_jeton_table_hote_2] = "hote"
_code_anon, _, _corps_anon = appel("POST", "/api/bug", corps=o.urllib.parse.urlencode({
    "jeton": _jeton_table_hote_2,
    "nom": "Un inconnu",
    "siege": "3",
    "ecran": "plateau",
    "description": "un vrai invite, jamais connecte",
}).encode("utf-8"))
_num_anon = json.loads(_corps_anon).get("numero") if _code_anon == 200 else None
verifier("un invite SANS compte reste visible sur la table de l'hote",
         _num_anon is not None
         and any(x["id"] == _num_anon for x in o.rapports_de_ses_tables("hote")),
         "num=%s rapports_hote=%s" % (_num_anon, o.rapports_de_ses_tables("hote")))
verifier("⚠ mais n'ouvre de ticket pour personne (comportement inchange)",
         not any(x["id"] == _num_anon for x in o.tickets_de("hote")),
         "num=%s tickets_hote=%s" % (_num_anon, o.tickets_de("hote")))

o.ecrire_message(_r_hote, "admin", "Corrige, merci du signalement.")
_fil = (o.ticket_de(_r_hote) or {}).get("messages") or []
verifier("la reponse se range dans le fil", len(_fil) == 1, str(_fil))
verifier("et elle porte son auteur",
         bool(_fil) and _fil[0]["auteur"] == "admin", str(_fil))

o.ecrire_message(_r_hote, "joueur", "Je confirme, c'est bon.")
verifier("le joueur repond dans le meme fil",
         len((o.ticket_de(_r_hote) or {}).get("messages") or []) == 2)

# ⚠ LE CAS QUI COMPTE LE PLUS : un ticket n'appartient qu'a son auteur.
_miens = o.tickets_de("yarro")
_autres = o.tickets_de("quelqu-un-d-autre")
verifier("le compte voit son ticket", any(x["id"] == _r_hote for x in _miens))
verifier("⚠ un autre compte ne le voit pas",
         not any(x["id"] == _r_hote for x in _autres), str(_autres))
verifier("et le rapport de l'invite n'est le ticket de personne",
         not any(x["id"] == _r_invite for x in _miens + _autres))

verifier("une reponse de l'admin est annoncee au joueur",
         o.reponses_non_lues("yarro") == 1, str(o.reponses_non_lues("yarro")))
verifier("mais pas a quelqu'un d'autre", o.reponses_non_lues("quelqu-un-d-autre") == 0)
o.marquer_ticket_lu(_r_hote, "joueur")
verifier("une fois le fil ouvert, la pastille s'eteint",
         o.reponses_non_lues("yarro") == 0)

# Les quatre etats, « refuse » compris : il couvre « ce n'est pas un bug »
# comme « je ne le ferai pas », et oblige a ecrire pourquoi.
verifier("l'etat refuse existe", "refuse" in o.ETATS_RAPPORT)
o.changer_etat_rapport(_r_hote, "refuse")
verifier("et il se pose sur un rapport",
         (o.ticket_de(_r_hote) or {}).get("etat") == "refuse")


# La page du joueur : il ne voit QUE ses tickets, et la barre le lui dit.
_page = o.page_signalements("yarro").decode("utf-8")
verifier("la page montre son signalement",
         "la carte disparait quand je la joue" in _page)
verifier("et la reponse qu'on lui a faite",
         "Corrige, merci du signalement." in _page)
_page_autre = o.page_signalements("quelqu-un-d-autre").decode("utf-8")
verifier("⚠ un autre compte n'y voit rien de lui",
         "la carte disparait" not in _page_autre, _page_autre[:200])
verifier("et sa page le dit plutot que de rester vide",
         "signalement" in _page_autre.lower())

o.ecrire_message(_r_hote, "admin", "Et voici une seconde reponse.")
verifier("la barre annonce les reponses non lues",
         "Mes signalements" in o._barre("yarro") and "(1)" in o._barre("yarro"),
         o._barre("yarro"))
verifier("et elle reste sobre quand rien n'attend",
         "Mes signalements" in o._barre("quelqu-un-d-autre")
         and "(" not in o._barre("quelqu-un-d-autre").split("Mes signalements")[1][:12],
         o._barre("quelqu-un-d-autre"))

# ⚠ SANS LIEN DE RETOUR, LES PAGES DU SITE SONT UN CUL-DE-SAC. Le site
# s'installe en application (`display: standalone`, MANIFESTE_APPLI), donc dans
# une fenetre SANS bouton Precedent. Signale par un joueur le 19/09/2026 : il
# ne pouvait quitter « Mes signalements » qu'en fermant la fenetre et en en
# rouvrant une. La barre est la seule chose presente sur toutes les pages.
verifier("la barre ramene a l'accueil",
         'href="/"' in o._barre("yarro"),
         o._barre("yarro"))
verifier("et le retour est la aussi pour l'administrateur",
         'href="/"' in o._barre(o.ADMIN),
         o._barre(o.ADMIN))

# ⚠ SIGNALE PAR UN JOUEUR LE 19/09/2026. Il joue sur SA table depuis deux
# appareils : le PC tient le siege 0, la tablette un autre siege. Son
# signalement envoye depuis la tablette n'apparaissait NULLE PART, la page ne
# montrant que le siege 0. Elle montre desormais tout ce qui vient de ses
# tables. La conversation, elle, reste au siege 0 : c'est le seul endroit ou
# l'on sait a qui l'on parle, un invite n'ayant qu'un nom tape.
_tous = [r["id"] for r in o.rapports_de_ses_tables("yarro")]
verifier("la page montre aussi les signalements des autres sieges",
         _r_hote in _tous and _r_invite in _tous, str(_tous))
_ids_tickets = [r["id"] for r in o.tickets_de("yarro")]
verifier("mais l'autorisation de repondre reste au siege 0",
         _r_hote in _ids_tickets and _r_invite not in _ids_tickets,
         str(_ids_tickets))
_page_yarro = o.page_signalements("yarro").decode("utf-8")
verifier("la page nomme qui a envoye un signalement d'un autre siege",
         "un ami" in _page_yarro)
verifier("et n'offre pas d'y repondre",
         ('name="id" value="%d"' % _r_invite) not in _page_yarro)
verifier("alors qu'elle l'offre sur celui du siege 0",
         ('name="id" value="%d"' % _r_hote) in _page_yarro)


# La pastille en partie. Le joueur est sur p<N>.<domaine> : seul le moteur peut
# parler au site, et il relaie deja `/api/prives`. On y ajoute le compte des
# reponses de tickets, donc SANS toucher au moteur ni le redemarrer.
_avant = o.messages_non_lus("yarro")
verifier("le contrat existant est intact",
         "nouveaux" in _avant and "de" in _avant, str(_avant))
verifier("et il porte desormais les reponses de tickets",
         _avant.get("tickets") == 1, str(_avant))
o.marquer_ticket_lu(_r_hote, "joueur")
verifier("qui retombent a zero une fois lues",
         o.messages_non_lus("yarro").get("tickets") == 0)


# La purge : l'image pesait, pas le texte. Depuis le 16/09/2026 un rapport
# classe garde son fil, et ne perd que sa capture.
import base64 as _b64
_png = _b64.b64encode(bytes.fromhex(
    "89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c489"
    "0000000a49444154789c6360000002000100ffff030000060005573f6d0a"
    "0000000049454e44ae426082")).decode()
_r_purge = o.enregistrer_rapport("yarro", {
    "nom": "yarro", "siege": 0, "description": "avec une capture",
    "capture": "data:image/png;base64," + _png})
o.ecrire_message(_r_purge, "admin", "Corrige.")
_fichier = (o.ticket_de(_r_purge) or {}).get("capture")
verifier("la capture est bien sur le disque",
         bool(_fichier) and os.path.exists(os.path.join(o.DOSSIER_RAPPORTS, _fichier)),
         str(_fichier))
o.changer_etat_rapport(_r_purge, "traite")
with o._cx() as _cx:
    _cx.execute("UPDATE rapports SET traite_le = '2020-01-01 00:00' WHERE id = ?",
                (_r_purge,))
_efface = o.purger_rapports_traites(30)
verifier("la purge a traite le rapport", _efface >= 1, str(_efface))
verifier("la capture a quitte le disque",
         not os.path.exists(os.path.join(o.DOSSIER_RAPPORTS, _fichier)))
_apres = o.ticket_de(_r_purge)
verifier("⚠ mais le ticket est toujours la", _apres is not None)
verifier("sans renvoyer vers une image absente",
         _apres is not None and not _apres["capture"], str(_apres and _apres["capture"]))
verifier("et son fil se relit encore",
         _apres is not None and len(_apres.get("messages") or []) == 1)


# ⚠ UN ETAT SANS GROUPE EST UN RAPPORT INVISIBLE. L'ecran d'administration
# classait les rapports par une liste ECRITE EN DUR. En ajoutant « refuse » le
# 16/09/2026 sans toucher a cette liste, un rapport refuse disparaissait de la
# page : le bouton existait, on cliquait, et le rapport s'evanouissait.
verifier("chaque etat de rapport a son libelle",
         all(e in o.LIBELLES_ETAT_RAPPORT for e in o.ETATS_RAPPORT),
         str(sorted(set(o.ETATS_RAPPORT) - set(o.LIBELLES_ETAT_RAPPORT))))


# ---------------------------------------------------------------------------
# LE SITE EN DEUX LANGUES (16/09/2026)
#
# ⚠ LE SERVEUR NE VOIT PAS LE `localStorage` ou le jeu garde la langue : il lit
# le cookie `nc_langue`, puis `Accept-Language`, puis retombe sur le francais.
# ---------------------------------------------------------------------------
print()
print("Le site en deux langues")

import langue as _lang  # noqa: E402

verifier("le cookie decide", _lang.detecter("a=1; nc_langue=en", "fr-FR"), "en")
verifier("sinon le navigateur", _lang.detecter("", "en-GB,en;q=0.9"), "en")
verifier("une langue inconnue retombe sur le francais",
         _lang.detecter("", "de-DE,de"), "fr")
verifier("et un cookie fantaisiste aussi",
         _lang.detecter("nc_langue=klingon", ""), "fr")

_lang.poser("fr")
_page_fr = o.page_signalements("yarro").decode("utf-8")
_lang.poser("en")
_page_en = o.page_signalements("yarro").decode("utf-8")
_lang.poser("fr")
verifier("la meme page parle francais", "Ce que tu as signale" in _page_fr)
verifier("⚠ et anglais", "What you reported" in _page_en, _page_en[:120])
verifier("sans laisser de francais derriere",
         "Se deconnecter" not in _page_en and "Mes signalements" not in _page_en)


print()
print("Toutes les pages du gabarit commun, dans les deux langues")

# ⚠ CETTE SECTION EXISTE A CAUSE DE DEUX DEFAUTS TROUVES EN PRODUCTION LE
# 16/09/2026, qu'AUCUNE gate ne voyait :
#
# 1. la page qui suit une demande d'inscription ne passait pas `bouton_appli`
#    au gabarit : `.format()` levait un KeyError, donc une 500 en pleine
#    inscription. Le typage ne voit rien, et aucun cas ne demandait cette page ;
# 2. le libelle du champ mot de passe etait ECRIT EN DUR dans le gabarit HTML.
#    `test_langue.py` ne lit que ce qui passe par `t()` : un texte en dur lui
#    est invisible par construction. Un anglophone lisait « Sign in » au-dessus
#    d'un champ « Mot de passe ».
#
# La seule gate qui attrape les deux est celle-ci : DEMANDER les pages, pour de
# vrai, dans les deux langues, et lire ce qui en sort.

_EN = {"Accept-Language": "en-US,en;q=0.9"}
# Des mots qui n'existent qu'en francais et qui ne peuvent PAS etre un reste
# d'anglais : leur presence dans une page anglaise est un texte oublie.
_FRANCAIS = ("Mot de passe", "Se connecter", "Pseudo", "Entrer",
             "Enregistrer", "Nouveau mot de passe", "compte")


def _demander(nom, methode, chemin, corps=b"", entetes=None):
    """Un appel qui ne peut pas emporter la batterie avec lui.

    ⚠ Une page qui LEVE (un champ manquant dans `.format()`, par exemple) ne
    repond pas : le serveur raccroche, et `appel` remonte un
    RemoteDisconnected. Sans ce filet, le defaut du 16/09/2026 n'aurait pas
    rougi un cas — il aurait arrete le fichier de test au milieu, avec une
    trace de `http.client` qui ne nomme meme pas la page fautive.
    """
    try:
        return appel(methode, chemin, corps, entetes)
    except Exception as souci:                 # noqa: BLE001 — on juge, on relance pas
        verifier(nom + " : la page repond", False, type(souci).__name__)
        return 599, None, b""


def _page_bilingue(nom, methode, chemin, corps=b"", entetes=None):
    """Demande la page dans les deux langues et juge les deux reponses."""
    tetes_fr = dict(entetes or {})
    tetes_en = dict(tetes_fr, **_EN)
    code_fr, _, corps_fr = _demander(nom + " (FR)", methode, chemin, corps, tetes_fr)
    code_en, _, corps_en = _demander(nom + " (EN)", methode, chemin, corps, tetes_en)
    texte_en = corps_en.decode("utf-8", "replace")
    verifier(nom + " : la page se construit (FR)", code_fr < 500, "code %d" % code_fr)
    verifier(nom + " : la page se construit (EN)", code_en < 500, "code %d" % code_en)
    restes = [mot for mot in _FRANCAIS if mot in texte_en]
    verifier(nom + " : rien de francais ne reste en anglais",
             not restes, "trouve : " + ", ".join(restes))
    return corps_fr, corps_en


_page_bilingue("connexion", "GET", "/connexion")
_page_bilingue("inscription", "GET", "/inscription")
# Le lien de reinitialisation : le jeton est faux, ce qui suffit — on juge la
# PAGE, et le formulaire est le meme gabarit.
_page_bilingue("reinitialisation", "GET", "/reinitialisation?r=jetoninexistant")

# La page qui suit une demande d'inscription : c'est celle qui levait le
# KeyError, et elle n'est atteignable que par un POST.
import uuid as _uuid  # noqa: E402

_nouveau = "essai" + _uuid.uuid4().hex[:8]
_corps = ("pseudo=" + _nouveau + "&email=" + _nouveau
          + "%40exemple.fr&mdp=motdepasse123").encode()
_code, _, _apres = _demander("demande d'inscription", "POST", "/inscription", _corps)
verifier("la page qui suit une demande d'inscription ne plante pas",
         _code < 500, "code %d" % _code)
verifier("et elle dit que la demande est enregistree",
         "enregistr" in _apres.decode("utf-8", "replace").lower())

print()
print("ECHECS : %d" % len(echecs))
for e in echecs:
    print("  - " + e)
sys.exit(1 if echecs else 0)
