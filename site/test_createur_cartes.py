"""Comptes « createur de cartes » : invitation, isolement des routes, stockage.

Passe par les VRAIES routes (serveur HTTP reel, base et dossiers temporaires).

Usage : python3 site/test_createur_cartes.py
"""
import http.client
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import threading
import urllib.parse
from http.server import ThreadingHTTPServer

_tmp = tempfile.mkdtemp(prefix="nc-createur-")
_base = os.path.join(_tmp, "narwhal.db")
os.environ["BASE"] = _base
os.environ["DOSSIER_CREATEUR"] = os.path.join(_tmp, "donnees")
os.environ["DOSSIER_PUBLIC_JEU"] = os.path.join(_tmp, "public")
os.environ["MAX_PROJET_OCTETS"] = "100000"          # 100 Ko pour le test
os.environ["QUOTA_CREATEUR_OCTETS"] = "400000"      # 400 Ko pour le test
os.environ["TENTATIVES_CONNEXION"] = "1000"
os.environ["ADMIN"] = "arnaud"
os.environ["MAX_COMPTES"] = "20"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Faux dossier public du jeu : la page du createur, un fichier statique, et un
# secret VOISIN que la traversee ne doit jamais atteindre.
os.makedirs(os.path.join(_tmp, "public", "createur-cartes", "img"))
with open(os.path.join(_tmp, "public", "createur-cartes.html"), "w") as f:
    f.write("<!doctype html><title>createur</title>")
with open(os.path.join(_tmp, "public", "createur-cartes", "app.js"), "w") as f:
    f.write("console.log(1)")
with open(os.path.join(_tmp, "public", "secret.html"), "w") as f:
    f.write("SECRET")
with open(os.path.join(_tmp, "secret.json"), "w") as f:
    f.write('{"secret": 1}')

import orchestrateur as o  # noqa: E402

o.initialiser_base()
echecs = []


def verifier(nom, condition, detail=""):
    print(("  OK   " if condition else "  RATE ") + nom + (" | " + str(detail) if detail and not condition else ""))
    if not condition:
        echecs.append(nom)


_serveur = ThreadingHTTPServer(("127.0.0.1", 0), o.Handler)
_port = _serveur.server_address[1]
threading.Thread(target=_serveur.serve_forever, daemon=True).start()


def appel(methode, chemin, corps=None, cookie=None, entetes=None, json_corps=None):
    """Une requete reelle. Rend (code, corps octets, en-tetes)."""
    tetes = dict(entetes or {})
    if cookie:
        tetes["Cookie"] = "nc_session=" + cookie
    octets = None
    if json_corps is not None:
        octets = json.dumps(json_corps).encode()
        tetes["Content-Type"] = "application/json"
    elif isinstance(corps, dict):
        octets = urllib.parse.urlencode(corps).encode()
        tetes["Content-Type"] = "application/x-www-form-urlencoded"
    elif corps is not None:
        octets = corps
    if octets is not None:
        tetes["Content-Length"] = str(len(octets))
    lien = http.client.HTTPConnection("127.0.0.1", _port, timeout=10)
    try:
        lien.request(methode, chemin, body=octets, headers=tetes)
        r = lien.getresponse()
        return r.status, r.read(), {k.lower(): v for k, v in r.getheaders()}
    finally:
        lien.close()


def connecter(pseudo, mdp="motdepasse1"):
    code, _c, tetes = appel("POST", "/connexion", {"pseudo": pseudo, "mdp": mdp})
    m = re.search(r"nc_session=([^;]+)", tetes.get("set-cookie", ""))
    return code, (m.group(1) if m else None), tetes


def creer_compte(pseudo, jeton=""):
    return o.inscrire(pseudo, pseudo + "@exemple.be", "motdepasse1", jeton)


def json_de(octets):
    return json.loads(octets.decode("utf-8"))


