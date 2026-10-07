"""Marques du mode manuel (cibles, fleches, surlignages), cote serveur.

Usage: RELEASE=1 python3.10 tools/test_marques.py
"""
import asyncio
import json
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "src"))
os.environ.setdefault("RELEASE", "1")

from engine.device.web.server import server_get

CLASSE = next(v for v in vars(server_get).values() if isinstance(v, type) and hasattr(v, "set_marque"))
echecs = 0


def cas(nom, obtenu, attendu):
    global echecs
    if obtenu == attendu:
        print("  ok    %s" % nom)
    else:
        echecs += 1
        print("  ECHEC %s : attendu %r, obtenu %r" % (nom, attendu, obtenu))


class Session:
    game_uid = "partie-1"


class Faux:
    COULEURS_SURLIGNAGE = CLASSE.COULEURS_SURLIGNAGE
    MARQUES_MAX = CLASSE.MARQUES_MAX
    _marques = CLASSE._marques

    def __init__(self):
        self.controller_manager = type("CM", (), {"game": type("G", (), {"session": Session()})()})()


class Requete:
    def __init__(self, donnees):
        self.donnees = donnees

    async def json(self):
        return self.donnees


serveur = Faux()


def envoyer(**donnees):
    reponse = asyncio.run(CLASSE.set_marque(serveur, Requete(donnees)))
    return reponse.status, json.loads(reponse.body)


cas("cibler", envoyer(p=0, genre="cibler", id=12)[1]["cibles"], {"12": 0})
cas("recibler decible", envoyer(p=0, genre="cibler", id=12)[1]["cibles"], {})
m = envoyer(p=1, genre="fleche", de=5, a=7)[1]
cas("fleche, la cible est marquee", (m["fleches"], m["cibles"]), ([{"de": 5, "a": 7, "p": 1}], {"7": 1}))
envoyer(p=0, genre="cibler", id=9)
m = envoyer(p=1, genre="decibler")[1]
cas("Echap : seulement MES cibles et fleches", (m["fleches"], m["cibles"]), ([], {"9": 0}))
cas("surligner", envoyer(p=0, genre="surligner", id=3, couleur="rouge")[1]["surlignages"], {"3": "rouge"})
cas("couleur inconnue refusee", envoyer(p=0, genre="surligner", id=3, couleur="rose")[0], 400)
cas("pave 0 retire", envoyer(p=0, genre="surligner", id=3, couleur=None)[1]["surlignages"], {})
cas("fin de phase : tout le monde", envoyer(p=-1, genre="decibler")[1]["cibles"], {})
envoyer(p=0, genre="cibler", id=4)
Session.game_uid = "partie-2"
cas("nouvelle partie, tout s'efface", asyncio.run(CLASSE.get_marques(serveur, None)).body and json.loads(asyncio.run(CLASSE.get_marques(serveur, None)).body)["cibles"], {})

print("\n%s" % ("TOUT EST VERT" if echecs == 0 else "%d ECHEC(S)" % echecs))
sys.exit(1 if echecs else 0)
