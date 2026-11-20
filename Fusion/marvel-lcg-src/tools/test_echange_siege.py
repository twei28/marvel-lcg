"""Echange de sieges avant le lancement (chantier du 06/11/2026), cote moteur.

Demande utilisateur : avant de demarrer, les joueurs doivent pouvoir choisir
qui est joueur 1, 2, 3 ou 4 — ca n'existait pas du tout. Teste
`post_demander_echange_siege`/`get_echange_siege`/`post_repondre_echange_siege`
dans `server_get.py`, sans demarrer de vrai serveur HTTP ni le moteur de jeu.

⚠ `seat_token_<p>` N'EST PAS UN JETON DE SESSION : c'est
`seat_hash(SEAT_PASSWORDS[p])`, une empreinte DETERMINISTE du mot de passe du
siege. Ces tests verifient donc que le bon cookie (la bonne empreinte) est
pose sur le bon navigateur, et que l'ancien est bien retire — pas qu'un jeton
aleatoire circule.

Usage: python3 tools/test_echange_siege.py <game_dir>
Viser .game-src-base (ou tout .game-src*), jamais .game.
"""
import asyncio
import hashlib
import os
import sys
import types

GAME_DIR = os.path.expanduser(sys.argv[1])
os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)
os.environ.setdefault("RELEASE", "1")

resultats = []


def verifier(nom, ok, detail=""):
    resultats.append((nom, bool(ok), detail))


from engine.device.web.server.server_get import GameServerGet  # noqa: E402
from engine.device.web.server.server_base import SEAT_PASSWORDS  # noqa: E402

MOTS_DE_PASSE = ["h0", "j1", "j2", "j3"]


def jeton(mot_de_passe):
    return hashlib.md5(mot_de_passe.encode()).hexdigest()


class FauxRequest:
    def __init__(self, cookies=None, corps=None, host="p1.exemple.com"):
        self.cookies = cookies or {}
        self.headers = {}
        self.host = host
        self.url = types.SimpleNamespace(scheme="http")
        self._corps = corps or {}

    async def json(self):
        return self._corps


class FauxServeur(GameServerGet):
    """Ne construit JAMAIS un vrai serveur. `game` est une propriete en
    lecture seule chez `GameServerBase` (derivee de `device_manager`,
    absent ici) : on la masque par la notre, pilotee par `_world`.
    `seat_orphelin` est reecrite pour ne pas toucher a `device_manager`
    non plus."""

    def __init__(self):
        self._world = None
        self._orphelins = set()

    @property
    def game(self):
        return types.SimpleNamespace(world=self._world)

    def seat_orphelin(self, seat):
        return seat in self._orphelins


def cookie_siege(seat):
    return {f"seat_token_{seat}": jeton(MOTS_DE_PASSE[seat])}


def appel(serveur, methode, cookies=None, corps=None):
    reponse = asyncio.run(methode(serveur, FauxRequest(cookies, corps)))
    import json
    return reponse.status, json.loads(reponse.body), reponse.cookies


SEAT_PASSWORDS.value = MOTS_DE_PASSE

# --- Demander un echange ------------------------------------------------

serveur = FauxServeur()
statut, corps, _ = appel(serveur, GameServerGet.post_demander_echange_siege,
                         cookie_siege(1), {"p_demande": 1, "p_cible": 2})
verifier("demande acceptee entre deux sieges occupes, avant lancement",
         statut == 200 and corps.get("result") == "ok")

serveur2 = FauxServeur()
statut, corps, _ = appel(serveur2, GameServerGet.post_demander_echange_siege,
                         cookie_siege(1), {"p_demande": 2, "p_cible": 1})
verifier("refuse si le demandeur ne tient pas le siege p_demande",
         statut == 403)

serveur3 = FauxServeur()
serveur3._orphelins = {2}
statut, corps, _ = appel(serveur3, GameServerGet.post_demander_echange_siege,
                         cookie_siege(1), {"p_demande": 1, "p_cible": 2})
verifier("refuse si le siege cible est vide (orphelin)",
         statut == 400)

serveur4 = FauxServeur()
serveur4._world = object()
statut, corps, _ = appel(serveur4, GameServerGet.post_demander_echange_siege,
                         cookie_siege(1), {"p_demande": 1, "p_cible": 2})
verifier("refuse une fois la partie demarree",
         statut == 409)

# --- Sonder la proposition -----------------------------------------------

serveur5 = FauxServeur()
asyncio.run(GameServerGet.post_demander_echange_siege(
    serveur5, FauxRequest(cookie_siege(1), {"p_demande": 1, "p_cible": 2})))
