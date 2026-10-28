"""Serveur de test sur une COPIE de la base du site (jamais la vraie).
Usage : cp site/narwhal.db <dossier>/copie.db ; python3 lancer.py  (dans ce dossier) ; puis node test-sync.mjs <dossier de captures>.
Port 8791, compte « valtest » (createur).
"""
import os, sys, threading
sc = os.path.dirname(os.path.abspath(__file__))
os.environ["BASE"] = os.path.join(sc, "copie.db")
os.environ["DOSSIER_CREATEUR"] = os.path.join(sc, "donnees-createur")
os.environ["TENTATIVES_CONNEXION"] = "1000"
sys.path.insert(0, "/home/oem/Desktop/Marvel LCG/site")
import orchestrateur as o
from http.server import ThreadingHTTPServer
o.initialiser_base()
if o.compte("valtest") is None:
    o.inscrire("valtest", "valtest@exemple.be", "motdepasse1", o.creer_invitation("createur"))
print("BASE", o.BASE, "DOSSIER", o.DOSSIER_CREATEUR, "PUBLIC", o.DOSSIER_PUBLIC_JEU, flush=True)
s = ThreadingHTTPServer(("127.0.0.1", 8791), o.Handler)
s.serve_forever()