# ---------------------------------------------------------------- invitation
print("Invitation et inscription")
creer_compte("arnaud")
jeton_createur = o.creer_invitation("createur")
jeton_joueur = o.creer_invitation()
verifier("invitation createur : valide", o.invitation_valide(jeton_createur))
code, corps, _ = appel("GET", "/inscription?i=" + jeton_createur)
verifier("formulaire d'inscription par le lien createur", code == 200, code)

# par la VRAIE route d'inscription
code, corps, _ = appel("POST", "/inscription", {
    "pseudo": "alice", "email": "alice@exemple.be", "mdp": "motdepasse1", "i": jeton_createur})
verifier("POST /inscription createur : 200", code == 200, code)
ligne = o.compte("alice")
verifier("compte alice : role createur, valide", ligne["role"] == "createur" and ligne["statut"] == "valide")
verifier("alice n'a AUCUN emplacement de jeu", ligne["emplacement"] is None)
verifier("le lien est consomme", not o.invitation_valide(jeton_createur))
code, corps, _ = appel("POST", "/inscription", {
    "pseudo": "alice2", "email": "alice2@exemple.be", "mdp": "motdepasse1", "i": jeton_createur})
verifier("lien reutilise : pas de compte createur", (o.compte("alice2") or {"role": None})["role"] != "createur")
creer_compte("bob", o.creer_invitation("createur"))
creer_compte("joueur1", jeton_joueur)
verifier("lien ordinaire : role joueur + emplacement",
         o.compte("joueur1")["role"] == "joueur" and o.compte("joueur1")["emplacement"] is not None)
creer_compte("inconnu1")        # inscription libre sans lien : joueur, en attente
verifier("inscription libre : joueur", o.compte("inconnu1")["role"] == "joueur")
o._attribuer_emplacements_manquants()
verifier("les createurs ne recoivent jamais d'emplacement",
         o.compte("alice")["emplacement"] is None and o.compte("bob")["emplacement"] is None)
verifier("nb_valides ne compte pas les createurs", o.nb_valides() == 2, o.nb_valides())
try:
    o.creer_invitation("root")
    verifier("role d'invitation inconnu refuse", False)
except ValueError:
    verifier("role d'invitation inconnu refuse", True)

code, cook_alice, tetes = connecter("alice")
verifier("connexion createur : redirige vers le createur",
         code == 303 and tetes.get("location") == "/createur-cartes.html", (code, tetes.get("location")))
_, cook_bob, _ = connecter("bob")
_, cook_adm, tetes_adm = connecter("arnaud")
verifier("connexion admin : /entrer comme avant", tetes_adm.get("location") == "/entrer", tetes_adm.get("location"))
joueur_valide = o.compte("joueur1")
_, cook_joueur, _ = connecter("joueur1")
verifier("sessions ouvertes", all([cook_alice, cook_bob, cook_adm, cook_joueur]))

# ------------------------------------------------------------ isolement
print("Isolement des routes d'un compte createur")
source = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "orchestrateur.py"),
              encoding="utf-8").read()
# Toutes les routes ecrites dans le gestionnaire : `self.chemin == "..."`,
# `in ("..", "..")`, `.startswith("...")`.
corps_handler = source[source.index("class Handler"):source.index("def main()")]
routes = set()
for m in re.finditer(r'self\.chemin\s*(?:==|in|\.startswith\()\s*\(?((?:"[^"]*"\s*,?\s*)+)', corps_handler):
    routes.update(re.findall(r'"(/[^"]*)"', m.group(1)))
routes -= {"/createur-cartes.html"}
verifier("routes extraites du serveur (au moins 30)", len(routes) >= 30, len(routes))
PERMISES = {"/connexion", "/deconnexion", "/inscription", "/reinitialisation",
            "/favicon.ico", "/favicon.png"}