statut, corps, _ = appel(serveur5, GameServerGet.get_echange_siege, cookie_siege(2))
verifier("le siege cible voit la proposition en attente",
         corps.get("proposition") == {"de": 1, "vers": 2} and corps.get("role") == "cible")

statut, corps, _ = appel(serveur5, GameServerGet.get_echange_siege, cookie_siege(1))
verifier("le demandeur voit sa propre proposition encore en attente",
         corps.get("role") == "demande" and corps.get("statut") == "attente")

statut, corps, _ = appel(serveur5, GameServerGet.get_echange_siege, cookie_siege(0))
verifier("un tiers (hote non concerne) ne voit rien",
         corps == {})

# --- Refuser ---------------------------------------------------------------

serveur6 = FauxServeur()
asyncio.run(GameServerGet.post_demander_echange_siege(
    serveur6, FauxRequest(cookie_siege(1), {"p_demande": 1, "p_cible": 2})))
statut, corps, _ = appel(serveur6, GameServerGet.post_repondre_echange_siege,
                         cookie_siege(0), {"accepte": True})
verifier("un tiers (pas le siege cible) ne peut pas repondre a sa place",
         statut == 403)

statut, corps, _ = appel(serveur6, GameServerGet.post_repondre_echange_siege,
                         cookie_siege(2), {"accepte": False})
verifier("le siege cible peut refuser",
         statut == 200 and corps.get("result") == "refuse")
verifier("la proposition est effacee apres refus",
         getattr(serveur6, "echange_siege", "absent") is None)

# --- Accepter : les DEUX navigateurs recoivent leur cookie ------------------

serveur7 = FauxServeur()
asyncio.run(GameServerGet.post_demander_echange_siege(
    serveur7, FauxRequest(cookie_siege(1), {"p_demande": 1, "p_cible": 2})))

statut, corps, cookies_cible = appel(serveur7, GameServerGet.post_repondre_echange_siege,
                                     cookie_siege(2), {"accepte": True})
verifier("le siege cible accepte : 200", statut == 200)
verifier("le siege cible recoit le jeton du siege demande (1)",
         cookies_cible.get("seat_token_1") is not None
         and cookies_cible["seat_token_1"].value == jeton(MOTS_DE_PASSE[1]))
verifier("le siege cible perd son ancien jeton (2), max-age 0",
         cookies_cible.get("seat_token_2") is not None
         and cookies_cible["seat_token_2"].value == ""
         and cookies_cible["seat_token_2"]["max-age"] == "0")

# Le demandeur n'a encore rien recu : c'est son PROCHAIN sondage qui le lui donne.
statut, corps, cookies_demande = appel(serveur7, GameServerGet.get_echange_siege,
                                       cookie_siege(1))
verifier("le prochain sondage du demandeur applique l'echange",
         corps.get("resultat") == "echange" and corps.get("nouveau_siege") == 2)
verifier("le demandeur recoit le jeton du siege cible (2)",
         cookies_demande.get("seat_token_2") is not None
         and cookies_demande["seat_token_2"].value == jeton(MOTS_DE_PASSE[2]))
verifier("le demandeur perd son ancien jeton (1), max-age 0",
         cookies_demande.get("seat_token_1") is not None
         and cookies_demande["seat_token_1"].value == ""
         and cookies_demande["seat_token_1"]["max-age"] == "0")
verifier("la proposition est entierement purgee une fois les deux appliques",
         getattr(serveur7, "echange_siege", "absent") is None)

# --- La partie demarre entre la proposition et l'acceptation ---------------

serveur8 = FauxServeur()
asyncio.run(GameServerGet.post_demander_echange_siege(
    serveur8, FauxRequest(cookie_siege(1), {"p_demande": 1, "p_cible": 2})))
serveur8._world = object()
statut, corps, _ = appel(serveur8, GameServerGet.post_repondre_echange_siege,
                         cookie_siege(2), {"accepte": True})
verifier("accepter trop tard (partie demarree entre-temps) est refuse",
         statut == 409)
verifier("la proposition tardive est purgee malgre le refus",
         getattr(serveur8, "echange_siege", "absent") is None)

for nom, ok, detail in resultats:
    print(("OK    " if ok else "ECHEC ") + nom + ("" if ok else f"   [{detail}]"))
rates = [nom for nom, ok, _ in resultats if not ok]
print(("\nTOUT PASSE" if not rates else f"\n{len(rates)} ECHEC(S)"))
sys.exit(0 if not rates else 1)