refusees_ok = True
details = []
for route in sorted(routes):
    concret = route.rstrip("/") + ("/x.jpg" if route.endswith("/") else "")
    if route in PERMISES or route.startswith("/createur-cartes") or route.startswith("/api/createur"):
        continue
    for methode in ("GET", "POST", "PUT", "DELETE"):
        code, corps, tetes = appel(methode, concret, cookie=cook_alice,
                                   corps=(b"a=b" if methode != "GET" else None))
        ok = code == 403 or (code == 303 and tetes.get("location") == "/createur-cartes.html"
                             and methode == "GET" and route in ("/", "/index.html", "/entrer"))
        if not ok:
            refusees_ok = False
            details.append("%s %s -> %s" % (methode, concret, code))
verifier("TOUTE route du site hors createur refusee (GET/POST/PUT/DELETE)", refusees_ok, details[:5])
for chemin in ("/", "/entrer", "/index.html"):
    code, _c, tetes = appel("GET", chemin, cookie=cook_alice)
    verifier("GET %s redirige le createur chez lui" % chemin,
             code == 303 and tetes.get("location") == "/createur-cartes.html", (code, tetes))
for chemin in ("/admin", "/suivi", "/entrer", "/api/suivi", "/admin/images", "/etat", "/regarder?joueur=arnaud",
               "/signalements", "/nouvelle-partie", "/reprendre", "/pret", "/vilains/x.jpg"):
    code, _c, _t = appel("GET", chemin, cookie=cook_alice)
    verifier("createur : GET %s refuse" % chemin, code in (403, 303), code)
code, _c, _t = appel("POST", "/admin", {"action": "inviter"}, cookie=cook_alice)
verifier("createur : POST /admin refuse", code == 403, code)
verifier("createur : aucune invitation creee par ce POST", len(o.invitations_libres()) == 0)
code, _c, _t = appel("POST", "/api/vue", {"jeton": "x"}, cookie=cook_alice)
verifier("createur : API du moteur refusee", code == 403, code)
code, _c, _t = appel("POST", "/eteindre", b"", cookie=cook_alice)
verifier("createur : POST /eteindre refuse", code == 403, code)
# l'admin et le joueur gardent l'acces
code, _c, _t = appel("GET", "/admin", cookie=cook_adm)
verifier("admin : /admin passe", code == 200, code)
code, _c, _t = appel("GET", "/admin", cookie=cook_joueur)
verifier("joueur : /admin toujours refuse", code == 403, code)
code, _c, tetes = appel("GET", "/", cookie=cook_joueur)
verifier("joueur : / -> /entrer comme avant", code == 303 and tetes.get("location") == "/entrer", (code, tetes))
code, _c, _t = appel("GET", "/signalements", cookie=cook_joueur)
verifier("joueur : /signalements passe", code == 200, code)
code, _c, _t = appel("GET", "/createur-cartes.html", cookie=cook_joueur)
verifier("joueur : page du createur ouverte (decision du 28/10)", code == 200, code)
code, _c, _t = appel("GET", "/api/createur/projets", cookie=cook_joueur)
verifier("joueur : API du createur ouverte", code == 200, code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=alice", cookie=cook_joueur)
verifier("joueur : ne lit pas les projets d'alice", code == 403, code)

print("Pages statiques du createur")
code, corps, tetes = appel("GET", "/createur-cartes.html", cookie=cook_alice)
verifier("page du createur servie", code == 200 and b"createur" in corps and "text/html" in tetes["content-type"], code)
code, corps, tetes = appel("GET", "/createur-cartes/app.js", cookie=cook_alice)
verifier("fichier statique servi", code == 200 and corps == b"console.log(1)" and "javascript" in tetes["content-type"], code)
code, _c, _t = appel("GET", "/createur-cartes.html")
verifier("sans session : redirection vers la connexion", code == 303, code)
code, _c, _t = appel("GET", "/createur-cartes/app.js")
verifier("sans session : statique refuse", code == 303, code)
code, _c, _t = appel("GET", "/createur-cartes.html", cookie=cook_adm)
verifier("admin : page du createur", code == 200, code)
for mauvais in ("/createur-cartes/../secret.html", "/createur-cartes/%2e%2e/secret.html",
                "/createur-cartes/..%2fsecret.html", "/createur-cartes/img/../../secret.html",
                "/createur-cartes/%2e%2e%2f%2e%2e%2fsecret.json", "/createur-cartes//etc/passwd",
                "/createur-cartes/app.js%00.png", "/createur-cartes/.env"):
    code, corps, _t = appel("GET", mauvais, cookie=cook_alice)
    verifier("statique : traversee %s" % mauvais, code in (400, 403, 404) and b"SECRET" not in corps and b'"secret"' not in corps, code)

# ----------------------------------------------------------------- API
print("Scans officiels (carte comparable)")
code, corps, tetes = appel("GET", "/api/createur/scan/01001a", cookie=cook_alice)
verifier("scan : 200 image/jpeg", code == 200 and tetes.get("content-type") == "image/jpeg" and corps[:2] == b"\xff\xd8", (code, tetes.get("content-type")))
code, corps, _ = appel("GET", "/api/createur/scan/01001a", cookie=cook_joueur)
verifier("scan : ouvert aux joueurs connectes", code == 200, code)
code, _c, _t = appel("GET", "/api/createur/scan/01001a")
verifier("scan : sans session = 401", code == 401, code)
for mauvais in ("..%2f..%2fsite%2fnarwhal", "..", "a%2fb", "01001a.jpg", "x"):
    code, _c, _t = appel("GET", "/api/createur/scan/" + mauvais, cookie=cook_alice)
    verifier("scan : code refuse (%s)" % mauvais, code in (400, 404), code)
code, _c, _t = appel("GET", "/api/createur/scan/zzzzzz9", cookie=cook_alice)
verifier("scan : inconnu = 404", code == 404, code)
code, _c, _t = appel("PUT", "/api/createur/scan/01001a", cookie=cook_alice, json_corps={"x": 1})
verifier("scan : lecture seule", code == 405, code)

print("API de stockage")
code, corps, tetes = appel("GET", "/api/createur/projets")
verifier("API sans session : 401", code == 401, code)
code, corps, tetes = appel("GET", "/api/createur/projets", cookie=cook_alice)
verifier("liste vide au depart", code == 200 and json_de(corps)["projets"] == [], (code, corps))
verifier("JSON : Cache-Control no-store", tetes.get("cache-control") == "no-store", tetes.get("cache-control"))

projet = {"nom": "Ma <b>carte</b>", "dossier": "Heros", "cartes": [{"img": "data:image/png;base64,AAAA"}]}
code, corps, _ = appel("PUT", "/api/createur/projet/p1", cookie=cook_alice, json_corps=projet)
verifier("PUT cree le projet", code == 200 and json_de(corps)["id"] == "p1", (code, corps))
code, corps, tetes = appel("GET", "/api/createur/projet/p1", cookie=cook_alice)
verifier("GET rend le projet complet", code == 200 and json_de(corps) == projet, code)
verifier("GET projet : no-store", tetes.get("cache-control") == "no-store")
code, corps, _ = appel("GET", "/api/createur/projets", cookie=cook_alice)
liste = json_de(corps)["projets"]
verifier("liste : id, nom, dossier, modifie",
         len(liste) == 1 and liste[0]["id"] == "p1" and liste[0]["nom"] == "Ma <b>carte</b>"
         and liste[0]["dossier"] == "Heros" and liste[0]["modifie"], liste)
code, corps, _ = appel("GET", "/api/createur/projet/inexistant", cookie=cook_alice)
verifier("projet inconnu : 404", code == 404, code)

# versions
for n in range(2, 36):
    appel("PUT", "/api/createur/projet/p1", cookie=cook_alice,
          json_corps={"nom": "v%d" % n, "dossier": "Heros"})
code, corps, _ = appel("GET", "/api/createur/projet/p1/versions", cookie=cook_alice)
versions = json_de(corps)["versions"]
verifier("30 versions gardees au plus", code == 200 and len(versions) == 30, len(versions))
verifier("versions : la plus recente d'abord, avec n et date",
         versions[0]["n"] == 34 and versions[-1]["n"] == 5 and versions[0]["modifie"], versions[:2])
code, corps, _ = appel("GET", "/api/createur/projet/p1/versions/34", cookie=cook_alice)
verifier("version 34 = l'avant-derniere ecriture", code == 200 and json_de(corps)["nom"] == "v34", corps[:80])
code, corps, _ = appel("GET", "/api/createur/projet/p1", cookie=cook_alice)
verifier("courant = derniere ecriture", json_de(corps)["nom"] == "v35")
code, _c, _t = appel("GET", "/api/createur/projet/p1/versions/1", cookie=cook_alice)
verifier("version purgee : 404", code == 404, code)
code, _c, _t = appel("GET", "/api/createur/projet/p1/versions/abc", cookie=cook_alice)
verifier("numero de version invalide : 400", code == 400, code)
code, _c, _t = appel("GET", "/api/createur/projet/p1/versions/-1", cookie=cook_alice)
verifier("numero negatif : 400", code == 400, code)

# acces croise
print("Acces croise entre createurs")
code, corps, _ = appel("GET", "/api/createur/projets", cookie=cook_bob)
verifier("bob ne voit pas les projets d'alice", code == 200 and json_de(corps)["projets"] == [], corps)
code, _c, _t = appel("GET", "/api/createur/projet/p1", cookie=cook_bob)
verifier("bob ne lit pas p1 d'alice", code == 404, code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=alice", cookie=cook_bob)
verifier("bob avec ?compte=alice : 403", code == 403, code)
code, _c, _t = appel("GET", "/api/createur/projet/p1?compte=alice", cookie=cook_bob)
verifier("bob lit p1 d'alice par ?compte : 403", code == 403, code)
code, _c, _t = appel("DELETE", "/api/createur/projet/p1?compte=alice", cookie=cook_bob)
verifier("bob supprime chez alice : 403", code == 403, code)
code, _c, _t = appel("PUT", "/api/createur/projet/p1?compte=alice", cookie=cook_bob, json_corps={"nom": "pirate"})
verifier("bob ecrase chez alice : 403", code == 403, code)
code, corps, _ = appel("GET", "/api/createur/projet/p1", cookie=cook_alice)
verifier("le projet d'alice est intact", json_de(corps)["nom"] == "v35")
code, corps, _ = appel("PUT", "/api/createur/projet/p1", cookie=cook_bob, json_corps={"nom": "celui de bob"})
code2, corps2, _ = appel("GET", "/api/createur/projet/p1", cookie=cook_alice)
verifier("meme identifiant chez bob : deux projets distincts", json_de(corps2)["nom"] == "v35")
code, corps, _ = appel("GET", "/api/createur/projet/p1", cookie=cook_bob)
verifier("... et bob lit le sien", json_de(corps)["nom"] == "celui de bob")
code, corps, _ = appel("GET", "/api/createur/projets?compte=alice", cookie=cook_adm)
verifier("admin liste les projets d'alice", code == 200 and len(json_de(corps)["projets"]) == 1, (code, corps))
code, corps, _ = appel("GET", "/api/createur/projet/p1?compte=bob", cookie=cook_adm)
verifier("admin lit un projet de bob", code == 200 and json_de(corps)["nom"] == "celui de bob", code)
code, corps, _ = appel("GET", "/api/createur/projet/p1/versions?compte=alice", cookie=cook_adm)
verifier("admin lit les versions d'alice", code == 200 and len(json_de(corps)["versions"]) == 30, code)
code, _c, _t = appel("PUT", "/api/createur/projet/p1?compte=alice", cookie=cook_adm, json_corps={"nom": "x"})
verifier("admin n'ecrit pas chez un createur", code == 403, code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=joueur1", cookie=cook_adm)
verifier("?compte= d'un joueur : lisible par l'admin", code == 200, code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=inexistant9", cookie=cook_adm)
verifier("?compte= inexistant : 404", code == 404, code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=..%2f..", cookie=cook_adm)
verifier("?compte= avec traversee : refuse", code in (400, 404), code)
code, _c, _t = appel("GET", "/api/createur/projets?compte=zorglub", cookie=cook_adm)
verifier("?compte= inconnu : 404", code == 404, code)

# traversee de chemin
print("Traversee de chemin (identifiants)")
for mauvais in ("..", "../x", "%2e%2e", "a%2fb", "a/b", "..%2f..%2fetc", ".hidden", "x" * 65, "a%20b", "a.json", "%00"):
    code, corps, _ = appel("PUT", "/api/createur/projet/" + mauvais, cookie=cook_alice, json_corps={"nom": "x"})
    verifier("PUT id %r refuse" % mauvais, code in (400, 404), code)
    code, corps, _ = appel("GET", "/api/createur/projet/" + mauvais, cookie=cook_alice)
    verifier("GET id %r refuse" % mauvais, code in (400, 404), code)
    code, corps, _ = appel("DELETE", "/api/createur/projet/" + mauvais, cookie=cook_alice)
    verifier("DELETE id %r refuse" % mauvais, code in (400, 404), code)
racine_donnees = os.environ["DOSSIER_CREATEUR"]
contenu = sorted(os.listdir(racine_donnees))
verifier("aucun fichier hors des dossiers de comptes", contenu == ["alice", "bob"], contenu)
verifier("aucun fichier cree a cote du dossier de donnees",
         sorted(os.listdir(_tmp)) == sorted(["narwhal.db", "narwhal.db-wal", "narwhal.db-shm", "donnees", "public", "secret.json"])
         or set(os.listdir(_tmp)) <= {"narwhal.db", "narwhal.db-wal", "narwhal.db-shm", "donnees", "public", "secret.json"},
         os.listdir(_tmp))
# la couche de stockage seule, sans passer par HTTP
import createur_cartes as cc  # noqa: E402
for mauvais_compte in ("../alice", "al/ice", "", "a", "ALICE/..", "alice\x00"):
    try:
        cc.lister(racine_donnees, mauvais_compte)
        verifier("stockage : compte %r refuse" % mauvais_compte, mauvais_compte.lower() == "alice")
    except cc.ErreurCreateur:
        verifier("stockage : compte %r refuse" % mauvais_compte, True)
# un lien symbolique place sous la racine ne doit pas permettre de sortir
os.symlink(_tmp, os.path.join(racine_donnees, "alice", "evasion"))
try:
    cc.lire(racine_donnees, "alice", "evasion")
    verifier("lien symbolique sortant refuse", False)
except cc.ErreurCreateur:
    verifier("lien symbolique sortant refuse", True)
os.remove(os.path.join(racine_donnees, "alice", "evasion"))
code, corps, _ = appel("GET", "/api/createur/projets", cookie=cook_alice)
verifier("un dossier etranger n'apparait pas dans la liste", all(p["id"] == "p1" for p in json_de(corps)["projets"]))

# taille et format
print("Taille maximale, format, quota")
gros = b'{"nom":"gros","x":"' + b"a" * 100001 + b'"}'
code, corps, _ = appel("PUT", "/api/createur/projet/gros", cookie=cook_bob, corps=gros,
                       entetes={"Content-Type": "application/json"})
verifier("corps au-dela du maximum : 413", code == 413, code)
verifier("... avec un message", "erreur" in json_de(corps), corps)
verifier("... et rien n'est ecrit", not os.path.exists(os.path.join(racine_donnees, "bob", "gros")))
code, corps, _ = appel("PUT", "/api/createur/projet/limite", cookie=cook_bob,
                       corps=b'{"nom":"ok","x":"' + b"a" * 90000 + b'"}',
                       entetes={"Content-Type": "application/json"})
verifier("corps sous le maximum accepte", code == 200, code)
verifier("le maximum par defaut est bien 25 Mo",
         int(re.search(r'"MAX_PROJET_OCTETS", str\((\d+) \* 1024 \* 1024\)', source).group(1)) == 25)
code, corps, _ = appel("PUT", "/api/createur/projet/mauvais", cookie=cook_bob, corps=b"pas du json",
                       entetes={"Content-Type": "application/json"})
verifier("JSON invalide : 400", code == 400, code)
code, corps, _ = appel("PUT", "/api/createur/projet/mauvais", cookie=cook_bob, corps=b"[1,2]",
                       entetes={"Content-Type": "application/json"})
verifier("JSON qui n'est pas un objet : 400", code == 400, code)
code, corps, _ = appel("PUT", "/api/createur/projet/mauvais", cookie=cook_bob, corps=b'{"nom":"x"}',
                       entetes={"Content-Type": "text/plain"})
verifier("Content-Type autre que JSON : 415", code == 415, code)
code, corps, _ = appel("PUT", "/api/createur/projet/mauvais", cookie=cook_bob, json_corps={"nom": "x"},
                       entetes={"Origin": "http://pirate.example"})
verifier("Origin etrangere : 403", code == 403, code)
code, corps, _ = appel("PUT", "/api/createur/projet/bon", cookie=cook_bob, json_corps={"nom": "x"},
                       entetes={"Origin": "http://127.0.0.1:%d" % _port})
verifier("Origin identique : accepte", code == 200, code)

# quota : 400 Ko ; bob a deja ~190 Ko (limite + bon + p1 + ...)
rempli = False
for i in range(20):
    code, corps, _ = appel("PUT", "/api/createur/projet/q%d" % i, cookie=cook_bob,
                           corps=b'{"nom":"q","x":"' + b"a" * 90000 + b'"}',
                           entetes={"Content-Type": "application/json"})
    if code == 507:
        rempli = True
        message = json_de(corps)["erreur"]
        break
verifier("quota atteint : 507 avec message clair", rempli and "Mo" in message and "Espace" in message,
         (code, corps[:100]))
code, corps, _ = appel("GET", "/api/createur/projets", cookie=cook_bob)
verifier("la liste indique utilise et quota",
         json_de(corps)["quota"] == 400000 and 0 < json_de(corps)["utilise"] <= 400000, corps[:150])
verifier("le quota d'un compte ne bloque pas un autre",
         appel("PUT", "/api/createur/projet/libre", cookie=cook_alice, json_corps={"nom": "ok"})[0] == 200)
code, _c, _t = appel("DELETE", "/api/createur/projet/limite", cookie=cook_bob)
verifier("DELETE : 200", code == 200, code)
code, _c, _t = appel("GET", "/api/createur/projet/limite", cookie=cook_bob)
verifier("supprime : 404", code == 404, code)
code, _c, _t = appel("DELETE", "/api/createur/projet/limite", cookie=cook_bob)
verifier("DELETE deux fois : 404", code == 404, code)
verifier("DELETE emporte aussi l'historique", not os.path.exists(os.path.join(racine_donnees, "bob", "limite")))
code, _c, _t = appel("PATCH", "/api/createur/projets", cookie=cook_bob)
verifier("methode inconnue : pas de succes", code in (404, 405, 501), code)
code, _c, _t = appel("PUT", "/api/createur/projets", cookie=cook_bob, json_corps={})
verifier("PUT sur la liste : 404", code == 404, code)

# pas de fichier temporaire oublie
restes = [f for _d, _s, fs in os.walk(racine_donnees) for f in fs if f.endswith(".tmp")]
verifier("aucun fichier .tmp oublie (ecriture atomique)", not restes, restes)

# ------------------------------------------------------------- desactivation
print("Administration")
code, corps, _ = appel("GET", "/admin", cookie=cook_adm)
page = corps.decode("utf-8")
verifier("admin : bouton « Inviter un createur de cartes »", "Inviter un créateur de cartes" in page)
verifier("admin : les createurs sont listes", "alice" in page and "bob" in page)
verifier("admin : alice absente de la liste des joueurs (pas dans les fiches comptes)",
         len(o.liste_comptes()) == len([c for c in o.liste_comptes() if c["role"] != "createur"]))
code, _c, _t = appel("POST", "/admin", {"action": "inviter_createur"}, cookie=cook_adm)
verifier("POST /admin inviter_createur : redirige", code == 303, code)
libres = [i for i in o.invitations_libres() if i["role"] == "createur"]
verifier("une invitation createur de plus", len(libres) == 1)
code, corps, _ = appel("GET", "/admin", cookie=cook_adm)
verifier("le lien d'invitation createur est affiche", ("/inscription?i=" + libres[0]["jeton"]) in corps.decode("utf-8"))
code, _c, _t = appel("POST", "/admin", {"action": "inviter_createur"}, cookie=cook_joueur)
verifier("un joueur ne peut pas inviter", code == 403, code)
code, _c, _t = appel("POST", "/admin", {"pseudo": "alice", "statut": "refuse"}, cookie=cook_adm)
code, _c, _t = appel("GET", "/api/createur/projets", cookie=cook_alice)
verifier("compte desactive : session coupee", code == 401, code)
code, _c, _t = connecter("alice")
verifier("compte desactive : connexion refusee", code == 400, code)
code, _c, _t = appel("POST", "/admin", {"pseudo": "alice", "statut": "valide"}, cookie=cook_adm)
verifier("reactive : toujours aucun emplacement", o.compte("alice")["emplacement"] is None)
code, cook_alice, _t = connecter("alice")
verifier("reactive : peut se reconnecter", code == 303 and cook_alice)
verifier("reactive : retrouve ses projets",
         json_de(appel("GET", "/api/createur/projets", cookie=cook_alice)[1])["projets"] != [])
code, _c, _t = appel("GET", "/deconnexion", cookie=cook_alice)
verifier("deconnexion permise au createur", code == 303, code)

# ------------------------------------------------------------- migration douce
print("Migration d'une base ancienne")
ancienne = os.path.join(_tmp, "ancienne.db")
cx = sqlite3.connect(ancienne)
cx.executescript("""
CREATE TABLE comptes (pseudo TEXT PRIMARY KEY, email TEXT UNIQUE, sel TEXT NOT NULL,
  empreinte TEXT NOT NULL, statut TEXT NOT NULL DEFAULT 'attente', cree TEXT NOT NULL,
  derniere_connexion TEXT, emplacement INTEGER, mdp_jeu TEXT);
CREATE TABLE invitations (jeton TEXT PRIMARY KEY, cree_le TEXT NOT NULL, utilise_par TEXT, utilise_le TEXT);
INSERT INTO comptes (pseudo, email, sel, empreinte, statut, cree, emplacement)
  VALUES ('vieux', 'v@x.be', 's', 'e', 'valide', '2026-01-01', 3);
INSERT INTO invitations (jeton, cree_le) VALUES ('jvieux', '2026-01-01');
""")
cx.commit()
cx.close()
o.BASE = ancienne
o.initialiser_base()
o.initialiser_base()          # idempotente
with o._cx() as cx:
    vieux = cx.execute("SELECT * FROM comptes WHERE pseudo='vieux'").fetchone()
    inv = cx.execute("SELECT * FROM invitations WHERE jeton='jvieux'").fetchone()
verifier("ancien compte : devient joueur, emplacement intact",
         vieux["role"] == "joueur" and vieux["emplacement"] == 3)
verifier("ancienne invitation : role joueur", inv["role"] == "joueur")

shutil.rmtree(_tmp, ignore_errors=True)
print()
if echecs:
    print("%d ECHEC(S) : %s" % (len(echecs), ", ".join(echecs)))
    sys.exit(1)
print("Tout est vert.")
